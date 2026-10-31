MAX_NUMBERS_ORDERED = 20


class Cart:
    """Giỏ hàng chứa tối đa MAX_NUMBERS_ORDERED đĩa DVD."""

    def __init__(self):
        self.items = []

    def add_dvd(self, dvd):
        if len(self.items) >= MAX_NUMBERS_ORDERED:
            print("The cart is almost full")
            return False
        self.items.append(dvd)
        print(f"Đã thêm đĩa vào giỏ hàng: {dvd.title}")
        return True

    def remove_dvd(self, dvd):
        if dvd in self.items:
            self.items.remove(dvd)
            print("The disc has been removed")
            return True
        print("The disc is not in the cart")
        return False

    def total_cost(self):
        return sum(item.cost for item in self.items)

    def sort_by_title(self):
        """Sort in place by title, case-insensitively; preserve ties."""
        self.items.sort(key=lambda dvd: dvd.title.casefold())

    def sort_by_cost(self):
        """Sort in place by ascending cost; preserve ties."""
        self.items.sort(key=lambda dvd: dvd.cost)

    def discounted_total(self, percent):
        """Return the total after applying a percentage discount."""
        if not 0 <= percent <= 100:
            raise ValueError("Discount percentage must be between 0 and 100")
        return self.total_cost() * (1 - percent / 100)

    def print_cart(self):
        if not self.items:
            print("The cart is empty")
            return
        for index, dvd in enumerate(self.items, start=1):
            print(f"{index}. {dvd}")
        print(f"Total cost: {self.total_cost():.2f} $")
