"""Utility functions for immichporter."""

import random


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


def generate_password() -> str:
    """Generate a password using 5 words from English, German, and French."""
    words = {
        "en": ["house", "garden", "pool", "door", "bed"],
        "de": ["Haus", "Garten", "Bad", "Pforte", "Bett"],
        "fr": ["maison", "jardin", "piscine", "porte", "lit"],
    }

    # Select 5 random words, one from each language and two more random ones
    selected = [
        random.choice(random.choice(list(words.values()))),
        random.choice(random.choice(list(words.values()))),
        random.choice(random.choice(list(words.values()))),
    ]

    # Shuffle the words and join with a hyphen
    random.shuffle(selected)
    return (
        random.choice(["-", "_", "+"]).join(selected)
        + random.choice(["$", "#", "!"])
        + str(random.randint(10, 99))
    )


def is_number(value: str) -> bool:
    """Check if a string can be converted to a number (int or float)."""
    try:
        float(str(value).strip())
        return True
    except (ValueError, TypeError):
        return False


def format_csv_value(value) -> str:
    """Format a value for CSV output."""
    if value is None:
        return '""'

    # Convert to string and strip whitespace for number checking
    str_value = str(value).strip()

    # Check if it's a number (int or float)
    if is_number(str_value):
        # If it's a whole number, convert to int, otherwise keep as float
        try:
            if float(str_value).is_integer():
                return str(int(float(str_value)))
            return str(float(str_value))
        except (ValueError, TypeError):
            pass

    if isinstance(value, bool):
        return "1" if value else "0"

    if value is None:
        return ""

    # If we get here, it's not a number or boolean, so treat as string
    escaped_value = str_value.replace('"', '""')
    return '"' + escaped_value + '"'


if __name__ == "__main__":
    for _ in range(10):
        print(generate_password())
