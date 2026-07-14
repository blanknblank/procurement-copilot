from src.data_loader import df

def get_monthly_trend():
    monthly_spend=(
        df.groupby("month")["spend"]
        .sum()
        .reset_index()
    )
    return monthly_spend.to_dict(
        orient="records"
    )