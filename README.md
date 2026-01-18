# bitsom_ba_25071955-fleximart-data-architecture
Fleximart Data architecture assignment.

# FlexiMart Data Architecture Project

**Student Name:** Priya Tushar Mahajan  
**Student ID:** 25071955  
**Email:** priya.mahajan@email.com  
**Date:** January 2026  

---

## Project Overview

The FlexiMart Data Architecture Project demonstrates the design and implementation of a complete data pipeline, including ETL processing, NoSQL data modeling, and data warehouse analytics. The project focuses on cleaning raw transactional data, storing structured and semi-structured data, and enabling analytical insights through optimized schemas and queries.

---

## Repository Structure

├── part1-database-etl/
│ ├── etl_pipeline.py
│ ├── schema_documentation.md
│ ├── business_queries.sql
│ └── data_quality_report.txt
│
├── part2-nosql/
│ ├── nosql_analysis.md
│ ├── mongodb_operations.js
│ └── products_catalog.json
│
├── part3-datawarehouse/
│ ├── star_schema_design.md
│ ├── warehouse_schema.sql
│ ├── warehouse_data.sql
│ └── analytics_queries.sql
│
└── README.md


---

## Technologies Used

- **Programming Language:** Python 3.x  
- **Libraries:** pandas, mysql-connector-python  
- **Relational Database:** MySQL 8.0  
- **NoSQL Database:** MongoDB 6.0  
- **Data Modeling:** Star Schema (Fact & Dimension tables)

---

## Setup Instructions

### Prerequisites
- Python 3.x installed
- MySQL Server running
- MongoDB installed and running
- Required Python packages installed:
  ```bash
  pip install pandas mysql-connector-python

# Database Setup (MySQL)
# ############################
# Create transactional and warehouse databases
mysql -u root -p -e "CREATE DATABASE fleximart;"
mysql -u root -p -e "CREATE DATABASE fleximart_dw;"

# Run Part 1 - ETL Pipeline
python part1-database-etl/etl_pipeline.py

# Execute business queries
mysql -u root -p fleximart < part1-database-etl/business_queries.sql


# Data Warehouse Setup
# #####################
# Create warehouse schema
mysql -u root -p fleximart_dw < part3-datawarehouse/warehouse_schema.sql

# Load warehouse data
mysql -u root -p fleximart_dw < part3-datawarehouse/warehouse_data.sql

# Run analytics queries
mysql -u root -p fleximart_dw < part3-datawarehouse/analytics_queries.sql


# MongoDB Setup
# #####################
mongosh < part2-nosql/mongodb_operations.js

# ################Key Learnings##################

Designed and implemented a complete ETL pipeline with data validation and error handling.

Gained hands-on experience in relational and NoSQL data modeling.

Learned how to design and query a star schema for analytical reporting.

Improved understanding of real-world data quality challenges and solutions.


# ######################## Challenges Faced #####################

Handling inconsistent and missing data:
Solved by implementing validation checks and removing invalid records during ETL.

Integrating multiple data storage systems:
Addressed by separating transactional, NoSQL, and warehouse layers with clear responsibilities.

Authentication and GitHub version control issues:
Resolved using GitHub Personal Access Tokens and proper Git workflows.

# Conclusion

This project provides an end-to-end understanding of modern data architecture concepts, combining ETL processing, NoSQL storage, and data warehousing techniques to support business analytics.