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
        ct.product_category_name_english,
        COUNT(oi.order_id) as order_count
    FROM 
        products p
    JOIN 
        order_items oi ON p.product_id = oi.product_id
    JOIN
        Category_translation ct ON p.product_category_name = ct.product_category_name
    GROUP BY 
        ct.product_category_name_english
    ORDER BY 
        order_count DESC
    LIMIT 10;
    """
    df = pd.read_sql_query(query_top_products, engine)

    # Display the dataframe
    st.table(df.style.set_properties(subset=['product_category_name_english'], **{'width': '300px'}))

    # Bar chart
    fig, ax = plt.subplots(1, 2, figsize=(18,6))
    sns.barplot(y='product_category_name_english', x='order_count', data=df,  palette='viridis', ax=ax[0])
    ax[0].set_xlabel('Order Count')
    ax[0].set_ylabel('Product Category Name (English)')
    ax[0].set_title('Top 10 Most Popular Product Categories')

    # Pie chart
    df.set_index('product_category_name_english', inplace=True)
    df['order_count'].plot(kind='pie', autopct='%1.1f%%', startangle=140, ax=ax[1])
    ax[1].set_ylabel('')  # This removes 'order_count' from the y-axis
    ax[1].set_title('Sales Distribution Across Top 10 Categories')

    st.pyplot(fig)
    plt.clf()



# if choice == "Top 10 Most Popular Product Categories":
#     query_top_products = """
#     SELECT 
#         p.product_id, 
#         ct.product_category_name_english,
#         COUNT(oi.order_id) as order_count
#     FROM 
#         products p
#     JOIN 
#         order_items oi ON p.product_id = oi.product_id
#     JOIN
#         Category_translation ct ON p.product_category_name = ct.product_category_name
#     GROUP BY 
#         p.product_id, ct.product_category_name_english
#     ORDER BY 
#         order_count DESC
#     LIMIT 10;
#     """
#     df_top_products = pd.read_sql_query(query_top_products, engine)
#     st.table(df_top_products)
#     fig, ax = plt.subplots(figsize=(12,6))
#     sns.barplot(y='product_category_name_english', x='order_count', data=df_top_products,  palette='viridis')
#     plt.xlabel('Order Count')
#     plt.ylabel('Product Category Name (English)')
#     plt.title('Top 10 Most Popular Product Categories')
#     st.pyplot(fig)
#     plt.clf()

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
        )   AS retention_rate_2017,
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


    # Use pandas to execute the SQL query and store the result in a DataFrame
    df_customer_retention_rate = pd.read_sql_query(query_customer_retention_rate, engine)

    # Reshape the dataframe
    df_customer_retention_rate = df_customer_retention_rate.melt(var_name='Year', value_name='Retention Rate')

    # Replace the column names with actual year values
    df_customer_retention_rate['Year'] = df_customer_retention_rate['Year'].replace({'retention_rate_2017': '2017', 'retention_rate_2018': '2018'})

    # Convert 'Year' column to string
    df_customer_retention_rate['Year'] = df_customer_retention_rate['Year'].astype(str)

    # Display the query results with Streamlit
    st.table(df_customer_retention_rate)

    # Plotting with Seaborn
    fig, ax = plt.subplots(figsize=(12,6))
    sns.barplot(x='Year', y='Retention Rate', data=df_customer_retention_rate,  palette='viridis', ax=ax)
    ax.set_xlabel('Year')
    ax.set_ylabel('Retention Rate (%)')
    ax.set_title('Customer Retention Rate')
    ax.set_yscale('log')
    # format y-axis
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda y, _: '{:.2%}'.format(y)))
    # Display the plot with Streamlit
    st.pyplot(fig)
    plt.clf()


