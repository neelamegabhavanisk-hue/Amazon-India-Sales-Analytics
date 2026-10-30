# Amazon India: A Decade of Sales Analytics 📈🇮🇳

This project builds a complete sales analytics dashboard for an Amazon India-style marketplace dataset spanning 2014 to 2023.

## Project objective

The goal is to explore patterns in revenue, orders, regional demand, category contribution, and customer satisfaction over a decade of commerce activity.

## Included files

- `app.py` — Streamlit dashboard for interactive analysis
- `generate_data.py` — Generates realistic synthetic sales data for 2014–2023
- `data/amazon_india_sales_analytics.csv` — dataset used by the dashboard
- `requirements.txt` — Python dependencies

## How to run

1. Create and activate a virtual environment
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Generate the dataset:
   ```bash
   python generate_data.py
   ```
4. Launch the dashboard:
   ```bash
   streamlit run app.py
   ```

## Dashboard highlights

- Annual revenue trend
- Regional revenue analysis
- Category contribution split
- Monthly operational performance
- KPI summary cards for revenue, orders, rating, and returns

## Data fields

- `year`, `month`, `month_name`
- `region`
- `category`
- `orders`
- `revenue`
- `returns`
- `net_revenue`
- `discount_pct`
- `customer_rating`
- `delivery_days`
- `shipment_cost`

## Notes

The dataset is intentionally generated to make the project executable without needing external files. It is designed to look realistic and support analytical storytelling.
