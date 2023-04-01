import shutil
from pathlib import Path

import nox

PYTHON_VERSIONS = ("3.8", "3.9", "3.10", "3.11")
DEFAULT_VERSION = PYTHON_VERSIONS[-1]


@nox.session(python=PYTHON_VERSIONS)
def tests(session):
    """Run the test suite."""
    session.install("-r", "requirements-dev.txt")

    session.install("-e", ".")

    session.run("pytest", *session.posargs)


@nox.session(python=DEFAULT_VERSION)
def textx(session):
    """Check the command line interface."""
    session.install("-r", "requirements.txt")

    session.install("-e", ".")

    session.run("textx", "list-languages")


@nox.session(python=DEFAULT_VERSION)
def lint(session):
    """Run pre-commit hooks on ALL files."""
    session.install("-r", "requirements-dev.txt")
    session.install("pre-commit")

    args = [
        "pre-commit",
        "run",
        "--all-files",
    ]
    session.run(*args)


@nox.session(python=DEFAULT_VERSION)
def mypy_typing(session):
    """Run mypy type checking on files in src/ folder."""
    session.skip()

    session.install("mypy")

    session.run("mypy", "src")


@nox.session(python=DEFAULT_VERSION)
def build(session):
    """Build wheels for distribution."""
    session.install("-r", "requirements-dev.txt")

    clean(session)

    session.run("python", "-m", "build")
    session.run("twine", "check", "dist/*")


@nox.session(python=DEFAULT_VERSION)
def clean(_):
    """Clean wheels locally."""
    remove_build_folders()
    remove_egg_info()


def remove_build_folders():
    for p in ("build", "dist", "docs/_build"):
        shutil.rmtree(p, ignore_errors=True)


def remove_egg_info():
    for p in Path("src").glob("*.egg-info"):
        shutil.rmtree(p, ignore_errors=True)


@nox.session(python=DEFAULT_VERSION)
def publish(session) -> None:
    """Build and publish local version."""
    # TODO do quality check first, like testing and linting.

    build(session)

    args = [
        *["--repository", "atrifactory-de"],
        *["--config-file", str(Path(__file__).parent / "secrets" / ".pypirc")],
        *["--cert", "secrets/artifactory-de.cer"],
        "--verbose",
        "dist/*",
    ]
    session.run("twine", "upload", *args)


@nox.session(python=DEFAULT_VERSION)
def docs(session):
    """Build Sphinx style documentation."""
    session.install("-r", "docs/requirements.txt")

    build_type = "html"

    args = get_doc_build_args(build_type)

    session.run("sphinx-build", *args)


@nox.session(python=DEFAULT_VERSION)
def doctest(session):
    """Run doctests in documentation."""

    session.install("-r", "docs/requirements.txt")

    build_type = "doctest"

    args = get_doc_build_args(build_type)

    session.run("sphinx-build", *args)


def get_doc_build_args(build_type):
    return [
        *["-b", f"{build_type}"],
        *["-d", "docs/_build/doctrees"],
        "docs",
        f"docs/_build/{build_type}",
    ]
