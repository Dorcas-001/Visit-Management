import streamlit as st
import matplotlib.colors as mcolors
import plotly.express as px
import pandas as pd
import altair as alt
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from itertools import chain
from matplotlib.ticker import FuncFormatter
from datetime import datetime


# Centered and styled main title using inline styles
st.markdown('''
    <style>
        .main-title {
            color: #e66c37; /* Title color */
            text-align: center; /* Center align the title */
            font-size: 3rem; /* Title font size */
            font-weight: bold; /* Title font weight */
            margin-bottom: .5rem; /* Space below the title */
            text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.1); /* Subtle text shadow */
        }
        div.block-container {
            padding-top: 2rem; /* Padding for main content */
        }
    </style>
''', unsafe_allow_html=True)

st.markdown('<h1 class="main-title">VISIT DETAILS VIEW</h1>', unsafe_allow_html=True)


filepath_visits = "Visit Data 2024.xlsx"

sheet_name1 = "2023"
sheet_name2 = "2024"

# Read the VISIT data
df_2023 = pd.read_excel(filepath_visits, sheet_name=sheet_name1)
df_2024 = pd.read_excel(filepath_visits, sheet_name=sheet_name2)

# Read the visit logs
df = pd.concat([df_2023, df_2024])
# Ensure Visit Date is in datetime format
df['Visit Date'] = pd.to_datetime(df['Visit Date'])



# Inspect the merged DataFrame

# Sidebar styling and logo
st.markdown("""
    <style>
    .sidebar .sidebar-content {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }
    .sidebar .sidebar-content h2 {
        color: #007BFF; /* Change this color to your preferred title color */
        font-size: 1.5em;
        margin-bottom: 20px;
        text-align: center;
    }
    .sidebar .sidebar-content .filter-title {
        color: #e66c37;
        font-size: 1.2em;
        font-weight: bold;
        margin-top: 20px;
        margin-bottom: 10px;
        text-align: center;
    }
    .sidebar .sidebar-content .filter-header {
        color: #e66c37; /* Change this color to your preferred header color */
        font-size: 2.5em;
        font-weight: bold;
        margin-top: 20px;
        margin-bottom: 20px;
        text-align: center;
    }
    .sidebar .sidebar-content .filter-multiselect {
        margin-bottom: 15px;
    }
    .sidebar .sidebar-content .logo {
        text-align: center;
        margin-bottom: 20px;
    }
    .sidebar .sidebar-content .logo img {
        max-width: 80%;
        height: auto;
        border-radius: 50%;
    }
            
    </style>
    """, unsafe_allow_html=True)


df["Client Name"] = df["Client Name"].str.upper()



# Dictionary to map month names to their order
month_order = {
    "January": 1, "February": 2, "March": 3, "April": 4, 
    "May": 5, "June": 6, "July": 7, "August": 8, 
    "September": 9, "October": 10, "November": 11, "December": 12
}

# Sort months based on their order
sorted_months = sorted(df['Month'].dropna().unique(), key=lambda x: month_order[x])
df['Quarter'] = "Q" + df['Visit Date'].dt.quarter.astype(str)


# Sidebar for filters
st.sidebar.header("Filters")
year = st.sidebar.multiselect("Select Year", options=sorted(df['Year'].dropna().unique()))
quarter = st.sidebar.multiselect("Select Quarter", options=sorted(df['Quarter'].dropna().unique()))
month = st.sidebar.multiselect("Select Month", options=sorted_months)
type = st.sidebar.multiselect("Select Visit Type", options=df['Visit Type'].unique())
status = st.sidebar.multiselect("Select Visit Status", options=df['Visit Status'].unique())
client_name = st.sidebar.multiselect("Select Client Name", options=sorted(df['Client Name'].dropna().unique()))
prov_name = st.sidebar.multiselect("Select Provider Name", options=sorted(df['Provider Name'].dropna().unique()))


# Apply filters to the DataFrame
if 'Year' in df.columns and year:
    df = df[df['Year'].isin(year)]
if 'Month' in df.columns and month:
    df = df[df['Month'].isin(month)]
if 'Quarter' in df.columns and quarter:
    df = df[df['Quarter'].isin(quarter)]
if 'Visit Type' in df.columns and type:
    df = df[df['Visit Type'].isin(type)]
if 'Visit Status' in df.columns and status:
    df = df[df['Visit Status'].isin(status)]
if 'Client Name' in df.columns and client_name:
    df = df[df['Client Name'].isin(client_name)]
if 'Provider Name' in df.columns and prov_name:
    df = df[df['Provider Name'].isin(prov_name)]

# Determine the filter description
filter_description = ""
if year:
    filter_description += f"{', '.join(map(str, year))} "
# if cover:
#     filter_description += f"{', '.join(map(str, cover))} "
if month:
    filter_description += f"{', '.join(month)} "
if not filter_description:
    filter_description = "All data"



# Get minimum and maximum dates for the date input
startDate = df["Visit Date"].min()
endDate = df["Visit Date"].max()

# Define CSS for the styled date input boxes
st.markdown("""
    <style>
    .date-input-box {
        border-radius: 10px;
        text-align: left;
        margin: 5px;
        font-size: 1.2em;
        font-weight: bold;
    }
    .date-input-title {
        font-size: 1.2em;
        margin-bottom: 5px;
    }
    </style>
    """, unsafe_allow_html=True)


# Create 2-column layout for date inputs
col1, col2 = st.columns(2)


# Function to display date input in styled boxes
def display_date_input(col, title, default_date, min_date, max_date):
    col.markdown(f"""
        <div class="date-input-box">
            <div class="date-input-title">{title}</div>
        </div>
        """, unsafe_allow_html=True)
    return col.date_input("", default_date, min_value=min_date, max_value=max_date)

# Display date inputs
with col1:
    date1 = pd.to_datetime(display_date_input(col1, "Visit Date", startDate, startDate, endDate))

with col2:
    date2 = pd.to_datetime(display_date_input(col2, "Visit Date", endDate, startDate, endDate))



# Handle non-finite values in 'Start Year' column
df['Year'] = df['Year'].fillna(0).astype(int)  # Replace NaN with 0 or any specific value

# Handle non-finite values in 'Start Month' column
df['Month'] = df['Month'].fillna('Unknown')

# Create a 'Month-Year' column
df['Month-Year'] = df['Month'] + ' ' + df['Year'].astype(str)

# Function to sort month-year combinations
def sort_key(month_year):
    month, year = month_year.split()
    return (int(year), month_order.get(month, 0))  # Use .get() to handle 'Unknown' month

# Extract unique month-year combinations and sort them
month_years = sorted(df['Month-Year'].unique(), key=sort_key)

# Select slider for month-year range
selected_month_year_range = st.select_slider(
    "Select Month-Year Range",
    options=month_years,
    value=(month_years[0], month_years[-1])
)

# Filter DataFrame based on selected month-year range
start_month_year, end_month_year = selected_month_year_range
start_month, start_year = start_month_year.split()
end_month, end_year = end_month_year.split()

start_index = (int(start_year), month_order.get(start_month, 0))
end_index = (int(end_year), month_order.get(end_month, 0))

# Filter DataFrame based on month-year order indices
df = df[
    df['Month-Year'].apply(lambda x: (int(x.split()[1]), month_order.get(x.split()[0], 0))).between(start_index, end_index)
]



df_close = df[df['Visit Status'] == 'Close']
df_open = df[df['Visit Status'] == 'Open']

if not df.empty:

    scale=1_000_000  # For millions

    total_amount = (df["Total Amount"].sum())/scale
    average_amount =(df["Total Amount"].mean())/scale


    total_closed = (df_close["Total Amount"].sum())/scale
    total_open = (df_open["Total Amount"].sum())/scale



    total_clients = df["Client Name"].nunique()
    total_visits = df["Visit ID"].nunique()

    total_close = df_close["Visit ID"].nunique()
    total_ope = df_open["Visit ID"].nunique()
    total_closed_per = (total_close/total_visits)*100
    total_open_per = (total_ope/total_visits)*100








    # Create 4-column layout for metric cards# Define CSS for the styled boxes and tooltips
    st.markdown("""
        <style>
        .custom-subheader {
            color: #e66c37;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
            padding: 10px;
            border-radius: 5px;
            display: inline-block;
        }
        .metric-box {
            padding: 10px;
            border-radius: 10px;
            text-align: center;
            margin: 10px;
            font-size: 1.2em;
            font-weight: bold;
            box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
            border: 1px solid #ddd;
            position: relative;
        }
        .metric-title {
            color: #e66c37; /* Change this color to your preferred title color */
            font-size: 0.9em;
            margin-bottom: 10px;
        }
        .metric-value {
            color: #009DAE;
            font-size: 1em;
        }

        </style>
        """, unsafe_allow_html=True)



    # Function to display metrics in styled boxes with tooltips
    def display_metric(col, title, value):
        col.markdown(f"""
            <div class="metric-box">
                <div class="metric-title">{title}</div>
                <div class="metric-value">{value}</div>
            </div>
            """, unsafe_allow_html=True)




    # Calculate key metrics
    st.markdown('<h2 class="custom-subheader">For all Sales</h2>', unsafe_allow_html=True)    

    cols1,cols2, cols3 = st.columns(3)

    display_metric(cols1, "Total Clients", total_clients)
    display_metric(cols2, "Total Expected Claims", total_visits)
    display_metric(cols3, "Total Expected Claim Amount", F"{total_amount:,.0F} M")
    display_metric(cols1, "Average Expected Claim Amount Per Client", F"{average_amount:,.1F} M")
    display_metric(cols2, "Percentage Closed Visit", F"{total_closed_per:,.0F} %")
    display_metric(cols3, "Percentage Open Visit", F"{total_open_per:,.0F} %")


    # Assuming 'df' is your DataFrame and 'custom_colors' is defined somewhere in your code
    custom_colors = ["#009DAE", "#e66c37", "#461b09", "#f8a785", "#CC3636"]

    # Group by day and count the occurrences
    area_chart_count = df.groupby(df["Visit Date"].dt.strftime("%Y-%m-%d")).size().reset_index(name='Count')
    area_chart_amount = df.groupby(df["Visit Date"].dt.strftime("%Y-%m-%d"))['Total Amount'].sum().reset_index(name='Total Amount')

    # Sort by the Visit Date
    area_chart_count = area_chart_count.sort_values("Visit Date")
    area_chart_amount = area_chart_amount.sort_values("Visit Date")

    # Create the first chart for the number of visits
    fig1 = go.Figure()
    fig1.add_trace(
        go.Scatter(x=area_chart_count['Visit Date'], y=area_chart_count['Count'], name="Number of Visits", fill='tozeroy', line=dict(color='#e66c37'))
    )

    # Set x-axis and y-axis titles for the first chart
    fig1.update_xaxes(title_text="Visit Date", tickangle=45)  # Rotate x-axis labels to 45 degrees for better readability
    fig1.update_yaxes(title_text="<b>Number Of Visits</b>")

    # Create the second chart for the total amount
    fig2 = go.Figure()
    fig2.add_trace(
        go.Scatter(x=area_chart_amount['Visit Date'], y=area_chart_amount['Total Amount'], name="Total Visit Amount", fill='tozeroy', line=dict(color='#009DAE'))
    )

    # Set x-axis and y-axis titles for the second chart
    fig2.update_xaxes(title_text="Visit Date", tickangle=45)  # Rotate x-axis labels to 45 degrees for better readability
    fig2.update_yaxes(title_text="<b>Total Visit Amount</b>")

    # Create two columns
    col1, col2 = st.columns(2)

    # Display the first chart in the first column
    with col1:
        st.markdown('<h3 class="custom-subheader">Number of Visits Over Time</h3>', unsafe_allow_html=True)
        st.plotly_chart(fig1, use_container_width=True)

    # Display the second chart in the second column
    with col2:
        st.markdown('<h3 class="custom-subheader">Total Visit Amount Over Time</h3>', unsafe_allow_html=True)
        st.plotly_chart(fig2, use_container_width=True)


    cols1, cols2 = st.columns(2)

    # Group data by year
    yearly_visits = df.groupby('Year').size().reset_index(name='Number of Visits')
    yearly_amount = df.groupby('Year')['Total Amount'].sum().reset_index(name='Total Amount')

    # Merge yearly data for combined visualization
    yearly_data = pd.merge(yearly_visits, yearly_amount, on='Year')

    # Create a grouped bar chart for yearly visits and total amount
    fig_yearly = go.Figure()

    # First y-axis (Number of Visits)
    fig_yearly.add_trace(go.Bar(
        x=yearly_data['Year'],
        y=yearly_data['Number of Visits'],
        name='Number of Visits',
        marker_color='#e66c37',
        yaxis='y1'
    ))

    # Second y-axis (Total Visit Amount)
    fig_yearly.add_trace(go.Bar(
        x=yearly_data['Year'],
        y=yearly_data['Total Amount'],
        name='Total Visit Amount',
        marker_color='#009DAE',
        yaxis='y2'
    ))

    fig_yearly.update_layout(
        xaxis=dict(title="Year", tickmode='linear'),
        yaxis=dict(title="Number of Visits", side='left'),
        yaxis2=dict(title="Total Visit Amount", overlaying='y', side='right', showgrid=False),
        barmode='stack',
        margin=dict(l=0, r=0, t=30, b=50),
        height=450
    )

    # Display the chart in Streamlit
    with cols1:
        st.markdown('<h3 class="custom-subheader">Yearly Visits & Total Amount</h3>', unsafe_allow_html=True)
        st.plotly_chart(fig_yearly, use_container_width=True)

    # Group data by month
    monthly_visits = df.groupby('Month').size().reset_index(name='Number of Visits')
    monthly_amount = df.groupby('Month')['Total Amount'].sum().reset_index(name='Total Amount')

    # Merge monthly data for combined visualization
    monthly_data = pd.merge(monthly_visits, monthly_amount, on='Month')

    # Create a dual-axis bar chart for monthly visits and total amount
    fig_monthly = go.Figure()

    # First y-axis (Number of Visits)
    fig_monthly.add_trace(go.Bar(
        x=monthly_data['Month'],
        y=monthly_data['Number of Visits'],
        name='Number of Visits',
        marker_color='#e66c37',
        yaxis='y1'
    ))

    # Second y-axis (Total Visit Amount)
    fig_monthly.add_trace(go.Bar(
        x=monthly_data['Month'],
        y=monthly_data['Total Amount'],
        name='Total Visit Amount',
        marker_color='#009DAE',
        yaxis='y2'
    ))

    fig_monthly.update_layout(
        xaxis=dict(title="Month", tickangle=45),
        yaxis=dict(title="Number of Visits", side='left'),
        yaxis2=dict(title="Total Visit Amount", overlaying='y', side='right', showgrid=False),
        barmode='group',
        margin=dict(l=0, r=0, t=30, b=50),
        height=450
    )

    # Group data by hour for visits
    hourly_visits = df.groupby('Hour').size().reset_index(name='Number of Visits')

    # Create bar chart for hourly visits
    fig_hourly = go.Figure()

    fig_hourly.add_trace(go.Bar(
        x=hourly_visits['Hour'],
        y=hourly_visits['Number of Visits'],
        name='Number of Visits',
        marker_color='#e66c37'
    ))

    fig_hourly.update_layout(
        xaxis=dict(title="Hour of the Day", tickmode='linear'),
        yaxis=dict(title="Number of Visits"),
        margin=dict(l=0, r=0, t=30, b=50),
        height=450
    )

    # Create Streamlit layout with two columns
    col1, col2 = st.columns(2)

    # Display Monthly Chart
    with cols2:
        st.markdown('<h3 class="custom-subheader">Monthly Visits & Total Amount</h3>', unsafe_allow_html=True)
        st.plotly_chart(fig_monthly, use_container_width=True)

    # Display Hourly Chart
    with col1:
        st.markdown('<h3 class="custom-subheader">Hourly Visits</h3>', unsafe_allow_html=True)
        st.plotly_chart(fig_hourly, use_container_width=True)

# Calculate the Total Amount by Client Segment
    int_owner = df.groupby("Visit Status")["Total Amount"].sum().reset_index()
    int_owner.columns = ["Visit Status", "Total Amount"]    

    with col2:
        # Display the header
        st.markdown('<h3 class="custom-subheader">Total Expected Claim Amount by Visit Status</h3>', unsafe_allow_html=True)


        # Create a donut chart
        fig = px.pie(int_owner, names="Visit Status", values="Total Amount", hole=0.5, template="plotly_dark", color_discrete_sequence=custom_colors)
        fig.update_traces(textposition='inside', textinfo='value+percent')
        fig.update_layout(height=450, margin=dict(l=0, r=10, t=30, b=50))

        # Display the chart in Streamlit
        st.plotly_chart(fig, use_container_width=True)


    # Create the layout columns
    cls1, cls2 = st.columns(2)

    # Group by Provider Name to get Total Amount and Number of Visits
    df_grouped_provider = df.groupby('Provider Name').agg(
        {'Total Amount': 'sum', 'Visit Date': 'count'}  # Count visits
    ).nlargest(15, 'Total Amount').reset_index()

    # Sort by Total Amount in descending order
    df_grouped_provider = df_grouped_provider.sort_values(by='Total Amount', ascending=False)

    with cls2:
        # Create dual-axis chart for Providers
        fig_provider = go.Figure()

        # First y-axis (Number of Visits)
        fig_provider.add_trace(go.Bar(
            x=df_grouped_provider['Provider Name'],
            y=df_grouped_provider['Visit Date'],
            name='Number of Visits',
            marker_color='#e66c37',
            yaxis='y1'
        ))

        # Second y-axis (Total Amount)
        fig_provider.add_trace(go.Bar(
            x=df_grouped_provider['Provider Name'],
            y=df_grouped_provider['Total Amount'],
            name='Total Amount',
            marker_color='#009DAE',
            yaxis='y2'
        ))

        fig_provider.update_layout(
            xaxis=dict(title="Provider Name"),
            yaxis=dict(title="Number of Visits", side='left'),
            yaxis2=dict(title="Total Amount", overlaying='y', side='right', showgrid=False),
            barmode='group',
            margin=dict(l=0, r=0, t=30, b=50),
            height=450
        )

        # Display the chart in Streamlit
        st.markdown('<h3 class="custom-subheader">Top 10 Providers by Visits & Total Amount</h3>', unsafe_allow_html=True)
        st.plotly_chart(fig_provider, use_container_width=True)


    # Group by Client Name to get Total Amount and Number of Visits
    df_grouped_client = df.groupby('Client Name').agg(
        {'Total Amount': 'sum', 'Visit Date': 'count'}  # Count visits
    ).nlargest(15, 'Total Amount').reset_index()

    # Sort by Total Amount in descending order
    df_grouped_client = df_grouped_client.sort_values(by='Total Amount', ascending=False)

    with cls1:
        # Create dual-axis chart for Clients
        fig_client = go.Figure()

        # First y-axis (Number of Visits)
        fig_client.add_trace(go.Bar(
            x=df_grouped_client['Client Name'],
            y=df_grouped_client['Visit Date'],
            name='Number of Visits',
            marker_color='#e66c37',
            yaxis='y1'
        ))

        # Second y-axis (Total Amount)
        fig_client.add_trace(go.Bar(
            x=df_grouped_client['Client Name'],
            y=df_grouped_client['Total Amount'],
            name='Total Amount',
            marker_color='#009DAE',
            yaxis='y2'
        ))

        fig_client.update_layout(
            xaxis=dict(title="Client Name"),
            yaxis=dict(title="Number of Visits", side='left'),
            yaxis2=dict(title="Total Amount", overlaying='y', side='right', showgrid=False),
            barmode='group',
            margin=dict(l=0, r=0, t=30, b=50),
            height=450
        )

        # Display the chart in Streamlit
        st.markdown('<h3 class="custom-subheader">Top 10 Clients by Visits & Total Amount</h3>', unsafe_allow_html=True)
        st.plotly_chart(fig_client, use_container_width=True)


    # Group by Client Name to get Total Amount and Number of Visits
    df_grouped_client = df.groupby('Pharmacy Name').agg(
        {'Pharmacy Claim Amount': 'sum', 'Visit Date': 'count'}  # Count visits
    ).nlargest(15, 'Pharmacy Claim Amount').reset_index()

    # Sort by Total Amount in descending order
    df_grouped_client = df_grouped_client.sort_values(by='Pharmacy Claim Amount', ascending=False)

    with cls1:
        # Create dual-axis chart for Clients
        fig_client = go.Figure()

        # First y-axis (Number of Visits)
        fig_client.add_trace(go.Bar(
            x=df_grouped_client['Pharmacy Name'],
            y=df_grouped_client['Visit Date'],
            name='Number of Visits',
            marker_color='#e66c37',
            yaxis='y1'
        ))

        # Second y-axis (Total Amount)
        fig_client.add_trace(go.Bar(
            x=df_grouped_client['Pharmacy Name'],
            y=df_grouped_client['Pharmacy Claim Amount'],
            name='Total Amount',
            marker_color='#009DAE',
            yaxis='y2'
        ))

        fig_client.update_layout(
            xaxis=dict(title="Pharmacy Name"),
            yaxis=dict(title="Number of Visits", side='left'),
            yaxis2=dict(title="Pharmacy Amount", overlaying='y', side='right', showgrid=False),
            barmode='group',
            margin=dict(l=0, r=0, t=30, b=50),
            height=450
        )

        # Display the chart in Streamlit
        st.markdown('<h3 class="custom-subheader">Top 10 Pharmacies by Visits & Pharmacy Claim Amount</h3>', unsafe_allow_html=True)
        st.plotly_chart(fig_client, use_container_width=True)


    
    # Calculate the Total Amount by Client Segment
    int_owner = df.groupby("Visit Type")["Total Amount"].sum().reset_index()
    int_owner.columns = ["Visit Type", "Total Amount"]    

    with cls2:
        # Display the header
        st.markdown('<h3 class="custom-subheader">Total Expected Claim Amount by Visit Type</h3>', unsafe_allow_html=True)


        # Create a donut chart
        fig = px.pie(int_owner, names="Visit Type", values="Total Amount", hole=0.5, template="plotly_dark", color_discrete_sequence=custom_colors)
        fig.update_traces(textposition='inside', textinfo='value+percent')
        fig.update_layout(height=450, margin=dict(l=0, r=10, t=30, b=50))

        # Display the chart in Streamlit
        st.plotly_chart(fig, use_container_width=True)


