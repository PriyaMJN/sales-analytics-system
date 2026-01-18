# 1. Entity–Relationship Description
# ENTITY: customers

Purpose:
Stores information about customers who place orders on the FlexiMart platform.

Attributes:
customer_id: Unique identifier for each customer (Primary Key)
first_name: Customer’s first name
last_name: Customer’s last name
email: Customer’s email address (Unique)
phone: Contact phone number
city: City where the customer resides
registration_date: Date when the customer registered

Relationships:

One customer can place many orders
Relationship: customers (1) → orders (M)

# ENTITY: products

Purpose:
Stores details of products available for sale.

Attributes:
product_id: Unique identifier for each product (Primary Key)
product_name: Name of the product
category: Product category
price: Selling price of the product
stock_quantity: Available inventory quantity

Relationships:
One product can appear in many order_items
Relationship: products (1) → order_items (M)

# ENTITY: orders
Purpose:
Stores high-level order information for each customer transaction.

Attributes:
order_id: Unique identifier for each order (Primary Key)
customer_id: References the customer who placed the order (Foreign Key)
order_date: Date of the order
total_amount: Total value of the order
status: Order status (Pending, Completed, etc.)

Relationships:
Each order belongs to one customer

Each order can have many order items

# ENTITY: order_items

Purpose:
Stores item-level details for each order.

Attributes:
order_item_id: Unique identifier for each order item (Primary Key)
order_id: References the related order (Foreign Key)
product_id: References the purchased product (Foreign Key)
quantity: Number of units ordered
unit_price: Price per unit at purchase time
subtotal: Quantity × Unit Price

Relationships:
Many order items belong to one order
Many order items reference one product

# 2. Normalization Explanation (3NF)

The FlexiMart database schema is designed according to Third Normal Form (3NF) to ensure data integrity and minimize redundancy.

Functional Dependencies

customers:
customer_id → first_name, last_name, email, phone, city, registration_date

products:
product_id → product_name, category, price, stock_quantity

orders:
order_id → customer_id, order_date, total_amount, status

order_items:
order_item_id → order_id, product_id, quantity, unit_price, subtotal

Each non-key attribute is fully dependent on the primary key, and there are no partial dependencies.

# Why This Schema Is in 3NF

The schema is already in 1NF because all attributes contain atomic values.

It satisfies 2NF as there are no partial dependencies on composite keys.

It satisfies 3NF because there are no transitive dependencies—non-key attributes do not depend on other non-key attributes.

# Anomaly Prevention

Update anomaly is avoided by storing customer and product details only once.

Insert anomaly is avoided as new customers or products can be added independently.

Delete anomaly is prevented because deleting an order does not remove customer or product information.

This normalized design ensures efficient storage, consistency, and scalability.

# 3. Sample Data Representation
customers
customer_id	first_name	last_name	email	city
1	            Rahul	Sharma	  rahul@gmail.com Bangalore
2	            Priya	Patel	  priya@gmail.com Mumbai

products
product_id	product_name	category	price
1	          Laptop	   Electronics	45999
2	          Headphones   Electronics	2999

orders
order_id	customer_id	order_date	total_amount	status
1	              1	     2024-01-15	  45999	       Completed
2	              2	     2024-01-16	  5998	       Completed

order_items
order_item_id	order_id	product_id	quantity	subtotal
1	               1	      	1	       1         45999
2	               2	        2	       2	     5998