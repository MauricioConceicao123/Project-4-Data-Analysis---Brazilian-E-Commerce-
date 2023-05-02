/**Category Translation Table**/
CREATE TABLE category_translation 
(product_category_name VARCHAR (255) NOT NULL,
 product_category_name_english VARCHAR (255) NOT NULL);
 
 SELECT *FROM category_translation;
 
/**Category Sellers Table**/ 
CREATE TABLE sellers
(seller_id VARCHAR(255) NOT NULL,
 seller_zip_code_prefix INT NOT NULL,
 seller_city VARCHAR(255) NOT NULL,
 seller_state VARCHAR(255) NOT NULL,
 PRIMARY KEY (seller_id));
 
SELECT *FROM sellers;

/**Category Products Table**/ 
CREATE TABLE Products (product_id VARCHAR(255) NOT NULL,
 product_category_name VARCHAR(255) NOT NULL, product_name_lenght INT NOT NULL,
 product_description_lenght INT NOT NULL,
 product_photos_qty INT NOT NULL,
 product_weight_g INT NOT NULL,
 product_length_cm INT NOT NULL,
 product_height_cm INT NOT NULL);
 
 SELECT *FROM Products;
 
 /**Category Orders Table**/
 CREATE TABLE Orders (order_id VARCHAR(255) NOT NULL,
 customer_id VARCHAR(255) NOT NULL,
 order_status VARCHAR(255) NOT NULL,
 order_purchase_timestamp DATETIME NOT NULL,
 order_approved_at DATETIME NOT NULL,
 order_delivered_carrier_date DATETIME NOT NULL,
 order_delivered_customer_date DATETIME NOT NULL,
 order_estimated_delivery_date DATETIME NOT NULL);

 SELECT *FROM Orders;
 
  /**Category Orders Reviews Table**/
   CREATE TABLE Order_Reviews (review_id VARCHAR(255) NOT NULL,
   order_id VARCHAR(255) NOT NULL,
   review_score INT NOT NULL,
   review_comment_title VARCHAR(255) NOT NULL,
   review_creation_date DATETIME NOT NULL,
   review_answer_timestamp DATETIME NOT NULL);
   
 SELECT *FROM Order_Reviews;

  /**Category customers Table**/  
CREATE TABLE customers (
  customer_id VARCHAR(32),
  customer_unique_id VARCHAR(32),
  customer_zip_code_prefix INT,
  customer_city VARCHAR(32),
  customer_state VARCHAR(2),
  PRIMARY KEY customer_id
);

SELECT *FROM customers;

 
CREATE TABLE geolocation (
id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
geolocation_zip_code_prefix INT ,
geolocation_lat DOUBLE,
geolocation_lng DOUBLE,
geolocation_city VARCHAR(30),
geolocation_state VARCHAR(2)
);

SELECT *FROM geolocation;

  /**Category order_payments Table**/  

CREATE TABLE order_payments (
  id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
  order_id VARCHAR(32) NOT NULL,
  payment_sequential INT,
  payment_type VARCHAR(20),
  payment_installments INT,
  payment_value DOUBLE
  );
  
SELECT *FROM order_payments;


  /**Category order_items Table**/  
CREATE TABLE order_items (
id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
  order_id VARCHAR(32) NOT NULL,
  order_item_id INT,
  product_id VARCHAR(32),
  seller_id VARCHAR(32) NOT NULL,
  shipping_limit_date DATETIME ,
  price DOUBLE,
  freight_value DOUBLE,
  PRIMARY KEY (`order_id`)
);


SELECT *FROM order_items;
