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
<!-- # --8<-- [start:readme_index] <!-- -->

**Immichporter** exports google photos information into a database which can be used to import the information back into immich.

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

# Source-specific operations
immichporter gphoto export-albums
immichporter gphoto export-photos

# Database operations
immichporter db show-albums
immichporter db show-users
immichporter db show-stats

# Immich operations
immichporter immich create-album
immichporter immich import-photos
```

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
