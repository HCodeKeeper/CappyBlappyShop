def assert_cart_exists(request):
    cart = request.session.get("cart", None)
    if cart is None:
        request.session["cart"] = {}
