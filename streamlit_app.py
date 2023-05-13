# import streamlit as st
# import pandas as pd
# import seaborn as sns
# import matplotlib.pyplot as plt
# import mysql.connector
# from sqlalchemy import create_engine
# import datetime as dt
# from dateutil.relativedelta import relativedelta

# st.set_page_config(
#     page_title="Project Python!",
#     page_icon=":smiley:",
#     layout="wide",
# )
# #connection to mysql

# user = 'root'
# password = 'password'
# host = 'localhost'
# port = '3306'
# database = 'db'

# connection = mysql.connector.connect(user = 'root', password = 'password', host = 'localhost', port = '3306', database = 'db', use_pure = True)

# engine = create_engine(f'mysql://{user}:{password}@{host}:{port}/{database}')

# # # Define your SQL queries as strings

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

# # Reading SQL query into a DataFrame
# df = pd.read_sql_query(query_top_products, engine)

# # Display the query results with Streamlit
# st.write(df)

# # Close the connection
# connection.close()

# # Plotting with Seaborn
# plt.figure(figsize=(12,6))
# sns.barplot(y='product_category_name_english', x='order_count', data=df, orient='h', palette='viridis')
# plt.xlabel('Order Count')
# plt.ylabel('Product Category Name (English)')
# plt.title('Top 10 Most Popular Product Categories')
# plt.show()

# # Display the plot with Streamlit
# st.pyplot(plt)


# query_top_sellers = """
# SELECT 
#     	s.seller_id,
#     	SUM(oi.price) as total_revenue
# FROM 
#     	sellers s
# JOIN 
#     	order_items oi ON s.seller_id = oi.seller_id
# GROUP BY 
#     	s.seller_id
# ORDER BY 
#     	total_revenue DESC
# LIMIT 10;
# """


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

# query_top_sellers = """
# SELECT 
#     	s.seller_id,
#     	SUM(oi.price) as total_revenue
# FROM 
#     	sellers s
# JOIN 
#     	order_items oi ON s.seller_id = oi.seller_id
# GROUP BY 
#     	s.seller_id
# ORDER BY 
#     	total_revenue DESC
# LIMIT 10;
# """

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

# def run_query(query):
#     # Execute the query and store the result in a DataFrame
#     df = pd.read_sql_query(query, engine)
#     return df


# # Streamlit app structure
# st.title('E-commerce Data Analysis')

# # Run and display top products query
# st.header('Top 10 Products by Popularity')
# df_top_products = run_query(query_top_products)
# st.dataframe(df_top_products)

# # Run and display top customers query
# st.header('Top 10 Customers by Spending')
# df_top_customers = run_query(query_top_customers)
# st.dataframe(df_top_customers)


# # Run and display top sellers query
# st.header('Top 10 Sellers by Revenue')
# df_top_sellers = run_query(query_top_sellers)
# st.dataframe(df_top_sellers)

# # Run and display customer retention rate
# st.header('Customer Retention Rate')
# df_customer_retention_rate = run_query(query_customer_retention_rate)
# st.dataframe(df_customer_retention_rate)











# import pandas as pd
# import seaborn as sns
# import matplotlib.pyplot as plt
# import mysql.connector
# from sqlalchemy import create_engine
# import streamlit as st




import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import mysql.connector
from sqlalchemy import create_engine
import datetime as dt
from dateutil.relativedelta import relativedelta



# Connection settings
user = 'root'
password = 'password'
host = 'localhost'
port = '3306'
database = 'db'

# Connect to MySQL
connection = mysql.connector.connect(user=user, password=password, host=host, port=port, database=database, use_pure=True)
engine = create_engine(f'mysql://{user}:{password}@{host}:{port}/{database}')

# Define your queries


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
 # Reading SQL query into a DataFrame
df = pd.read_sql_query(query_top_products, engine)

# Display the query results with Streamlit
st.write(df)

# Close the connection
connection.close()

# Plotting with Seaborn
plt.figure(figsize=(12,6))
sns.barplot(y='product_category_name_english', x='order_count', data=df, orient='h', palette='viridis')
plt.xlabel('Order Count')
plt.ylabel('Product Category Name (English)')
plt.title('Top 10 Most Popular Product Categories')
plt.show()

# Display the plot with Streamlit
st.pyplot(plt)



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

# Reading SQL query into a DataFrame
df_top_sellers = pd.read_sql_query(query_top_sellers, engine)

# Display the query results with Streamlit
st.write(df)

# Close the connection
connection.close()

# Plotting
plt.figure(figsize=(10,6))
sns.barplot(x='total_revenue', y='seller_id', data=df_top_sellers, palette='viridis')
plt.xlabel('Total Revenue')
plt.ylabel('Seller ID')
plt.title('Top 10 Sellers by Revenue')
plt.show()

# Display the plot with Streamlit
st.pyplot(plt)

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

# Reading SQL query into a DataFrame
df_top_customers = pd.read_sql_query(query_top_customers, engine)


# Display the query results with Streamlit
st.write(df)

# Plotting
plt.figure(figsize=(10,6))
sns.barplot(x='total_spent', y='customer_id', data=df_top_customers, palette='viridis')
plt.xlabel('Total Spent')
plt.ylabel('Customer ID')
plt.title('Top 10 Customers by Spending')
plt.show()

# Display the plot with Streamlit
st.pyplot(plt)


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
# # Reading SQL query into a DataFrame
# df_customer_retention_rate = pd.read_sql_query(query_customer_retention_rate, engine)
# st.write(df_customer_retention_rate )
# # df_customer_retention_rate_long = df_customer_retention_rate.melt(var_name='Year', value_name='Retention Rate')

# # df_customer_retention_rate = df_customer_retention_rate.reset_index().melt(id_vars='index', var_name='Year', value_name='Retention Rate')
# # df_customer_retention_rate['Year'] = df_customer_retention_rate['Year'].str[-4:]  # to extract the year from column names



# # plt.figure(figsize=(10,6))
# # sns.barplot(x='year', y='customer_unique_id', data=df_customer_retention_rate, palette='viridis' )
# # plt.xlabel('Year')
# # plt.ylabel('Retention Rate')
# # plt.title('Customer Retention Rate by Year')
# # plt.show()


# # Display the plot with Streamlit
# st.pyplot(plt)









































































# Assuming these are the retention rates obtained from your SQL query
retention_rate_2017 = 15657.99257
retention_rate_2018 = 1.54084

# Constructing the DataFrame
data = {
    'Year': ['2017', '2018'],
    'Retention Rate': [retention_rate_2017, retention_rate_2018]
}

df = pd.DataFrame(data)

# Plotting
plt.figure(figsize=(10,6))
sns.barplot(x='Year', y='Retention Rate', data=df, palette='viridis')
plt.xlabel('Year')
plt.ylabel('Retention Rate (%)')
plt.title('Customer Retention Rate by Year')
plt.show()










# def run_query(query):
#     # Execute the query and store the result in a DataFrame
#     df = pd.read_sql_query(query, engine)
#     return df

# # Streamlit app structure
# st.title('E-commerce Data Analysis')

# # Run and display top products query
# st.header('Top 10 Products by Popularity')
# df_top_products = run_query(query_top_products)
# st.dataframe(df_top_products)

# # Plot the top 10 products
# sns.barplot(y='product_category_name_english', x='order_count', data=df_top_products, orient='h', palette='viridis')
# st.pyplot()

# # Run and display top customers query
# st.header('Top 10 Customers by Spending')
# df_top_customers = run_query(query_top_customers)
# st.dataframe(df_top_customers)

# # Plot the top 10 customers
# sns.barplot(y='customer_id', x='total_spent', data=df_top_customers, orient='h', palette='viridis')
# st.pyplot()

# # Run and display top sellers query
# st.header('Top 10 Sellers by Revenue')
# df_top_sellers = run_query(query_top_sellers)
# st.dataframe(df_top_sellers)

# # Plot the top 10 sellers
# sns.barplot(y='seller_id', x='total_revenue', data=df_top_sellers, orient='h', palette='viridis')
# st.pyplot()

# # Run and display customer retention rate
# st.header('Customer Retention Rate')
# df_customer_retention_rate = run_query(query_customer_retention_rate)
# st.dataframe(df_customer_retention_rate)

# # Plot the customer retention rate
# # Here you may need to adjust the code depending on how you would like to display this information

# # Close the connection
# connection.close()


