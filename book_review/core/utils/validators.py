import re
from django.core.exceptions import ValidationError


def clear_punctuation(document: str):
    """Remove from document all pontuation signals."""
    return re.sub("\D", "", str(document))
