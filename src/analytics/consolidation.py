from src.data_loader import df


def get_supplier_consolidation():

    supplier_item_price = (
        df.groupby(["item", "supplier"])["unit_price"]
        .mean()
        .reset_index()
    )

    cheapest_supplier = (
        supplier_item_price
        .sort_values("unit_price")
        .groupby("item")
        .first()
        .reset_index()
    )

    cheapest_supplier.columns = [
        "item",
        "best_supplier",
        "best_price"
    ]

    consolidation = supplier_item_price.merge(
        cheapest_supplier,
        on="item"
    )

    consolidation["price_difference"] = (
        consolidation["unit_price"]
        - consolidation["best_price"]
    )

    consolidation = consolidation[
        consolidation["price_difference"] > 0
    ]

    consolidation = consolidation.sort_values(
        "price_difference",
        ascending=False
    )

    return consolidation.to_dict(
        orient="records"
    )