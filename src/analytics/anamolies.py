from src.data_loader import df


def get_price_anomalies():

    price_stats = (
        df.groupby("item")["unit_price"]
        .agg(["mean", "std"])
        .reset_index()
    )

    price_check = df.merge(
        price_stats,
        on="item"
    )

    price_check["z_score"] = (
        (price_check["unit_price"] - price_check["mean"])
        / price_check["std"]
    )

    anomalies = price_check[
        abs(price_check["z_score"]) > 2
    ]

    return anomalies[
        [
            "supplier",
            "item",
            "unit_price",
            "z_score"
        ]
    ].to_dict(
        orient="records"
    )