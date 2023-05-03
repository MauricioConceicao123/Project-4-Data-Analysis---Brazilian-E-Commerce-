/**Category Translation Table**/
CREATE TABLE category_translation (
	product_category_name VARCHAR (50),
 	product_category_name_english VARCHAR (50) PRIMARY KEY
	);

 /*SELECT 

  COALESCE(product_category_name, 'N/A') AS product_category_name,
  COALESCE(product_category_name_english, 'N/A') AS product_category_name_english
FROM category_translation;
 */ 

 SELECT *FROM category_translation;

LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Data/category_translation.csv'
INTO TABLE category_translation
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 ROWS;



 
/**Category Sellers Table**/ 
CREATE TABLE sellers (
	seller_id VARCHAR(32)  PRIMARY KEY,
 	seller_zip_code_prefix INT NOT NULL,
 	seller_city VARCHAR(50),
 	seller_state VARCHAR(2),
	FOREIGN KEY (seller_zip_code_prefix) REFERENCES (customer_zip_code_prefix) 
	);

 /*SELECT 
  seller_id,
  COALESCE(seller_zip_code_prefix, 'N/A') AS seller_zip_code_prefix,
  COALESCE(seller_city, 'N/A') AS seller_city,
  COALESCE(seller_state, 'N/A') AS seller_state
FROM sellers; */

LOAD DATA INFILE 'C:\ProgramData\MySQL\MySQL Server 8.0\Data\olist_sellers_dataset.csv'
INTO TABLE sellers
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 ROWS;
 
SELECT *FROM sellers;

/**Category Products Table**/ 
CREATE TABLE Products (
	product_id VARCHAR(32) PRIMARY KEY,
 	product_category_name VARCHAR(50), product_name_lenght INT,
 	product_description_lenght INT,
 	product_photos_qty INT,
 	product_weight_g INT,
 	product_length_cm INT,
 	product_height_cm INT
	);

 
 SELECT *FROM Products;
 
 /**Category Orders Table**/
 CREATE TABLE Orders (
	order_id VARCHAR(50) PRIMARY KEY,
 	customer_id VARCHAR(32) NOT NULL,
 	order_status VARCHAR(20),
 	order_purchase_timestamp DATETIME,
 	order_approved_at DATETIME,
 	order_delivered_carrier_date DATETIME,
 	order_delivered_customer_date DATETIME,
 	order_estimated_delivery_date DATETIME,
  	FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
	);

 SELECT *FROM Orders;


 
  /**Category Orders Reviews Table**/
   CREATE TABLE Order_Reviews (
  	review_id VARCHAR(50) NOT NULL,
	order_id VARCHAR(32) PRIMARY KEY,
   	review_score INT,
   	review_comment_title VARCHAR(50),
   	review_creation_date DATETIME,
  	review_answer_timestamp DATETIME
	);
   
 SELECT *FROM Order_Reviews;



 /**Category customers Table**/ 
CREATE TABLE customers (
 	customer_id VARCHAR(32) PRIMARY KEY,
  	customer_unique_id VARCHAR(32),
  	customer_zip_code_prefix INT,
  	customer_city VARCHAR(32),
  	customer_state VARCHAR(2),
  	FOREIGN KEY zip_code_prefix
	);

SELECT *FROM customers;

 
 /**Category geolocation Table**/ 
CREATE TABLE geolocation (
	geolocation_zip_code_prefix INT  PRIMARY KEY ,
	geolocation_lat DOUBLE,
	geolocation_lng DOUBLE,
	geolocation_city VARCHAR(30),
	geolocation_state VARCHAR(2)
	);

SELECT *FROM geolocation;


  /**Category order_payments Table**/  

CREATE TABLE order_payments (
  	order_id VARCHAR(32) PRIMARY KEY,
  	payment_sequential INT,
  	payment_type VARCHAR(20),
  	payment_installments INT,
  	payment_value DOUBLE
  	);
  
SELECT *FROM order_payments;


  /**Category order_items Table**/  
CREATE TABLE order_items (
  	order_id VARCHAR(32) PRIMARY KEY,
  	order_item_id INT,
  	product_id VARCHAR(32),
  	seller_id VARCHAR(32) NOT NULL,
  	shipping_limit_date DATETIME ,
  	price DOUBLE,
  	freight_value DOUBLE,
  	FOREIGN KEY seller_id => Sellers(seller_id),
  	FOREIGN KEY product_id => Products(product_id)
	);


SELECT *FROM order_items;
