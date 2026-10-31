def search_by_title(items, keyword):
    """Return DVDs whose titles contain keyword (case-sensitive)."""
    return [dvd for dvd in items if keyword in dvd.title]
