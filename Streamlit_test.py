import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import mysql.connector
from sqlalchemy import create_engine
import matplotlib.ticker as mticker
import datetime as dt

# Connection settings
user = 'root'
password = 'password'
host = 'localhost'
port = '3306'
database = 'db'

# Connect to MySQL
connection = mysql.connector.connect(user=user, password=password, host=host, port=port, database=database, use_pure=True)
engine = create_engine(f'mysql://{user}:{password}@{host}:{port}/{database}')

st.title("Ecommerce Dashboard")

# Define your queries

# Query for retention rate
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
# Execute the SQL query and store the result in a DataFrame
df_customer_retention_rate = pd.read_sql_query(query_customer_retention_rate, engine)


# Reshape the dataframe
df_customer_retention_rate = df_customer_retention_rate.melt(var_name='Year', value_name='Retention Rate')

# Replace the column names with actual year values
df_customer_retention_rate['Year'] = df_customer_retention_rate['Year'].replace({'retention_rate_2017': '2017', 'retention_rate_2018': '2018'})

# Convert 'Year' column to integer
df_customer_retention_rate['Year'] = df_customer_retention_rate['Year'].astype(int)

# Display the query results with Streamlit
st.write(df_customer_retention_rate)

# Plotting retention rate with Seaborn
fig, ax = plt.subplots(figsize=(12,6))
sns.lineplot(x='Year', y='Retention Rate', data=df_customer_retention_rate,  palette='viridis', ax=ax)
ax.set_xlabel('Year')
ax.set_ylabel('Retention Rate (%)')
ax.set_title('Customer Retention Rate Over Years')
st.pyplot(fig)

# Query for sellers
query_sellers = """
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
df_sellers = pd.read_sql_query(query_sellers, engine)

# Plotting sellers with Seaborn
fig, ax = plt.subplots(figsize=(12,6))
sns.histplot(df_sellers['total_revenue'], bins=30, color='green', ax=ax)
ax.set_xlabel('Total Revenue')
ax.set_title('Distribution of Sellers Revenue')
st.pyplot(fig)

# Query for customers
query_customers = """
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
df_customers = pd.read_sql_query(query_customers, engine)

# Plotting customers with Seaborn
fig, ax = plt.subplots(figsize=(12,6))
sns.histplot(df_customers['total_spent'], bins=30, color='blue', ax=ax)
ax.set_xlabel('Total Spent')
ax.set_title('Distribution of Customers Spending')
st.pyplot(fig)

# Query for orders by product category and month
query_orders = """
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
df_orders = pd.read_sql_query(query_orders, engine)

# Create pivot table for the heatmap
pivot = df_orders.pivot_table(index='product_category_name_english', columns='order_purchase_month', values='order_count', fill_value=0)

# Plotting heatmap with Seaborn
fig, ax = plt.subplots(figsize=(12,6))
sns.heatmap(pivot, cmap='viridis', ax=ax)
ax.set_xlabel('Order Purchase Month')
ax.set_ylabel('Product Category Name (English)')
ax.set_title('Number of Orders by Product Category and Month')
st.pyplot(fig)










































# import streamlit as st
# import pandas as pd
# import seaborn as sns
# import matplotlib.pyplot as plt
# import mysql.connector
# from sqlalchemy import create_engine
# import matplotlib.ticker as mticker
# import datetime as dt


# # Connection settings
# user = 'root'
# password = 'password'
# host = 'localhost'
# port = '3306'
# database = 'db'

# # Connect to MySQL
# connection = mysql.connector.connect(user=user, password=password, host=host, port=port, database=database, use_pure=True)
# engine = create_engine(f'mysql://{user}:{password}@{host}:{port}/{database}')

# # Define your queries

# query_top_products = """
# SELECT 
#     p.product_id, 
#     ct.product_category_name_english,
#     COUNT(oi.order_id) as order_count
# FROM 
#     products p
# JOIN 
#     order_items oi ON p.product_id = oi.product_id
# JOIN
#     Category_translation ct ON p.product_category_name = ct.product_category_name
# GROUP BY 
#     p.product_id, ct.product_category_name_english
# ORDER BY 
#     order_count DESC
# LIMIT 10;
# """
#  # Reading SQL query into a DataFrame
# df = pd.read_sql_query(query_top_products, engine)

# # Display the query results with Streamlit
# st.write(df)

# # Plotting with Seaborn
# fig, ax = plt.subplots(figsize=(12,6))
# sns.barplot(y='product_category_name_english', x='order_count', data=df,  palette='viridis')
# plt.xlabel('Order Count')
# plt.ylabel('Product Category Name (English)')
# plt.title('Top 10 Most Popular Product Categories')
# # plt.show()

# # Display the plot with Streamlit
# st.pyplot(fig)


# query_top_sellers = """
# SELECT 
#     s.seller_id,
#     SUM(oi.price) as total_revenue
# FROM 
#     sellers s
# JOIN 
#     order_items oi ON s.seller_id = oi.seller_id
# GROUP BY 
#     s.seller_id
# ORDER BY 
#     total_revenue DESC
# LIMIT 10;
# """

# # Reading SQL query into a DataFrame
# df_top_sellers = pd.read_sql_query(query_top_sellers, engine)

# # Display the query results with Streamlit
# st.write(df)

# # Plotting
# fig, ax = plt.subplots(figsize=(12,6))
# sns.barplot(x='total_revenue', y='seller_id', data=df_top_sellers, palette='viridis')
# plt.xlabel('Total Revenue')
# plt.ylabel('Seller ID')
# plt.title('Top 10 Sellers by Revenue')
# # plt.show()

# # Display the plot with Streamlit
# st.pyplot(fig)


# query_top_customers = """
# SELECT 
#     o.customer_id, 
#     SUM(oi.price) as total_spent
# FROM 
#     orders o
# JOIN 
#     order_items oi ON o.order_id = oi.order_id
# GROUP BY 
#     o.customer_id
# ORDER BY 
#     total_spent DESC
# LIMIT 10;
# """

# # Reading SQL query into a DataFrame
# df_top_customers = pd.read_sql_query(query_top_customers, engine)


# # Display the query results with Streamlit
# st.write(df_top_customers)

# # Plotting
# fig, ax = plt.subplots(figsize=(12,6))
# # plt.figure(figsize=(10,6))
# sns.barplot(x='total_spent', y='customer_id', data=df_top_customers, palette='viridis')
# plt.xlabel('Total Spent')
# plt.ylabel('Customer ID')
# plt.title('Top 10 Customers by Spending')
# # plt.show()

# # Display the plot with Streamlit
# st.pyplot(fig)


# query_customer_retention_rate = """
# SELECT 
#     COUNT(DISTINCT CASE WHEN EXTRACT(YEAR FROM o.order_purchase_timestamp) = 2017 THEN c.customer_unique_id END) * 100.0 / 
#     (
#         SELECT 
#             COUNT(DISTINCT c.customer_unique_id)
#         FROM 
#             orders o
#         JOIN 
#             customers c ON o.customer_id = c.customer_id
#         WHERE 
#             EXTRACT(YEAR FROM o.order_purchase_timestamp) = 2016
#     ) AS retention_rate_2017,
#     COUNT(DISTINCT CASE WHEN EXTRACT(YEAR FROM o.order_purchase_timestamp) = 2018 THEN c.customer_unique_id END) * 100.0 / 
#     (
#         SELECT 
#             COUNT(DISTINCT c.customer_unique_id)
#         FROM 
#             orders o
#         JOIN 
#             customers c ON o.customer_id = c.customer_id
#         WHERE 
#             EXTRACT(YEAR FROM o.order_purchase_timestamp) = 2017
#     ) AS retention_rate_2018
# FROM 
#     orders o
# JOIN 
#     customers c ON o.customer_id = c.customer_id
# WHERE 
#     EXTRACT(YEAR FROM o.order_purchase_timestamp) IN (2017, 2018) AND 
#     c.customer_unique_id IN (
#         SELECT 
#             c.customer_unique_id 
#         FROM 
#             orders o
#         JOIN 
#             customers c ON o.customer_id = c.customer_id
#         WHERE 
#             EXTRACT(YEAR FROM o.order_purchase_timestamp) IN (2016, 2017)
#     );
# """


# # Use pandas to execute the SQL query and store the result in a DataFrame
# df_customer_retention_rate = pd.read_sql_query(query_customer_retention_rate, engine)

# # Reshape the dataframe
# df_customer_retention_rate = df_customer_retention_rate.melt(var_name='Year', value_name='Retention Rate')

# # Replace the column names with actual year values
# df_customer_retention_rate['Year'] = df_customer_retention_rate['Year'].replace({'retention_rate_2017': '2017', 'retention_rate_2018': '2018'})

# # Convert 'Year' column to integer
# df_customer_retention_rate['Year'] = df_customer_retention_rate['Year'].astype(int)

# # Display the query results with Streamlit
# st.write(df_customer_retention_rate)

# # Plotting with Seaborn
# fig, ax = plt.subplots(figsize=(12,6))
# sns.barplot(x='Year', y='Retention Rate', data=df_customer_retention_rate,  palette='viridis', ax=ax)
# ax.set_xlabel('Year')
# ax.set_ylabel('Retention Rate (%)')
# ax.set_title('Customer Retention Rate')
# ax.set_yscale('log')

# # format y-axis
# ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda y, _: '{:.2%}'.format(y)))

# # Display the plot with Streamlit
# st.pyplot(fig)