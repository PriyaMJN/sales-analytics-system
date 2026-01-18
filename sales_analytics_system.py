import pandas as pd
import re

def clean_sales_data(file_path):
    # Read file with encoding + delimiter handling
    df = pd.read_csv(
        file_path,
        sep="|",
        encoding="latin1",
        engine="python",
        on_bad_lines="skip"
    )

    # Total records parsed
    total_records = len(df)

    # Drop empty rows
    df = df.dropna(how="all")

    # Clean column names
    df.columns = df.columns.str.strip()

    # Fix commas in product name
    df["ProductName"] = df["ProductName"].astype(str).str.replace(",", "", regex=False)

    # Remove commas from numeric fields
    df["Quantity"] = df["Quantity"].astype(str).str.replace(",", "", regex=False)
    df["UnitPrice"] = df["UnitPrice"].astype(str).str.replace(",", "", regex=False)

    # Convert to numeric
    df["Quantity"] = pd.to_numeric(df["Quantity"], errors="coerce")
    df["UnitPrice"] = pd.to_numeric(df["UnitPrice"], errors="coerce")

    # ---------- INVALID RECORD FILTERING ----------
    total_records = len(df)

    df = df.dropna(subset=["CustomerID", "Region"])
    df = df[df["Quantity"] > 0]
    df = df[df["UnitPrice"] > 0]
    df = df[df["TransactionID"].astype(str).str.startswith("T")]

    df = df.reset_index(drop=True)

    valid_records = len(df)
    invalid_records = total_records - valid_records

    # ---------- REQUIRED OUTPUT ----------
    print(f"Total records parsed : {total_records}")
    print(f"Invalid records removed : {invalid_records}")
    print(f"Valid records after cleaning : {valid_records}")

    return df

clean_df = clean_sales_data("data/sales_data.txt")

#Saved cleaned data
clean_df.to_csv("data/sales_data_cleaned.csv", index=False)

