## Star Schema Design – FlexiMart
## Section 1: Schema Overview

FlexiMart requires a data warehouse to analyze historical sales trends, customer behavior, and product performance. A Star Schema is designed to support efficient analytical queries by separating transactional facts from descriptive dimensions.

## FACT TABLE: fact_sales

## Grain:
One row per product per order line item.

Business Process:
Sales transactions at FlexiMart, capturing product-level sales details for each customer order.

## Measures (Numeric Facts)

quantity_sold: Number of units sold in a transaction
unit_price: Price per unit at the time of sale
discount_amount: Discount applied to the product
total_amount: Final sale amount
(quantity_sold × unit_price − discount_amount)

Foreign Keys
date_key → dim_date
product_key → dim_product
customer_key → dim_customer
DIMENSION TABLE: dim_date

Purpose:
Provides a structured time dimension to support time-based sales analysis such as daily, monthly, quarterly, and yearly trends.

Type:
Conformed Dimension

Attributes
date_key (PK): Surrogate key (integer, format: YYYYMMDD)
full_date: Actual calendar date
day_of_week: Monday, Tuesday, etc.
month: Numeric month (1–12)
month_name: January, February, etc.
quarter: Q1, Q2, Q3, Q4
year: Calendar year (e.g., 2023, 2024)
is_weekend: Boolean flag (true/false)

## DIMENSION TABLE: dim_product

Purpose:
Stores descriptive information about products sold by FlexiMart for product-level analysis.

Type:
Slowly Changing Dimension (Type 1)

Attributes
product_key (PK): Surrogate key
product_id: Business product identifier
product_name: Name of the product
category: Product category (Electronics, Fashion, Grocery, etc.)
brand: Brand name
price: Current product price
launch_date: Product launch date
status: Active / Discontinued

## DIMENSION TABLE: dim_customer
Purpose:
Contains customer details to analyze purchasing behavior and customer segmentation.

Type:
Slowly Changing Dimension (Type 2)

Attributes
customer_key (PK): Surrogate key
customer_id: Business customer identifier
customer_name: Full name of customer
gender: Male / Female / Other
age_group: Age range (18–25, 26–35, etc.)
city: Customer city
state: Customer state
country: Customer country
signup_date: Date customer registered

### Section 2: Design Decisions (3 marks - 150 words) 

## Why you chose this granularity (transaction line-item level) 
The fact table in the FlexiMart star schema is designed at the transaction line-item level, where each row represents a single product within an order. This granularity was chosen because it captures the most detailed level of sales data, enabling accurate analysis of product performance, discounts, and customer purchasing behavior. It also allows aggregation at higher levels such as daily, monthly, or category-wise sales without losing detail.

## Why surrogate keys instead of natural keys 
Surrogate keys are used instead of natural keys to improve performance and maintain data integrity. Natural keys such as product IDs or customer IDs may change over time or have inconsistent formats across systems. Surrogate keys provide stable, integer-based identifiers that support efficient joins and simplify Slowly Changing Dimension management.

## How this design supports drill-down and roll-up operations
This star schema design supports drill-down and roll-up operations by organizing data hierarchically within dimensions. Analysts can roll up sales from day to month or year and drill down from category to individual products or customers, enabling flexible and efficient analytical reporting.