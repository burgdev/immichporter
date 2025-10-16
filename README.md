<h3 align="center"><b>Immichporter</b></h3>
<p align="center">
  <a href="https://burgdev.github.io/immichporter"><img src="https://raw.githubusercontent.com/burgdev/immichporter/refs/heads/main/assets/logo/logo.svg" alt="Immichporter" width="128" /></a>
</p>
<p align="center">
    <em>Google photos to immich importer helper</em>
</p>
<p align="center">
    <b><a href="https://burgdev.github.io/immichporter">Documentation</a></b>
    | <b><a href="https://pypi.org/project/immichporter">PyPI</a></b>
</p>

---


> [!WARNING]
> * **Still experimental:** Google Photos export works in some cases, but stability issues remain.
> * Only works in **English**
> * Immich import/update not yet tested!


**Immichporter** exports google photos *information* into a sqlite database which can be used to import the information back into immich.

> [!IMPORTANT]
> * This tool **does not** download any images from google photos. It only exports the information into a database.
> * Make sure to manulley save all shared pictures in google photos before running a takeout.

<!-- # --8<-- [start:readme_index] <!-- -->

Use [google takeout](https://takeout.google.com) to export your google photos assets and [`immich-go`](https://github.com/simulot/immich-go) to import the data into immich.

> [!IMPORTANT]

Use [`immichporter`](https://github.com/burgdev/immichporter) to get all assets and user per album and update/create all albums in immich again.
It can add all users again to shared albums and you can even move assets to the correct user.

## Installation

Using [uv](https://github.com/astral-sh/uv) (recommended):
```bash
uv add immichporter
```

Or with pip:
```bash
pip install immichporter
```


## Usage

```bash
# Show help
immichporter --help

playwright install # might be required the first time

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

# edit/update users
immichporter db show-users
immichporter db edit-users # select which users should be added to immich

# see the database with https://sqlitebrowser.org
sqlitebrowser immichporter.db

# !! CAUTION: create a backup of your immich database before running this commands !!

# this steps are needed to get the immich ids into the 'immichporter.db' sqlite database
# and create non existing users and albums in immich
immichporter immich update-albums
immichporter immich update-users


# delete ablums (optional) if you want to start over
# !! this delete all albums in immich !!
# this is only needed if you have different album names in immich
immichporter immich delete-albums

# sync albums to immich (create albums and users, add assets to albums)
export IMMICH_ENDPOINT=http://localhost:2283
export IMMICH_API_KEY=your_api_key
export IMMICH_INSECURE=1
immichporter sync-albums --dry-run  
immichporter sync-albums
```

## TODO:

* [x] export albums with photos and people from gphotos (first version)
* [ ] import to immich (80%)
* [ ] move assets to correct user (50%)
* [ ] improve documentation
* [ ] improve gphotos export stability (80%)

<!-- # --8<-- [end:readme_index] <!-- -->

<!--
## Documentation

For complete documentation, including API reference and advanced usage, please visit the [documentation site](https://burgdev.github.io/immichporter/docu/).
-->

<!-- # --8<-- [start:readme_development] <!-- -->
## Development

To set up the development environment:

```bash
# Clone the repository
git clone https://github.com/burgdev/immichporter.git
cd immichporter

# Install development dependencies
make
uv run invoke install # install 'dev' and 'test' dependencies per default, use --all to install all dependencies
```
<!-- # --8<-- [end:readme_development] <!-- -->

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details.

## License

MIT - See [LICENSE](LICENSE) for details.
