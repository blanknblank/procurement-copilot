from src.data_loader import df

preferred_suppliers = {
    "IT Hardware": ["Lenovo"],
    "Software": ["Microsoft"],
    "Marketing": ["Publicis"],
    "Logistics": ["BlueDart"],
    "Office Supplies": ["Office Depot"]
}


def is_maverick(row):

    return (
        row["supplier"]
        not in preferred_suppliers[row["category"]]
    )


def get_maverick_spend():

    temp = df.copy()

    temp["maverick"] = temp.apply(
        is_maverick,
        axis=1
    )

    maverick = temp[
        temp["maverick"]
    ]

    return {
        "transactions": len(maverick),
        "spend": float(
            maverick["spend"].sum()
        )
    }