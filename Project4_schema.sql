CREATE TABLE `category_translation` (
  `product_category_name` varchar(255),
  `product_category_name_english` varchar(255)
);

CREATE TABLE `sellers` (
  `seller_id` varchar(255),
  `seller_zip_code_prefix` integer,
  `seller_city` varchar(255),
  `seller_state` varchar(255)
);

CREATE TABLE `products` (
  `product_category_name` varchar(255),
  `product_name_lenght` integer,
  `product_description_lenght` integer,
  `product_photos_qty` integer,
  `product_weight_g` integer,
  `product_length_cm` integer,
  `product_height_cm` integer
);

CREATE TABLE `orders` (
  `customer_id` varchar(255),
  `order_status` varchar(255),
  `order_purchase_timestamp` DATETIME,
  `order_approved_at` DATETIME,
  `order_delivered_carrier_date` DATETIME,
  `order_delivered_customer_date` DATETIME,
  `order_estimated_delivery_date` DATETIME
);

CREATE TABLE `customers` (
  `customer_id` varchar(255),
  `customer_unique_id` varchar(255),
  `customer_zip_code_prefix` integer,
  `customer_city` varchar(255),
  `customer_state` varchar(255),
  `PRIMARY` KEY(customer_id)
);

CREATE TABLE `geolocation` (
  `geolocation_zip_code_prefix` integer,
  `geolocation_lat` DOUBLE,
  `geolocation_lng` DOUBLE,
  `geolocation_city` varchar(255),
  `geolocation_state` varchar(255),
  `PRIMARY` KEY(geolocation_zip_code_prefix)
);

CREATE TABLE `order_payments` (
  `order_id` varchar(255),
  `payment_sequential` integer,
  `payment_type` varchar(255),
  `payment_installments` integer,
  `payment_value` DOUBLE(10,2),
  `PRIMARY` KEY(order_id)
);

CREATE TABLE `order_items` (
  `order_id` varchar(255),
  `order_item_id` integer,
  `product_id` varchar(255),
  `seller_id` varchar(255),
  `shipping_limit_date` DATETIME,
  `price` DOUBLE(10,2),
  `freight_value` DOUBLE(10,2),
  `PRIMARY` KEY(order_id)
);

CREATE TABLE `order_reviews` (
  `review_id` varchar(255),
  `order_id` varchar(255),
  `review_score` integer,
  `review_comment_title` varchar(255),
  `review_creation_date` DATETIME,
  `review_answer_timestamp` DATETIME
);

ALTER TABLE `order_reviews` ADD FOREIGN KEY (`order_id`) REFERENCES `order_payments` (`order_id`);

ALTER TABLE `order_reviews` ADD FOREIGN KEY (`order_id`) REFERENCES `order_items` (`order_id`);

ALTER TABLE `customers` ADD FOREIGN KEY (`customer_id`) REFERENCES `orders` (`customer_id`);

ALTER TABLE `geolocation` ADD FOREIGN KEY (`geolocation_zip_code_prefix`) REFERENCES `sellers` (`seller_zip_code_prefix`);

ALTER TABLE `sellers` ADD FOREIGN KEY (`seller_zip_code_prefix`) REFERENCES `customers` (`customer_zip_code_prefix`);

ALTER TABLE `category_translation` ADD FOREIGN KEY (`product_category_name_english`) REFERENCES `products` (`product_category_name`);
