def search_by_category(items, keyword):
    """Return DVDs whose categories contain keyword, ignoring case."""
    return [dvd for dvd in items if keyword.lower() in dvd.category.lower()]


def search_by_title(items, keyword):
    """Return DVDs whose titles contain keyword, ignoring case."""
    return [dvd for dvd in items if keyword.lower() in dvd.title.lower()]
