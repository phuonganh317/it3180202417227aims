import unittest

from aims.cart import Cart
from aims.dvd import DigitalVideoDisc


class CartDiscountTests(unittest.TestCase):
    def make_cart(self, cost):
        cart = Cart()
        cart.items.append(DigitalVideoDisc("Example", cost=cost))
        return cart

    def test_twenty_percent_off_one_hundred(self):
        self.assertAlmostEqual(self.make_cart(100).discounted_total(20), 80)

    def test_twenty_percent_off_two_hundred(self):
        self.assertAlmostEqual(self.make_cart(200).discounted_total(20), 160)

    def test_invalid_percentages(self):
        for percent in (-1, 101, float("nan"), float("inf")):
            with self.subTest(percent=percent):
                with self.assertRaises(ValueError):
                    self.make_cart(100).discounted_total(percent)

    def test_discount_boundaries(self):
        cart = self.make_cart(100)
        self.assertEqual(cart.discounted_total(0), 100)
        self.assertEqual(cart.discounted_total(100), 0)

    def test_empty_cart(self):
        self.assertEqual(Cart().discounted_total(20), 0)

    def test_discount_does_not_change_prices(self):
        cart = self.make_cart(100)
        cart.discounted_total(20)
        self.assertEqual(cart.total_cost(), 100)
        self.assertEqual(cart.items[0].cost, 100)


if __name__ == "__main__":
    unittest.main()
