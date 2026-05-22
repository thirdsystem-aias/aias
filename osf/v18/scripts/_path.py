"""scripts/_path.py — bootstrap protocol/ onto sys.path

Python adds the script's own directory (scripts/) to sys.path automatically
when you run `python scripts/foo.py`, but does NOT add the parent project
root. This bootstrap inserts the project root so `from protocol import ...`
resolves correctly.

Usage — add ONE LINE before any `from protocol ...` import at the top of
the script:

    import _path  # noqa: F401   ← runs sys.path injection as a side effect
    from protocol import PROTOCOL_VERSION

The `noqa: F401` comment suppresses linter warnings about an "unused" import.
The import IS used — for its side effect of modifying sys.path.
"""
import sys
from pathlib import Path

# Project root = parent of scripts/ (where _path.py lives)
_PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))
