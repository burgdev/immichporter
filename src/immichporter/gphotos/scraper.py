"""Google Photos scraper implementation."""

import asyncio
from datetime import datetime
from dateutil import parser
import time
from typing import List, Optional
from loguru import logger
from rich.progress import Progress, SpinnerColumn, BarColumn
from playwright.async_api import async_playwright
from rich.console import Console
from dataclasses import asdict

from immichporter.database import (
    get_db_session,
    insert_or_update_album,
    insert_photo,
    insert_error,
    link_user_to_album,
    album_exists,
    get_albums_from_db,
    update_album_processed_items,
    get_album_processed_items,
    insert_or_update_user,
)
from playwright.async_api import TimeoutError as PlaywrightTimeoutError
from playwright.async_api import ElementHandle, Locator
from immichporter.schemas import ProcessingResult, AlbumInfo, PictureInfo
from immichporter.gphotos.settings import playwright_session_dir

from .utils import traceback

console = Console()

# Configuration constants
DEFAULT_TIMEOUT = 10000
INFO_PANEL_TIMEOUT = 4000
ALBUM_NAVIGATION_DELAY = 0
IMAGE_NAVIGATION_DELAY = 0.01
DUPLICATE_ERROR_THRESHOLD = 10
DUPLICATE_NEXT_IMAGE_THRESHOLD = 6
MAX_ALBUMS = 0

STEALTH_ARGS = [
    "--disable-features=IsolateOrigins,site-per-process",
    "--disable-blink-features=AutomationControlled",
    # "--no-sandbox",
    "--disable-infobars",
    "--disable-extensions",
    "--start-maximized",
    "--new-window",
]

STEALTH_INIT_SCRIPT = """
Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
Object.defineProperty(navigator, 'languages', { get: () => ['en-US','en'] });
Object.defineProperty(navigator, 'plugins', { get: () => [1,2,3,4,5] });
window.chrome = window.chrome || { runtime: {} };
"""


class GooglePhotosScraper:
    """Google Photos scraper for extracting album and photo information."""

    def __init__(
        self,
        max_albums: int = 0,
        start_album: int = 1,
        album_fresh: bool = False,
        albums_only: bool = False,
        clear_storage: bool = False,
        user_data_dir: str = playwright_session_dir,
    ):
        self.max_albums = max_albums
        self.start_album = start_album
        self.album_fresh = album_fresh
        self.skip_existing = not album_fresh
        self.albums_only = albums_only
        self.clear_storage = clear_storage
        self.user_data_dir = user_data_dir
        self.playwright = None
        self.context = None
        self.page = None
        self._default_user = None
        self._info_box_parent_element = None

    async def setup_browser(self) -> None:
        """Initialize and setup the browser context."""
        logger.info("Starting Playwright ...")
        self.playwright = await async_playwright().start()

        console.print("Launching browser ...")
        # Add arguments to force new session and prevent conflicts
        storage_args = [
            "--clear-browsing-data",
            "--clear-browsing-data-on-exit",
            "--disable-session-crashed-bubble",
            "--disable-infobars",
            "--disable-restore-session-state",
        ]
        all_args = STEALTH_ARGS + storage_args

        # Launch non-persistent context to avoid session conflicts
        self.context = await self.playwright.chromium.launch_persistent_context(
            user_data_dir=self.user_data_dir,
            headless=False,
            executable_path=None,  # Use Playwright's Chromium
            args=all_args,
            ignore_default_args=["--enable-automation"],
            viewport={"width": 1000, "height": 700},
            slow_mo=40,
            timeout=DEFAULT_TIMEOUT,
        )

        logger.debug("Creating page ...")
        # self.page = await self.context.new_page()
        self.page = (
            self.context.pages[0]
            if self.context.pages
            else await self.context.new_page()
        )
        # await self.page.set_viewport_size({"width": 1280, "height": 720})

        logger.debug("Adding stealth script ...")
        # Set up stealth mode
        await self.page.add_init_script(STEALTH_INIT_SCRIPT)

    async def open_gphotos(self, path=""):
        url = "https://photos.google.com"
        if path:
            url += f"/{path}"
        try:
            console.print(f"Navigating to [blue]'{url}'[/blue]")
            await self.page.goto(url, wait_until="domcontentloaded")
        except PlaywrightTimeoutError as e:
            raise TimeoutError(
                f"Navigation timeout, could not navigate to '{url}'"
            ) from e

    async def login(self) -> bool:
        """Handle Google Photos login flow.

        Returns:
            bool: True if already logged in, False if login required
        """
        # Clear browser storage if requested
        if self.clear_storage:
            await self.clear_browser_storage()

        await self.open_gphotos(path="login")

        # Wait for navigation to complete and get current URL
        current_url = await self.page.evaluate("window.location.href")
        logger.debug(f"Current URL: {current_url}")

        # Check if we're already logged in (redirected to main photos page)
        if "photos.google.com/" in current_url and "login" not in current_url:
            console.print("[green]Already logged in to Google Photos[/green]")
            return True

        # If we get here, we're on the login page
        console.print(
            "[yellow]Please log in to Google Photos in the browser ...[/yellow]"
        )
        while "photos.google.com/" not in current_url and "login" in current_url:
            await self.page.wait_for_load_state("domcontentloaded")
            current_url = await self.page.evaluate("window.location.href")
            await asyncio.sleep(0.2)
        console.print(
            "[yellow]Press Enter in the console when you are logged in.[/yellow]"
        )
        console.print("[green]Login successful![/green]")
        return True

    async def get_album_info(self) -> AlbumInfo:
        """Extract album information from the current selection."""
        try:
            # Get the currently selected album element
            selected_element = await self.page.evaluate_handle("document.activeElement")

            children = await selected_element.query_selector_all("div")
            href = await selected_element.get_attribute("href")
            url = "https://photos.google.com" + href.strip(".")

            if len(children) < 2:
                raise ValueError("Could not find album information elements")

            album_title, description = (await children[1].inner_text()).split("\n", 1)
            logger.info(f"Album Title: {album_title}")
            shared = "shared" in description.lower()
            logger.info(f"Shared: {shared}")
            items = int(description.split(" ")[0])
            logger.info(f"Items: {items}")

            return AlbumInfo(title=album_title, items=items, shared=shared, url=url)

        except Exception as e:
            console.print(f"[red]Error getting album info: {e}[/red]")
            logger.debug(traceback(e))
            return None

    async def set_info_box_parent_element(self) -> Locator | None:
        await self.page.wait_for_load_state("domcontentloaded")
        await asyncio.sleep(0.2)
        c_wiz_locator = self.page.locator('c-wiz[style*="display: none"]')
        cnt = 0
        hidden_c_wiz = None
        while hidden_c_wiz is None and cnt < 20:
            try:
                await c_wiz_locator.wait_for(state="hidden", timeout=4000)
                hidden_c_wiz = c_wiz_locator.first
            except PlaywrightTimeoutError as e:
                logger.debug(f"c-wiz locator not found: {e}")
                if cnt % 4 == 0 and cnt > 0:
                    logger.debug("Page reload")
                    await self.page.reload(wait_until="domcontentloaded")
                else:
                    await self.keyboard_press("i", delay=1)
                    await self.page.wait_for_load_state("domcontentloaded")
            cnt += 1
        if hidden_c_wiz is None:
            raise ValueError("Could not find info box")
        logger.debug(f"Found hidden c-wiz: {hidden_c_wiz}")
        parent = hidden_c_wiz.locator("..")
        await parent.wait_for()
        logger.debug(f"Found info box parrent locator: {parent}")
        self._info_box_parent_element = parent
        return parent

    async def _get_all_visible(self, el: Locator) -> list[ElementHandle] | None:
        el_visible = []
        for eles in await el.all():
            if await eles.is_visible():
                el_visible.append(eles)
        return el_visible

    async def get_source_id(self) -> str:
        """Returns source_id from the page url"""
        # await self.page.wait_for_load_state("load")
        return self.page.url.split("/")[-1].split("?")[0]

    async def get_info_box_element(
        self, loc: Locator | None = None
    ) -> tuple[str | None, ElementHandle | None]:
        """Returns source_id and locator of current info box"""
        source_id = await self.get_source_id()
        loc = loc or self.page.locator(f'c-wiz[jslog*="{source_id}"]')
        try:
            await loc.first.wait_for(state="attached", timeout=1000)
        except PlaywrightTimeoutError:
            try:  # try page reload
                await self.page.reload(wait_until="domcontentloaded")
                source_id2 = await self.get_source_id()
                if source_id != source_id2:
                    logger.warning(
                        f"Source ID changed from {source_id} to {source_id2}"
                    )
                loc = self.page.locator(f'c-wiz[jslog*="{source_id2}"]')
                await loc.first.wait_for(state="attached", timeout=5000)
            except PlaywrightTimeoutError:
                # check if info box is okay
                await self.set_info_box_parent_element()
                await loc.first.wait_for(state="attached", timeout=5000)
        return source_id, loc.first

    async def get_photo_info(
        self, album: AlbumInfo, el: Locator | None = None
    ) -> Optional[PictureInfo]:
        """Extract information from the current picture."""
        if el is None:
            source_id, el = await self.get_info_box_element()
        else:
            source_id = await self.get_source_id(el)
        try:
            el_timeout = 2000
            # Extract filename
            filename_el = el.locator('div[aria-label*="Filename"]')
            await filename_el.wait_for(state="attached", timeout=el_timeout)
            filename = await filename_el.inner_text()
            # Extract date information
            date_obj = None
            date_text_el = el.locator('div[aria-label*="Date taken"]')
            await date_text_el.wait_for(state="attached", timeout=el_timeout)
            date_text = await date_text_el.inner_text()
            time_element = el.locator('span[aria-label*="Time taken"]')
            await time_element.wait_for(state="attached", timeout=el_timeout)
            time_text = await time_element.inner_text() if time_element else "N/A"
            date_obj, date_str = self._parse_date(f"{date_text} {time_text}")
            default_user = await self.get_default_user()
            try:
                shared_by_el = el.locator('div:text("Shared by")')
                await shared_by_el.wait_for(state="attached", timeout=200)
                shared_by = (
                    (await shared_by_el.inner_text()).replace("Shared by", "").strip()
                )
            except PlaywrightTimeoutError:
                if album.shared:
                    logger.error(
                        f"Could not get shared user, use default user ({default_user})."
                    )
                shared_by = default_user
            # make sure the source id did not change
            new_source_id = self.page.url.split("/")[-1].split("?")[0]
            if new_source_id != source_id:
                raise RuntimeError(
                    f"Source ID changed from {source_id} to {new_source_id}, this is not expected!"
                )

            return PictureInfo(
                filename=filename,
                date_taken=date_obj,
                user=shared_by,
                source_id=source_id,
            )

        except PlaywrightTimeoutError as e:
            raise RuntimeError(
                f"Getting picture info for source '{source_id}' failed due to some timeout"
            ) from e

    def _parse_date(self, date_str: str) -> tuple[datetime, str]:
        """Parse date string and return both datetime object and formatted string."""
        try:
            date_obj = parser.parse(date_str)
            date_formatted = date_obj.strftime("%d.%m.%y %H:%M")
            return date_obj, date_formatted
        except (ValueError, TypeError) as e:
            raise ValueError(f"Could not parse data '{date_str}'") from e
        except OverflowError as e:
            raise OverflowError(f"Date '{date_str}' is out of range") from e

    async def get_default_user(self) -> str:
        """Extract information from the current picture."""
        if self._default_user is not None:
            return self._default_user
        try:
            google_account_element = await self.page.wait_for_selector(
                'a[aria-label*="Google Account"]', timeout=5000
            )
            google_account = await google_account_element.get_attribute("aria-label")
            name_email = google_account.split(":", 1)[1].strip()
            name = name_email.split("\n")[0].strip()
            # email = name_email.split("\n")[1].strp("() ")
            self._default_user = name
            console.print(f"Default user: [green]'{name}'[/green]")
            return name

        except PlaywrightTimeoutError as e:
            raise TimeoutError("Could not get default user") from e
        except ValueError as e:
            raise ValueError("Could not get default user") from e

    async def process_album_from_db(
        self,
        album: AlbumInfo,
        skip_existing: bool = True,
    ) -> AlbumInfo:
        """Process images from an album using its gphoto_url URL."""
        console.print(
            f"Processing album {album.album_id} [green]'{album.title}'[/green]", end=""
        )

        # Get existing photo count
        with get_db_session() as session:
            # existing_count = get_album_photos_count(session, album.album_id)
            processed_count = get_album_processed_items(session, album.album_id)

        # Skip if already fully processed
        if processed_count >= album.items and self.skip_existing:
            console.print("[red] - already fully processed. Skipping.[/red]")
            return
        else:
            console.print(
                f" - [blue]{processed_count}/{album.items}[/blue] items already processed"
            )

        # Navigate to album - convert relative URL to absolute URL
        logger.info(f"Navigating to: {album.url}")
        try:
            await self.page.goto(
                album.url, timeout=10000, wait_until="domcontentloaded"
            )
        except PlaywrightTimeoutError:
            await self.page.reload(wait_until="commit")
            await self.page.goto(
                album.url, timeout=15000, wait_until="domcontentloaded"
            )
        # Process photos
        processed_photos = 0
        duplicate_count = 0
        # processed_count = existing_count

        # Find and navigate to the first image
        logger.info("Looking for first image in album ...")
        first_image_url = None
        try:
            # Look for the first tag with aria-label containing "Photo -"
            first_image_loc = self.page.locator('a[aria-label*="Photo -"]')
            await first_image_loc.first.wait_for(state="attached", timeout=5000)
            # Get the href attribute directly from the a tag
            first_image_url = await first_image_loc.first.get_attribute("href")

            if first_image_url:
                logger.debug(f"Found first image URL: {first_image_url}")
                # Construct absolute URL if needed
                if first_image_url.startswith("./"):
                    first_image_url = f"https://photos.google.com{first_image_url[1:]}"
                elif first_image_url.startswith("/"):
                    first_image_url = f"https://photos.google.com{first_image_url}"

                # Navigate to the first image
                logger.debug("Navigating to first image...")
                await self.page.goto(first_image_url, wait_until="domcontentloaded")
            else:
                console.print("[red]Could not get href from first image element[/red]")

        except PlaywrightTimeoutError as e:
            raise TimeoutError("Could not find first image element") from e

        if not first_image_url:
            console.print(
                f"[red]Could not find first photo for album {album.title}, please fix it manually and press Enter to continue.[/red]"
            )
            return

        pictures = []
        last_source_id = None
        last_filename = None
        duplicate_count = 0
        processed_users: dict[str, int] = dict()  # set()

        # Skip check already done at the beginning of the method

        # Get current photo count to continue from where we left off
        # with Progress(
        #    SpinnerColumn(),
        #    TextColumn("[progress.description]{task.description}"),
        #    console=console,
        # ) as progress:
        with Progress(
            SpinnerColumn(),
            "[cyan]{task.completed}/{task.total}",
            BarColumn(bar_width=50),
            "[progress.percentage]{task.percentage:>3.0f}%",
            "•",
            "[progress.description]{task.description}",
            console=console,
        ) as progress:
            task = progress.add_task(
                f"Processing {album.title}...",
                total=album.items,
                completed=processed_photos,
            )

            while processed_photos < album.items:
                try:  # catch album errors, then proceed to next album
                    picture_info = await self.get_photo_info(album)
                    logger.debug(f"Picture info: {picture_info}")
                    if picture_info.filename == last_filename:
                        logger.debug(
                            "Filename did not change, waiting a bit longer and try again ..."
                        )
                        # sometimes it takes longer until the filename is updated, in this case we wait a bit more.
                        await asyncio.sleep(0.4)
                        picture_info = await self.get_photo_info(album)
                        logger.debug(f"Picture info 2: {picture_info}")

                    # Check for duplicates to detect end of album
                    if (
                        picture_info.source_id == last_source_id
                        and picture_info.source_id != ""
                    ):
                        duplicate_count += 1
                        logger.debug(
                            f"Duplicate count: {duplicate_count}, source id: '{picture_info.source_id}, last source id: '{last_source_id}'"
                        )
                        progress.update(
                            task,
                            advance=0,
                            description=f"[green]{picture_info.filename}[/green] [red](taking a bit longer {'.' * duplicate_count})[/red]",
                        )
                        if duplicate_count == DUPLICATE_NEXT_IMAGE_THRESHOLD:
                            logger.warning(
                                "Probably missed an 'arrowright' key press, try one more ..."
                            )
                            await self.keyboard_press(
                                "ArrowRight", delay=IMAGE_NAVIGATION_DELAY + 0.1
                            )

                        if duplicate_count >= DUPLICATE_ERROR_THRESHOLD:
                            logger.error("Reached end of album before expected")
                            break  # next album

                        else:
                            await asyncio.sleep(0.15 * (duplicate_count + 1))
                            continue

                    # New picture found
                    last_source_id = picture_info.source_id
                    last_filename = picture_info.filename
                    pictures.append(picture_info)
                    duplicate_count = 0

                    # Save to database
                    try:
                        if (
                            picture_info.user
                            and picture_info.user != "N/A"
                            and picture_info.user not in processed_users
                        ):
                            with get_db_session() as session:
                                user_id = insert_or_update_user(
                                    session, picture_info.user
                                )
                                link_user_to_album(session, album.album_id, user_id)
                                processed_users[picture_info.user] = user_id

                        picture_info.user_id = processed_users[picture_info.user]
                        # Insert photo
                        with get_db_session() as session:
                            photo_updated, photo_id = insert_photo(
                                session,
                                picture_info,
                                album_id=album.album_id,
                                update=not skip_existing,
                            )

                        if photo_updated is not None:
                            logger.debug(
                                f"Got photo id '{photo_id}' which is {'updated' if photo_updated else 'new'}"
                            )
                        else:
                            logger.debug(
                                f"Photos {picture_info.filename} already exists"
                            )

                        # Update processed items count
                        processed_photos += 1
                        with get_db_session() as session:
                            update_album_processed_items(
                                session, album.album_id, processed_photos
                            )
                        if photo_updated is not None:
                            description_prefix = (
                                f"[green]{picture_info.filename}[/green]"
                            )
                            description_prefix += (
                                " [blue](updated)[/blue]"
                                if photo_updated
                                else " [orange](new)[/orange]"
                            )
                        else:  # photo already exists
                            description_prefix = f"[blue]{picture_info.filename} (already processed)[/blue]"
                        progress.update(
                            task,
                            advance=1,
                            description=f"{description_prefix}",
                        )

                    except Exception as e:  # catch all
                        insert_error(
                            f"Error saving picture {picture_info.filename}: {e}",
                            album.album_id,
                        )
                        raise RuntimeError(
                            f"Error saving picture {picture_info.filename} ({picture_info.source_id})"
                        ) from e

                    source_id = await self.get_source_id()
                    # Navigate to next image
                    await self.keyboard_press(
                        "ArrowRight", delay=IMAGE_NAVIGATION_DELAY
                    )
                    # make sure the page url changed
                    old_source_id = source_id
                    timer = time.perf_counter()
                    while old_source_id == source_id and processed_photos < album.items:
                        source_id = await self.get_source_id()
                        await asyncio.sleep(0.005)
                        if time.perf_counter() - timer > 5:  # wait max 5 seconds
                            raise TimeoutError(
                                f"Timeout waiting for page to change (current source id: {source_id})"
                            )

                except Exception as e:
                    err_str = str(e).split("\n")[0]
                    progress.update(
                        task,
                        advance=0,
                        description=f"[red]{album.title}[/red] • [red]ERROR: [dim]{err_str}[/red]",
                    )
                    raise RuntimeError(
                        f"Error processing album {album.album_id} ({album.title})"
                    ) from e

            description = f"[green]{album.title}[/green] • "
            description += f"[blue]{'Users' if len(processed_users) > 1 else 'User'}: [blue]{', '.join(processed_users.keys())}[/blue]"
            progress.update(
                task,
                advance=0,
                description=description,
            )
        return album

    async def navigate_to_album(self, album_position: int) -> None:
        """Navigate to the next album using arrow keys."""
        logger.info(f"Navigating to album {album_position}")
        for _ in range(album_position):
            await self.keyboard_press("ArrowRight", delay=ALBUM_NAVIGATION_DELAY)

    async def keyboard_press(self, key: str, delay: int | None = 0.2):
        """Press a keyboard key with optional delay."""
        logger.debug(f"Pressing key '{key}'")
        await self.page.keyboard.press(key)
        if delay is not None and delay > 0:
            await asyncio.sleep(delay)

    async def collect_albums(
        self, max_albums: int = None, start_album: int = 1
    ) -> List[AlbumInfo]:
        """Collect albums from Google Photos UI and add them to database."""
        # await self.setup_browser()

        console.print("[green]Collecting albums from Google Photos UI...[/green]")
        console.print(f"Starting from album position [blue]{start_album}[/blue]")
        if max_albums:
            logger.info(f"Maximum albums to collect: {max_albums}")

        albums_collected = []
        albums_processed = 0

        # Navigate to Google Photos albums
        await self.open_gphotos(path="albums")
        await asyncio.sleep(1)

        # Press ArrowRight to select the first album
        logger.debug("Pressing ArrowRight to select first album...")
        await self.keyboard_press("ArrowRight", delay=ALBUM_NAVIGATION_DELAY)

        # Wait a moment for the focus to settle
        await asyncio.sleep(0.2)

        # Navigate to the first album to process
        if start_album > 1:
            console.print(f"Navigating to album index [blue]{start_album}[/blue] ...")
            await self.navigate_to_album(
                start_album - 2
            )  # Convert to 0-based and adjust for starting position

        prev_album = None
        for album_position in range(start_album - 1, start_album - 1 + max_albums):
            try:
                # Navigate to next album (only one step from current position)
                # Only navigate if we're past the first album in our collection
                if album_position > start_album - 1:
                    logger.info(
                        f"Navigating to album {album_position}... (start album: {start_album})"
                    )
                    await self.keyboard_press(
                        "ArrowRight", delay=ALBUM_NAVIGATION_DELAY
                    )

                # Get album info
                album_info = await self.get_album_info()
                if album_info is None:
                    logger.warning("No album info found, stopping collection")
                    break

                logger.info(f"Collecting album: {album_info.title}")

                # Check if album already exists in database
                with get_db_session() as session:
                    exists = album_exists(session, album_info.title)

                if not exists:
                    # Insert album into database
                    with get_db_session() as session:
                        album_id = insert_or_update_album(session, album_info)
                    console.print(
                        f"Added album [green]'{album_info.title}'[/green] to database (ID: [blue]{album_id}[/blue])"
                    )
                    albums_collected.append(album_info)
                else:
                    console.print(
                        f"Album [green]'{album_info.title}'[/green] already exists in database. [yellow]Skipping.[/yellow]"
                    )

                albums_processed += 1

                if prev_album and prev_album.url == album_info.url:
                    console.print("All albums collected ...")
                    break
                prev_album = AlbumInfo(**asdict(album_info))

            except Exception as e:
                error_msg = f"Error collecting album: {e}"
                console.print(f"[red]{error_msg}[/red]")
                with get_db_session() as session:
                    insert_error(session, error_msg)
                logger.debug(traceback(e))
                break

        console.print(
            f"[green]Completed collecting [blue]{len(albums_collected)}[/blue] albums[/green]"
        )
        return albums_collected

    async def scrape_albums_from_db(
        self,
        max_albums: int | None = None,
        start_album: int = 1,
        album_ids: list[int] | None = None,
        not_finished: bool = False,
        skip_existing: bool = True,
    ) -> ProcessingResult:
        """Process images from albums stored in the database.

        Args:
            max_albums: Maximum number of albums to process (ignored if album_id is provided)
            start_album: Starting album position (1-based, ignored if album_id is provided)
            album_ids: Specific album ID to process (overrides max_albums and start_album)
        """
        await self.open_gphotos(path="albums")
        await self.get_default_user()  # save default user

        # Get albums from database
        with get_db_session() as session:
            # Get albums with pagination
            console.print("Processing albums from database ...")
            logger.info(f"Starting from album position {start_album}")
            if album_ids:
                max_albums = None
                start_album = 1

            if max_albums:
                logger.info(f"Maximum albums to process: {max_albums}")
            albums = get_albums_from_db(
                session,
                limit=max_albums,
                offset=start_album - 1,
                not_finished=not_finished,
                album_ids=album_ids,
            )

        if not albums:
            # If no albums exist and we're in albums-only mode, collect them first
            if self.albums_only:
                console.print(
                    "No albums found in database, [yellow] collecting them now[/yellow]"
                )
                collected_albums = await self.collect_albums(
                    max_albums=max_albums, start_album=start_album
                )
                return ProcessingResult(
                    total_albums=len(collected_albums),
                    total_pictures=0,
                    albums_processed=collected_albums,
                    errors=[],
                )
            else:
                console.print(
                    "[red]No albums found in database, run first [yellow]'immichporter photos albums'[/yellow][/red]"
                )

            return ProcessingResult(
                total_albums=0, total_pictures=0, albums_processed=[], errors=[]
            )

        console.print(f"Found [blue]{len(albums)}[/blue] albums to process")

        # Process each album
        albums_processed = []
        total_pictures = 0
        errors = []

        # for album_id, album_gphoto_url, album_gphoto_title, album_items in albums:
        for album in albums:
            try:
                if self.albums_only:
                    # In albums-only mode, we just need to ensure the album exists
                    console.print(
                        f"Album [green]'{album.title}'[/green] already exists in database"
                    )
                    albums_processed.append(album)
                else:
                    # Process the album
                    await self.process_album_from_db(album, skip_existing=skip_existing)
                    albums_processed.append(album)
                    total_pictures += album.items

            except Exception as e:
                error_msg = f"Error processing album {album.title}: {e}"
                console.print(f"[red]{error_msg}[/red]")
                errors.append(error_msg)
                with get_db_session() as session:
                    insert_error(session, error_msg, album.album_id)
                logger.debug(traceback(e))
                continue

        # Note: Storage state not saved with non-persistent context

        return ProcessingResult(
            total_albums=len(albums_processed),
            total_pictures=total_pictures,
            albums_processed=albums_processed,
            errors=errors,
        )

    async def clear_browser_storage(self) -> None:
        """Clear browser storage (localStorage, sessionStorage) while preserving auth cookies."""
        console.print("[yellow]Clearing browser storage...[/yellow]")

        # Clear localStorage
        await self.page.evaluate(
            "() => { window.localStorage && window.localStorage.clear(); }"
        )

        # Clear sessionStorage
        await self.page.evaluate(
            "() => { window.sessionStorage && window.sessionStorage.clear(); }"
        )

        # Clear IndexedDB
        await self.page.evaluate(
            "() => { if (window.indexedDB) { window.indexedDB.databases && window.indexedDB.databases().then(dbs => dbs.forEach(db => window.indexedDB.deleteDatabase(db.name))); } }"
        )

        # Clear cache
        await self.page.evaluate(
            "() => { if ('caches' in window) { caches.keys().then(names => names.forEach(name => caches.delete(name))); } }"
        )

        console.print("[green]Browser storage cleared successfully[/green]")

    async def close(self) -> None:
        """Close the browser context and clean up resources."""
        if self.context:
            await self.context.close()
        if self.playwright:
            await self.playwright.stop()
