from tasks import (
    Ctx,
    doc,
    header,
    task,
)


@task
def run(c: Ctx, parallel: bool = False):
    """Run tests"""
    header(doc())
    c.run("pytest -v" + (" -n auto" if parallel else ""), echo=True, pty=True)
