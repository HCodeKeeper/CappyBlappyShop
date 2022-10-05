from shop.models import Order, OrderItem
from helpers.checkout import int_to_price
from django.db.utils import DatabaseError
from typing import List
from pprint import pprint


class StripeProduct:
    def __init__(self, product_id, count, addon_id, unit_price):
        self.product_id = product_id
        self.count = count
        self.addon_id = addon_id
        self.unit_price = unit_price

    @staticmethod
    def create_with_line_item(line_item):
        count = line_item["quantity"]
        unit_price = line_item["price"]["unit_amount"]
        product_id = line_item["price"]["metadata"]["self_id"]
        addon_id = line_item["price"]["metadata"]["addon_id"]

        return StripeProduct(product_id, count, addon_id, unit_price)

    def add_to_db(self, order_id):
        order_item = OrderItem(
            product=self.product_id,
            addon=self.addon_id,
            quantity=self.count,
            unit_price=self.unit_price,
            order=order_id
        )
        order_item.save()


class StripeOrder:
    def __init__(self, products: List[StripeProduct], user_email: str, payment_date, total_price):
        self.payment_date = payment_date
        self.products = products
        self.email = user_email
        self.total_price = total_price

    @staticmethod
    def create_with_session(session, payment_date, line_items):
        user_email = session["customer_details"]["email"]
        products = []
        total_price = int_to_price(session["amount_total"])

        for item in line_items:
            product = StripeProduct.create_with_line_item(item)
            products.append(product)

        return StripeOrder(products, user_email, payment_date, total_price)

    def add_to_db(self):
        order = Order(
            creation_date=self.payment_date,
            email=self.email,
            price=self.total_price
            )
        order.save()
        for order_item in self.products:
            order_item.add_to_db()


def fulfill_order(session, payment_date, line_items):
    pprint(line_items)
    stripe_order = StripeOrder.create_with_session(session, payment_date, line_items)
    try:
        stripe_order.add_to_db()
    except DatabaseError as e:
        raise e
