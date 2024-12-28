import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

# Load data
df = pd.read_excel('autobazaar_27K_csv.xlsx', engine='openpyxl')  # replace with your CSV file path

# Title for the app
st.title('Auto Bazaar Report')

# Convert 'invoice_date' to datetime format for easy filtering
df['invoice_date'] = pd.to_datetime(df['invoice_date'])

# Streamlit sidebar filters
st.sidebar.header('Filters')

# Filters for the dashboard
regions = df['customer_region'].unique().tolist()
regions.insert(0, 'All')  # Add 'All' option to the filter

cities = df['customer_city'].unique().tolist()
cities.insert(0, 'All')

invoice_codes = df['invoice_code'].unique().tolist()
invoice_codes.insert(0, 'All')

models = df['model'].unique().tolist()
models.insert(0, 'All')

names = df['name'].unique().tolist()
names.insert(0, 'All')

# Add a reset button to the sidebar
reset_button = st.sidebar.button('Reset Filters')

# Use session state to remember the state of the filters
if reset_button:
    st.session_state.selected_region = 'All'
    st.session_state.selected_city = 'All'
    st.session_state.selected_invoice_code = 'All'
    st.session_state.selected_model = 'All'
    st.session_state.selected_name = 'All'
    st.session_state.start_date = df['invoice_date'].min()
    st.session_state.end_date = df['invoice_date'].max()
else:
    # Set default values if session state does not exist
    if 'selected_region' not in st.session_state:
        st.session_state.selected_region = 'All'
    if 'selected_city' not in st.session_state:
        st.session_state.selected_city = 'All'
    if 'selected_invoice_code' not in st.session_state:
        st.session_state.selected_invoice_code = 'All'
    if 'selected_model' not in st.session_state:
        st.session_state.selected_model = 'All'
    if 'selected_name' not in st.session_state:
        st.session_state.selected_name = 'All'
    if 'start_date' not in st.session_state:
        st.session_state.start_date = df['invoice_date'].min()
    if 'end_date' not in st.session_state:
        st.session_state.end_date = df['invoice_date'].max()

# Create filters in sidebar
selected_region = st.sidebar.selectbox('Select Region', regions, index=regions.index(st.session_state.selected_region))
selected_city = st.sidebar.selectbox('Select City', cities, index=cities.index(st.session_state.selected_city))
selected_invoice_code = st.sidebar.selectbox('Select Invoice Code', invoice_codes, index=invoice_codes.index(st.session_state.selected_invoice_code))
selected_model = st.sidebar.selectbox('Select Model', models, index=models.index(st.session_state.selected_model))
selected_name = st.sidebar.selectbox('Select Name', names, index=names.index(st.session_state.selected_name))

# Date filter: Select Date range
start_date = st.sidebar.date_input('Start Date', st.session_state.start_date)
end_date = st.sidebar.date_input('End Date', st.session_state.end_date)

# Apply filters to dataframe
filtered_df = df.copy()

if selected_region != 'All':
    filtered_df = filtered_df[filtered_df['customer_region'] == selected_region]
if selected_city != 'All':
    filtered_df = filtered_df[filtered_df['customer_city'] == selected_city]
if selected_invoice_code != 'All':
    filtered_df = filtered_df[filtered_df['invoice_code'] == selected_invoice_code]
if selected_model != 'All':
    filtered_df = filtered_df[filtered_df['model'] == selected_model]
if selected_name != 'All':
    filtered_df = filtered_df[filtered_df['name'] == selected_name]
if start_date and end_date:
    filtered_df = filtered_df[(filtered_df['invoice_date'] >= pd.to_datetime(start_date)) & 
                              (filtered_df['invoice_date'] <= pd.to_datetime(end_date))]

# Update session state when filters change
st.session_state.selected_region = selected_region
st.session_state.selected_city = selected_city
st.session_state.selected_invoice_code = selected_invoice_code
st.session_state.selected_model = selected_model
st.session_state.selected_name = selected_name
st.session_state.start_date = start_date
st.session_state.end_date = end_date

# Display filtered data table
st.dataframe(filtered_df)

# Visualizations
# Bar chart for order quantity by region
st.subheader('Order Quantity by Region')
region_order_quantity = filtered_df.groupby('customer_region')['orderqtytotal'].sum().reset_index()
fig = px.bar(region_order_quantity, x='customer_region', y='orderqtytotal', title="Order Quantity by Region")
st.plotly_chart(fig)

# Line chart for total order amount over time
st.subheader('Total Order Amount Over Time')
total_order_amount = filtered_df.groupby('invoice_date')['orderamounttotal'].sum().reset_index()
fig = px.line(total_order_amount, x='invoice_date', y='orderamounttotal', title="Total Order Amount Over Time")
st.plotly_chart(fig)

# Insights Section (e.g., total orders, average order amount, etc.)
st.subheader('Insights')
total_orders = filtered_df['invoice_code'].nunique()
total_quantity = filtered_df['orderqtytotal'].sum()
total_amount = filtered_df['orderamounttotal'].sum()

st.write(f"Total Orders: {total_orders}")
st.write(f"Total Quantity Ordered: {total_quantity}")
st.write(f"Total Order Amount: {total_amount}")
st.write(f"Average Order Amount: {filtered_df['orderamounttotal'].mean()}")
