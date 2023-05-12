import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import mysql.connector
import datetime as dt
from dateutil.relativedelta import relativedelta

st.set_page_config(
    page_title="Project Python!",
    page_icon=":smiley:",
    layout="wide",
)
#connection to mysql

connection = mysql.connector.connect(user = 'root', password = 'password', host = '51.178.25.157', port = '3306', database = 'db', use_pure = True)