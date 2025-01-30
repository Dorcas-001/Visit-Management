
import streamlit as st
import json
import bcrypt
import pandas as pd
import altair as alt
from PIL import Image
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

st.set_page_config(
    page_title="Eden Care Visit Dashboard",
    page_icon=Image.open("logo.png"),
    layout="wide",
    initial_sidebar_state="expanded"
)
# Function to load users from the JSON file
def load_users():
    with open('users.json', 'r') as file:
        return json.load(file)['users']

# Function to authenticate a user
def authenticate(username, password):
    users = load_users()
    for user in users:
        if user['username'] == username and bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
            return True
    return False

# Dictionary to map month names to their order
month_order = {
    "January": 1, "February": 2, "March": 3, "April": 4, 
    "May": 5, "June": 6, "July": 7, "August": 8, 
    "September": 9, "October": 10, "November": 11, "December": 12
}
current_date = datetime.now()


# Function to display the dashboard
def display_dashboard(username):
    # SIDEBAR FILTER
    logo_url = 'EC_logo.png'  
    st.sidebar.image(logo_url, use_column_width=True)

    page = st.sidebar.selectbox("Choose a dashboard", ["Home", "Overview", "Visit Details View", "Visit Type View", "Visit Member Details View"])

    st.markdown(
        """
        <style>
        .reportview-container {
            background-color: #013220;
            color: white;
        }
        .sidebar .sidebar-content {
            background-color: #013220;
            color: white;
        }
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
        .subheader {
            color: #e66c37;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
            padding: 10px;
            border-radius: 5px;
            display: inline-block;
        }
        .section-title {
            font-size: 1.75rem;
            color: #004d99;
            margin-top: 2rem;
            margin-bottom: 0.5rem;
        }
        .text {
            font-size: 1.1rem;
            color: #333;
            padding: 10px;
            line-height: 1.6;
            margin-bottom: 1rem;
        }
        .nav-item {
            font-size: 1.2rem;
            color: #004d99;
            margin-bottom: 0.5rem;
        }
        .separator {
            margin: 2rem 0;
            border-bottom: 2px solid #ddd;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    if page == "Home":
        st.markdown('<h1 class="main-title">EDEN CARE VISIT MANAGEMENT DASHBOARD</h1>', unsafe_allow_html=True)
        st.image("pexels-thirdman-5327647.jpg", caption='Eden Care Medical', use_column_width=True)
        st.markdown('<h2 class="subheader">Welcome to the Eden Care Visit Management Dashboard</h2>', unsafe_allow_html=True)
        
        # Introduction
        st.markdown('<div class="text">Welcome to the Eden Care Visit Management Dashboard! This comprehensive tool provides a clear and insightful overview of our visit management performance across several key areas: <strong>Visit Details, Visit Types, and Visit Member Details</strong>. The <strong>Visit Details View</strong> provides detailed information about each visit, helping to understand the purpose and outcomes of visits. The <strong>Visit Type View</strong> categorizes visits by type, offering insights into common visit purposes and trends. The <strong>Visit Member Details View</strong> tracks the details of members involved in visits, giving a comprehensive view of member interactions.</div>', unsafe_allow_html=True)

        st.markdown('<div class="separator"></div>', unsafe_allow_html=True)

        # User Instructions
        st.markdown('<h2 class="subheader">User Instructions</h2>', unsafe_allow_html=True)
        st.markdown('<div class="text">1. <strong>Navigation:</strong> Use the menu on the left to navigate between visits, claims and Preauthorisation dashboards.</div>', unsafe_allow_html=True)
        st.markdown('<div class="text">2. <strong>Filters:</strong> Apply filters on the left side of each page to customize the data view.</div>', unsafe_allow_html=True)
        st.markdown('<div class="text">3. <strong>Manage visuals:</strong> Hover over the visuals and use the options on the top right corner of each visual to download zoom or view on fullscreen</div>', unsafe_allow_html=True)
        st.markdown('<div class="text">3. <strong>Manage Table:</strong> click on the dropdown icon (<img src="https://img.icons8.com/ios-glyphs/30/000000/expand-arrow.png"/>) on table below each visual to get a full view of the table data and use the options on the top right corner of each table to download or search and view on fullscreen.</div>', unsafe_allow_html=True)    
        st.markdown('<div class="text">4. <strong>Refresh Data:</strong> The data will be manually refreshed on the last week of every quarter. </div>', unsafe_allow_html=True)
        st.markdown('<div class="separator"></div>', unsafe_allow_html=True)

        

    elif page == "Overview":
        exec(open("overview.py").read())
    elif page == "Visit Details View":
        exec(open("visit.py").read())
    elif page == "Visit Type View":
        exec(open("visit_type.py").read())
    elif page == "Visit Member Details View":
        exec(open("members.py").read())
   

# Streamlit app
def main():
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False
        st.session_state['username'] = ""

    if st.session_state['logged_in']:
        display_dashboard(st.session_state['username'])
    else:
        st.title("Login Page")

        username = st.text_input("Enter username")
        password = st.text_input("Enter password", type="password")
        
        st.markdown('<div class="text">Please double-click on the login or logout button </div>', unsafe_allow_html=True)
        if st.button("Login"):
            if authenticate(username, password):
                st.session_state['logged_in'] = True
                st.session_state['username'] = username
                st.success("Authentication successful")
                st.experimental_rerun()
            else:
                st.error("Authentication failed")

if __name__ == "__main__":
    main()
