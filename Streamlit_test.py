import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import mysql.connector
from sqlalchemy import create_engine
import matplotlib.ticker as mticker
import datetime as dt

st.markdown("# Sales Analysis Dashboard")
st.markdown("An interactive dashboard for exploring sales data.")


# Connection settings
user = 'root'
password = 'password'
host = 'localhost'
port = '3306'
database = 'db'

# Connect to MySQL
connection = mysql.connector.connect(user=user, password=password, host=host, port=port, database=database, use_pure=True)
engine = create_engine(f'mysql://{user}:{password}@{host}:{port}/{database}')

# Choices for the dropdown menu
options = ["Top 10 Most Popular Product Categories", "Top 10 Sellers by Revenue", "Top 10 Customers by Spending", "Customer Retention Rate"]

# Create the dropdown menu in the sidebar
st.sidebar.markdown("## Instructions")
st.sidebar.markdown("Please select an analysis from the dropdown menu.")
choice = st.sidebar.selectbox("", options)


if choice == "Top 10 Most Popular Product Categories":
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
    df_top_products = pd.read_sql_query(query_top_products, engine)
    
    # Display the dataframe
    st.table(df_top_products.style.set_properties(subset=['product_category_name_english'], **{'width': '300px'}))

    # Bar chart
    fig, ax = plt.subplots(1, 2, figsize=(18,6))
    sns.barplot(y='product_category_name_english', x='order_count', data=df_top_products,  palette='viridis', ax=ax[0])
    ax[0].set_xlabel('Order Count')
    ax[0].set_ylabel('Product Category Name (English)')
    ax[0].set_title('Top 10 Most Popular Product Categories')

    # Pie chart
    df_top_products.set_index('product_category_name_english', inplace=True)
    df_top_products['order_count'].plot(kind='pie', autopct='%1.1f%%', startangle=140, ax=ax[1])
    ax[1].set_ylabel('')  # This removes 'order_count' from the y-axis
    ax[1].set_title('Sales Distribution Across Top 10 Categories')

    st.pyplot(fig)
    plt.clf()

    

elif choice == "Top 10 Sellers by Revenue":
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
    df_top_sellers = pd.read_sql_query(query_top_sellers, engine)
    st.table(df_top_sellers)
    fig, ax = plt.subplots(figsize=(12,6))
    sns.barplot(x='total_revenue', y='seller_id', data=df_top_sellers, palette='viridis')
    plt.xlabel('Total Revenue')
    plt.ylabel('Seller ID')
    plt.title('Top 10 Sellers by Revenue')
    st.pyplot(fig)
    plt.clf()

elif choice == "Top 10 Customers by Spending":
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
    df_top_customers = pd.read_sql_query(query_top_customers, engine)
    st.table(df_top_customers)
    fig, ax = plt.subplots(figsize=(12,6))
    sns.barplot(x='total_spent', y='customer_id', data=df_top_customers, palette='viridis')
    plt.xlabel('Total Spent')
    plt.ylabel('Customer ID')
    plt.title('Top 10 Customers by Spending')
    st.pyplot(fig)
    
   
   
 


elif choice == "Customer Retention Rate":    
    query_customer_retention_rate = """
    SELECT 
        EXTRACT(YEAR FROM o.order_purchase_timestamp) AS year,
        COUNT(DISTINCT c.customer_unique_id) AS unique_customers
    FROM 
        orders o
    JOIN 
        customers c ON o.customer_id = c.customer_id
    WHERE 
        EXTRACT(YEAR FROM o.order_purchase_timestamp) BETWEEN 2016 AND 2018
    GROUP BY 
        year
    ORDER BY 
        year; 
    """

    # Fetch data from database
    df_customer_retention_rate = pd.read_sql_query(query_customer_retention_rate, engine)
    
    
    # Display the query results with Streamlit
    st.table(df_customer_retention_rate)
    
    # Set the plot style and size
    sns.set(style="whitegrid")
    fig, axes = plt.subplots(1, 2, figsize=(16,6))  # 1 row, 2 columns

    # Create the line plot using Seaborn
    sns.lineplot(x='year', y='unique_customers', data=df_customer_retention_rate, marker='o', ax=axes[0])

    # Set the title and labels for line plot
    axes[0].set_title('Customer Growth Over Time')
    axes[0].set_xlabel('Year')
    axes[0].set_ylabel('Unique Customers')

    # Create the bar plot using Seaborn
    sns.barplot(x='year', y='unique_customers', data=df_customer_retention_rate, ax=axes[1])

    # Set the title and labels for bar plot
    axes[1].set_title('Customer Growth Over Time')
    axes[1].set_xlabel('Year')
    axes[1].set_ylabel('Unique Customers')

    # Display the plot with Streamlit
    st.pyplot(fig)
    # plt.show()












