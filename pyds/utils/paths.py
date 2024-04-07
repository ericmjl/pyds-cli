"""Definition for special paths that we're looking for."""
from pathlib import Path

PYPIRC_PATH = Path.home() / ".pypirc"

SOURCE_DIR = Path(__file__).parent.parent

PROJECT_TEMPLATE_DIR = SOURCE_DIR / "templates" / "project"
TALK_TEMPLATE_DIR = SOURCE_DIR / "templates" / "talk"
