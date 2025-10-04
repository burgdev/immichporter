"""Utility functions for immichporter."""


def sanitize_for_email(name: str) -> str:
    """Sanitize a name for use in an email address.

    Replaces spaces with dots, converts to lowercase, and removes umlauts.
    """
    # First replace special characters
    replacements = {
        "ä": "ae",
        "ö": "oe",
        "ü": "ue",
        "ß": "ss",
        "é": "e",
        "è": "e",
        "ê": "e",
        "ë": "e",
        "à": "a",
        "â": "a",
        "á": "a",
        "å": "a",
        "ô": "o",
        "ó": "o",
        "ò": "o",
        "õ": "o",
        "î": "i",
        "í": "i",
        "ì": "i",
        "ï": "i",
        "û": "u",
        "ú": "u",
        "ù": "u",
        "ÿ": "y",
        "ý": "y",
        "ç": "c",
        "ñ": "n",
    }

    # Replace each character
    for orig, repl in replacements.items():
        name = name.replace(orig, repl)

    # Now normalize to handle any remaining unicode characters
    import unicodedata

    name = unicodedata.normalize("NFKD", name)

    # Remove any remaining non-ASCII characters and convert to lowercase
    name = "".join(c for c in name if ord(c) < 128)

    # Replace spaces with dots and convert to lowercase
    return name.replace(" ", ".").lower()
