<h3 align="center"><b>Imgora</b></h3>
<p align="center">
  <a href="https://burgdev.github.io/imgora"><img src="https://raw.githubusercontent.com/burgdev/imgora/refs/heads/main/assets/logo/logo.svg" alt="Imgora" width="128" /></a>
</p>
<p align="center">
    <em>Chainable Python client for Imagor and Thumbor image processing servers</em>
</p>
<p align="center">
    <b><a href="https://burgdev.github.io/imgora">Documentation</a></b>
    | <b><a href="https://pypi.org/project/imgora">PyPI</a></b>
</p>

---
<!-- # --8<-- [start:readme_index] <!-- -->

**Imgora** provides a clean, chainable interface for generating image URLs for [Imagor](https://github.com/cshum/imagor), [Thumbor](https://github.com/thumbor/thumbor) and [Wsrv.nl](https://wsrv.nl) image processing servers. It supports all standard operations and filters with full type hints and documentation.

## Features

- **[Imagor](https://github.com/cshum/imagor), [Thumbor](https://github.com/thumbor/thumbor) & [Wsrv.nl](https://wsrv.nl) Support**: Compatible with Imagor, Thumbor and Wsrv.nl servers
- **URL Signing**: Built-in support for secure URL signing
- **Chainable API**: Fluent interface for building complex image processing pipelines
- **Comprehensive Filter Support**: Implements all standard filters and operations
- **Fully Typed**: Built with Python's type hints for better IDE support and code quality

## Installation

Using [uv](https://github.com/astral-sh/uv) (recommended):
```bash
uv pip install imgora
```

Or with pip:
```bash
pip install imgora
```

## Quick Start

```python
from imgora import WsrvNl

image_url = "https://wsrv.nl/puppy.jpg"

img = (
    # Imagor(base_url="http://localhost:8018", signer=Signer(key="my_key", type="sha256"))
    WsrvNl()
    .with_image(image_url)
    .crop(0.1, 0.2, 0.6, -100)
    .resize(200, 150)
    .blur(3)
    .grayscale()
    .quality(50)
)

# print(img.path()) # path without url
print(img.url())
```
Which returns:

```
https://wsrv.nl/?url=https%3A%2F%2Fwsrv.nl%2Fpuppy.jpg&cx=166&cy=221&cw=831&ch=787&precrop&w=200&h=150&blur=2.50&filt=greyscale&quality=50
```


<figure>
<a href="https://wsrv.nl/?url=https%3A%2F%2Fwsrv.nl%2Fpuppy.jpg&cx=166&cy=221&cw=831&ch=787&precrop&w=200&h=150&blur=2.50&filt=greyscale&quality=50" target="_blank">
    <img src="https://wsrv.nl/?url=https%3A%2F%2Fwsrv.nl%2Fpuppy.jpg&cx=166&cy=221&cw=831&ch=787&precrop&w=200&h=150&blur=2.50&filt=greyscale&quality=50" />
</a><br />
    <figcaption>Processed image</figcaption>
</figure>
<br />
<figure>
<a href="https://wsrv.nl/puppy.jpg" target="_blank">
    <img src="https://wsrv.nl/puppy.jpg" width="400" />
</a><br />
    <figcaption><a href="https://wsrv.nl/puppy.jpg" target="_blank">Original image</a> (width reduced to 400px)</figcaption>
</figure>
<br /><br />

**NOTE:**

In order to test the url with Imagor or Thumbor you need to start a server.
You can do this with the following command:

```bash
docker compose up imagor -d
docker compose up thumbor -d
```

### More Examples

```bash
docker compose up -d # start imagor and thumbor server
uv run examples/compare_backends.py
```
<!-- # --8<-- [end:readme_index] <!-- -->

## Documentation

For complete documentation, including API reference and advanced usage, please visit the [documentation site](https://burgdev.github.io/imgora/docu/).

<!-- # --8<-- [start:readme_development] <!-- -->
## Development

To set up the development environment:

```bash
# Clone the repository
git clone https://github.com/burgdev/imgora.git
cd imgora

# Install development dependencies
make
uv run invoke install # install 'dev' and 'test' dependencies per default, use --all to install all dependencies
```
<!-- # --8<-- [end:readme_development] <!-- -->

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details.

## License

MIT - See [LICENSE](LICENSE) for details.
