<h3 align="center"><b>Immichporter</b></h3>
<p align="center">
  <a href="https://burgdev.github.io/immichporter"><img src="https://raw.githubusercontent.com/burgdev/immichporter/refs/heads/main/assets/logo/logo.svg" alt="Immichporter" width="128" /></a>
</p>
<p align="center">
    <em>Import your Google Photos structure and sharing info into Immich — metadata only, no image data.</em>
</p>
<p align="center">
    <b><a href="https://burgdev.github.io/immichporter">Documentation</a></b>
    | <b><a href="https://pypi.org/project/immichporter">PyPI</a></b>
</p>

---


> [!WARNING]
> * **Still experimental:** Google Photos export works in some cases, but stability issues remain.
> * Only works in **English**

**[`Immichporter`](https://github.com/burgdev/immichporter)** retrieves metadata not available in google takeout, including shared albums, assets, and shared users. You can use this data to update assets in Immich, re-add users to shared albums, and even move assets to their correct owners.

> [!IMPORTANT]
> * This tool **does not** download any images from google photos. It only extracts the information into a local database.
> * Make sure to manually save all shared pictures in google photos before running a takeout.

<!-- # --8<-- [start:readme_index] <!-- -->

Use [google takeout](https://takeout.google.com) to export your google photos assets and [`immich-go`](https://github.com/simulot/immich-go) to import the data into immich.


## Installation

Run it directly with [uv](https://github.com/astral-sh/uv) (recommended):

```bash
uvx immichporter -h
```

or install it:

Using:

```bash
uv add immichporter
```

Or with pip:
```bash
pip install immichporter
```

## Usage

**NOTE:** You need to import the assets into immich first, before running photos sync to immich.

```bash
# Show help
immichporter --help

# login is required the first time, the session is saved
immichporter gphotos login

# add all albums to the database
immichporter gphotos albums

# add all photos for each album to the database
# it can run multiple times and only processes the not fully processed albums again
immichporter gphotos photos

# multiple runs might be needed until everything is correct,
# you can check with if every album is fully processed
immichporter db show-albums --not-finished
# run again
immichporter gphotos photos --not-finished

# edit/update users
immichporter db show-users
immichporter db edit-users # select which users should be added to immich

# see the database with https://sqlitebrowser.org
sqlitebrowser immichporter.db

# !! CAUTION: create a backup of your immich database before running this commands !!

export IMMICH_ENDPOINT=http://localhost:2283
export IMMICH_API_KEY=your_api_key
export IMMICH_INSECURE=1

# this steps are needed to get the immich ids into the 'immichporter.db' sqlite database
# and create non existing users and albums in immich
immichporter immich update-albums
immichporter immich update-users

# delete ablums (optional) if you want to start over
# !! this delete all albums in immich !!
# this is only needed if you have different album names in immich
immichporter immich delete-albums

# sync albums to immich (create albums and users, add assets to albums)
immichporter sync-albums --dry-run  
immichporter sync-albums
```

## TODO

* [x] get all ablums from gphotos
* [x] get all metadata from photos inside the albums (shared with, timestamp, ...)
* [x] update user information (local DB)
* [x] create or update albums in immich
* [x] create or update users in immich
* [x] add/update assets to albums in immich
* [ ] move assets to correct user (needs to be tested)
* [ ] improve documentation
* [ ] interactive wizard with ui (web or gui ...)
* [ ] submit changes to server for an admin to review and update

<!-- # --8<-- [end:readme_index] <!-- -->

<!--
## Documentation

For complete documentation, including API reference and advanced usage, please visit the [documentation site](https://burgdev.github.io/immichporter/docu/).
-->

<!-- # --8<-- [start:readme_development] <!-- -->
## Development

### Dependencies

* [uv](https://github.com/astral-sh/uv)
* [just](https://github.com/casey/just)

### Setup

To set up the development environment:

```bash
# Clone the repository
git clone https://github.com/burgdev/immichporter.git
cd immichporter

# Install development dependencies
just install
source .venv/bin/activate
```
<!-- # --8<-- [end:readme_development] <!-- -->

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details.

## License

MIT - See [LICENSE](LICENSE) for details.
