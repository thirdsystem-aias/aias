"""LOCAL FAKE of google.genai.types (rehearsal only)."""
from types import SimpleNamespace as NS


def Tool(**kw):
    return NS(**kw)


def GoogleSearch(**kw):
    return NS(**kw)


def GenerateContentConfig(**kw):
    return NS(**kw)
