import re

def clean_text(text):
    """Simple cleaning: remove extra whitespace, newlines, and non-printable characters."""
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[^\x00-\x7F]+', '', text)
    return text.strip()