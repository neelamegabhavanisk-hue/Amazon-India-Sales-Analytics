from __future__ import annotations

import numpy as np
import pandas as pd
from pathlib import Path


def generate_data() -> pd.DataFrame:
    np.random.seed(42)
    years = list(range(2014, 2024))
    months = list(range(1, 13))
    regions = ["North", "South", "East", "West", "Central"]
    categories = [
        "Electronics",
        "Home & Kitchen",
        "Fashion",
        "Beauty",
        "Books",
        "Groceries",
        "Appliances",
    ]

    rows = []

    for year in years:
        year_growth = 1 + (year - 2014) * 0.11
        for month in months:
            month_factor = 1 + 0.22 * np.sin((month / 12) * 2 * np.pi)
            for region in regions:
                region_factor = {
                    "North": 1.1,
                    "South": 1.22,
                    "East": 0.92,
                    "West": 1.18,
                    "Central": 0.98,
                }[region]

                for category in categories:
                    category_multiplier = {
                        "Electronics": 1.45,
                        "Home & Kitchen": 1.22,
                        "Fashion": 1.18,
                        "Beauty": 1.1,
                        "Books": 0.82,
                        "Groceries": 0.94,
                        "Appliances": 1.28,
                    }[category]

                    base_orders = 620 + int(year * 65 + month * 48 + np.random.normal(0, 54))
                    orders = int(max(120, base_orders * year_growth * month_factor * region_factor * category_multiplier))
                    avg_sale_value = {
                        "Electronics": 1800,
                        "Home & Kitchen": 1200,
                        "Fashion": 980,
                        "Beauty": 700,
                        "Books": 520,
                        "Groceries": 420,
                        "Appliances": 1600,
                    }[category]

                    revenue = orders * avg_sale_value * (1 + np.random.uniform(-0.18, 0.22))
                    returns = int(orders * np.random.uniform(0.03, 0.09))
                    net_revenue = revenue * (1 - np.random.uniform(0.02, 0.08))
                    discount_pct = round(np.random.uniform(8, 32), 1)
                    rating = round(np.random.uniform(3.8, 4.9), 2)
                    delivery_days = int(np.random.uniform(2, 8))
                    shipment_cost = round(np.random.uniform(60, 320), 2)

                    rows.append(
                        {
                            "year": year,
                            "month": month,
                            "date": pd.Timestamp(year=year, month=month, day=1),
                            "region": region,
                            "category": category,
                            "orders": orders,
                            "revenue": round(revenue, 2),
                            "returns": returns,
                            "net_revenue": round(net_revenue, 2),
                            "discount_pct": discount_pct,
                            "customer_rating": rating,
                            "delivery_days": delivery_days,
                            "shipment_cost": shipment_cost,
                        }
                    )

    df = pd.DataFrame(rows)
    df["month_name"] = df["date"].dt.month_name()
    return df


def main() -> None:
    output_dir = Path("data")
    output_dir.mkdir(exist_ok=True)

    df = generate_data()
    out_file = output_dir / "amazon_india_sales_analytics.csv"
    df.to_csv(out_file, index=False)
    print(f"Saved {len(df)} rows to {out_file}")


if __name__ == "__main__":
    main()
