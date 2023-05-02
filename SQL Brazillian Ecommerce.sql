/**Category Translation Table**/
CREATE TABLE category_translation 
(product_category_name VARCHAR (50) NOT NULL,
 product_category_name_english VARCHAR (50) NOT NULL);
 /*SELECT 

  COALESCE(product_category_name, 'N/A') AS product_category_name,
  COALESCE(product_category_name_english, 'N/A') AS product_category_name_english
FROM category_translation;
 */ 

LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Data/category_translation.csv'
INTO TABLE category_translation
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 ROWS;


 SELECT *FROM category_translation;
 
/**Category Sellers Table**/ 
CREATE TABLE sellers
(seller_id VARCHAR(32),
 seller_zip_code_prefix INT NOT NULL,
 seller_city VARCHAR(50),
 seller_state VARCHAR(2),
 PRIMARY KEY (seller_id));
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
CREATE TABLE Products (product_id VARCHAR(32) NOT NULL,
 product_category_name VARCHAR(50), product_name_lenght INT,
 product_description_lenght INT,
 product_photos_qty INT,
 product_weight_g INT,
 product_length_cm INT,
 product_height_cm INT);

 
 SELECT *FROM Products;
 
 /**Category Orders Table**/
 CREATE TABLE Orders (order_id VARCHAR(50) NOT NULL,
 customer_id VARCHAR(32) NOT NULL,
 order_status VARCHAR(20),
 order_purchase_timestamp DATETIME,
 order_approved_at DATETIME,
 order_delivered_carrier_date DATETIME,
 order_delivered_customer_date DATETIME,
 order_estimated_delivery_date DATETIME);

 SELECT *FROM Orders;
 
  /**Category Orders Reviews Table**/
   CREATE TABLE Order_Reviews (review_id VARCHAR(50) NOT NULL,
   order_id VARCHAR(32) NOT NULL,
   review_score INT,
   review_comment_title VARCHAR(50),
   review_creation_date DATETIME,
   review_answer_timestamp DATETIME);
   
    SELECT *FROM Order_Reviews;
   