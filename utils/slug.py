def _slug(name):
    """Sauce Labs Backpack → sauce-labs-backpack"""
    return name.lower().replace(" ", "-").replace("'", "")
