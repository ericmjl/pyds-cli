"""Top-level module for pyds."""

from .version import __version__

# Try importing pixi from sh, if not available, then auto-install pixi
try:
    from sh import pixi  # noqa: F401
except ImportError:
    import subprocess

    subprocess.run("curl", "-fsSL", "https://pixi.sh/install.sh", "|", "bash")

__all__ = ["__version__"]
