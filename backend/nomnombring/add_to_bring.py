#!/usr/bin/python3
from .bring_api import Bring


def consolidate_ingredients(recipes):
    """
    Consolidate the ingredients from all recipes into one dict.
    :return: dict with d["onions"] = ["2, 100g (red), 1 (medium)"]
    """
    # Get the ingredients of all recipes (and flatten list)
    all_ingredients = [
        ing
        for ingredients in [r["ingredients"] for r in recipes]
        for ing in ingredients
    ]

    # Group identical ingredients and concatenate the amounts
    ing_dict = dict()
    for ing in all_ingredients:
        name = ing["name"]
        amount = ing["amount"]
        description = ing["description"]

        if name not in ing_dict:
            ing_dict[name] = amount
        else:
            ing_dict[name] += f", {amount}"

        if description:
            ing_dict[name] += f" ({description})"

    return ing_dict


def merge_with_existing_ingredients(ingredients, existingIngredients):
    """
    Add the descriptions of any existing ingredients to the new ingredients
    """
    # Convert items to dict
    existing_items = dict()
    for item in existingIngredients:
        existing_items[item["name"]] = item["specification"]

    # Go over items to add
    # If they already exist, edit the description
    for ing in ingredients:
        if ing in existing_items:
            ingredients[ing] += ", " + existing_items[ing]

    return ingredients


def add_recipes_by_id(config, all_recipes, selected_ids):
    # Create list of all ingredients that need to be added
    recipes = [r for r in all_recipes if r["id"] in selected_ids]
    ingredients = consolidate_ingredients(recipes)

    print(recipes)
    print(ingredients)
    if len(ingredients) == 0:
        print(f"Empty ingredient list, not adding anything.")
        return

    # Connect to bring API and find the active list
    user = config["BRING"]["user"]
    password = config["BRING"]["password"]
    key = config["BRING"]["key"]
    b = Bring(user, password, key)
    b.login()
    lists = b.get_lists()
    listUuid = lists["lists"][0]["listUuid"]

    # Existing items are overwritten when re-adding, so we need to merge
    items = b.get_items(listUuid)
    ingredients = merge_with_existing_ingredients(ingredients, items["purchase"])

    for name, spec in ingredients.items():
        b.add_item(name, spec, listUuid)

    b.close_session()
    print(f"Added: {ingredients}")
