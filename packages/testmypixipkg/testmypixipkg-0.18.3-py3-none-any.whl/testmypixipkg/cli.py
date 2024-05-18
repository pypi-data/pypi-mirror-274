"""This module contains the CLI commands for the package."""

import rich_click as click


def test_func() -> None:
    """A test function."""
    click.echo("This is a test function.")


if "__main__" == __name__:
    test_func()
