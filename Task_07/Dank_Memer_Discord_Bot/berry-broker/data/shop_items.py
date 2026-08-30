# data/shop_items.py
# Static seed data for the Berry Broker shop.
# These items are loaded into the SQLite database on first run.

SHOP_ITEMS = [
    {
        "name": "Berry Compass",
        "price": 500,
        "description": "A compass that points to the richest pirates",
        "effect": "+10% raid success"
    },
    {
        "name": "Lucky Dice",
        "price": 1000,
        "description": "Enchanted dice from a mysterious island",
        "effect": "+15% gambling bonus"
    },
    {
        "name": "Sea Stone",
        "price": 2000,
        "description": "Nullifies devil fruit powers",
        "effect": "Raid protection (50% damage reduction)"
    },
    {
        "name": "Log Pose",
        "price": 1500,
        "description": "Navigates the Grand Line",
        "effect": "Unlocks special raids"
    },
    {
        "name": "Vivre Card",
        "price": 800,
        "description": "Points to a loved one",
        "effect": "+5% trade success"
    }
]


def get_seed_items():
    """
    Return the shop items as a list of tuples ready for SQLite insertion.
    Format: (name, price, description, effect)
    """
    return [
        (item["name"], item["price"], item["description"], item["effect"])
        for item in SHOP_ITEMS
    ]