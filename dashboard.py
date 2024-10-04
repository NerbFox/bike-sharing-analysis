import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import numpy as np

sns.set_theme(style="dark")

# Helper function yang dibutuhkan untuk analisis data dan visualisasi data

# Function to create a line plot with accurate legend and custom color
def create_line_plot(data, x, y, hue, title, xlabel, ylabel, xticks=None, palette='dark'):
    fig, ax = plt.subplots(figsize=(14, 7))
    sns.lineplot(data=data, x=x, y=y, hue=hue, marker='o', palette=palette if hue else None, ax=ax)
    ax.set_title(title, fontsize=16, fontweight='bold')
    ax.set_xlabel(xlabel, fontsize=14, labelpad=10)
    ax.set_ylabel(ylabel, fontsize=14, labelpad=10)

    if xticks is not None:
        ax.set_xticks(np.arange(1, len(xticks) + 1))
        ax.set_xticklabels(xticks, fontsize=12)

    ax.grid(True)
    plt.tight_layout()
    st.pyplot(fig)

# function to create a bar plot
def create_bar_plot(x_values, y_values, title, xlabel, ylabel, xticks=None):
    fig, ax = plt.subplots(figsize=(12, 7))
    sns.barplot(x=x_values, y=y_values, palette=sns.color_palette('GnBu', len(x_values)), hue=x_values, dodge=False, ax=ax)
    ax.set_title(title, fontsize=16)
    ax.set_xlabel(xlabel, fontsize=14)
    ax.set_ylabel(ylabel, fontsize=14)
    if xticks is not None:
        ax.set_xticks(ticks=range(len(xticks)))
        ax.set_xticklabels(labels=xticks, fontsize=12)
    ax.grid(axis='y', linestyle='--', alpha=0.4)
    plt.tight_layout()
    st.pyplot(fig)

# function to create a pie chart
def create_pie_plot(values, labels, title, size=(5, 4)):
    fig, ax = plt.subplots(figsize=size)
    _ = ax.pie(values, labels=labels, autopct='%1.1f%%', startangle=140, colors=sns.color_palette('Blues', len(labels)))
    ax.set_title(title, fontsize=16)
    ax.axis('equal')
    plt.tight_layout()
    st.pyplot(fig)

# function to group data based on temperature
def group_by_temp(data, temp_col, temp_max):
    temp_bins = pd.cut(data[temp_col], bins=[0, 0.2, 0.4, 0.6, 0.8, 1.0])
    temp_group = data.groupby(temp_bins, observed=False)['cnt'].sum()
    # change the temp column to actual range
    temp_group.index = temp_group.index.map(lambda x: f"{int(x.left * temp_max)}-{int(x.right * temp_max)}")
    return temp_group

# function to create line plots
def create_line_plots(data, x, array_y, hue, title, xlabel, ylabel, xticks=None, palette='dark'):
    fig, ax = plt.subplots(figsize=(14, 7))
    for y in array_y:
        sns.lineplot(data=data, x=x, y=y, hue=hue, marker='o', label=y, palette=palette if hue else None, ax=ax)
    ax.set_title(title, fontsize=16)
    ax.set_xlabel(xlabel, fontsize=14)
    ax.set_ylabel(ylabel, fontsize=14)
    if xticks is not None:
        ax.set_xticks(ticks=range(len(xticks)))
        ax.set_xticklabels(labels=xticks, fontsize=12)
    ax.legend(title="User Type", fontsize=12)
    ax.grid(True)
    plt.tight_layout()
    st.pyplot(fig)

# Load the data
day_df = pd.read_csv('main_day.csv')
hour_df = pd.read_csv('main_hour.csv')

# change the dteday column to datetime
day_df['dteday'] = pd.to_datetime(day_df['dteday'])
hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])

# change the weekday column to actual name
day_min = day_df['dteday'].min()
day_max = day_df['dteday'].max()

# sidebar
with st.sidebar:
    # logo bicycle image centered
    
    # use markdown to show image centered and add bold centered text
    st.markdown('''
    <p align="center"><img src="https://img.icons8.com/ios/452/bicycle.png" width="150"></p>
    ''', unsafe_allow_html=True)
    
    # start_date and end_date from date_input
    start_date, end_date = st.date_input(
        label='Select Date Range',
        min_value=day_min,
        max_value=day_max,
        value=[day_min, day_max]
    )
    
# change day_df and hour_df based on start_date and end_date
day_df = day_df[(day_df['dteday'] >= str(start_date)) & 
                (day_df['dteday'] <= str(end_date))]
hour_df = hour_df[(hour_df['dteday'] >= str(start_date)) &
                  (hour_df['dteday'] <= str(end_date))]


# prepare all the data needed for the dashboard

casual_user = day_df['casual'].sum()
registered_user = day_df['registered'].sum()
total_user = casual_user + registered_user

# weekday map
weekday_map = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']

# change the year to 2011 and 2012
day_df_visual = day_df.copy()
day_df_visual['yr'] = day_df_visual['yr'].map({0: 2011, 1: 2012})

# New Column for month_year in day_df_visual
day_df_visual['month_year'] = day_df_visual['dteday'].dt.to_period('M').dt.to_timestamp()

# monthly rental full data (data grouped by month_year)
monthly_rental_full = day_df_visual.groupby('month_year')['cnt'].sum().reset_index()

# Grouping data based on season
season_group = day_df.groupby('season')['cnt'].sum()

# Grouping data based on month
weekday_group = day_df.groupby('weekday')['cnt'].sum()

# Grouping data based on workingday
workingday_group = day_df.groupby('workingday')['cnt'].sum()

# Grouping data based on holiday
holiday_group = day_df.groupby('holiday')['cnt'].sum()

# Grouping data based on month
mnth_group = day_df.groupby('mnth')['cnt'].sum()


weathersit_group = day_df.groupby('weathersit')['cnt'].sum()

# - temp : Normalized temperature in Celsius. The values are divided to 41 (max)
# - atemp: Normalized feeling temperature in Celsius. The values are divided to 50 (max)
# - hum: Normalized humidity. The values are divided to 100 (max)
# - windspeed: Normalized wind speed. The values are divided to 67 (max)

temp_max = 41
atemp_max = 50
hum_max = 100
windspeed_max = 67

# Grouping data based on temp in 5 bins
temp_group = group_by_temp(day_df, 'temp', temp_max)

# Grouping data based on atemp in 5 bins
atemp_group = group_by_temp(day_df, 'atemp', atemp_max)

# Grouping data based on humidity in 5 bins
hum_group = group_by_temp(day_df, 'hum', hum_max)

# Grouping data based on windspeed in 5 bins
windspeed_group = group_by_temp(day_df, 'windspeed', windspeed_max)

# Grouping data based on hour
hourly_rental = hour_df.groupby('hr')['cnt'].sum()
hourly_rental_df = hourly_rental.reset_index()

# Grouping data based on user type hourly
hourly_casual = hour_df.groupby('hr')['casual'].sum()
hourly_registered = hour_df.groupby('hr')['registered'].sum()
hourly_casual_registered = pd.concat([hourly_casual, hourly_registered], axis=1)
hourly_casual_registered.columns = ['casual', 'registered']

# Grouping data based on user type hourly
weekday_casual = day_df.groupby('weekday')['casual'].sum()
weekday_registered = day_df.groupby('weekday')['registered'].sum()
weekday_casual_registered = pd.concat([weekday_casual, weekday_registered], axis=1)
weekday_casual_registered.columns = ['casual', 'registered']

# Grouping data based on user type monthly
monthly_casual = day_df.groupby('mnth')['casual'].sum()
monthly_registered = day_df.groupby('mnth')['registered'].sum()
monthly_casual_registered = pd.concat([monthly_casual, monthly_registered], axis=1)
monthly_casual_registered.columns = ['casual', 'registered']

# Grouping data based on user type holiday
holiday_casual = day_df.groupby('holiday')['casual'].sum()
holiday_registered = day_df.groupby('holiday')['registered'].sum()
holiday_casual_registered = pd.concat([holiday_casual, holiday_registered], axis=1)
holiday_casual_registered.columns = ['casual', 'registered']

# User casual and registered hourly
hourly_casual_registered_df = hourly_casual_registered.reset_index()

# User casual and registered in holiday
holiday_casual_registered_df = holiday_casual_registered.reset_index()


# Web Application

# title
st.title('Bike Sharing Data Analysis Dashboard')
st.markdown('''
This dashboard provides insights analysis of bike sharing data from year 2011-2012.
''')

col1, col2, col3 = st.columns(3)

# Total User
with col1:
    st.metric('Total User', value=total_user)
with col2:
    st.metric('Casual User', value=casual_user)
with col3:
    st.metric('Registered User', value=registered_user)

daily = "Daily"
monthly_year = "Monthly - Year"
monthly = "Monthly"


st.write('')
st.subheader('Bike Rental Performance Over the Months 2011-2012')

# Create tabs for different visualizations
tab1, tab2, tab3 = st.tabs([daily, monthly_year, monthly])

with tab1:
    create_line_plot(day_df_visual, x='dteday', y='cnt', hue='yr', 
                     title='Daily Bike Rental (2011-2012)', 
                     xlabel='Date', ylabel='Total Rentals')

with tab2:
    create_line_plot(day_df_visual, x='mnth', y='cnt', hue='yr', 
                     title='Monthly Bike Rental (2011-2012) - Year Separation',
                     xlabel='Month', ylabel='Total Rentals', 
                     xticks=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])

with tab3:
    create_line_plot(monthly_rental_full, x='month_year', y='cnt', hue=None, 
                     title='Monthly Bike Rental (2011-2012)', 
                     xlabel='Month', ylabel='Total Rentals')


st.write('')
st.subheader('Bike Rental Performance Over Time')

# Create tabs for different bar plot visualizations
tab1, tab2, tab3 = st.tabs(['Total Rental Count by Month', 'Total Rental Count by Season', 'Total Rental Count by Weekday'])

with tab1:
    create_bar_plot(mnth_group.index, mnth_group.values, "Total Rental Count by Month", "Month", "Total Rental Count")

with tab2:
    create_bar_plot(season_group.index, season_group.values, "Total Rental Count by Season", "Season", "Total Rental Count")

with tab3:
    create_bar_plot(weekday_group.index, weekday_group.values, "Total Rental Count by Weekday", "Weekday", "Total Rental Count", xticks=weekday_map)


st.write('')
st.subheader('Bike Rental Performance Based on Special Days')

col1, col2 = st.columns(2)

with col1:
    # Visualize holiday data
    create_pie_plot(holiday_group.values, ['Non-Holiday', 'Holiday'], "Total Rental Count by Holiday", size=(6, 5))
with col2:
    # Visualize workingday data
    create_pie_plot(workingday_group.values, ['Non-Working Day', 'Working Day'], "Total Rental Count by Workingday", size=(6, 5))
    
    
st.write('')
st.subheader('Bike Rental Performance Based on Environmental Factors')

# Create tabs for different visualizations
tab1, tab2, tab3, tab4, tab5 = st.tabs(['Temperature', 'Feeling Temperature', 'Weathersit', 'Humidity', 'Windspeed'])

with tab1:
    # Visualize temp data
    create_bar_plot(temp_group.index, temp_group.values, "Total Rental Count by Temperature", "Temperature Range (Celsius)", "Total Rental Count")

with tab2:
    # Visualize atemp data
    create_bar_plot(atemp_group.index, atemp_group.values, "Total Rental Count by Feeling Temperature", "Feeling Temperature Range (Celsius)", "Total Rental Count")

with tab3:
    # Visualize weathersit data
    create_bar_plot(weathersit_group.index, weathersit_group.values, "Total Rental Count by Weathersit", "Weather Situation", "Total Rental Count")

with tab4:
    # Visualize hum data
    create_bar_plot(hum_group.index, hum_group.values, "Total Rental Count by Humidity", "Humidity Range (%)", "Total Rental Count")

with tab5:
    # Visualize windspeed data
    create_bar_plot(windspeed_group.index, windspeed_group.values, "Total Rental Count by Windspeed", "Windspeed Range (km/h)", "Total Rental Count")

st.write('')
st.subheader('Hourly Bike Rental Performance')

# Select option to choose the type of hourly rental visualization
tab1, tab2 = st.tabs(['Hourly Bike Rental', 'Hourly Bike Rental (2011-2012)'])

with tab1:
    create_line_plot(hourly_rental_df, x='hr', y='cnt', hue=None,
                     title='Hourly Bike Rental',
                     xlabel='Hour', ylabel='Total Rentals')

with tab2:
    create_line_plot(hour_df, x='hr', y='cnt', hue='yr',
                     title='Hourly Bike Rental (2011-2012)',
                     xlabel='Hour', ylabel='Total Rentals')


st.write('')
st.subheader('User Patterns Visualization Hourly')

tab1, tab2, tab3 = st.tabs(['Hourly', 'Weekly', 'Monthly'])

with tab1:
    create_line_plots(hourly_casual_registered_df, x='hr', array_y=['casual', 'registered'], 
                        hue=None, title='Hourly Bike Rental by Casual and Registered Users',
                        xlabel='Hour', ylabel='Total Rentals')

with tab2:
    weekday_casual_registered_df = weekday_casual_registered.reset_index()
    create_line_plots(weekday_casual_registered_df, x='weekday', array_y=['casual', 'registered'], 
                        hue=None, title='Weekly Bike Rental by Casual and Registered Users',
                        xlabel='Weekday', ylabel='Total Rentals', xticks=weekday_map)

with tab3:
    monthly_casual_registered_df = monthly_casual_registered.reset_index()
    create_line_plots(monthly_casual_registered_df, x='mnth', array_y=['casual', 'registered'], 
                        hue=None, title='Monthly Bike Rental by Casual and Registered Users',
                        xlabel='Month', ylabel='Total Rentals')
    
    
st.write('')
st.subheader('User Patterns Visualization on Special Days')

row1_col1, row1_col2 = st.columns(2)
row2_col1, row2_col2 = st.columns(2)

with row1_col1:
    # Metric for total rental by casual users on holiday 
    holiday_casual = holiday_casual_registered_df['casual'][1]
    st.metric("Casual User Rentals on Holiday", value=holiday_casual)

with row1_col2:
    # Metric for total rental by registered users on holiday 
    holiday_registered = holiday_casual_registered_df['registered'][1]
    st.metric("Registered User Rentals on Holiday", value=holiday_registered)

with row2_col1:
    # Metric for total rental by casual users on non-holiday 
    non_holiday_casual = holiday_casual_registered_df['casual'][0]
    st.metric("Casual User Rentals on Non-Holiday", value=non_holiday_casual)

with row2_col2:
    # Metric for total rental by registered users on non-holiday 
    non_holiday_registered = holiday_casual_registered_df['registered'][0]
    st.metric("Registered User Rentals on Non-Holiday", value=non_holiday_registered)

st.write('')
st.caption('Authored by Nigel Sahl | Copyright © Dicoding 2023')