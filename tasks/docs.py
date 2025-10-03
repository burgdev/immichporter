from tasks import (  # noqa: F401
    Ctx,
    EnvError,
    echo,
    env,
    error,
    header,
    info,
    success,
    task,
    warning,
)


@task(help={"port": "Port to serve documentation locally, default: '8000'"})
def serve(c: Ctx, port: int = 8088):
    """Serve docu for preview."""
    dev_addr = f"localhost:{port}"
    c.run(f"mkdocs serve --dev-addr {dev_addr}", echo=True, pty=True)


@task
def build(c: Ctx):
    """Build docu."""
    c.run("mkdocs build", echo=True, pty=True)
    success("Documentation build in 'site' directory.")
    info("Run 'python -m http.server -d site' for testing (not in production).")
