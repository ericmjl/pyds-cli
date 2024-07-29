"""Top-level module for pyds."""

from .version import __version__

# Try importing pixi from sh, if not available, then auto-install pixi
try:
    from sh import pixi  # noqa: F401
except ImportError:
    err_msg = """To use `pyds`, you need to have `pixi` installed.

Please follow installation instructions available at: https://pixi.sh/latest/
"""
    raise ImportError(err_msg)

__all__ = ["__version__"]
