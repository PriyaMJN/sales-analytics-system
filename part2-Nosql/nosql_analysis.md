# Task 2.1: NoSQL Justification Report

## Section A: Limitations of RDBMS 

FlexiMart plans to expand its product catalog to include highly diverse products such as electronics, footwear, clothing, and accessories. Using a traditional Relational Database Management System (RDBMS) like MySQL would create several challenges. RDBMS relies on a fixed schema, which makes it difficult to handle products with different attributes. For example, laptops require fields like RAM and processor, while shoes need size and color. Managing these variations would result in many nullable columns or multiple tables, increasing complexity.

Frequent schema changes are another limitation. As FlexiMart introduces new product categories, table structures would need to be altered repeatedly, leading to maintenance overhead and potential downtime. Additionally, storing customer reviews as nested data is inefficient in RDBMS. Reviews must be stored in separate tables and retrieved using joins, which increases query complexity and reduces performance when FlexiMart needs to fetch products along with their reviews.


## Section B: NoSQL Benefits 

MongoDB is well-suited for FlexiMart’s expanding and diverse product catalog due to its flexible, document-based schema. Each product can be stored as a document with attributes specific to its category, allowing FlexiMart to store laptops, shoes, and other products in the same collection without schema modifications.

MongoDB supports embedded documents, which enables customer reviews to be stored directly inside the product document. This simplifies data modeling and improves read performance by eliminating costly joins. FlexiMart can easily retrieve complete product details along with reviews in a single query.

Additionally, MongoDB provides horizontal scalability through sharding. As FlexiMart grows and experiences increased traffic and data volume, MongoDB can distribute data across multiple servers, ensuring high availability and performance. These features make MongoDB an ideal choice for FlexiMart’s evolving product catalog.


## Section C: Trade-offs (≈100 words)

Despite its advantages, using MongoDB for FlexiMart also involves trade-offs. One disadvantage is the lack of strict relational constraints such as foreign keys. Ensuring data consistency between customers, products, and orders must be handled at the application level, increasing development responsibility.

Another limitation is that MongoDB is less optimized for complex transactional workloads compared to MySQL. While MongoDB supports transactions, relational databases still perform better for highly structured, transaction-heavy systems. Therefore, FlexiMart must carefully evaluate where strong consistency is required before fully replacing MySQL with MongoDB.

## Conclusion: MongoDB is highly suitable for FlexiMart’s diverse and evolving product catalog.