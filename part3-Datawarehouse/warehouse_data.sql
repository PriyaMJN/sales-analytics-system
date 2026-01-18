INSERT INTO dim_date VALUES
(20240101,'2024-01-01','Monday',1,1,'January','Q1',2024,false),
(20240102,'2024-01-02','Tuesday',2,1,'January','Q1',2024,false),
(20240103,'2024-01-03','Wednesday',3,1,'January','Q1',2024,false),
(20240104,'2024-01-04','Thursday',4,1,'January','Q1',2024,false),
(20240105,'2024-01-05','Friday',5,1,'January','Q1',2024,false),
(20240106,'2024-01-06','Saturday',6,1,'January','Q1',2024,true),
(20240107,'2024-01-07','Sunday',7,1,'January','Q1',2024,true),
(20240108,'2024-01-08','Monday',8,1,'January','Q1',2024,false),
(20240109,'2024-01-09','Tuesday',9,1,'January','Q1',2024,false),
(20240110,'2024-01-10','Wednesday',10,1,'January','Q1',2024,false),
(20240111,'2024-01-11','Thursday',11,1,'January','Q1',2024,false),
(20240112,'2024-01-12','Friday',12,1,'January','Q1',2024,false),
(20240113,'2024-01-13','Saturday',13,1,'January','Q1',2024,true),
(20240114,'2024-01-14','Sunday',14,1,'January','Q1',2024,true),
(20240115,'2024-01-15','Monday',15,1,'January','Q1',2024,false),
(20240120,'2024-01-20','Saturday',20,1,'January','Q1',2024,true),
(20240121,'2024-01-21','Sunday',21,1,'January','Q1',2024,true),
(20240125,'2024-01-25','Thursday',25,1,'January','Q1',2024,false),
(20240131,'2024-01-31','Wednesday',31,1,'January','Q1',2024,false),
(20240201,'2024-02-01','Thursday',1,2,'February','Q1',2024,false),
(20240202,'2024-02-02','Friday',2,2,'February','Q1',2024,false),
(20240203,'2024-02-03','Saturday',3,2,'February','Q1',2024,true),
(20240204,'2024-02-04','Sunday',4,2,'February','Q1',2024,true),
(20240205,'2024-02-05','Monday',5,2,'February','Q1',2024,false),
(20240210,'2024-02-10','Saturday',10,2,'February','Q1',2024,true),
(20240211,'2024-02-11','Sunday',11,2,'February','Q1',2024,true),
(20240214,'2024-02-14','Wednesday',14,2,'February','Q1',2024,false),
(20240220,'2024-02-20','Tuesday',20,2,'February','Q1',2024,false),
(20240225,'2024-02-25','Sunday',25,2,'February','Q1',2024,true),
(20240228,'2024-02-28','Wednesday',28,2,'February','Q1',2024,false);

select * FROM dim_date;

INSERT INTO dim_product (product_id, product_name, category, subcategory, unit_price) VALUES
('P001','Smartphone','Electronics','Mobile',45000),
('P002','Laptop','Electronics','Computer',85000),
('P003','Headphones','Electronics','Accessories',3000),
('P004','Smart TV','Electronics','Television',65000),
('P005','Power Bank','Electronics','Accessories',2000),

('P006','T-Shirt','Fashion','Clothing',799),
('P007','Jeans','Fashion','Clothing',1999),
('P008','Jacket','Fashion','Outerwear',4999),
('P009','Sneakers','Fashion','Footwear',3499),
('P010','Watch','Fashion','Accessories',8999),

('P011','Rice Bag','Grocery','Grains',1200),
('P012','Cooking Oil','Grocery','Edible Oil',900),
('P013','Milk Pack','Grocery','Dairy',100),
('P014','Coffee','Grocery','Beverages',450),
('P015','Chocolate Box','Grocery','Snacks',650);

SELECT * FROM dim_product;

INSERT INTO dim_customer (customer_id, customer_name, city, state, customer_segment) VALUES
('C001','John Doe','Mumbai','Maharashtra','Retail'),
('C002','Amit Shah','Ahmedabad','Gujarat','Retail'),
('C003','Priya Mehta','Delhi','Delhi','Corporate'),
('C004','Rohit Verma','Bengaluru','Karnataka','Retail'),
('C005','Sneha Patil','Mumbai','Maharashtra','Corporate'),
('C006','Karan Singh','Delhi','Delhi','Retail'),
('C007','Neha Sharma','Jaipur','Rajasthan','Retail'),
('C008','Vikas Jain','Ahmedabad','Gujarat','Wholesale'),
('C009','Pooja Kulkarni','Pune','Maharashtra','Retail'),
('C010','Arjun Nair','Bengaluru','Karnataka','Corporate'),
('C011','Ritu Malhotra','Delhi','Delhi','Wholesale'),
('C012','Manish Gupta','Jaipur','Rajasthan','Retail');

SELECT * FROM dim_customer;

INSERT INTO fact_sales
(date_key, product_key, customer_key, quantity_sold, unit_price, discount_amount, total_amount)
VALUES
(20240106,1,1,2,45000,2000,88000),
(20240106,2,2,1,85000,5000,80000),
(20240107,3,3,3,3000,0,9000),
(20240107,6,4,4,799,0,3196),
(20240107,11,5,2,1200,0,2400),

(20240113,4,6,1,65000,3000,62000),
(20240113,9,7,2,3499,0,6998),
(20240114,10,8,1,8999,999,8000),
(20240114,15,9,5,650,0,3250),
(20240114,13,10,10,100,0,1000),

(20240120,5,11,3,2000,0,6000),
(20240120,8,12,1,4999,0,4999),
(20240121,7,1,2,1999,0,3998),
(20240121,14,2,4,450,0,1800),
(20240121,12,3,3,900,0,2700),

(20240203,2,4,1,85000,7000,78000),
(20240203,6,5,5,799,0,3995),
(20240204,1,6,1,45000,0,45000),
(20240204,11,7,2,1200,0,2400),
(20240204,15,8,3,650,0,1950),

(20240210,9,9,2,3499,0,6998),
(20240210,4,10,1,65000,4000,61000),
(20240211,3,11,4,3000,0,12000),
(20240211,14,12,6,450,0,2700),
(20240211,7,1,1,1999,0,1999),

(20240214,10,2,1,8999,999,8000),
(20240214,8,3,2,4999,0,9998),
(20240220,12,4,3,900,0,2700),
(20240220,6,5,4,799,0,3196),
(20240225,2,6,1,85000,5000,80000),

(20240225,1,7,2,45000,3000,87000),
(20240225,15,8,5,650,0,3250),
(20240225,13,9,12,100,0,1200),
(20240228,11,10,3,1200,0,3600),
(20240228,9,11,1,3499,0,3499),

(20240228,4,12,1,65000,5000,60000),
(20240228,5,1,2,2000,0,4000),
(20240228,14,2,6,450,0,2700),
(20240228,7,3,1,1999,0,1999),
(20240211, 2, 4, 1, 85000, 5000, 80000);

SELECT * FROM fact_sales;
