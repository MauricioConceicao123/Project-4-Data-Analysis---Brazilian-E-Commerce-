import streamlit as st
import mysql.connector
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import mysql.connector
from sqlalchemy import create_engine
import datetime as dt
from dateutil.relativedelta import relativedelta

st.set_page_config(
    page_title="Project Python!",
    page_icon=":smiley:",
    layout="wide",
)
#connection to mysql

user = 'root'
password = 'password'
host = 'localhost'
port = '3306'
database = 'db'

connection = mysql.connector.connect(user = 'root', password = '123password', host = 'localhost', port = '3306', database = 'db', use_pure = True)

#engine = create_engine(f'mysql://{user}:{password}@{host}:{port}/{database}')

# Define your SQL queries as strings

query_top_products = """
SELECT 
    p.product_id, 
    ct.product_category_name_english,
    COUNT(oi.order_id) as order_count
FROM 
    products p
JOIN 
    order_items oi ON p.product_id = oi.product_id
JOIN
    Category_translation ct ON p.product_category_name = ct.product_category_name
GROUP BY 
    p.product_id, ct.product_category_name_english
ORDER BY 
    order_count DESC
LIMIT 10;
"""

# query_top_products = """
# SELECT 
#     p.product_id, 
#     p.product_category_name,
#     COUNT(oi.order_id) as order_count
# FROM 
#     products p
# JOIN 
#     order_items oi ON p.product_id = oi.product_id
# GROUP BY 
#     p.product_id, p.product_category_name
# ORDER BY 
#     order_count DESC
# LIMIT 10;
# """


query_top_sellers = """
SELECT 
    	s.seller_id,
    	SUM(oi.price) as total_revenue
FROM 
    	sellers s
JOIN 
    	order_items oi ON s.seller_id = oi.seller_id
GROUP BY 
    	s.seller_id
ORDER BY 
    	total_revenue DESC
LIMIT 10;
"""


query_top_customers = """
SELECT 
    o.customer_id, 
    SUM(oi.price) as total_spent
FROM 
    orders o
JOIN 
    order_items oi ON o.order_id = oi.order_id
GROUP BY 
    o.customer_id
ORDER BY 
    total_spent DESC
LIMIT 10;
"""

query_top_sellers = """
SELECT 
    	s.seller_id,
    	SUM(oi.price) as total_revenue
FROM 
    	sellers s
JOIN 
    	order_items oi ON s.seller_id = oi.seller_id
GROUP BY 
    	s.seller_id
ORDER BY 
    	total_revenue DESC
LIMIT 10;
"""

query_customer_retention_rate = """
SELECT 
    COUNT(DISTINCT CASE WHEN EXTRACT(YEAR FROM o.order_purchase_timestamp) = 2017 THEN c.customer_unique_id END) * 100.0 / 
    (
        SELECT 
            COUNT(DISTINCT c.customer_unique_id)
        FROM 
            orders o
        JOIN 
            customers c ON o.customer_id = c.customer_id
        WHERE 
            EXTRACT(YEAR FROM o.order_purchase_timestamp) = 2016
    ) AS retention_rate_2017,
    COUNT(DISTINCT CASE WHEN EXTRACT(YEAR FROM o.order_purchase_timestamp) = 2018 THEN c.customer_unique_id END) * 100.0 / 
    (
        SELECT 
            COUNT(DISTINCT c.customer_unique_id)
        FROM 
            orders o
        JOIN 
            customers c ON o.customer_id = c.customer_id
        WHERE 
            EXTRACT(YEAR FROM o.order_purchase_timestamp) = 2017
    ) AS retention_rate_2018
FROM 
    orders o
JOIN 
    customers c ON o.customer_id = c.customer_id
WHERE 
    EXTRACT(YEAR FROM o.order_purchase_timestamp) IN (2017, 2018) AND 
    c.customer_unique_id IN (
        SELECT 
            c.customer_unique_id 
        FROM 
            orders o
        JOIN 
            customers c ON o.customer_id = c.customer_id
        WHERE 
            EXTRACT(YEAR FROM o.order_purchase_timestamp) IN (2016, 2017)
    );
"""

def run_query(query):
    # Execute the query and store the result in a DataFrame
    df = pd.read_sql_query(query, connection)
    return df


# Streamlit app structure
st.title('E-commerce Data Analysis')

# Run and display top products query
st.header('Top 10 Products by Popularity')
df_top_products = run_query(query_top_products)
st.dataframe(df_top_products)

# Run and display top customers query
st.header('Top 10 Customers by Spending')
df_top_customers = run_query(query_top_customers)
st.dataframe(df_top_customers)


# Run and display top sellers query
st.header('Top 10 Sellers by Revenue')
df_top_sellers = run_query(query_top_sellers)
st.dataframe(df_top_sellers)

# Run and display customer retention rate
st.header('Customer Retention Rate')
df_customer_retention_rate = run_query(query_customer_retention_rate)
st.dataframe(df_customer_retention_rate)


#MAURICIOS STUFF

#connection = mysql.connector.connect(user = 'root', password = 'password', host = '127.0.0.1', port = '3306', database = 'brazil_commerce_project')
#query_orders = "SELECT*FROM orders"
#df_orders = pd.read_sql_query(query_orders,connection)
#df_orders

##Here we shall make the necessary calculations in order to achieve the order completion rate

#order_status_count = df_orders['order_status'].value_counts()
#print (order_status_count)

#order_status_list = df_orders['order_status'].unique()
#print(order_status_list)

#order_status_count = df_orders['order_status'].value_counts()
#fig, ax = plt.subplots(1,1)
#order_status_count.plot(kind='bar', ax=ax)
#ax.set_title('Order Completion Rate')
#ax.set_xlabel('')
#ax.set_ylabel('Frequency')
#plt.show()

#query_orderpayments = "SELECT*FROM order_payments"
#df_orderpayments = pd.read_sql_query(query_orderpayments,connection)
#df_orderpayments

###Here are the different payment types used by the clients of the company
#order_payment_type = df_orderpayments['payment_type'].value_counts()
#print (order_payment_type)

##boleto --> bill or invoice that can be paid at banks and other places. Alternative to credit cards very popular in Brazil
## Here we shall create the graphs regarding the Payment Type

#payment_counts = df_orderpayments['payment_type'].value_counts()
#fig, ax = plt.subplots(1,1)
#payment_counts.plot(kind='bar', ax=ax)
#ax.set_title('Payment Type Frequencies')
#ax.set_xlabel('Payment Type')
#ax.set_ylabel('Frequency')
#plt.show()

#payment_counts = df_orderpayments['payment_type'].value_counts()
#payment_percentages = payment_counts / payment_counts.sum() * 100

#payment_percentages = payment_percentages.loc[['credit_card', 'boleto', 'voucher']]
#labels = [label if label in ['credit_card', 'boleto', 'voucher'] else '' for label in payment_percentages.index]

#fig, ax = plt.subplots(1,1)
#ax.pie(payment_percentages, labels=labels, autopct='%1.1f%%')
#ax.set_title('Payment Type Percentages')

#plt.show()