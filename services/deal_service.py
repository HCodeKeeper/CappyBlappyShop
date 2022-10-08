from shop.models import Deal


def get_random_json():
    return deal_to_json(
        get_random()
    )


def get_random():
    random_deal = Deal.objects.order_by('?').first()
    return random_deal


def deal_to_json(deal):
    return {
        deal.title: f"/product/{deal.product}"
    }

