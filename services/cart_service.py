from django.http import HttpRequest
from shop.models import Product, Addon


class Cart:
    def __init__(self, request: HttpRequest):
        self.request = request
        if not self.__assert_cart_exists():
            self.__insert_cart_in_session()
        self.session_cart = self.request.session["cart"]

    def add(self, product_id, count: int, addon_id="-1"):
        self.session_cart[product_id] = {"self": product_id, "count": count, "addon_id": addon_id}
        self.request.session.modified = True

    def set(self, product_id, count: int = None, addon_id=None):
        if count is not None:
            self.session_cart[product_id]["count"] = count
        if addon_id is not None:
            self.session_cart[product_id]["addon_id"]

    def get_data(self) -> dict:
        items = {}
        items_count = 0
        sub_total_price = 0
        for product_id in self.session_cart.values():
            product = Product.objects.get(id=product_id["self"])
            addon = ""
            if product_id["addon_id"] != "-1":
                addon = Addon.objects.get(id=product_id["addon_id"])
                sub_total_price += float(addon.price)
            count = product_id["count"]
            items_count += int(count)
            sub_total_price += float(product.price) * int(count)
            items[product_id["self"]] = {
                "self": product,
                "count": count,
                "addon": addon
            }
        return {"items": items, "sub_total_price": sub_total_price, "items_count": items_count}

    def remove_item(self, product_id):
        self.session_cart.pop(product_id)

    def remove_addon(self, product_id):
        self.session_cart[product_id]["addon_id"] = "-1"

    def __assert_cart_exists(self):
        cart = self.request.session.get("cart", None)
        if cart is None:
            return False
        return True

    def item_exists(self, product_id):
        return bool(self.session_cart.get(product_id, False))

    def __insert_cart_in_session(self):
        self.request.session["cart"] = {}
