"""Conjure the perfect CV with Typst magic - transform YAML data into professional documents."""

__version__ = "0.1.0"

def main():
    """Entry point for the CLI."""
    from .cli import main as cli_main
    return cli_main()

__all__ = ["main"]