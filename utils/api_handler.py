import requests
import re
import os
from datetime import datetime
from collections import defaultdict, Counter

# Task 3.1 Fetch All Product 
def fetch_all_products():
    """
    Fetches all products from DummyJSON API

    Returns: list of product dictionaries
    """
    url = "https://dummyjson.com/products?limit=100"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # raises HTTPError for bad responses

        data = response.json()
        products = data.get('products', [])

        print(" Products fetched successfully through API")
        return products

    except requests.exceptions.RequestException as e:
        print(" Failed to fetch products through api:", e)
        return []

# Task 3.2 Create product mapping
def create_product_mapping(api_products):
    """
    Creates a mapping of product IDs to product info

    Parameters: api_products from fetch_all_products()

    Returns: dictionary mapping product IDs to info

    Expected Output Format:
    {
        1: {'title': 'iPhone 9', 'category': 'smartphones', 'brand': 'Apple', 'rating': 4.69},
        2: {'title': 'iPhone X', 'category': 'smartphones', 'brand': 'Apple', 'rating': 4.44},
        ...
    }
    """

    product_mapping = {}

    for product in api_products:
        try:
            product_id = product.get('id')

            if product_id is None:
                continue

            product_mapping[product_id] = {
                'title': product.get('title', 'Unknown'),
                'category': product.get('category', 'Unknown'),
                'brand': product.get('brand', 'Unknown'),
                'rating': float(product.get('rating', 0))
            }

        except (TypeError, ValueError):
            continue  # Skip malformed product records

    return product_mapping

# Task 3.3 Enrich sales data
#helper function
import os

def save_enriched_data(enriched_transactions, filename='data/enriched_sales_data.txt'):
    """
    Saves enriched transactions back to file using pipe-delimited format
    """

    if not enriched_transactions:
        return

    # Ensure directory exists
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    headers = enriched_transactions[0].keys()

    with open(filename, "w", encoding="utf-8") as file:
        # Write header
        file.write("|".join(headers) + "\n")

        # Write rows
        for txn in enriched_transactions:
            row = []
            for h in headers:
                value = txn.get(h)
                row.append("" if value is None else str(value))
            file.write("|".join(row) + "\n")


def enrich_sales_data(transactions, product_mapping):
    """
    Enriches transaction data with API product information
    """

    enriched_transactions = []

    for txn in transactions:
        enriched_txn = txn.copy()

        try:
            # Extract numeric ID from ProductID (P101 → 101)
            match = re.search(r"\d+", txn.get("ProductID", ""))

            if not match:
                raise ValueError("Invalid ProductID")

            numeric_id = int(match.group())

            # Enrich if product exists
            if numeric_id in product_mapping:
                api_product = product_mapping[numeric_id]

                enriched_txn["API_Category"] = api_product.get("category")
                enriched_txn["API_Brand"] = api_product.get("brand")
                enriched_txn["API_Rating"] = api_product.get("rating")
                enriched_txn["API_Match"] = True
            else:
                enriched_txn["API_Category"] = None
                enriched_txn["API_Brand"] = None
                enriched_txn["API_Rating"] = None
                enriched_txn["API_Match"] = False

        except Exception:
            enriched_txn["API_Category"] = None
            enriched_txn["API_Brand"] = None
            enriched_txn["API_Rating"] = None
            enriched_txn["API_Match"] = False

        enriched_transactions.append(enriched_txn)

    # Save using helper function
    save_enriched_data(enriched_transactions)

    return enriched_transactions

# Task 4.1 Genrate comprensive text report 

def generate_sales_report(transactions, enriched_transactions, output_file='output/sales_report.txt'):
    """
    Generates a comprehensive formatted sales report
    """

    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    total_records = len(transactions)

    # ---------- OVERALL METRICS ----------
    total_revenue = sum(t["Quantity"] * t["UnitPrice"] for t in transactions)
    total_transactions = total_records
    avg_order_value = total_revenue / total_transactions if total_transactions else 0

    dates = [t["Date"] for t in transactions]
    date_range = f"{min(dates)} to {max(dates)}" if dates else "N/A"

    # ---------- REGION-WISE PERFORMANCE ----------
    region_sales = defaultdict(lambda: {"revenue": 0, "count": 0})

    for t in transactions:
        region_sales[t["Region"]]["revenue"] += t["Quantity"] * t["UnitPrice"]
        region_sales[t["Region"]]["count"] += 1

    sorted_regions = sorted(
        region_sales.items(),
        key=lambda x: x[1]["revenue"],
        reverse=True
    )

    # ---------- TOP 5 PRODUCTS ----------
    product_stats = defaultdict(lambda: {"qty": 0, "revenue": 0})

    for t in transactions:
        product_stats[t["ProductName"]]["qty"] += t["Quantity"]
        product_stats[t["ProductName"]]["revenue"] += t["Quantity"] * t["UnitPrice"]

    top_products = sorted(
        product_stats.items(),
        key=lambda x: x[1]["revenue"],
        reverse=True
    )[:5]

    # ---------- TOP 5 CUSTOMERS ----------
    customer_stats = defaultdict(lambda: {"spent": 0, "orders": 0})

    for t in transactions:
        customer_stats[t["CustomerID"]]["spent"] += t["Quantity"] * t["UnitPrice"]
        customer_stats[t["CustomerID"]]["orders"] += 1

    top_customers = sorted(
        customer_stats.items(),
        key=lambda x: x[1]["spent"],
        reverse=True
    )[:5]

    # ---------- DAILY SALES TREND ----------
    daily_stats = defaultdict(lambda: {"revenue": 0, "transactions": 0, "customers": set()})

    for t in transactions:
        day = t["Date"]
        daily_stats[day]["revenue"] += t["Quantity"] * t["UnitPrice"]
        daily_stats[day]["transactions"] += 1
        daily_stats[day]["customers"].add(t["CustomerID"])

    # ---------- PRODUCT PERFORMANCE ----------
    best_day = max(daily_stats.items(), key=lambda x: x[1]["revenue"])[0] if daily_stats else "N/A"
    low_products = [p for p, v in product_stats.items() if v["qty"] <= 1]

    avg_value_per_region = {
        r: v["revenue"] / v["count"]
        for r, v in region_sales.items()
    }

    # ---------- API ENRICHMENT SUMMARY ----------
    enriched_count = sum(1 for t in enriched_transactions if t.get("API_Match"))
    total_enriched = len(enriched_transactions)
    success_rate = (enriched_count / total_enriched * 100) if total_enriched else 0

    failed_products = {
        t["ProductName"]
        for t in enriched_transactions
        if not t.get("API_Match")
    }

    # ---------- WRITE REPORT ----------
    with open(output_file, "w", encoding="utf-8") as f:

        f.write("=" * 44 + "\n")
        f.write("           SALES ANALYTICS REPORT\n")
        f.write(f"         Generated: {now}\n")
        f.write(f"         Records Processed: {total_records}\n")
        f.write("=" * 44 + "\n\n")

        f.write("OVERALL SUMMARY\n")
        f.write("-" * 44 + "\n")
        f.write(f"Total Revenue:        ₹{total_revenue:,.2f}\n")
        f.write(f"Total Transactions:   {total_transactions}\n")
        f.write(f"Average Order Value:  ₹{avg_order_value:,.2f}\n")
        f.write(f"Date Range:           {date_range}\n\n")

        f.write("REGION-WISE PERFORMANCE\n")
        f.write("-" * 44 + "\n")
        f.write("Region    Sales           % of Total   Transactions\n")

        for region, data in sorted_regions:
            percent = (data["revenue"] / total_revenue * 100) if total_revenue else 0
            f.write(
                f"{region:<9} ₹{data['revenue']:>10,.0f}     {percent:>6.2f}%        {data['count']}\n"
            )
        f.write("\n")

        f.write("TOP 5 PRODUCTS\n")
        f.write("-" * 44 + "\n")
        f.write("Rank  Product Name       Qty Sold   Revenue\n")
        for i, (product, data) in enumerate(top_products, 1):
            f.write(
                f"{i:<5} {product:<18} {data['qty']:<10} ₹{data['revenue']:,.0f}\n"
            )
        f.write("\n")

        f.write("TOP 5 CUSTOMERS\n")
        f.write("-" * 44 + "\n")
        f.write("Rank  Customer ID   Total Spent   Orders\n")
        for i, (cust, data) in enumerate(top_customers, 1):
            f.write(
                f"{i:<5} {cust:<12} ₹{data['spent']:,.0f}     {data['orders']}\n"
            )
        f.write("\n")

        f.write("DAILY SALES TREND\n")
        f.write("-" * 44 + "\n")
        f.write("Date         Revenue       Transactions   Customers\n")
        for date, data in sorted(daily_stats.items()):
            f.write(
                f"{date}  ₹{data['revenue']:>8,.0f}      {data['transactions']:<14} {len(data['customers'])}\n"
            )
        f.write("\n")

        f.write("PRODUCT PERFORMANCE ANALYSIS\n")
        f.write("-" * 44 + "\n")
        f.write(f"Best Selling Day: {best_day}\n")
        f.write("Low Performing Products:\n")
        for p in low_products:
            f.write(f" - {p}\n")

        f.write("\nAverage Transaction Value per Region:\n")
        for region, value in avg_value_per_region.items():
            f.write(f" {region}: ₹{value:,.2f}\n")

        f.write("\nAPI ENRICHMENT SUMMARY\n")
        f.write("-" * 44 + "\n")
        f.write(f"Total Products Enriched: {enriched_count}\n")
        f.write(f"Success Rate: {success_rate:.2f}%\n")
        f.write("Products Not Enriched:\n")
        for p in failed_products:
            f.write(f" - {p}\n")
