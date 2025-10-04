<h3 align="center"><b>Immichporter</b></h3>
<p align="center">
  <a href="https://burgdev.github.io/immichporter"><img src="https://raw.githubusercontent.com/burgdev/immichporter/refs/heads/main/assets/logo/logo.svg" alt="Immichporter" width="128" /></a>
</p>
<p align="center">
    <em>Google photos to immich importer helper</em>
</p>
<!--
<p align="center">
    <b><a href="https://burgdev.github.io/immichporter">Documentation</a></b>
    | <b><a href="https://pypi.org/project/immichporter">PyPI</a></b>
    -->
</p>

---


> [!WARNING]
> Still in a early stage. At the moment only exporting from google photos is supported.


**Immichporter** exports google photos information into a database which can be used to import the information back into immich.

> [!IMPORTANT]
> This tool does not download any images from google photos. It only exports the information into a database.

<!-- # --8<-- [start:readme_index] <!-- -->

Use [google takeout](https://takeout.google.com) to export your google photos data and the [`immich-go`](https://github.com/simulot/immich-go) tool to import the data into immich. After this you can use [`immichporter`](https://github.com/burgdev/immichporter) to create all albums and add people to shared albums.

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

# login is required the first time, the session is saved
immichporter gphotos login

# add all albums to the database
immichporter gphotos albums

# add all photos for each album to the database
immichporter gphotos photos
# multiple runs miht be needed until everything is correct!

# see the database with https://sqlitebrowser.org
sqlitebrowser immichporter.db
```

## TODO:

* [x] export albums with photos and people from gphotos (first version)
* [ ] import to immich
* [ ] improve documentation
* [ ] imporve gphotos export stability

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
