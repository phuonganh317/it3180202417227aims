import unittest

from aims.cart import Cart
from aims.dvd import DigitalVideoDisc


class CartSortTests(unittest.TestCase):
    def setUp(self):
        self.cart = Cart()
        self.discs = [
            DigitalVideoDisc("Zulu", cost=30),
            DigitalVideoDisc("alpha", cost=20),
            DigitalVideoDisc("Alpha", cost=10),
            DigitalVideoDisc("Beta", cost=20),
        ]
        self.cart.items.extend(self.discs)

    def test_sort_by_title_is_case_insensitive_and_stable(self):
        original_list = self.cart.items
        self.cart.sort_by_title()
        self.assertIs(self.cart.items, original_list)
        self.assertEqual(self.cart.items, [self.discs[i] for i in (1, 2, 3, 0)])
        self.assertEqual(self.cart.total_cost(), 80)

    def test_sort_by_cost_is_ascending_and_stable(self):
        original_list = self.cart.items
        self.cart.sort_by_cost()
        self.assertIs(self.cart.items, original_list)
        self.assertEqual(self.cart.items, [self.discs[i] for i in (2, 1, 3, 0)])
        self.assertEqual(self.cart.total_cost(), 80)

    def test_empty_cart(self):
        cart = Cart()
        cart.sort_by_title()
        cart.sort_by_cost()
        self.assertEqual(cart.items, [])

    def test_single_disc(self):
        cart = Cart()
        cart.items.append(self.discs[0])
        cart.sort_by_title()
        cart.sort_by_cost()
        self.assertEqual(cart.items, [self.discs[0]])


if __name__ == "__main__":
    unittest.main()
