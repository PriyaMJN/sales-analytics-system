from utils.file_handler import (
    read_sales_data,
    parse_transactions,
    validate_and_filter
)

from utils.data_processor import (
    calculate_total_revenue,
    region_wise_sales,
    top_selling_products,
    customer_analysis,
    daily_sales_trend,
    find_peak_sales_day,
    low_performing_products
)

from utils.api_handler import (
    fetch_all_products,
    create_product_mapping,
    enrich_sales_data,
    generate_sales_report
)


def main():
    try:

        print("=" * 40)
        print("SALES ANALYTICS SYSTEM")
        print("=" * 40)

        # 1. Read sales data
        print("\n[1/10] Reading sales data...")
        raw_data = read_sales_data("data/sales_data.txt")
        print(f"✓ Successfully read {len(raw_data)} transactions")

        # 2. Parse data
        print("\n[2/10] Parsing and cleaning data...")
        transactions = parse_transactions(raw_data)
        print(f"✓ Parsed {len(transactions)} records")

        # 3. Filter options (display only)
        regions = sorted({t["Region"] for t in transactions})
        amounts = [t["Quantity"] * t["UnitPrice"] for t in transactions]

        print("\n[3/10] Filter Options Available:")
        print("Regions:", ", ".join(regions))
        print(f"Amount Range: ₹{min(amounts):,.0f} - ₹{max(amounts):,.0f}")

        choice = input("\nDo you want to filter data? (y/n): ").strip().lower()
        if choice == "n":
            print("✓ No filters applied")

        # 4. Validate transactions
        print("\n[4/10] Validating transactions...")
        valid_txns, invalid_count, summary = validate_and_filter(transactions)

        print(f"✓ Valid: {len(valid_txns)} | Invalid: {invalid_count}")
        print("Validation Summary:", summary)

        # 5. Perform analysis 
        print("\n[5/10] Analyzing sales data...")
        total_revenue = calculate_total_revenue(valid_txns)
        region_wise_sales(valid_txns)
        top_selling_products(valid_txns, n=5)
        customer_analysis(valid_txns)
        daily_sales_trend(valid_txns)
        find_peak_sales_day(valid_txns)
        low_performing_products(valid_txns)
        print("✓ Analysis complete")

        # 6. Fetch API products
        print("\n[6/10] Fetching product data from API...")
        products = fetch_all_products()
        print(f"✓ Fetched {len(products)} products")

        # 7. Enrich sales data
        print("\n[7/10] Enriching sales data...")
        product_mapping = create_product_mapping(products)
        enriched_transactions = enrich_sales_data(valid_txns, product_mapping)

        enriched_count = sum(1 for t in enriched_transactions if t["API_Match"])
        success_rate = (enriched_count / len(valid_txns)) * 100 if valid_txns else 0
        print(f"✓ Enriched {enriched_count}/{len(valid_txns)} transactions ({success_rate:.1f}%)")

        # 8. Save enriched data
        print("\n[8/10] Saving enriched data...")
        print("✓ Saved to: data/enriched_sales_data.txt")

        # 9. Generate report
        print("\n[9/10] Generating report...")
        generate_sales_report(valid_txns, enriched_transactions)
        print("✓ Report saved to: output/sales_report.txt")

        # 10. Completion
        print("\n[10/10] Process Complete!")
        print("=" * 40)

        ''' Rough work
        raw_data = read_sales_data("data/sales_data.txt")
        print("Raw Data Count:", len(raw_data))   

        parsed_data = parse_transactions(raw_data)
        print("Parsed Data Count:", len(parsed_data))  

        valid_tx, invalid_count, summary = validate_and_filter(parsed_data)
        print("Valid Transactions Count:", len(valid_tx))  
        print("Invalid Transactions:", invalid_count)
        print("Summary:", summary)

        # Total revenue
        total_revenue = calculate_total_revenue(valid_tx)
        print("Total Revenue:", total_revenue)

        #  REGION-WISE SALES ANALYSIS
        region_sales = region_wise_sales(valid_tx)

        print("\nRegion-wise Sales Analysis:")
        for region, stats in region_sales.items():
            print(
                f"{region} -> "
                f"Total Sales: {stats['total_sales']}, "
                f"Transactions: {stats['transaction_count']}, "
                f"Percentage: {stats['percentage']}%"
            )

        # Printing top selling products
        top_products = top_selling_products(valid_tx, n=5)

        print("\nTop Selling Products:")
        for product, qty, revenue in top_products:
            print(f"{product} → Qty Sold: {qty}, Revenue: {revenue}")

        customer_stats = customer_analysis(valid_tx)

        # Printing Purchase Analysis
        print("\nCustomer Purchase Analysis:")
        for customer, stats in customer_stats.items():
            print(
                f"{customer} → Total Spent: {stats['total_spent']}, "
                f"Purchases: {stats['purchase_count']}, "
                f"Avg Order: {stats['avg_order_value']}, "
                f"Products: {stats['products_bought']}"
            )

        print(daily_sales_trend(valid_tx))
        print("****** Highest Sales Day ********")
        print(find_peak_sales_day(valid_tx))
        print("****** Low Performing Products ********")
        print(low_performing_products(valid_tx, threshold=10))

        # API HANDLING
        print("****** Products ferched through API ********")
        products = fetch_all_products()
        print(len(products))        # should be > 0
        print(products[0])          # check structure


        product_mapping = create_product_mapping(products)
        # print(product_mapping)

        enriched_data = enrich_sales_data(valid_tx, product_mapping)
        for txn in enriched_data:
            print(txn)

        generate_sales_report(valid_tx, enriched_data)'''

    except Exception as e:
        print("\n❌ ERROR OCCURRED")
        print("Something went wrong while processing the data.")
        print("Error:", e)


if __name__ == "__main__":
    main()
