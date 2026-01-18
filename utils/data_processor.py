# ###### Task 2.1 Sales Summary calculator
# a. Calculate Total revenue
def calculate_total_revenue(transactions):
    """
    Calculates total revenue from all transactions

    Returns: float (total revenue)
    """
    total_revenue = 0.0

    for tx in transactions:
        try:
            total_revenue += tx['Quantity'] * tx['UnitPrice']
        except (KeyError, TypeError):
            # Skip transactions with missing or invalid data
            continue

    return round(total_revenue, 2)

# b. Region wise sales analysis
def region_wise_sales(transactions):
    region_stats = {}
    total_sales_all_regions = 0.0

    for tx in transactions:
        try:
            region = tx['Region'].strip()

            # 🔴 Skip empty or invalid region
            if not region:
                continue

            amount = tx['Quantity'] * tx['UnitPrice']

            if region not in region_stats:
                region_stats[region] = {
                    'total_sales': 0.0,
                    'transaction_count': 0
                }

            region_stats[region]['total_sales'] += amount
            region_stats[region]['transaction_count'] += 1
            total_sales_all_regions += amount

        except (KeyError, TypeError):
            continue

    for region, stats in region_stats.items():
        stats['percentage'] = round(
            (stats['total_sales'] / total_sales_all_regions) * 100, 2
        )

    return dict(
        sorted(
            region_stats.items(),
            key=lambda item: item[1]['total_sales'],
            reverse=True
        )
    )

# c.Top selling products
def top_selling_products(transactions, n=5):
    """
    Finds top n products by total quantity sold

    Returns: list of tuples
    """

    product_stats = {}

    # Step 1: Aggregate quantity and revenue by ProductName
    for tx in transactions:
        try:
            product = tx['ProductName']
            quantity = tx['Quantity']
            revenue = tx['Quantity'] * tx['UnitPrice']

            if product not in product_stats:
                product_stats[product] = {
                    'total_quantity': 0,
                    'total_revenue': 0.0
                }

            product_stats[product]['total_quantity'] += quantity
            product_stats[product]['total_revenue'] += revenue

        except (KeyError, TypeError):
            continue

    # Step 2: Convert to list of tuples
    result = [
        (product,
         stats['total_quantity'],
         round(stats['total_revenue'], 2))
        for product, stats in product_stats.items()
    ]

    # Step 3: Sort by total quantity (descending)
    result.sort(key=lambda x: x[1], reverse=True)

    # Step 4: Return top n products
    return result[:n]

# Customer Purchess analysis
def customer_analysis(transactions):
    """
    Analyzes customer purchase patterns

    Returns: dictionary of customer statistics
    """

    customer_stats = {}

    # Step 1: Aggregate data per customer
    for tx in transactions:
        try:
            customer = tx['CustomerID']
            product = tx['ProductName']
            amount = tx['Quantity'] * tx['UnitPrice']

            if customer not in customer_stats:
                customer_stats[customer] = {
                    'total_spent': 0.0,
                    'purchase_count': 0,
                    'products_bought': set()  # 🔹 ensures unique products
                }

            customer_stats[customer]['total_spent'] += amount
            customer_stats[customer]['purchase_count'] += 1
            customer_stats[customer]['products_bought'].add(product)

        except (KeyError, TypeError):
            continue

    # Step 2: Calculate average order value and convert products to sorted list
    for customer, stats in customer_stats.items():
        if stats['purchase_count'] > 0:
            stats['avg_order_value'] = round(
                stats['total_spent'] / stats['purchase_count'], 2
            )
        else:
            stats['avg_order_value'] = 0.0

        # 🔹 Convert set to sorted list → unique and consistent order
        stats['products_bought'] = sorted(list(stats['products_bought']))
        stats['total_spent'] = round(stats['total_spent'], 2)

    # Step 3: Sort customers by total_spent descending → ensures top spenders first
    sorted_customer_stats = dict(
        sorted(
            customer_stats.items(),
            key=lambda item: item[1]['total_spent'],
            reverse=True
        )
    )

    return sorted_customer_stats

# ############## Task 2.2 Date Based Aanalyis
# a.Daily sales trend

def daily_sales_trend(transactions):
    daily_data = {}

    # Step 1: Group by date and aggregate metrics
    for txn in transactions:
        date = txn['Date']
        amount = txn['UnitPrice']
        customer = txn['CustomerID']

        if date not in daily_data:
            daily_data[date] = {
                'revenue': 0.0,
                'transaction_count': 0,
                'unique_customers': set()   # set for uniqueness
            }

        daily_data[date]['revenue'] += amount
        daily_data[date]['transaction_count'] += 1
        daily_data[date]['unique_customers'].add(customer)

    # Step 2: Convert set → count
    for date in daily_data:
        daily_data[date]['unique_customers'] = len(
            daily_data[date]['unique_customers']
        )

    # Step 3: Sort chronologically by date
    sorted_daily_data = dict(
        sorted(daily_data.items())
    )

    return sorted_daily_data

# b. Peak sales day
def find_peak_sales_day(transactions):
    daily_sales = {}

    # Step 1: Aggregate revenue and transaction count per date
    for txn in transactions:
        date = txn['Date']
        amount = txn['UnitPrice']

        if date not in daily_sales:
            daily_sales[date] = {
                'revenue': 0.0,
                'transaction_count': 0
            }

        daily_sales[date]['revenue'] += amount
        daily_sales[date]['transaction_count'] += 1

    # Step 2: Find date with highest revenue
    peak_date = max(
        daily_sales.items(),
        key=lambda x: x[1]['revenue']
    )

    # Step 3: Return required tuple
    return (
        peak_date[0],
        peak_date[1]['revenue'],
        peak_date[1]['transaction_count']
    )

# ############## Task 2.3 Product Performance
# a.Low Performing Products
def low_performing_products(transactions, threshold=10):
    product_data = {}

    # Step 1: Aggregate quantity and revenue per product
    for txn in transactions:
        product = txn['ProductName']
        quantity = txn['Quantity']
        revenue = txn['UnitPrice']

        if product not in product_data:
            product_data[product] = {
                'total_quantity': 0,
                'total_revenue': 0.0
            }

        product_data[product]['total_quantity'] += quantity
        product_data[product]['total_revenue'] += revenue

    # Step 2: Filter products below threshold
    low_products = [
        (product, data['total_quantity'], data['total_revenue'])
        for product, data in product_data.items()
        if data['total_quantity'] < threshold
    ]

    # Step 3: Sort by TotalQuantity ascending
    low_products.sort(key=lambda x: x[1])

    return low_products
