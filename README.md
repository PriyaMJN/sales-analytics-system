# bitsom_ba_25071955-sales-analytics-system
Sales Analytics System assignment.

# Sales Analytics System 

**Student Name:** Priya Tushar Mahajan  
**Student ID:** 25071955  
**Email:** priya.mahajan@email.com  
**Date:** January 2026  

---

## Project Overview

The Sales Analytics System is a Python-based data processing and reporting application designed to analyze raw sales transaction data and generate meaningful business insights. The system processes structured sales records, performs multiple levels of analysis, enriches product data using an external API, and produces a comprehensive, human-readable sales report.

This project demonstrates end-to-end data handling, including file processing, data validation, aggregation, API integration, and report generation, making it suitable for real-world analytics use cases

---

## 🔑 Key Features

- **Data Ingestion:** Reads raw sales data from text files with error handling.
- **Parsing & Validation:** Cleans and validates transaction records.
- **Sales Analysis:** Computes total revenue, average order value, region-wise sales, top products, top customers, and daily sales trends.
- **API Data Enrichment:** Enriches transactions with product category, brand, and rating from an external API.
- **Report Generation:** Creates a formatted sales analytics report including overall summary, region-wise performance, top products/customers, daily trends, and enrichment statistics.
- **Modular Design:** Organized into reusable Python modules for maintainability and scalability.

---

## 🗂️ Project Structure

sales-analytics-system/
│
├── data/
│ ├── sales_data.txt # Raw sales transactions
│ └── enriched_sales_data.txt # Enriched transaction data
│
├── output/
│ └── sales_report.txt # Generated sales report
│
├── utils/
│ ├── file_handler.py # File read/write and parsing functions
│ ├── data_processor.py # Analysis functions
│ └── api_handler.py # API fetching and data enrichment
│
├── main.py # Main execution script
└── README.md # Project documentation

---

## 🛠️ Technologies Used

- Python 3
- File handling and data processing
- REST API integration for product enrichment
- Modular programming with reusable utility modules
- Exception handling and input validation

---

## 🚀 Workflow

1. **Read Sales Data:** Load transactions from a pipe-delimited file.
2. **Parse & Clean:** Convert raw records into structured transactions.
3. **Filter Options:** Optional region and transaction amount filtering.
4. **Validate Transactions:** Identify valid and invalid records.
5. **Perform Analysis:** Customer, product, and region analysis, revenue metrics, daily trends.
6. **Fetch API Data:** Retrieve product info from external API.
7. **Enrich Transactions:** Add product category, brand, and rating to transactions.
8. **Save Enriched Data:** Save enriched transactions to a file.
9. **Generate Report:** Create a formatted sales report including all summaries and analysis.
10. **Completion:** Output success messages and file paths.

---

## 🎯 Learning Outcomes

- Practical understanding of end-to-end sales data processing
- Experience with API integration and data enrichment
- Ability to analyze sales metrics across multiple dimensions
- Skills in generating professional, formatted reports
- Modular Python programming and error handling

---

## 💡 Use Cases

- Business intelligence and sales performance tracking
- Academic assignments and Python analytics projects
- Entry-level data analytics training
- Demonstration of Python programming and API usage

---

## ⚡ How to Run

1. Clone the repository:
```bash
git clone git@github.com:PriyaMJN/sales-analytics-system.git
cd sales-analytics-system

2. Install required dependencies (if any):
pip install -r requirements.txt

3. Run the main script:
python main.py

4. Output:
Enriched transaction data → data/enriched_sales_data.txt
Sales report → output/sales_report.txt
