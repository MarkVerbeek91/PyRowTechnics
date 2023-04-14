import shutil
from pathlib import Path

import nox

PYTHON_VERSIONS = ("3.8", "3.9", "3.10", "3.11")
DEFAULT_VERSION = "3.10"


@nox.session(python=PYTHON_VERSIONS)
def tests(session):
    """Run the test suite."""
    base_install(session)

    session.install("-e", ".")

    session.run("pytest", *session.posargs)


@nox.session(python=DEFAULT_VERSION)
def lint(session):
    """Run pre-commit hooks on ALL files."""
    base_install(session)
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
    base_install(session)

    clean(session)

    session.run("python", "-m", "build")
    session.run("twine", "check", "dist/*")


@nox.session(python=DEFAULT_VERSION)
def clean(_):
    """Clean wheels locally."""
    remove_build_folders()
    remove_egg_info()


@nox.session(python=DEFAULT_VERSION)
def publish(session) -> None:
    """Build and publish local version."""
    build(session)

    session.run("twine", "upload", "-r", "testpypi", "dist/*")


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

    base_install(session)

    build_type = "doctest"

    args = get_doc_build_args(build_type)

    session.run("sphinx-build", *args)


def base_install(session):
    """Do base install"""
    session.install("-r", "requirements-dev.txt")


def get_doc_build_args(build_type):
    return [
        *["-b", f"{build_type}"],
        *["-d", "docs/_build/doctrees"],
        "docs",
        f"docs/_build/{build_type}",
    ]


def remove_build_folders():
    for p in ("build", "dist", "docs/_build"):
        shutil.rmtree(p, ignore_errors=True)


def remove_egg_info():
    for p in Path("src").glob("*.egg-info"):
        shutil.rmtree(p, ignore_errors=True)
