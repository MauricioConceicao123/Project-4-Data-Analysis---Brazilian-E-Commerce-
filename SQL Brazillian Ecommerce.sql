-- /**Category Products Table**/ 
-- CREATE TABLE IF NOT EXISTS products (
-- 	product_id VARCHAR(32) PRIMARY KEY,
--  	product_category_name VARCHAR(50), product_name_lenght INT,
--  	product_description_lenght INT,
--  	product_photos_qty INT,
--  	product_weight_g INT,
--  	product_length_cm INT,
--  	product_height_cm INT,
--     product_width_cm INT,
--     FOREIGN KEY (product_category_name) REFERENCES category_translation (product_category_name)
-- 	);
    
-- SET FOREIGN_KEY_CHECKS=0;

-- LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Data/products.csv'
-- INTO TABLE products
-- FIELDS TERMINATED BY ','
-- OPTIONALLY ENCLOSED BY '"'
-- LINES TERMINATED BY '\n'
-- IGNORE 1 ROWS;

-- SET FOREIGN_KEY_CHECKS=1;

SET FOREIGN_KEY_CHECKS=0;

/**Category category_translation Table**/
CREATE TABLE IF NOT EXISTS category_translation (
	product_category_name VARCHAR(50) PRIMARY KEY,
	product_category_name_english VARCHAR(50)
);

LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Data/category_translation.csv'
INTO TABLE category_translation
FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;


 /**Category geolocation Table**/ 
 CREATE TABLE IF NOT EXISTS geolocation (
	geolocation_zip_code_prefix INT  PRIMARY KEY,
	geolocation_lat DOUBLE,
	geolocation_lng DOUBLE,
	geolocation_city VARCHAR(30),
	geolocation_state VARCHAR(2)
	);
    
LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Data/geolocation_unique.csv'
INTO TABLE geolocation
FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;


/**Category Products Table**/ 
CREATE TABLE IF NOT EXISTS products (
	product_id VARCHAR(32) PRIMARY KEY,
 	product_category_name VARCHAR(50), product_name_lenght INT,
 	product_description_lenght INT,
 	product_photos_qty INT,
 	product_weight_g INT,
 	product_length_cm INT,
 	product_height_cm INT,
    product_width_cm INT,
    FOREIGN KEY (product_category_name) REFERENCES category_translation (product_category_name)
	);
    
LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Data/products.csv'
INTO TABLE products
FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

            
/**Category Sellers Table**/ 
CREATE TABLE IF NOT EXISTS sellers (
	seller_id VARCHAR(32)  PRIMARY KEY,
 	seller_zip_code_prefix INT,
 	seller_city VARCHAR(50),
 	seller_state VARCHAR(2),
    FOREIGN KEY (seller_zip_code_prefix) REFERENCES geolocation (geolocation_zip_code_prefix)
	);
    
LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Data/sellers.csv'
INTO TABLE sellers
FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n'
IGNORE 1 ROWS;
   
 
 /**Category customers Table**/ 
CREATE TABLE IF NOT EXISTS customers (
	customer_id VARCHAR(32) PRIMARY KEY,
	customer_unique_id VARCHAR(32),
	customer_zip_code_prefix INT,
	customer_city VARCHAR(32),
	customer_state VARCHAR(2),
	FOREIGN KEY (customer_zip_code_prefix) REFERENCES geolocation (geolocation_zip_code_prefix)
  );
    
LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Data/customers.csv'
INTO TABLE customers
FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;



/**Category orders Table**/
CREATE TABLE IF NOT EXISTS orders (
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
    

LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Data/orders.csv'
INTO TABLE orders
FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

    
 /**Category order_items Table**/  
CREATE TABLE IF NOT EXISTS order_items (
  	order_id VARCHAR(32) PRIMARY KEY,
  	order_item_id INT,
  	product_id VARCHAR(32),
  	seller_id VARCHAR(32) NOT NULL,
  	shipping_limit_date DATETIME ,
  	price DOUBLE,
  	freight_value DOUBLE,
    FOREIGN KEY (seller_id) REFERENCES sellers(seller_id),
	FOREIGN KEY (product_id) REFERENCES products (product_id)
	);


 /**Category order_items Table**/  
CREATE TABLE IF NOT EXISTS temp_order_items_no_pk (
  	order_id VARCHAR(32),
  	order_item_id INT,
  	product_id VARCHAR(32),
  	seller_id VARCHAR(32) NOT NULL,
  	shipping_limit_date DATETIME ,
  	price DOUBLE,
  	freight_value DOUBLE
	);

LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Data/order_items.csv' 
INTO TABLE temp_order_items_no_pk 
FIELDS TERMINATED BY ',' 
OPTIONALLY ENCLOSED BY '"' 
LINES TERMINATED BY '\n' 
IGNORE 1 ROWS
(order_id, order_item_id, product_id, seller_id, @shipping_limit_date, price, freight_value)
SET shipping_limit_date = STR_TO_DATE(@shipping_limit_date, '%m/%d/%Y %H:%i');

INSERT IGNORE INTO order_items (order_id, order_item_id, product_id, seller_id, shipping_limit_date, price, freight_value)
SELECT order_id, order_item_id, product_id, seller_id, shipping_limit_date, price, freight_value
FROM temp_order_items_no_pk;


/**Category order_payments Table**/
 CREATE TABLE order_payments (
  	order_id VARCHAR(32) PRIMARY KEY,
  	payment_sequential INT,
  	payment_type VARCHAR(20),
  	payment_installments INT,
  	payment_value DOUBLE
  	);


LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Data/order_payments.csv'
INTO TABLE order_payments
FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;
    
 
/**Category  order_reviews Table**/
CREATE TABLE order_reviews (
  	review_id VARCHAR(32) PRIMARY KEY,
	order_id VARCHAR(32),
   	review_score INT,
   	review_comment_title VARCHAR(26),
	review_comment_message VARCHAR(208),
   	review_creation_date DATETIME,
  	review_answer_timestamp DATETIME,
   	FOREIGN KEY (order_id) REFERENCES orders(order_id)
);


CREATE TABLE temp_order_reviews_no_pk (
    review_id VARCHAR(32),
    order_id VARCHAR(32),
    review_score INT,
    review_comment_title VARCHAR(255),
    review_comment_message TEXT,
    review_creation_date DATETIME,
    review_answer_timestamp DATETIME
);

LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Data/order_reviews_clean.csv' 
INTO TABLE temp_order_reviews_no_pk 
FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"' 
LINES TERMINATED BY '\n' 
IGNORE 1 ROWS
(review_id, order_id, review_score, review_comment_title, review_comment_message, @review_creation_date, @review_answer_timestamp)
SET review_creation_date = STR_TO_DATE(@review_creation_date, '%m/%d/%Y %H:%i'),
    review_answer_timestamp = STR_TO_DATE(@review_answer_timestamp, '%m/%d/%Y %H:%i');

INSERT IGNORE INTO order_reviews (review_id, order_id, review_score, review_comment_title, review_comment_message, review_creation_date, review_answer_timestamp)
SELECT review_id, order_id, review_score, review_comment_title, review_comment_message, review_creation_date, review_answer_timestamp
FROM temp_order_reviews_no_pk;

DROP TABLE temp_order_reviews_no_pk;

DROP TABLE temp_order_reviews;

SET FOREIGN_KEY_CHECKS=1;




















    
    

    

  
 



-- /**Category category_translation Table**/
-- CREATE TABLE IF NOT EXISTS category_translation (
-- 	product_category_name VARCHAR(50) PRIMARY KEY,
-- 	product_category_name_english VARCHAR(50)
-- );

-- LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Data/category_translation.csv'
-- INTO TABLE category_translation
-- FIELDS TERMINATED BY ','
-- OPTIONALLY ENCLOSED BY '"'
-- LINES TERMINATED BY '\r\n'
-- IGNORE 1 ROWS;

        
-- /**Category Sellers Table**/ 
-- CREATE TABLE IF NOT EXISTS  sellers (
-- 	seller_id VARCHAR(32)  PRIMARY KEY,
--  	seller_zip_code_prefix INT,
--  	seller_city VARCHAR(50),
--  	seller_state VARCHAR(2),
--     FOREIGN KEY (seller_zip_code_prefix) REFERENCES geolocation (geolocation_zip_code_prefix)
-- 	);
   
-- CREATE TABLE temp_sellers (
--   seller_id VARCHAR(32),
--   seller_zip_code_prefix INT,
--   seller_city VARCHAR(100),
--   seller_state CHAR(2)
-- );

-- LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Data/sellers.csv'
-- INTO TABLE temp_sellers
-- FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n'
-- IGNORE 1 ROWS;

-- SELECT seller_id, COUNT(*)
-- FROM temp_sellers
-- GROUP BY seller_id
-- HAVING COUNT(*) > 1;

-- INSERT INTO sellers (seller_id, seller_zip_code_prefix, seller_city, seller_state)
-- SELECT seller_id, seller_zip_code_prefix, seller_city, seller_state
-- FROM temp_sellers;

-- CREATE TABLE temp_sellers_unique (
--    seller_id VARCHAR(32),
--    seller_zip_code_prefix INT,
--    seller_city VARCHAR(100),
--    seller_state CHAR(2)
-- );
-- INSERT INTO temp_sellers_unique (seller_id, seller_zip_code_prefix, seller_city, seller_state)
-- SELECT seller_id, seller_zip_code_prefix, seller_city, seller_state
-- FROM temp_sellers
-- GROUP BY seller_id, seller_zip_code_prefix, seller_city, seller_state;

-- INSERT INTO sellers (seller_id, seller_zip_code_prefix, seller_city, seller_state)
-- SELECT seller_id, seller_zip_code_prefix, seller_city, seller_state
-- FROM temp_sellers_unique;

-- DROP TABLE temp_sellers;

-- DROP TABLE temp_sellers_unique;


 
--  /**Category customers Table**/ 
-- CREATE TABLE IF NOT EXISTS customers (
-- 	customer_id VARCHAR(32) PRIMARY KEY,
-- 	customer_unique_id VARCHAR(32),
-- 	customer_zip_code_prefix INT,
-- 	customer_city VARCHAR(32),
-- 	customer_state VARCHAR(2),
-- 	FOREIGN KEY (customer_zip_code_prefix) REFERENCES geolocation (geolocation_zip_code_prefix)
--   );
    
-- LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Data/customers.csv'
-- INTO TABLE customers
-- FIELDS TERMINATED BY ','
-- OPTIONALLY ENCLOSED BY '"'
-- LINES TERMINATED BY '\n'
-- IGNORE 1 ROWS;

--  /**Category geolocation Table**/ 
--  CREATE TABLE IF NOT EXISTS geolocation (
-- 	geolocation_zip_code_prefix INT  PRIMARY KEY ,
-- 	geolocation_lat DOUBLE,
-- 	geolocation_lng DOUBLE,
-- 	geolocation_city VARCHAR(30),
-- 	geolocation_state VARCHAR(2)
-- 	);
    
-- LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Data/geolocation_unique.csv'
-- INTO TABLE geolocation
-- FIELDS TERMINATED BY ','
-- OPTIONALLY ENCLOSED BY '"'
-- LINES TERMINATED BY '\n'
-- IGNORE 1 ROWS;
    

-- /**Category orders Table**/
-- CREATE TABLE IF NOT EXISTS orders (
-- 	order_id VARCHAR(50) PRIMARY KEY,
--  	customer_id VARCHAR(32) NOT NULL,
--  	order_status VARCHAR(20),
--  	order_purchase_timestamp DATETIME,
--  	order_approved_at DATETIME,
--  	order_delivered_carrier_date DATETIME,
--  	order_delivered_customer_date DATETIME,
--  	order_estimated_delivery_date DATETIME,
--   	FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
-- 	);
    
-- SET FOREIGN_KEY_CHECKS=0;

-- LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Data/orders.csv'
-- INTO TABLE orders
-- FIELDS TERMINATED BY ','
-- OPTIONALLY ENCLOSED BY '"'
-- LINES TERMINATED BY '\n'
-- IGNORE 1 ROWS;

-- SET FOREIGN_KEY_CHECKS=1;
    
--  /**Category order_items Table**/  
-- CREATE TABLE IF NOT EXISTS order_items (
--   	order_id VARCHAR(32) PRIMARY KEY,
--   	order_item_id INT,
--   	product_id VARCHAR(32),
--   	seller_id VARCHAR(32) NOT NULL,
--   	shipping_limit_date DATETIME ,
--   	price DOUBLE,
--   	freight_value DOUBLE,
--     FOREIGN KEY (seller_id) REFERENCES sellers(seller_id),
-- 	FOREIGN KEY (product_id) REFERENCES products (product_id)
-- 	);

-- SET FOREIGN_KEY_CHECKS=0;

-- LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Data/order_items.csv'
-- INTO TABLE order_items
-- FIELDS TERMINATED BY ','
-- OPTIONALLY ENCLOSED BY '"'
-- LINES TERMINATED BY '\r\n'
-- IGNORE 1 ROWS;

-- SET FOREIGN_KEY_CHECKS=1;


-- /**Category order_payments Table**/
--  CREATE TABLE IF NOT EXISTS order_payments (
--   	order_id VARCHAR(32) PRIMARY KEY,
--   	payment_sequential INT,
--   	payment_type VARCHAR(20),
--   	payment_installments INT,
--   	payment_value DOUBLE
--   	);

-- SET FOREIGN_KEY_CHECKS=0;

-- LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Data/order_payments.csv'
-- INTO TABLE order_payments
-- FIELDS TERMINATED BY ','
-- OPTIONALLY ENCLOSED BY '"'
-- LINES TERMINATED BY '\n'
-- IGNORE 1 ROWS;
    
-- SET FOREIGN_KEY_CHECKS=1;
 
-- /**Category  order_reviews Table**/
-- CREATE TABLE IF NOT EXISTS order_reviews (
--   	review_id VARCHAR(32) PRIMARY KEY,
-- 	order_id VARCHAR(32),
--    	review_score INT,
--    	review_comment_title VARCHAR(26),
-- 	review_comment_message VARCHAR(208),
--    	review_creation_date DATETIME,
--   	review_answer_timestamp DATETIME,
--    	FOREIGN KEY (order_id) REFERENCES orders(order_id)
-- );

-- SET FOREIGN_KEY_CHECKS=0;

-- CREATE TABLE temp_order_reviews_no_pk (
--     review_id VARCHAR(32),
--     order_id VARCHAR(32),
--     review_score INT,
--     review_comment_title VARCHAR(255),
--     review_comment_message TEXT,
--     review_creation_date DATETIME,
--     review_answer_timestamp DATETIME
-- );

-- LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Data/order_reviews_clean.csv'
-- INTO TABLE temp_order_reviews_no_pk
-- FIELDS TERMINATED BY ','
-- OPTIONALLY ENCLOSED BY '"'
-- LINES TERMINATED BY '\n'
-- IGNORE 1 ROWS
-- (review_id, order_id, review_score, review_comment_title, review_comment_message, @review_creation_date, @review_answer_timestamp)
-- SET review_creation_date = IF(@review_creation_date = '', '1000-01-01 00:00:00', @review_creation_date),
--     review_answer_timestamp = IF(@review_answer_timestamp = '', '1000-01-01 00:00:00', @review_answer_timestamp);

-- INSERT IGNORE INTO order_reviews (review_id, order_id, review_score, review_comment_title, review_comment_message, review_creation_date, review_answer_timestamp)
-- SELECT review_id, order_id, review_score, review_comment_title, review_comment_message, review_creation_date, review_answer_timestamp
-- FROM temp_order_reviews_no_pk;

-- DROP TABLE temp_order_reviews_no_pk;

-- DROP TABLE temp_order_reviews;

-- SET FOREIGN_KEY_CHECKS=1;




















    
    

    

  
 
