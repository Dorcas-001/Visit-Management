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

st.markdown('<h1 class="main-title">VISIT MEMBER DETAILS VIEW</h1>', unsafe_allow_html=True)


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


# Convert 'Date of Birth' to datetime
df['Date of Birth'] = pd.to_datetime(df['Date of Birth'])

# Calculate age
current_date = datetime.now()
df['Age'] = df['Date of Birth'].apply(lambda dob: current_date.year - dob.year - ((current_date.month, current_date.day) < (dob.month, dob.day)))

# Define age ranges
def age_range(age):
    if age < 20:
        return '0-19'
    elif 20 <= age < 30:
        return '20-29'
    elif 30 <= age < 40:
        return '30-39'
    elif 40 <= age < 50:
        return '40-49'
    elif 50 <= age < 60:
        return '50-59'
    else:
        return '60+'

df['Age Range'] = df['Age'].apply(age_range)


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
age = st.sidebar.multiselect("Select Age Range", options=sorted(df['Age Range'].dropna().unique()))
gender = st.sidebar.multiselect("Select Client Gender", options=df['Gender'].unique())
type = st.sidebar.multiselect("Select Visit Type", options=sorted(df['Visit Type'].unique()))
client_name = st.sidebar.multiselect("Select Client Name", options=sorted(df['Client Name'].dropna().unique()))
prov_name = st.sidebar.multiselect("Select Provider Name", options=sorted(df['Provider Name'].dropna().unique()))


# Apply filters to the DataFrame
if 'Year' in df.columns and year:
    df = df[df['Year'].isin(year)]
if 'Month' in df.columns and month:
    df = df[df['Month'].isin(month)]
if 'Quarter' in df.columns and quarter:
    df = df[df['Quarter'].isin(quarter)]
if 'Age Range' in df.columns and age:
    df = df[df['Age Range'].isin(age)]
if 'Visit Type' in df.columns and type:
    df = df[df['Visit Type'].isin(type)]
if 'Gender' in df.columns and gender:
    df = df[df['Gender'].isin(gender)]
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



# Get unique age ranges and sort them
age_ranges = sorted(df['Age Range'].unique())

# Select slider for age range
selected_age_range = st.select_slider(
    "Select Age Range",
    options=age_ranges,
    value=(age_ranges[0], age_ranges[-1])
)

# Filter DataFrame based on selected age range
start_age_range, end_age_range = selected_age_range

# Define a function to convert age range string to a tuple of integers
def age_range_to_tuple(age_range):
    if age_range == '60+':
        return (60, float('inf'))
    start, end = map(int, age_range.split('-'))
    return (start, end)

# Convert selected age ranges to tuples
start_age_tuple = age_range_to_tuple(start_age_range)
end_age_tuple = age_range_to_tuple(end_age_range)



df_close = df[df['Visit Status'] == 'Close']
df_open = df[df['Visit Status'] == 'Open']

df_male = df[df['Gender'] == 'Male']
df_female = df[df['Gender'] == 'Female']

if not df.empty:

    scale=1_000_000  # For millions

    total_amount = (df["Total Amount"].sum())/scale
    average_amount =(df["Total Amount"].mean())/scale


    total_closed = (df_close["Total Amount"].sum())/scale
    total_open = (df_open["Total Amount"].sum())/scale

    total_male=df_male["Visit ID"].nunique()
    total_female=df_female["Visit ID"].nunique()


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
    display_metric(cols2, "Total Visits", total_visits)
    display_metric(cols3, "Total Expected Claim Amount", F"{total_amount:,.0F} M")
    display_metric(cols1, "Average Expected Claim Amount Per Client", F"{average_amount:,.1F} M")
    display_metric(cols2, "Percentage Closed Visit", F"{total_closed_per:,.0F} %")
    display_metric(cols3, "Percentage Open Visit", F"{total_open_per:,.0F} %")

    st.markdown('<h2 class="custom-subheader">For Visit Member Demographics</h2>', unsafe_allow_html=True)    

    cols1,cols2, cols3 = st.columns(3)

    display_metric(cols1, "Total Visits", total_visits)
    display_metric(cols2, "Total Male Visits", total_male)
    display_metric(cols3, "Total Female Visits", total_female)


    st.dataframe(df)
    custom_colors = ["#009DAE", "#e66c37", "#461b09", "#f8a785", "#CC3636","#9ACBD0"]

    # Group by day and gender, then count occurrences
    gender_visit_trend = df.groupby([df["Visit Date"].dt.strftime("%Y-%m-%d"), "Gender"]).size().reset_index(name="Count")

    # Sort by Visit Date
    gender_visit_trend = gender_visit_trend.sort_values("Visit Date")

    # Create the chart for the number of visits by gender
    fig = go.Figure()

    # Add traces for each gender
    for idx, gender in enumerate(gender_visit_trend["Gender"].unique()):
        subset = gender_visit_trend[gender_visit_trend["Gender"] == gender]
        fig.add_trace(go.Scatter(
            x=subset["Visit Date"],
            y=subset["Count"],
            name=f"Visits ({gender})",
            fill="tozeroy",
            line=dict(width=2, color=custom_colors[idx % len(custom_colors)]) 
        ))
    

    # Set x-axis and y-axis titles
    fig.update_xaxes(title_text="Visit Date", tickangle=45)  # Rotate labels for better readability
    fig.update_yaxes(title_text="<b>Number of Visits</b>")

    cols1, cols2 = st.columns(2)
    
    with cols1:
        # Display the chart in Streamlit
        st.markdown('<h3 class="custom-subheader">Number of Visits Over Time by Gender</h3>', unsafe_allow_html=True)
        st.plotly_chart(fig, use_container_width=True)

    # Group data by "Year" and "Gender" and count the number of visits
    yearly_visits_by_gender = df.groupby(['Year', 'Gender']).size().unstack().fillna(0)

    with cols2:
        # Create the grouped bar chart
        fig_yearly_visits = go.Figure()

        for idx, gender in enumerate(yearly_visits_by_gender.columns):
            fig_yearly_visits.add_trace(go.Bar(
                x=yearly_visits_by_gender.index,
                y=yearly_visits_by_gender[gender],
                name=gender,
                textposition='inside',
                textfont=dict(color='white'),
                hoverinfo='x+y+name',
                marker_color=custom_colors[idx % len(custom_colors)]  # Cycle through custom colors
            ))

        fig_yearly_visits.update_layout(
            barmode='group',  # Grouped bar chart
            xaxis_title="Year",
            yaxis_title="Number of Visits",
            font=dict(color='Black'),
            xaxis=dict(title_font=dict(size=14), tickfont=dict(size=12)),
            yaxis=dict(title_font=dict(size=14), tickfont=dict(size=12)),
            margin=dict(l=0, r=0, t=30, b=50),
            height=450
        )

        # Display the chart in Streamlit
        st.markdown('<h3 class="custom-subheader">Yearly Visits by Gender</h3>', unsafe_allow_html=True)
        st.plotly_chart(fig_yearly_visits, use_container_width=True)

    # Group data by Month and Gender
    monthly_visits_by_gender = df.groupby(['Month', 'Gender']).size().unstack().fillna(0)

    # Group data by Age Range
    age_range_visits = df.groupby('Age').size().reset_index(name='Number of Visits')

    # Create the first chart for monthly visits by gender
    fig_monthly_gender = go.Figure()

    for idx, gender in enumerate(monthly_visits_by_gender.columns):
        fig_monthly_gender.add_trace(go.Bar(
            x=monthly_visits_by_gender.index,
            y=monthly_visits_by_gender[gender],
            name=gender,
            marker_color=custom_colors[idx % len(custom_colors)]  # Apply custom colors
        ))

    fig_monthly_gender.update_layout(
        xaxis=dict(title="Month", tickangle=45),
        yaxis=dict(title="Number of Visits"),
        barmode='group',  # Display bars side by side
        margin=dict(l=0, r=0, t=30, b=50),
        height=450
    )

    # Create the second chart for visits by age range
    fig_age_range = go.Figure()

    fig_age_range.add_trace(go.Bar(
        x=age_range_visits['Age'],
        y=age_range_visits['Number of Visits'],
        name="Visits by Age Range",
        marker_color=custom_colors[0]  # Use the first custom color
    ))

    fig_age_range.update_layout(
        xaxis=dict(title="Age"),
        yaxis=dict(title="Number of Visits"),
        margin=dict(l=0, r=0, t=30, b=50),
        height=450
    )

    # Display the charts in Streamlit
    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<h3 class="custom-subheader">Monthly Visits by Gender</h3>', unsafe_allow_html=True)
        st.plotly_chart(fig_monthly_gender, use_container_width=True)

    with col2:
        st.markdown('<h3 class="custom-subheader">Number of Visits by Age</h3>', unsafe_allow_html=True)
        st.plotly_chart(fig_age_range, use_container_width=True)


    # Group by Gender and calculate Total Amount and Number of Visits
    gender_data = df.groupby("Gender").agg({"Total Amount": "sum", "Gender": "count"}).rename(columns={"Gender": "Number of Visits"}).reset_index()

    # Group by Age Range and calculate Total Amount and Number of Visits
    age_data = df.groupby("Age Range").agg({"Total Amount": "sum", "Age Range": "count"}).rename(columns={"Age Range": "Number of Visits"}).reset_index()

    # Create a new column for the text info (Amount, Visits, Percent)
    gender_data["Text"] = gender_data.apply(lambda row: f"${row['Total Amount'] / 1e6:.1f}M | {row['Number of Visits']} Visits", axis=1)
    age_data["Text"] = age_data.apply(lambda row: f"${row['Total Amount'] / 1e6:.1f}M | {row['Number of Visits']} Visits", axis=1)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<h3 class="custom-subheader">Distribution of Visits by Gender</h3>', unsafe_allow_html=True)

        fig_gender = px.pie(
            gender_data, 
            names="Gender", 
            values="Number of Visits", 
            hole=0.5, 
            template="plotly_dark", 
            color_discrete_sequence=custom_colors
        )
        
        fig_gender.update_traces(
            textinfo="percent+value",
            hoverinfo="label+text",
            text=gender_data["Text"]
        )
        
        fig_gender.update_layout(height=450, margin=dict(l=0, r=10, t=30, b=50))

        st.plotly_chart(fig_gender, use_container_width=True)

    with col2:
        st.markdown('<h3 class="custom-subheader">Distribution of Visits by Age Range</h3>', unsafe_allow_html=True)

        fig_age = px.pie(
            age_data, 
            names="Age Range", 
            values="Number of Visits", 
            hole=0.5, 
            template="plotly_dark", 
            color_discrete_sequence=custom_colors
        )

        fig_age.update_traces(
            textinfo="percent+value",
            hoverinfo="label+text",
            text=age_data["Text"]
        )
        
        fig_age.update_layout(height=450, margin=dict(l=0, r=10, t=30, b=50))

        st.plotly_chart(fig_age, use_container_width=True)




    # Group data by Hour and Gender
    hourly_visits_gender = df.groupby(['Hour', 'Gender']).size().unstack().fillna(0)

    # Group data by Hour and Age Range
    hourly_visits_age = df.groupby(['Hour', 'Age Range']).size().unstack().fillna(0)

    col1, col2 = st.columns(2)

    # Create hourly visits by Gender chart
    with col1:
        st.markdown('<h3 class="custom-subheader">Hourly Visits by Gender</h3>', unsafe_allow_html=True)
        
        fig_hourly_gender = go.Figure()
        
        for idx, gender in enumerate(hourly_visits_gender.columns):
            fig_hourly_gender.add_trace(go.Bar(
                x=hourly_visits_gender.index,
                y=hourly_visits_gender[gender],
                name=gender,
                marker_color=custom_colors[idx % len(custom_colors)]
            ))

        fig_hourly_gender.update_layout(
            barmode='group',
            xaxis=dict(title="Hour of the Day", tickmode='linear'),
            yaxis=dict(title="Number of Visits"),
            margin=dict(l=0, r=0, t=30, b=50),
            height=450
        )

        st.plotly_chart(fig_hourly_gender, use_container_width=True)

    # Create hourly visits by Age Range chart
    with col2:
        st.markdown('<h3 class="custom-subheader">Hourly Visits by Age Range</h3>', unsafe_allow_html=True)
        
        fig_hourly_age = go.Figure()
        
        for idx, age_range in enumerate(hourly_visits_age.columns):
            fig_hourly_age.add_trace(go.Bar(
                x=hourly_visits_age.index,
                y=hourly_visits_age[age_range],
                name=age_range,
                marker_color=custom_colors[idx % len(custom_colors)]
            ))

        fig_hourly_age.update_layout(
            barmode='stack',
            xaxis=dict(title="Hour of the Day", tickmode='linear'),
            yaxis=dict(title="Number of Visits"),
            margin=dict(l=0, r=0, t=30, b=50),
            height=450
        )

        st.plotly_chart(fig_hourly_age, use_container_width=True)

    # Group data by "Age Range" and "Visit Type" to calculate total visits
    visits_by_age = df.groupby(['Age Range', 'Visit Type']).size().unstack().fillna(0)

    # Group data by "Visit Type" and "Gender" to calculate total visits
    visits_by_gender = df.groupby(['Visit Type', 'Gender']).size().unstack().fillna(0)

    col1, col2 = st.columns(2)

    # Chart: Visit Type by Age Range
    with col1:
        st.markdown('<h3 class="custom-subheader">Number of Visits by Age Range and Visit Type</h3>', unsafe_allow_html=True)
        
        fig_visits_by_age = go.Figure()
        
        for idx, visit_type in enumerate(visits_by_age.columns):
            fig_visits_by_age.add_trace(go.Bar(
                x=visits_by_age.index,
                y=visits_by_age[visit_type],
                name=visit_type,
                textposition='inside',
                textfont=dict(color='white'),
                hoverinfo='x+y+name',
                marker_color=custom_colors[idx % len(custom_colors)]
            ))

        fig_visits_by_age.update_layout(
            barmode='group',
            xaxis_title="Age Range",
            yaxis_title="Number of Visits",
            font=dict(color='Black'),
            xaxis=dict(title_font=dict(size=14), tickfont=dict(size=12)),
            yaxis=dict(title_font=dict(size=14), tickfont=dict(size=12)),
            margin=dict(l=0, r=0, t=30, b=50),
            height=450
        )

        st.plotly_chart(fig_visits_by_age, use_container_width=True)

    # Chart: Gender by Visit Type
    with col2:
        st.markdown('<h3 class="custom-subheader">Number of Visits by Gender and Visit Type</h3>', unsafe_allow_html=True)
        
        fig_visits_by_gender = go.Figure()
        
        for idx, gender in enumerate(visits_by_gender.columns):
            fig_visits_by_gender.add_trace(go.Bar(
                x=visits_by_gender.index,
                y=visits_by_gender[gender],
                name=gender,
                textposition='inside',
                textfont=dict(color='white'),
                hoverinfo='x+y+name',
                marker_color=custom_colors[idx % len(custom_colors)]
            ))

        fig_visits_by_gender.update_layout(
            barmode='group',
            xaxis_title="Visit Type",
            yaxis_title="Number of Visits",
            font=dict(color='Black'),
            xaxis=dict(title_font=dict(size=14), tickfont=dict(size=12)),
            yaxis=dict(title_font=dict(size=14), tickfont=dict(size=12)),
            margin=dict(l=0, r=0, t=30, b=50),
            height=450
        )

        st.plotly_chart(fig_visits_by_gender, use_container_width=True)

