import unittest

from aims.dvd import DigitalVideoDisc
from aims.search import search_by_category


class CategorySearchTests(unittest.TestCase):
    def test_matches_category_case_insensitively_and_preserves_order(self):
        items = [DigitalVideoDisc("A", "Animation"),
                 DigitalVideoDisc("B", "Drama"),
                 DigitalVideoDisc("C", "Animation")]
        self.assertEqual(search_by_category(items, "ANIM"), [items[0], items[2]])
        self.assertEqual(len(items), 3)

    def test_empty_and_missing_matches(self):
        items = [DigitalVideoDisc("A", "Drama")]
        self.assertEqual(search_by_category([], "Drama"), [])
        self.assertEqual(search_by_category(items, "Animation"), [])
        self.assertEqual(search_by_category(items, ""), items)


if __name__ == "__main__":
    unittest.main()
