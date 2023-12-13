import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Set style seaborn
sns.set(style='dark')

day = pd.read_csv('datasets/day.csv')
day.head()

# Delete columns that are not needed
drop = ['instant']

for i in day.columns:
  if i in drop:
    day.drop(labels=i, axis=1, inplace=True)

# Rename column headings
day.rename(columns={'dteday': 'dateday', 'yr': 'year', 'mnth': 'month', 'cnt': 'count'}, inplace=True)

# Convert a value that was previously numeric, into a category
day['season'] = day['season'].map({1: 'Springer', 2: 'Summer', 3: 'Fall', 4: 'Winter'})
day['year'] = day['year'].map({0: '2011', 1:'2012'})
day['month'] = day['month'].map({1:'Jan', 2: 'Feb', 3:'Mar', 4:'Apr', 5:'May', 6:'Jun', 7:'Jul', 8:'Aug', 9:'Sep', 10:'Oct', 11:'Nov', 12:'Dec'})
day['weathersit'] = day['weathersit'].map({1: 'Clear/Partly Cloudy', 2: 'Misty/Cloudy', 3: 'Light Snow/Rain', 4: 'Severe Weather'})


# Setting up daily_rent
def create_daily_rent(df):
    daily_rent = df.groupby(by='dateday').agg({'count': 'sum'}).reset_index()
    return daily_rent

# Setting up season_rent
def create_season_rent(df):
    season_rent = df.groupby(by='season').agg({'count': 'sum'})
    return season_rent

# Setting up monthly_rent
def create_monthly_rent(df):
    monthly_rent = df.groupby(by='month').agg({'count': 'sum'})
    ordered_months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    monthly_rent = monthly_rent.reindex(ordered_months, fill_value=0)
    return monthly_rent

# Setting up holiday_rent
def create_holiday_rent(df):
    holiday_rent = df.groupby(by='holiday')[['registered', 'casual']].sum().reset_index()
    return holiday_rent

# Setting up weekday_rent
def create_weekday_rent(df):
    weekday_rent = df.groupby(by='weekday').agg({'count': 'sum'}).reset_index()
    return weekday_rent

# Setting up workingday_rent
def create_workingday_rent(df):
    workingday_rent = df.groupby(by='workingday')[['registered', 'casual']].sum().reset_index()
    return workingday_rent

# Setting up weather_rent
def create_weather_rent(df):
    weather_rent = df.groupby(by='weathersit').agg({'count': 'sum'})
    return weather_rent

# Setting up casual_rent
def create_casual_rent(df):
    casual_rent = df.groupby(by='dateday').agg({'casual': 'sum'}).reset_index()
    return casual_rent

# Setting up daily_registered_rent
def create_registered_rent(df):
    registered_rent = df.groupby(by='dateday').agg({'registered': 'sum'}).reset_index()
    return registered_rent

# Creating a filter component
min_date = pd.to_datetime(day['dateday']).dt.date.min()
max_date = pd.to_datetime(day['dateday']).dt.date.max()
 
with st.sidebar:
    st.image('datasets/RB.png')
    
    # Retrieve start_date & end_date from date_input
    start_date, end_date = st.sidebar.date_input(label='Time Range', min_value= min_date, max_value= max_date, value=[min_date, max_date])

main = day[(day['dateday'] >= str(start_date)) & 
           (day['dateday'] <= str(end_date))]

# Setting up various dataframes
daily_rent = create_daily_rent(main)
season_rent = create_season_rent(main)
monthly_rent = create_monthly_rent(main)
holiday_rent = create_holiday_rent(main)
weekday_rent = create_weekday_rent(main)
workingday_rent = create_workingday_rent(main)
weather_rent = create_weather_rent(main)
casual_rent = create_casual_rent(main)
registered_rent = create_registered_rent(main)


# Creating a complete Dashboard
st.header('Bike Sharing Rentals')

# Create a rental report
st.subheader('Report Rentals')
col1, col2, col3 = st.columns(3)

with col1:
    rent_casual = casual_rent['casual'].sum()
    st.metric('Casual User', value= rent_casual)

with col2:
    rent_registered = registered_rent['registered'].sum()
    st.metric('Registered User', value= rent_registered)
 
with col3:
    rent_total = daily_rent['count'].sum()
    st.metric('Total User', value= rent_total)


# Create Rent amount by month
st.subheader('Monthly Report')
fig, ax = plt.subplots(figsize=(20, 8))
ax.plot(monthly_rent.index.to_numpy(), monthly_rent['count'].to_numpy(), marker='o', linewidth=2, color='tab:red')

for index, row in enumerate(monthly_rent['count']):
    ax.text(index, row + 1, str(row), ha='center', va='bottom', fontsize=12)

ax.tick_params(axis='x', labelsize=20)
ax.tick_params(axis='y', labelsize=20)
st.pyplot(fig)


# Create rental amount based on season
st.subheader('Season Report')
fig, ax = plt.subplots(figsize=(16, 8))
colors=['tab:blue', 'tab:orange', 'tab:green', 'tab:red']
sns.barplot(x=season_rent.index, y=season_rent['count'], palette=colors, ax=ax)

for index, row in enumerate(season_rent['count']):
    ax.text(index, row + 1, str(row), ha='center', va='bottom', fontsize=12)

ax.set_xlabel(None)
ax.set_ylabel(None)
ax.tick_params(axis='x', labelsize=20)
ax.tick_params(axis='y', labelsize=15)
st.pyplot(fig)


# Generate rental amount based on weather conditions
st.subheader('Weather Report')
fig, ax = plt.subplots(figsize=(16, 8))
colors=['tab:orange', 'tab:green', 'tab:red']
sns.barplot(x=weather_rent.index, y=weather_rent['count'], palette=colors, ax=ax)

for index, row in enumerate(weather_rent['count']):
    ax.text(index, row + 1, str(row), ha='center', va='bottom', fontsize=12)

ax.set_xlabel(None)
ax.set_ylabel(None)
ax.tick_params(axis='x', labelsize=20)
ax.tick_params(axis='y', labelsize=15)
st.pyplot(fig)


# Create rental amount based on holiday
st.subheader('Holiday Rentals')
fig, ax = plt.subplots(figsize=(16, 8))
sns.barplot(x='holiday', y='registered', data=holiday_rent, label='Registered', color='tab:blue', ax=ax)
sns.barplot(x='holiday', y='casual', data=holiday_rent, label='Casual', color='tab:orange', ax=ax)

for index, row in holiday_rent.iterrows():
    ax.text(index, row['registered'], str(row['registered']), ha='center', va='bottom', fontsize=12)
    ax.text(index, row['casual'], str(row['casual']), ha='center', va='bottom', fontsize=12)

ax.set_xlabel(None)
ax.set_ylabel(None)
ax.tick_params(axis='x', labelsize=20)
ax.tick_params(axis='y', labelsize=15)
ax.legend()
st.pyplot(fig)


# Create rental amount based on working
st.subheader('Working Rentals')
fig, ax = plt.subplots(figsize=(16, 8))
sns.barplot(x='workingday', y='registered', data=workingday_rent, label='Registered', color='tab:blue', ax=ax)
sns.barplot(x='workingday', y='casual', data=workingday_rent, label='Casual', color='tab:orange', ax=ax)

for index, row in workingday_rent.iterrows():
    ax.text(index, row['registered'], str(row['registered']), ha='center', va='bottom', fontsize=12)
    ax.text(index, row['casual'], str(row['casual']), ha='center', va='bottom', fontsize=12)

ax.set_xlabel(None)
ax.set_ylabel(None)
ax.tick_params(axis='x', labelsize=20, rotation=0)
ax.tick_params(axis='y', labelsize=15)
ax.legend()
st.pyplot(fig)


# Create rental amount based on weekday
st.subheader('Weekday Rentals')
fig, ax = plt.subplots(figsize=(16, 8))
colors1=['tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple', 'tab:brown', 'tab:pink']
sns.barplot(x='weekday', y='count', data=weekday_rent, palette=colors1, ax=ax)

for index, row in enumerate(weekday_rent['count']):
    ax.text(index, row + 1, str(row), ha='center', va='bottom', fontsize=12)

ax.set_title('Number of Rents based on Weekday')
ax.set_ylabel(None)
ax.tick_params(axis='x', labelsize=15)
ax.tick_params(axis='y', labelsize=10)
plt.tight_layout()
st.pyplot(fig)

st.caption('Copyright © Gladis Hafifah 2023')