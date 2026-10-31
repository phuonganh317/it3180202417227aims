import unittest

from aims.dvd import DigitalVideoDisc
from aims.search import search_by_title


class TitleSearchTests(unittest.TestCase):
    def setUp(self):
        self.items = [DigitalVideoDisc("The Lion King"),
                      DigitalVideoDisc("Star Wars"),
                      DigitalVideoDisc("LION documentary")]

    def test_lowercase_keyword_matches_mixed_case_titles(self):
        self.assertEqual(search_by_title(self.items, "lion"),
                         [self.items[0], self.items[2]])

    def test_uppercase_keyword_matches_mixed_case_title(self):
        self.assertEqual(search_by_title(self.items, "STAR"), [self.items[1]])

    def test_no_match_and_empty_input(self):
        self.assertEqual(search_by_title(self.items, "missing"), [])
        self.assertEqual(search_by_title([], "lion"), [])

    def test_empty_keyword_preserves_items_and_order(self):
        original = list(self.items)
        self.assertEqual(search_by_title(self.items, ""), original)
        self.assertEqual(self.items, original)


if __name__ == "__main__":
    unittest.main()
