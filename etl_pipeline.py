import pandas as pd
import numpy as np
import re
from datetime import datetime
import pymysql

customers_df = pd.read_csv("data/customers_raw.csv")
products_df = pd.read_csv("data/products_raw.csv")
sales_df = pd.read_csv("data/sales_raw.csv")

# DATA QUALITY METRICS

dq_metrics = {
    "customers": {},
    "products": {},
    "sales": {}
}

# ---- CUSTOMERS ----
dq_metrics["customers"]["records_before"] = len(customers_df)
dq_metrics["customers"]["duplicates"] = customers_df.duplicated(subset=["email"]).sum()
dq_metrics["customers"]["missing_values"] = customers_df.isnull().sum().sum()

# Clean customers
customers_df = customers_df.drop_duplicates(subset=["email"])
customers_df = customers_df.dropna(subset=["email", "first_name", "last_name"])

dq_metrics["customers"]["records_after"] = len(customers_df)

# ---- PRODUCTS ----
dq_metrics["products"]["records_before"] = len(products_df)
dq_metrics["products"]["duplicates"] = products_df.duplicated(subset=["product_name"]).sum()
dq_metrics["products"]["missing_values"] = products_df.isnull().sum().sum()

products_df = products_df.drop_duplicates(subset=["product_name"])
products_df = products_df.dropna(subset=["price", "category"])

dq_metrics["products"]["records_after"] = len(products_df)

# ---- SALES ----
dq_metrics["sales"]["records_before"] = len(sales_df)
dq_metrics["sales"]["duplicates"] = sales_df.duplicated(subset=["transaction_id"]).sum()
dq_metrics["sales"]["missing_values"] = sales_df.isnull().sum().sum()

sales_df = sales_df.drop_duplicates(subset=["transaction_id"])
sales_df = sales_df.dropna(subset=["customer_id", "product_id"])

dq_metrics["sales"]["records_after"] = len(sales_df)

# 1. removing duplicates
customers_df = customers_df.drop_duplicates(subset="email")
products_df = products_df.drop_duplicates(subset="product_name")
sales_df = sales_df.drop_duplicates()

# 2. Handling Missing values for customers
# Droping rows where email is missing (cannot identify customer)
customers_df = customers_df.dropna(subset=["email"])

# Phone can be optional
customers_df["phone"] = customers_df["phone"].fillna("")

# Registration date – keep NaT if missing
def parse_date_safe(date_value):
    if pd.isna(date_value):
        return pd.NaT

    date_value = str(date_value).strip()

    formats = [
        "%d/%m/%Y",
        "%Y-%m-%d",
        "%m/%d/%Y",
        "%m-%d-%Y",
        "%d-%m-%Y"
    ]

    for fmt in formats:
        try:
            return datetime.strptime(date_value, fmt)
        except ValueError:
            continue

    return pd.NaT
customers_df["registration_date"] = customers_df["registration_date"].apply(parse_date_safe)


def parse_date_safe(date_value):
    if pd.isna(date_value):
        return pd.NaT

    date_value = str(date_value).strip()

    formats = [
        "%d/%m/%Y",
        "%Y-%m-%d",
        "%m/%d/%Y",
        "%m-%d-%Y",
        "%d-%m-%Y"
    ]

    for fmt in formats:
        try:
            return datetime.strptime(date_value, fmt)
        except ValueError:
            continue

    return pd.NaT
sales_df["transaction_date"] = sales_df["transaction_date"].apply(parse_date_safe)

sales_df["transaction_date"] = sales_df["transaction_date"].dt.strftime("%Y-%m-%d")

#Handling Missing values for Products
# Price is important – filled with average price
products_df["price"] = products_df["price"].fillna(products_df["price"].mean())

# Stock can be 0
products_df["stock_quantity"] = products_df["stock_quantity"].fillna(0)

#Handling Missing values for Sales
# Remove rows where customer or product info is missing
sales_df = sales_df.dropna(subset=["transaction_date", "quantity", "unit_price"])


#3. Standardize phone formats (e.g., +91-9876543210)
def format_phone(phone):
    if pd.isna(phone):
        return None

    phone = str(phone)
    digits = re.sub(r"\D", "", phone)

    # Case 1: 12 digits with country code
    if len(digits) == 12 and digits.startswith("91"):
        return "+91-" + digits[2:]

    # Case 2: 11 digits starting with 0 (trunk prefix)
    if len(digits) == 11 and digits.startswith("0"):
        return "+91-" + digits[1:]

    # Case 3: plain 10-digit mobile
    if len(digits) == 10:
        return "+91-" + digits

    # Invalid / unknown format
    return None

customers_df["phone"] = customers_df["phone"].apply(format_phone)

# 4. Standardize category names (e.g., "electronics", "Electronics", "ELECTRONICS" → "Electronics")
products_df["category"] = products_df["category"].str.strip().str.title()

# 5. Convert date formats to YYYY-MM-DD
customers_df["registration_date"] = pd.to_datetime(
    customers_df["registration_date"], errors="coerce"
).dt.strftime("%Y-%m-%d")

sales_df["transaction_date"] = pd.to_datetime(
    sales_df["transaction_date"], errors="coerce"
).dt.strftime("%Y-%m-%d")

# 6. Add surrogate keys (auto-incrementing IDs)
customers_df = customers_df.reset_index(drop=True)
customers_df["customer_id"] = customers_df.index + 1

products_df = products_df.reset_index(drop=True)
products_df["product_id"] = products_df.index + 1

sales_df = sales_df.reset_index(drop=True)
sales_df["transaction_id"] = sales_df.index + 1

# Database Connectivity
conn = pymysql.connect(
    host="localhost",
    user="root",
    password="root",
    database="fleximart"
)
cursor = conn.cursor()

# Loading customers data into customer table
customer_sql = """
INSERT INTO customers (first_name, last_name, email, phone, city, registration_date)
VALUES (%s, %s, %s, %s, %s, %s)
"""

try:
    for _, row in customers_df.iterrows():
        try:
            cursor.execute(customer_sql, (
                row['first_name'],
                row['last_name'],
                row['email'],
                row['phone'],
                row['city'],
                row['registration_date']
            ))
        except pymysql.err.IntegrityError as e:
            print(f"Skipping duplicate customer: {row['email']} | {e}")

    conn.commit()
    print("Customers loaded successfully")

except Exception as e:
    conn.rollback()
    print("Customers load failed:", e)

# Loading products data into product table
product_sql = """
INSERT INTO products (product_name, category, price, stock_quantity)
VALUES (%s, %s, %s, %s)
"""

try:
    for _, row in products_df.iterrows():
        cursor.execute(product_sql, (
            row['product_name'],
            row['category'],
            row['price'],
            row['stock_quantity']
        ))

    conn.commit()
    print(" Products loaded successfully")

except Exception as e:
    conn.rollback()
    print(" Products load failed:", e)

# Loading Orders 
sales_df = sales_df.dropna(subset=["customer_id", "product_id"])
sales_df["subtotal"] = sales_df["quantity"] * sales_df["unit_price"]

#  CUSTOMER ID MAPPING

cursor.execute("SELECT customer_id, email FROM customers")
customer_map = {}

for cid, email in cursor.fetchall():
    # Assuming email or some field was derived from C001 earlier
    # Example mapping logic:
    customer_map[f"C{cid:03d}"] = cid

# PRODUCT ID MAPPING
cursor.execute("SELECT product_id, product_name FROM products")
product_map = {}

for pid, _ in cursor.fetchall():
    product_map[f"P{pid:03d}"] = pid

# SQL STATEMENTS
order_sql = """
INSERT INTO orders (customer_id, order_date, total_amount, status)
VALUES (%s, %s, %s, %s)
"""

order_item_sql = """
INSERT INTO order_items (order_id, product_id, quantity, unit_price, subtotal)
VALUES (%s, %s, %s, %s, %s)
"""

# LOAD WITH PROPER MAPPING
try:
    for _, row in sales_df.iterrows():

        cust_code = row["customer_id"]
        prod_code = row["product_id"]

        # Skip if mapping missing
        if cust_code not in customer_map or prod_code not in product_map:
            print(f"Skipping row (mapping missing): {cust_code}, {prod_code}")
            continue

        customer_id = customer_map[cust_code]
        product_id = product_map[prod_code]

        # Insert into orders
        cursor.execute(order_sql, (
            customer_id,
            row["transaction_date"],
            row["subtotal"],
            row["status"]
        ))

        order_id = cursor.lastrowid

        # Insert into order_items
        cursor.execute(order_item_sql, (
            order_id,
            product_id,
            int(row["quantity"]),
            float(row["unit_price"]),
            float(row["subtotal"])
        ))

    conn.commit()
    print(" Orders and order_items inserted successfully")

except Exception as e:
    conn.rollback()
    print(" Load failed:", e)

cursor.execute("SELECT COUNT(*) FROM customers")
customers_loaded = cursor.fetchone()[0]

cursor.execute("SELECT COUNT(*) FROM products")
products_loaded = cursor.fetchone()[0]

cursor.execute("SELECT COUNT(*) FROM orders")
orders_loaded = cursor.fetchone()[0]

cursor.execute("SELECT COUNT(*) FROM order_items")
order_items_loaded = cursor.fetchone()[0]

# Closing Connection
cursor.close()
conn.close()
print(" Database connection closed")


# Generating Report
with open("data_quality_report.txt", "w", encoding="utf-8") as report:
    report.write("DATA QUALITY REPORT - FLEXIMART ETL PIPELINE\n")
    report.write("=" * 50 + "\n\n")

    report.write("1. RECORDS PROCESSED PER FILE\n")
    report.write(f"Customers: {dq_metrics['customers']['records_before']}\n")
    report.write(f"Products : {dq_metrics['products']['records_before']}\n")
    report.write(f"Sales    : {dq_metrics['sales']['records_before']}\n\n")

    report.write("2. DUPLICATES REMOVED\n")
    report.write(f"Customers: {dq_metrics['customers']['duplicates']}\n")
    report.write(f"Products : {dq_metrics['products']['duplicates']}\n")
    report.write(f"Sales    : {dq_metrics['sales']['duplicates']}\n\n")

    report.write("3. MISSING VALUES HANDLED\n")
    report.write(f"Customers: {dq_metrics['customers']['missing_values']}\n")
    report.write(f"Products : {dq_metrics['products']['missing_values']}\n")
    report.write(f"Sales    : {dq_metrics['sales']['missing_values']}\n\n")

    report.write("4. RECORDS LOADED SUCCESSFULLY INTO DATABASE\n")
    report.write(f"Customers loaded   : {customers_loaded}\n")
    report.write(f"Products loaded    : {products_loaded}\n")
    report.write(f"Orders loaded      : {orders_loaded}\n")
    report.write(f"Order Items loaded : {order_items_loaded}\n")

print("Data_quality_report.txt generated successfully")

