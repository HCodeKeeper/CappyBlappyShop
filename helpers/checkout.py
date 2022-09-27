from services.cart_service import Cart


def price_to_int(price):
    return int(price*100)


def generate_product_line(request):
    cart = Cart(request)
    raw_products = [product_data.values() for product_data in (cart.get_data()["items"]).values()]
    line_products = []
    for product, count, addon in raw_products:
        product_name = product.name
        if addon:
            product_name += f" + {addon.name}"
        line_products.append(
            {
                "price_data": {
                    "currency": "usd",
                    "unit_amount": price_to_int(product.price),
                    "product_data": {
                        "name": product_name,
                        "description": product.description
                    },
                },
                "quantity": count,
            },
        )

    return line_products
