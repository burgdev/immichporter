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


if __name__ == "__main__":
    for _ in range(10):
        print(generate_password())
