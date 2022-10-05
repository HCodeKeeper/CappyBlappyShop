from services.cart_service import Cart
import stripe
from django.urls import reverse
from cappy_blappy_shop.settings import DOMAIN


def price_to_int(price):
    return int(price*100)


def int_to_price(value):
    return value/100


def generate_product_line(request):
    cart = Cart(request)
    raw_products = [product_data.values() for product_data in (cart.get_data()["items"]).values()]
    line_products = []
    for product, count, addon in raw_products:
        product_name = product.name
        if addon.id != "-1":
            product_name += f" + {addon.name}"
        line_products.append(
            {
                "price_data": {
                    "currency": "usd",
                    "unit_amount": price_to_int(product.price),
                    "product_data": {
                        "name": product_name,
                        "description": product.description,
                        "metadata": {
                            "self_id": product.id,
                            "addon_id": addon.id
                        }
                    },
                },
                "quantity": count,
            },
        )

    return line_products


def create_session(request):
    session = stripe.checkout.Session.create(
        line_items=generate_product_line(request),
        mode='payment',
        success_url=DOMAIN + reverse('checkout_succeed'),
        cancel_url=DOMAIN + reverse('checkout_cancelled'),
    )
    return session
