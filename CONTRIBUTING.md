
## Development

### Initial Setup

```bash
make
```

### Commands

After this the command `inv` is used:

```bash
source .venv/bin/activate
inv help
inv install        # install updates
inv check          # run all quality checks
```

### Release

For a release run `inv release`.
Merge this change into the `main` branch and tag it accordingly
and if needed create a GitHub release.
