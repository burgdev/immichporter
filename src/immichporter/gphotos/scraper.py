"""Google Photos scraper implementation."""

import asyncio
from datetime import datetime
from dateutil import parser
import time
from typing import List, Optional
from loguru import logger
from rich.progress import Progress, SpinnerColumn, TextColumn
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
    get_album_photos_count,
    insert_or_update_user,
)
from playwright.async_api import TimeoutError as PlaywrightTimeoutError
from immichporter.gphotos.models import ProcessingResult
from immichporter.gphotos.models import AlbumInfo, PictureInfo

console = Console()

# Configuration constants
USER_DATA_DIR = "./brave_playwright_profile2"
DEFAULT_TIMEOUT = 10000
INFO_PANEL_TIMEOUT = 2000
ALBUM_NAVIGATION_DELAY = 0
IMAGE_NAVIGATION_DELAY = 0.05
DUPLICATE_THRESHOLD = 10
DUPLICATE_LOG_THRESHOLD = 5
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
        max_albums: int = 5,
        start_album: int = 1,
        album_fresh: bool = False,
        albums_only: bool = False,
        clear_storage: bool = False,
        user_data_dir: str = USER_DATA_DIR,
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

    async def setup_browser(self) -> None:
        """Initialize and setup the browser context."""
        console.print("[blue]Starting Playwright...[/blue]")
        self.playwright = await async_playwright().start()

        console.print("[blue]Launching browser...[/blue]")
        # Add arguments to force new session and prevent conflicts
        storage_args = [
            "--clear-browsing-data",
            "--clear-browsing-data-on-exit",
            "--disable-session-crashed-bubble",
            "--disable-infobars",
            "--disable-restore-session-state",
            #'--disable-session-crashed-bubble',
            #'--disable-infobars',
            #'--disable-restore-session-state',
            #'--no-first-run',
            #'--no-default-browser-check',
            #'--disable-features=TranslateUI',
            #'--disable-background-mode',
            #'--disable-background-timer-throttling',
            #'--disable-renderer-backgrounding',
            #'--disable-backgrounding-occluded-windows',
            #'--disable-client-side-phishing-detection',
            #'--disable-crash-reporter',
            #'--disable-extensions',
            #'--disable-plugins',
            #'--disable-popup-blocking',
            #'--disable-prompt-on-repost',
            #'--disable-sync',
            #'--disable-web-security',
            #'--disable-features=VizDisplayCompositor',
            #'--disable-blink-features=AutomationControlled'
        ]
        all_args = STEALTH_ARGS + storage_args

        # Launch non-persistent context to avoid session conflicts
        self.context = await self.playwright.chromium.launch_persistent_context(
            user_data_dir=self.user_data_dir,
            headless=False,
            executable_path=None,  # Use Playwright's Chromium
            args=all_args,
            ignore_default_args=["--enable-automation"],
            viewport={"width": 1280, "height": 720},
            slow_mo=40,
        )

        console.print("[blue]Creating page...[/blue]")
        # self.page = await self.context.new_page()
        self.page = (
            self.context.pages[0]
            if self.context.pages
            else await self.context.new_page()
        )
        # await self.page.set_viewport_size({"width": 1280, "height": 720})

        console.print("[blue]Adding stealth script...[/blue]")
        # Set up stealth mode
        await self.page.add_init_script(STEALTH_INIT_SCRIPT)

    async def open_gphotos(self, path=""):
        url = "https://photos.google.com"
        if path:
            url += f"/{path}"
        try:
            console.print(f"[blue]Navigating to '{url}'[/blue]")
            await self.page.goto(url)
            await self.page.wait_for_load_state("domcontentloaded")
        except Exception as e:
            console.print(f"[red]Navigation error: {e}[/red]")
            raise

    async def login(self):
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
        console.print(f"[blue]Current URL: {current_url}[/blue]")

        # Check if we're already logged in (redirected to main photos page)
        if "photos.google.com/" in current_url and "login" not in current_url:
            console.print("[green]Already logged in to Google Photos[/green]")
            return True

        # If we get here, we're on the login page
        console.print(
            "[yellow]Please log in to Google Photos in the browser...[/yellow]"
        )
        console.print(
            "[yellow]Press Enter in the console when you are logged in.[/yellow]"
        )
        input()

        # Verify login was successful
        await self.page.wait_for_load_state("domcontentloaded")
        current_url = await self.page.evaluate("window.location.href")
        if "login" in current_url:
            console.print(
                "[red]Login may not have been successful. Still on login page.[/red]"
            )
            return False

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
            console.print(f"[blue]Album Title:[/blue] {album_title}")
            shared = "shared" in description.lower()
            console.print(f"[blue]Shared:[/blue] {shared}")
            items = int(description.split(" ")[0])
            console.print(f"[blue]Items:[/blue] {items}")

            return AlbumInfo(title=album_title, items=items, shared=shared, url=url)

        except Exception as e:
            console.print(f"[red]Error getting album info: {e}[/red]")
            return None

    async def get_picture_info(self, album_title: str) -> Optional[PictureInfo]:
        """Extract information from the current picture."""
        try:
            # Wait for info panel to be visible
            # await self.page.wait_for_selector('div[aria-label*="Filename"]', timeout=INFO_PANEL_TIMEOUT)

            # Extract filename
            filename = None
            cnt = 0
            while not filename and cnt < 6:
                cnt += 1
                filename = await self._get_text_safely(
                    'div[aria-label*="Filename"]', timeout=INFO_PANEL_TIMEOUT
                )
                if cnt == 5:
                    logger.error(
                        f"Could not find filename after {cnt} attempts, next album."
                    )
                    return None

                if not filename:
                    logger.info(
                        "Could not find filename, make page reload and try again"
                    )
                    await self.page.reload(wait_until="domcontentloaded")
                    await asyncio.sleep(1.0 * cnt)
                    if cnt == 2:
                        await self.keyboard_press("i", delay=0.1)

            # Extract date information
            date_text = await self._get_text_safely(
                'div[aria-label*="Date taken"]', timeout=INFO_PANEL_TIMEOUT
            )
            time_element = await self.page.query_selector(
                'span[aria-label*="Time taken"]'
            )
            time_text = await time_element.inner_text() if time_element else "N/A"

            current_url = await self.page.evaluate("window.location.href")
            source_id = current_url.split("/")[-1].split("?")[0]
            # Parse date
            date_obj, date_str = self._parse_date(f"{date_text} {time_text}")

            # Extract shared by information
            shared_by = await self._get_text_safely(
                'div:text("Shared by")', timeout=INFO_PANEL_TIMEOUT
            )
            shared_by = (
                shared_by.replace("Shared by", "").strip() if shared_by else "N/A"
            )

            return PictureInfo(
                filename=filename,
                date_taken=date_obj,
                user=shared_by,
                source_id=source_id,
            )

        except Exception as e:
            logger.error(f"Getting picture info: {e}")
            return None

    async def _get_text_safely(
        self, selector: str, timeout: int = 2000
    ) -> Optional[str]:
        """Safely extract text from an element with timeout."""
        start = time.perf_counter() * 1000
        while time.perf_counter() * 1000 - start < timeout:
            try:
                elements = await self.page.query_selector_all(selector)
                visible_elements = []
                for element in elements:
                    if await element.is_visible():
                        visible_elements.append(await element.inner_text())
                if len(visible_elements) > 1:
                    logger.debug(
                        f"Multiple visible elements found for selector: {selector}"
                    )
                elif len(visible_elements) == 1:
                    return visible_elements[0]
            except PlaywrightTimeoutError:
                logger.warning(f"Timed out waiting for element: {selector}")
            await asyncio.sleep(0.05)
        return None

    def _parse_date(self, date_str: str) -> tuple[datetime, str]:
        """Parse date string and return both datetime object and formatted string."""
        try:
            date_obj = parser.parse(date_str)
            date_formatted = date_obj.strftime("%d.%m.%y %H:%M")
            return date_obj, date_formatted
        except Exception as e:
            logger.warning(f"Error parsing date '{date_str}': {e}")
            return None, date_str

    async def process_album_from_db(
        self,
        album_id: int,
        album_gphoto_url: str,
        album_gphoto_title: str,
        album_items: int,
    ) -> AlbumInfo:
        """Process images from an album using its gphoto_url URL."""
        console.print(f"[green]Processing album: {album_gphoto_title}[/green]")

        # Navigate to album - convert relative URL to absolute URL
        if album_gphoto_url.startswith("./"):
            album_gphoto_url = f"https://photos.google.com{album_gphoto_url[1:]}"
        elif album_gphoto_url.startswith("./album/"):
            album_gphoto_url = f"https://photos.google.com{album_gphoto_url[1:]}"

        console.print(f"[blue]Navigating to: {album_gphoto_url}[/blue]")
        await self.page.goto(album_gphoto_url)
        await self.page.wait_for_load_state("domcontentloaded")

        # Get existing photo count
        with get_db_session() as session:
            existing_count = get_album_photos_count(session, album_id)

        console.print(
            f"[blue]Album has {album_items} items, {existing_count} already processed[/blue]"
        )

        # Skip if already fully processed
        if existing_count >= album_items and self.skip_existing:
            console.print(
                f"[yellow]Album {album_gphoto_title} already fully processed. Skipping.[/yellow]"
            )
            return

        # Process photos
        processed_photos = 0
        duplicate_count = 0
        # processed_count = existing_count

        # Find and navigate to the first image
        console.print("[blue]Looking for first image in album...[/blue]")
        first_image_url = None
        try:
            # Look for the first a tag with aria-label containing "Photo -"
            first_image_element = await self.page.wait_for_selector(
                'a[aria-label*="Photo -"]', timeout=5000
            )

            # Get the href attribute directly from the a tag
            first_image_url = await first_image_element.get_attribute("href")

            if first_image_url:
                logger.debug(f"Found first image URL: {first_image_url}")
                # Construct absolute URL if needed
                if first_image_url.startswith("./"):
                    first_image_url = f"https://photos.google.com{first_image_url[1:]}"
                elif first_image_url.startswith("/"):
                    first_image_url = f"https://photos.google.com{first_image_url}"

                # Navigate to the first image
                logger.debug("Navigating to first image...")
                await self.page.goto(first_image_url)
                await self.page.wait_for_load_state("domcontentloaded")
            else:
                console.print(
                    "[yellow]Could not get href from first image element[/yellow]"
                )

        except Exception as e:
            console.print(f"[yellow]Could not find first image element: {e}[/yellow]")

        if not first_image_url:
            console.print(
                f"[red]Could not find first photo for album {album_gphoto_title}, please fix it manually and press Enter to continue."
            )
            input()

        # Get picture info for the first image after navigation
        picture_info = await self.get_picture_info(album_gphoto_title)
        pictures = []
        last_source_id = None
        duplicate_count = 0
        processed_users = set()

        # Skip check already done at the beginning of the method

        # Get current photo count to continue from where we left off
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task(
                f"Processing {album_gphoto_title}...",
                total=album_items,
                completed=processed_photos,
            )

            photo_position = 1
            while processed_photos < album_items:
                # go to the correct photo position (needed if some where already processed)
                if photo_position < processed_photos:
                    await self.keyboard_press(
                        "ArrowRight", delay=IMAGE_NAVIGATION_DELAY
                    )
                    photo_position += 1
                    continue

                try:
                    picture_info = await self.get_picture_info(album_gphoto_title)

                    if not picture_info:
                        logger.error("Could not extract info for current image")
                        break

                    # Check for duplicates to detect end of album
                    if (
                        picture_info.source_id == last_source_id
                        and picture_info.source_id != ""
                    ):
                        duplicate_count += 1
                        if duplicate_count >= DUPLICATE_LOG_THRESHOLD:
                            await asyncio.sleep(1)
                            logger.warning(
                                f"Duplicate url detected: {picture_info.url} ({duplicate_count})"
                            )
                            console.print("[red]Press Enter to continue...[/red]")
                            input()

                        if duplicate_count >= DUPLICATE_THRESHOLD:
                            logger.error(
                                "Reached end of album before expected (duplicate threshold met)"
                            )
                            # we add the same name to the album

                        else:
                            # we missed a arrow right
                            await self.keyboard_press(
                                "ArrowRight", delay=IMAGE_NAVIGATION_DELAY
                            )
                            await asyncio.sleep(0.15)
                            continue

                    # New picture found
                    last_source_id = picture_info.source_id
                    pictures.append(picture_info)
                    duplicate_count = 0

                    # Save to database
                    try:
                        if picture_info.user and picture_info.user != "N/A":
                            with get_db_session() as session:
                                user_id = insert_or_update_user(
                                    session, picture_info.user
                                )
                                link_user_to_album(session, album_id, user_id)
                                processed_users.add(picture_info.user)

                        # Insert photo
                        with get_db_session() as session:
                            photo_id = insert_photo(
                                session,
                                picture_info,
                                user_id=user_id,
                                album_id=album_id,
                            )

                        # Photo was successfully inserted (not a duplicate)
                        photo_position += 1
                        # Update processed items count
                        processed_photos += 1
                        if photo_id is not None:
                            with get_db_session() as session:
                                update_album_processed_items(
                                    session, album_id, processed_photos
                                )

                            # Link user to album for shared photos

                            # Display progress for successfully processed photo
                            progress.update(
                                task,
                                advance=1,
                                description=f"[green]{processed_photos}/{album_items} - {picture_info.filename}[/green]",
                            )
                        else:
                            # Photo is a duplicate, skip it but continue processing
                            console.print(
                                f"[yellow]Skipping exiting photo: {picture_info.filename}[/yellow]"
                            )

                    except Exception as e:
                        logger.error(f"Error saving picture to database: {e}")
                        insert_error(
                            f"Error saving picture {picture_info.filename}: {e}",
                            album_id,
                        )

                    # Navigate to next image (always advance, even for duplicates)
                    await self.keyboard_press(
                        "ArrowRight", delay=IMAGE_NAVIGATION_DELAY
                    )

                except Exception as e:
                    logger.error(f"Error processing picture: {e}")
                    insert_error(
                        f"Error processing picture in album {album_gphoto_title}: {e}",
                        album_id,
                    )
                    break

        # Return to albums view
        await self.page.goto("https://photos.google.com/albums")
        await self.page.wait_for_load_state("domcontentloaded")

        # Create AlbumInfo object for return
        album_info = AlbumInfo(
            title=album_gphoto_title,
            items=album_items,
            shared=False,  # We'll get this from DB if needed
            # pictures=pictures,
            url=album_gphoto_url,
        )

        console.print(
            f"[green]Processed {len(pictures)} pictures from {album_gphoto_title}[/green]"
        )
        if processed_users:
            console.print(
                f"[blue]Associated users: {', '.join(processed_users)}[/blue]"
            )
        return album_info

        #
        ## Navigate to first photo if needed
        # if existing_count > 0:
        #    console.print(f"[blue]Resuming from photo {existing_count + 1}[/blue]")
        #    # This would need navigation logic to skip to the right photo
        #    # For now, we'll start from the beginning and handle duplicates
        #
        # while processed_photos < (album_items - existing_count):
        #    try:
        #        # Get picture info
        #        picture_info = await self.get_picture_info(album_gphoto_title)
        #        if not picture_info:
        #            break
        #
        #        # Get or create user
        #        with get_db_session() as session:
        #            user_id = insert_or_update_user(session, picture_info.user)
        #
        #        # Insert photo (returns None if already exists)
        #        with get_db_session() as session:
        #            photo_id = insert_photo(session, picture_info, user_id, album_id)
        #
        #        if photo_id is None:
        #            duplicate_count += 1
        #            if duplicate_count <= DUPLICATE_LOG_THRESHOLD:
        #                console.print(f"[yellow]Duplicate photo: {picture_info.filename}[/yellow]")
        #            elif duplicate_count == DUPLICATE_LOG_THRESHOLD + 1:
        #                console.print(f"[yellow]... (more duplicates suppressed) [/yellow]")
        #        else:
        #            processed_photos += 1
        #            console.print(f"[green]Processed photo {processed_count + processed_photos}/{album_items}: {picture_info.filename}[/green]")
        #
        #            # Update processed items count
        #            with get_db_session() as session:
        #                update_album_processed_items(session, album_id, processed_count + processed_photos)
        #
        #            # Link user to album
        #            with get_db_session() as session:
        #                link_user_to_album(session, album_id, user_id)
        #
        #        # Navigate to next photo
        #        await self.page.keyboard.press('ArrowRight')
        #        await asyncio.sleep(IMAGE_NAVIGATION_DELAY)
        #
        #        # Check if we've reached the end (circular navigation)
        #        if processed_photos > 0 and duplicate_count > DUPLICATE_THRESHOLD:
        #            console.print(f"[yellow]Reached end of album (too many duplicates)[/yellow]")
        #            break
        #
        #    except Exception as e:
        #        error_msg = f"Error processing photo in album {album_gphoto_title}: {e}"
        #        console.print(f"[red]{error_msg}[/red]")
        #        with get_db_session() as session:
        #            insert_error(session, error_msg, album_id)
        #
        #        # Try to continue to next photo
        #        await self.page.keyboard.press('ArrowRight')
        #        await asyncio.sleep(IMAGE_NAVIGATION_DELAY)
        #        continue
        #
        # console.print(f"[green]Completed processing album {album_gphoto_title}[/green]")
        # console.print(f"[green]Processed {processed_photos} new photos, encountered {duplicate_count} duplicates[/green]")

    async def navigate_to_album(self, album_position: int) -> None:
        """Navigate to the next album using arrow keys."""
        console.print(f"[blue]Navigating to album {album_position}[/blue]")
        for _ in range(album_position):
            await self.keyboard_press("ArrowRight", delay=ALBUM_NAVIGATION_DELAY)
        console.print("[blue]Done[/blue]")

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
        console.print(f"[blue]Starting from album position {start_album}[/blue]")
        if max_albums:
            console.print(f"[blue]Maximum albums to collect: {max_albums}[/blue]")

        albums_collected = []
        albums_processed = 0

        # Navigate to Google Photos albums
        await self.open_gphotos(path="albums")
        # if self.login:
        #    console.print("[yellow]Press Enter when logged in and on the albums site...[/yellow]")
        #    input()
        # else:
        #    await self.page.wait_for_load_state("domcontentloaded")
        #    await asyncio.sleep(1)

        # Wait for the page to be fully ready
        # console.print("[yellow]Waiting for page to be fully ready...[/yellow]")
        await asyncio.sleep(1)

        # Press ArrowRight to select the first album
        logger.debug("Pressing ArrowRight to select first album...")
        await self.keyboard_press("ArrowRight", delay=ALBUM_NAVIGATION_DELAY)

        # Wait a moment for the focus to settle
        await asyncio.sleep(0.2)

        console.print(
            f"[blue]Starting to collect {max_albums} albums from index {start_album}...[/blue]"
        )

        # Navigate to the first album to process
        if start_album > 1:
            console.print(
                f"[yellow]Navigating to album index {start_album}...[/yellow]"
            )
            await self.navigate_to_album(
                start_album - 2
            )  # Convert to 0-based and adjust for starting position

        prev_album = None
        for album_position in range(start_album - 1, start_album - 1 + max_albums):
            try:
                # Navigate to next album (only one step from current position)
                # Only navigate if we're past the first album in our collection
                if album_position > start_album - 1:
                    console.print(
                        f"[blue]Navigating to album {album_position}... (start album: {start_album})[/blue]"
                    )
                    await self.keyboard_press(
                        "ArrowRight", delay=ALBUM_NAVIGATION_DELAY
                    )

                # Get album info
                album_info = await self.get_album_info()
                if album_info is None:
                    console.print(
                        "[yellow]No album info found, stopping collection[/yellow]"
                    )
                    break

                console.print(f"[green]Collecting album: {album_info.title}[/green]")

                # Check if album already exists in database
                with get_db_session() as session:
                    exists = album_exists(session, album_info.title)

                if not exists:
                    # Insert album into database
                    with get_db_session() as session:
                        album_id = insert_or_update_album(session, album_info)
                    console.print(
                        f"[green]Added album {album_info.title} to database (ID: {album_id})[/green]"
                    )
                    albums_collected.append(album_info)
                else:
                    console.print(
                        f"[yellow]Album {album_info.title} already exists in database. Skipping.[/yellow]"
                    )

                albums_processed += 1

                if prev_album and prev_album.url == album_info.url:
                    console.print(
                        "[yellow]All albums collected (duplicate detected)[/yellow]"
                    )
                    break
                prev_album = AlbumInfo(**asdict(album_info))

            except Exception as e:
                error_msg = f"Error collecting album: {e}"
                console.print(f"[red]{error_msg}[/red]")
                with get_db_session() as session:
                    insert_error(session, error_msg)
                break

        console.print(
            f"[green]Completed collecting {len(albums_collected)} albums[/green]"
        )
        return albums_collected

    async def scrape_albums_from_db(
        self, max_albums: int = None, start_album: int = 1
    ) -> ProcessingResult:
        """Process images from albums stored in the database."""
        # await self.setup_browser()

        self.open_gphotos(path="albums")

        console.print("[green]Processing albums from database...[/green]")
        console.print(f"[blue]Starting from album position {start_album}[/blue]")
        if max_albums:
            console.print(f"[blue]Maximum albums to process: {max_albums}[/blue]")

        # Get albums from database
        with get_db_session() as session:
            albums = get_albums_from_db(
                session, limit=max_albums, offset=start_album - 1
            )

        if not albums:
            console.print("[yellow]No albums found in database.[/yellow]")

            # If no albums exist and we're in albums-only mode, collect them first
            if self.albums_only:
                console.print(
                    "[blue]No albums found, collecting from UI first...[/blue]"
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

            return ProcessingResult(
                total_albums=0, total_pictures=0, albums_processed=[], errors=[]
            )

        console.print(f"[blue]Found {len(albums)} albums to process[/blue]")

        # Process each album
        albums_processed = []
        total_pictures = 0
        errors = []

        for album_id, album_gphoto_url, album_gphoto_title, album_items in albums:
            try:
                if self.albums_only:
                    # In albums-only mode, we just need to ensure the album exists
                    console.print(
                        f"[blue]Album {album_gphoto_title} already exists in database[/blue]"
                    )
                    albums_processed.append(
                        AlbumInfo(
                            title=album_gphoto_title,
                            items=album_items,
                            shared=False,  # We don't have this info in the tuple
                            url=album_gphoto_url,
                        )
                    )
                else:
                    # Process the album
                    await self.process_album_from_db(
                        album_id, album_gphoto_url, album_gphoto_title, album_items
                    )
                    albums_processed.append(
                        AlbumInfo(
                            title=album_gphoto_title,
                            items=album_items,
                            shared=False,  # We don't have this info in the tuple
                            url=album_gphoto_url,
                        )
                    )
                    total_pictures += album_items

            except Exception as e:
                error_msg = f"Error processing album {album_gphoto_title}: {e}"
                console.print(f"[red]{error_msg}[/red]")
                errors.append(error_msg)
                with get_db_session() as session:
                    insert_error(session, error_msg, album_id)
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
