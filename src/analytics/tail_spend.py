from src.data_loader import df


def get_tail_spend():

    supplier_spend = (
        df.groupby("supplier")["spend"]
        .sum()
        .reset_index()
    )

    total_spend = supplier_spend["spend"].sum()

    supplier_spend["share"] = (
        supplier_spend["spend"] / total_spend
    )

    tail_spend = supplier_spend[
        supplier_spend["share"] < 0.01
    ]

    return tail_spend.to_dict(
        orient="records"
    )