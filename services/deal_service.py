from shop.models import Deal
from random import choice


def get_random_json():
    return deal_to_json(
        get_random()
    )


def get_random():
    deal = choice(Deal.objects.all())
    return deal


def deal_to_json(deal):
    return {
        deal.title: deal.percents
    }

