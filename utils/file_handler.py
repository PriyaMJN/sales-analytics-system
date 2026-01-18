# Task 1.1 Read sales data with encoding handling
def read_sales_data(filename):
    """
    Reads sales data from file handling encoding issues

    Returns: list of raw lines (strings)
    """
    encodings = ['utf-8', 'latin-1', 'cp1252']

    for encoding in encodings:
        try:
            with open(filename, 'r', encoding=encoding) as file:
                lines = file.readlines()

            # Skip header row and remove empty lines
            cleaned_lines = [
                line.strip()
                for line in lines[1:]   # skip header
                if line.strip()         # remove empty lines
            ]

            return cleaned_lines

        except UnicodeDecodeError:
            # Try next encoding
            continue

        except FileNotFoundError:
            print(f"Error: File '{filename}' not found.")
            return []

    # If all encodings fail
    print("Error: Unable to read file with supported encodings.")
    return []

# Task 1.2 Parse and cleaned data
def read_sales_data(filename):
    """
    Reads sales data from file handling encoding issues
    """
    encodings = ['utf-8', 'latin-1', 'cp1252']

    for encoding in encodings:
        try:
            with open(filename, 'r', encoding=encoding) as file:
                lines = file.readlines()

            # Skip header and remove empty lines
            cleaned_lines = [
                line.strip()
                for line in lines[1:]
                if line.strip()
            ]

            return cleaned_lines

        except UnicodeDecodeError:
            continue

        except FileNotFoundError:
            print(f"Error: File '{filename}' not found.")
            return []

    print("Error: Unable to read file with supported encodings.")
    return []

# Task 1.3 Data Validation and Filtering
def parse_transactions(raw_lines):
    """
    Parses raw lines into clean list of dictionaries
    """
    transactions = []

    for line in raw_lines:
        fields = line.split('|')

        # Skip rows with incorrect number of fields
        if len(fields) != 8:
            continue

        try:
            transaction = {
                'TransactionID': fields[0].strip(),
                'Date': fields[1].strip(),
                'ProductID': fields[2].strip(),

                # Handle comma in product name
                'ProductName': fields[3].replace(',', ' ').strip(),

                # Remove commas and convert data types
                'Quantity': int(fields[4].replace(',', '').strip()),
                'UnitPrice': float(fields[5].replace(',', '').strip()),

                'CustomerID': fields[6].strip(),
                'Region': fields[7].strip()
            }

            transactions.append(transaction)

        except ValueError:
            # Skip rows with invalid numeric data
            continue

    return transactions

def validate_and_filter(transactions, region=None, min_amount=None, max_amount=None):
    """
    Validates transactions and applies optional filters
    """

    required_fields = [
        'TransactionID', 'Date', 'ProductID', 'ProductName',
        'Quantity', 'UnitPrice', 'CustomerID', 'Region'
    ]

    valid_transactions = []
    invalid_count = 0

    total_input = len(transactions)

    # Collect available regions and amount range
    regions = set()
    amounts = []

    for tx in transactions:
        try:
            # Check required fields
            if not all(field in tx for field in required_fields):
                invalid_count += 1
                continue

            # Validation rules
            if tx['Quantity'] <= 0 or tx['UnitPrice'] <= 0:
                invalid_count += 1
                continue

            if not (
                tx['TransactionID'].startswith('T') and
                tx['ProductID'].startswith('P') and
                tx['CustomerID'].startswith('C')
            ):
                invalid_count += 1
                continue

            amount = tx['Quantity'] * tx['UnitPrice']
            regions.add(tx['Region'])
            amounts.append(amount)

            valid_transactions.append(tx)

        except Exception:
            invalid_count += 1

    # Display available options
    if regions:
        print("Available Regions:", sorted(regions))
    if amounts:
        print(f"Transaction Amount Range: {min(amounts)} - {max(amounts)}")

    # Apply region filter
    filtered_by_region = 0
    if region:
        before_count = len(valid_transactions)
        valid_transactions = [
            tx for tx in valid_transactions if tx['Region'] == region
        ]
        filtered_by_region = before_count - len(valid_transactions)
        print(f"Records after region filter ({region}): {len(valid_transactions)}")

    # Apply amount filter
    filtered_by_amount = 0
    if min_amount is not None or max_amount is not None:
        before_count = len(valid_transactions)

        def amount_in_range(tx):
            amount = tx['Quantity'] * tx['UnitPrice']
            if min_amount is not None and amount < min_amount:
                return False
            if max_amount is not None and amount > max_amount:
                return False
            return True

        valid_transactions = [
            tx for tx in valid_transactions if amount_in_range(tx)
        ]

        filtered_by_amount = before_count - len(valid_transactions)
        print(f"Records after amount filter: {len(valid_transactions)}")

    filter_summary = {
        'total_input': total_input,
        'invalid': invalid_count,
        'filtered_by_region': filtered_by_region,
        'filtered_by_amount': filtered_by_amount,
        'final_count': len(valid_transactions)
    }

    return valid_transactions, invalid_count, filter_summary
