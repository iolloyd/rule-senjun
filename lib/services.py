from redis_lib.query import get_outfit_items, get_outfits
from helpers import filtered_combos


def items(idList):
    items = get_outfit_items(idList)
    return items


def outfits(idList):
    item_outfits = get_outfit_items(idList)
    item_outfits = [x for x in sorted(item_outfits[:400]) if len(x) == 3]
    return filtered_combos(item_outfits)
