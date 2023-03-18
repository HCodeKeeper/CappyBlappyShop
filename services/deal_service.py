from shop.models import Deal, Product
from decimal import Decimal


def get_random_json():
    try:
        deal = get_random()
    except Deal.DoesNotExist:
        raise
    return deal_to_json(
        deal
    )


def get_random() -> Deal:
    random_deal = Deal.objects.order_by('?').first()
    if random_deal is None:
        raise Deal.DoesNotExist()
    return random_deal


def deal_to_json(deal: Deal):
    return {
        deal.title: f"/product/{deal.product.id}"
    }


def _apply_discount_on_price(full_price: Decimal, discount_percentage: int) -> Decimal:
    discount_to_money = full_price * Decimal(int(discount_percentage) / 100)
    price = full_price - discount_to_money
    price = round(price, 2)
    return price


# get discounted price or full if no discounts are available
def get_discounted_price(product: Product) -> Decimal:
    full_price = Decimal(product.price)
    try:
        discount = Deal.objects.get(product=product)
    except Deal.DoesNotExist:
        return full_price
    discounted_price = _apply_discount_on_price(full_price, discount.percents)
    return discounted_price
