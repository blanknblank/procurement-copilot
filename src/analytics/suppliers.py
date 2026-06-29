import pandas as pd
from src.data_loader import df
# df = pd.read_csv("data/procurement_transactions.csv")

def top_suppliers():

    result = (
        df.groupby("supplier")["spend"]
          .sum()
          .reset_index()
          .sort_values("spend", ascending=False)
          .head(10)
    )

    return result.to_dict(orient="records")