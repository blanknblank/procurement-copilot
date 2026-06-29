import pandas as pd
from src.data_loader import df
# df = pd.read_csv("data/procurement_transactions.csv")

def category_spend():

    result = (

        df.groupby("category")["spend"]

        .sum()

        .reset_index()

        .sort_values(

            "spend",

            ascending=False

        )

    )

    return result.to_dict(

        orient="records"

    )