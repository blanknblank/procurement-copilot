import pandas as pd
import numpy as np
from faker import Faker

fake = Faker()

np.random.seed(42)

# ----------------------------------
# CONFIG
# ----------------------------------

N_ROWS = 100_000

categories = {
    "IT Hardware": {
        "Laptop": (55000, 70000),
        "Monitor": (10000, 25000),
        "Keyboard": (500, 2500),
        "Mouse": (300, 1500),
    },
    "Software": {
        "Microsoft 365": (5000, 15000),
        "Adobe License": (12000, 25000),
        "Atlassian License": (8000, 18000),
    },
    "Marketing": {
        "Digital Campaign": (50000, 500000),
        "Event Sponsorship": (100000, 1000000),
        "Branding Material": (10000, 150000),
    },
    "Logistics": {
        "Air Freight": (20000, 200000),
        "Road Transport": (5000, 80000),
        "Warehouse Service": (20000, 300000),
    },
    "Office Supplies": {
        "Printer Paper": (200, 500),
        "Stationery Kit": (300, 1000),
        "Ink Cartridge": (800, 5000),
    }
}

suppliers = {
    "IT Hardware": ["Dell", "HP", "Lenovo"],
    "Software": ["Microsoft", "Adobe", "Atlassian"],
    "Marketing": ["WPP", "Dentsu", "Publicis"],
    "Logistics": ["DHL", "FedEx", "BlueDart"],
    "Office Supplies": ["Staples", "Office Depot", "Stationery World"]
}

business_units = [
    "Engineering",
    "Sales",
    "Marketing",
    "Finance",
    "HR",
    "Operations"
]

locations = [
    "Bangalore",
    "Hyderabad",
    "Mumbai",
    "Chennai",
    "Pune"
]

payment_terms = [
    "Net15",
    "Net30",
    "Net45",
    "Net60"
]

# ----------------------------------
# SUPPLIER PRICE MULTIPLIERS
# Creates savings opportunities later
# ----------------------------------

supplier_price_multiplier = {
    "Dell": 1.08,
    "HP": 1.02,
    "Lenovo": 0.95,

    "Microsoft": 1.05,
    "Adobe": 1.08,
    "Atlassian": 0.97,

    "WPP": 1.10,
    "Dentsu": 1.00,
    "Publicis": 0.95,

    "DHL": 1.06,
    "FedEx": 1.03,
    "BlueDart": 0.96,

    "Staples": 1.02,
    "Office Depot": 1.00,
    "Stationery World": 0.95
}

# ----------------------------------
# GENERATION
# ----------------------------------

records = []

for i in range(N_ROWS):

    category = np.random.choice(
        list(categories.keys()),
        p=[0.30, 0.20, 0.15, 0.20, 0.15]
    )

    item = np.random.choice(list(categories[category].keys()))

    supplier = np.random.choice(suppliers[category])

    min_price, max_price = categories[category][item]

    base_price = np.random.uniform(min_price, max_price)

    unit_price = (
        base_price *
        supplier_price_multiplier[supplier]
    )

    order_date = fake.date_between(
        start_date="-3y",
        end_date="today"
    )

    month = pd.Timestamp(order_date).month

    # Marketing seasonality
    if category == "Marketing" and month in [10, 11, 12]:
        quantity = np.random.randint(5, 20)
    else:
        quantity = np.random.randint(1, 10)

    spend = quantity * unit_price

    record = {
        "po_id": f"PO{i+1:07d}",
        "order_date": order_date,
        "supplier": supplier,
        "category": category,
        "item": item,
        "quantity": quantity,
        "unit_price": round(unit_price, 2),
        "spend": round(spend, 2),
        "business_unit": np.random.choice(business_units),
        "location": np.random.choice(locations),
        "payment_terms": np.random.choice(payment_terms)
    }

    records.append(record)

# ----------------------------------
# DATAFRAME
# ----------------------------------

df = pd.DataFrame(records)

# ----------------------------------
# SAVE
# ----------------------------------

output_path = "data/procurement_transactions.csv"

df.to_csv(output_path, index=False)

print(df.head())
print("\nRows:", len(df))
print("\nSaved to:", output_path)