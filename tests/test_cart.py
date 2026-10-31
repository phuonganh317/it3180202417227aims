import contextlib
import io
import unittest

from aims.cart import Cart, MAX_NUMBERS_ORDERED
from aims.dvd import DigitalVideoDisc


class CartLimitTests(unittest.TestCase):
    def test_accepts_twenty_dvds_and_rejects_twenty_first(self):
        cart = Cart()
        self.assertEqual(MAX_NUMBERS_ORDERED, 20)
        with contextlib.redirect_stdout(io.StringIO()):
            for index in range(20):
                with self.subTest(index=index):
                    self.assertTrue(cart.add_dvd(DigitalVideoDisc(f"DVD {index}", cost=1)))
            self.assertEqual(len(cart.items), 20)
            self.assertFalse(cart.add_dvd(DigitalVideoDisc("DVD 21", cost=99)))
        self.assertEqual(len(cart.items), 20)
        self.assertEqual(cart.total_cost(), 20)


class CartMessageTests(unittest.TestCase):
    def test_addition_message_is_vietnamese_and_contains_title(self):
        cart = Cart()
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            self.assertTrue(cart.add_dvd(DigitalVideoDisc("Star Wars")))
        self.assertEqual(output.getvalue(), "Đã thêm đĩa vào giỏ hàng: Star Wars\n")


if __name__ == "__main__":
    unittest.main()
