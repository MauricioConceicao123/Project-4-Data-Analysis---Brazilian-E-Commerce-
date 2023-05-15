import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import mysql.connector
from sqlalchemy import create_engine
import matplotlib.ticker as mticker
import datetime as dt
import numpy as np

st.set_page_config(layout="wide")

st.markdown("# Sales Analysis Dashboard")
st.markdown("An interactive dashboard for exploring sales data.")


# Connection settings
user = 'root'
password = 'password'
host = 'localhost'
port = '3306'
database = 'db'

connection = mysql.connector.connect(user=user, password=password, host=host, port=port, database=database, use_pure=True)
engine = create_engine(f'mysql://{user}:{password}@{host}:{port}/{database}')

# Choices for the dropdown menu
options = ["Top 10 Most Popular Product Categories", "Top 10 Sellers by Revenue", "Top 10 Customers by Spending", "Customer Retention Rate", "Order Completion Rate", "Payment Type"]

# dropdown menu in the sidebar
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
        ct.product_category_name_english, p.product_id
    ORDER BY 
        order_count DESC
    LIMIT 10;
    """
    df = pd.read_sql_query(query_top_products, engine)

    st.table(df.style.set_properties(subset=['product_category_name_english', 'product_id'], **{'width': '300px'}))

    # Bar chart for top products
    fig, ax = plt.subplots(1, 2, figsize=(18,6))
    sns.barplot(y='product_id', x='order_count', data=df,  palette='viridis', ax=ax[0])
    ax[0].set_xlabel('Order Count')
    ax[0].set_ylabel('Product ID')
    ax[0].set_title('Top 10 Most Popular Products')

    # Pie chart for top categories
    category_counts = df.groupby('product_category_name_english')['order_count'].sum().reset_index()
    category_counts.set_index('product_category_name_english', inplace=True)
    category_counts['order_count'].plot(kind='pie', autopct='%1.1f%%', startangle=140, ax=ax[1])
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

    df_customer_retention_rate = pd.read_sql_query(query_customer_retention_rate, engine)
    
    st.table(df_customer_retention_rate)

    sns.set(style="whitegrid")
    
    fig, axes = plt.subplots(1, 2, figsize=(16,6))  # 1 row, 2 columns

    sns.lineplot(x='year', y='unique_customers', data=df_customer_retention_rate, marker='o', ax=axes[0])

    axes[0].set_title('Customer Growth Over Time')
    axes[0].set_xlabel('Year')
    axes[0].set_ylabel('Unique Customers')

    sns.barplot(x='year', y='unique_customers', data=df_customer_retention_rate, ax=axes[1])

    axes[1].set_title('Customer Growth Over Time')
    axes[1].set_xlabel('Year')
    axes[1].set_ylabel('Unique Customers')

    st.pyplot(fig)
 
    #Mauricios Part
    

if choice == "Order Completion Rate":

    query_orders = "SELECT*FROM orders"
    df_orders = pd.read_sql_query(query_orders,connection)

    df_orders

    #Here we shall make the necessary calculations in order to achieve the order completion rate

    order_status_count = df_orders['order_status'].value_counts()
    # print (order_status_count)

    order_status_list = df_orders['order_status'].unique()
    # print(order_status_list)

    order_status_count = df_orders['order_status'].value_counts()
    fig, ax = plt.subplots(1,1)
    order_status_count.plot(kind='bar', ax=ax)
    ax.set_title('Order Completion Rate')
    ax.set_xlabel('')
    ax.set_ylabel('Frequency')
    st.pyplot(fig)
    # plt.show()
     
if choice == "Payment Type":
    query_orderpayments = "SELECT*FROM order_payments"
    df_orderpayments = pd.read_sql_query(query_orderpayments,connection)

    df_orderpayments

    #Here are the different payment types used by the clients of the company

    order_payment_type = df_orderpayments['payment_type'].value_counts()
    # print (order_payment_type)

    #boleto --> bill or invoice that can be paid at banks and other places. Alternative to credit cards very popular in Brazil
    # Here we shall create the graphs regarding the Payment Type

    payment_counts = df_orderpayments['payment_type'].value_counts()
    fig, ax = plt.subplots(1,1)
    payment_counts.plot(kind='bar', ax=ax)
    ax.set_title('Payment Type Frequencies')
    ax.set_xlabel('Payment Type')
    ax.set_ylabel('Frequency')
    st.pyplot(fig)
    # plt.show()



    payment_counts = df_orderpayments['payment_type'].value_counts()
    payment_percentages = payment_counts / payment_counts.sum() * 100

    payment_percentages = payment_percentages.loc[['credit_card', 'boleto', 'voucher']]
    labels = [label if label in ['credit_card', 'boleto', 'voucher'] else '' for label in payment_percentages.index]

    fig, ax = plt.subplots(1,1)
    ax.pie(payment_percentages, labels=labels, autopct='%1.1f%%')
    ax.set_title('Payment Type Percentages')
    st.pyplot(fig)
    # plt.show()

