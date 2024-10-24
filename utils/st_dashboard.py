import streamlit as st
import pandas as pd
from datetime import timedelta, datetime
import pathlib

st.set_page_config(page_title="Taiwan Air Quality Dashboard", layout="wide")

@st.cache_data
def load_data():
    data_dir = pathlib.Path(__file__)
    data_dir = data_dir.parent.parent.joinpath("data/air_quality.pkl")
    my_data = pd.read_pickle(data_dir)
    return my_data, [col_name for col_name in my_data.columns.to_list() if col_name not in ["date", "sitename", "county", "pollutant", "status", "unit"]]

def custom_quarter(date):
    month = date.month
    year = date.year
    if month in [2, 3, 4]:
        return pd.Period(year=year, quarter=1, freq='Q')
    elif month in [5, 6, 7]:
        return pd.Period(year=year, quarter=2, freq='Q')
    elif month in [8, 9, 10]:
        return pd.Period(year=year, quarter=3, freq='Q')
    else:  # month in [11, 12, 1]
        return pd.Period(year=year if month != 1 else year-1, quarter=4, freq='Q')

def custom_quarter(date):
    month = date.month
    year = date.year
    if month in [2, 3, 4]:
        return pd.Period(year=year, quarter=1, freq='Q')
    elif month in [5, 6, 7]:
        return pd.Period(year=year, quarter=2, freq='Q')
    elif month in [8, 9, 10]:
        return pd.Period(year=year, quarter=3, freq='Q')
    else:  # month in [11, 12, 1]
        return pd.Period(year=year if month != 1 else year-1, quarter=4, freq='Q')

def aggregate_data(df, freq, num_cols, opp='sum'):
    agg_d={}
    for col_name in num_cols:
        agg_d[col_name]= opp
    if freq == 'Q':
        df = df.copy()
        df['CUSTOM_Q'] = df['date'].apply(custom_quarter)
        df_agg = df.groupby('CUSTOM_Q').agg(agg_d)
        return df_agg
    else:
        return df.resample(freq, on='date').agg(agg_d)

def get_weekly_data(df):
    return aggregate_data(df, 'W-MON')

def get_monthly_data(df):
    return aggregate_data(df, 'M')

def get_quarterly_data(df):
    return aggregate_data(df, 'Q')

def create_metric_chart(df, column, color, chart_type, height=150, time_frame='Daily'):
    chart_data = df[[column]].copy()
    if time_frame == 'Quarterly':
        chart_data.index = chart_data.index.strftime('%Y Q%q ')
    if chart_type=='Bar':
        st.bar_chart(chart_data, y=column, color=color, height=height)
    if chart_type=='Area':
        st.area_chart(chart_data, y=column, color=color, height=height)

def format_with_commas(number):
    return f"{number:,}"

def is_period_complete(date, freq):
    today = datetime.now()
    if freq == 'D':
        return date.date() < today.date()
    elif freq == 'W':
        return date + timedelta(days=6) < today
    elif freq == 'M':
        next_month = date.replace(day=28) + timedelta(days=4)
        return next_month.replace(day=1) <= today
    elif freq == 'Q':
        current_quarter = custom_quarter(today)
        return date < current_quarter

def display_metric(col, title, value, df, column, color, time_frame):
    with col:
        with st.container(border=True):
            if len(df) < 2:
                delta, delta_percent = 0, 0
            else:
                current_value = df[column].iloc[-1]
                previous_value = df[column].iloc[-2]
                delta = current_value - previous_value
                delta_percent = (delta / previous_value) * 100 if previous_value != 0 else 0
            delta_str = f"{delta:+,.0f} ({delta_percent:+.2f}%)"
            st.metric(title, format_with_commas(value), delta=delta_str)
            create_metric_chart(df, column, color, time_frame=time_frame, chart_type=chart_selection)
            
            last_period = df.index[-1]
            freq = {'Daily': 'D', 'Weekly': 'W', 'Monthly': 'ME', 'Quarterly': 'Q'}[time_frame]
            if not is_period_complete(last_period, freq):
                st.caption(f"Note: The last {time_frame.lower()[:-2] if time_frame != 'Daily' else 'day'} is incomplete.")

# Starts here

my_data, num_cols = load_data()
my_data = my_data.sample(50000, random_state=42)

data_dir = pathlib.Path(__file__)
data_dir = data_dir.parent.parent.joinpath("data/images/air_q_logo.png")
st.logo(image=str(data_dir), size="large", link="https://www.kaggle.com/datasets/taweilo/taiwan-air-quality-data-20162024")

with st.sidebar:
    st.title("Selection Sidebar")
    st.header("⚙️ Settings")

    max_date = my_data["date"].max().date()
    default_start_date = my_data["date"].min().date()
    default_end_date = my_data["date"].max().date()
    start_date = st.date_input("Start date", default_start_date, min_value=default_start_date, max_value=default_end_date)
    end_date = st.date_input("End date", default_end_date, min_value=default_start_date, max_value=default_end_date)
    time_frame = st.selectbox("Select time frame", ("Daily", "Weekly", "Monthly", "Quarterly"))
    chart_selection = st.selectbox("Select chart type", ("Bar", "Area"))

    match time_frame:
        case "Daily":
            my_display_data = my_data.set_index('date') #aggregate_data(my_data, freq='W-MON', num_cols=num_cols)
        case "Weekly":
            my_display_data = aggregate_data(my_data, freq='W-MON', num_cols=num_cols)
        case "Monthly":
            my_display_data = aggregate_data(my_data, freq='ME', num_cols=num_cols)
        case "Quarterly":
            my_display_data = aggregate_data(my_data, freq='Q', num_cols=num_cols)

st.subheader("Single-variable plots")

metrics = [
    ("PM10", "pm10", '#29b5e8'),
    ("PM2.5", "pm2.5", '#FF9F36'),
    ("PM10 avg", "pm10_avg", '#D45B90'),
    ("PM2.5 avg", "pm2.5_avg", '#7D44CF')
]

cols = st.columns(4)
for col, (title, column, color) in zip(cols, metrics):
    total_value = my_data[column].sum()
    display_metric(col, title, total_value, my_display_data, column, color, time_frame)

st.subheader("Selected Duration")

if time_frame == 'Quarterly':
    start_quarter = custom_quarter(start_date)
    end_quarter = custom_quarter(end_date)
    mask = (my_display_data.index.values >= start_quarter) & (my_display_data.index.values <= end_quarter)
else:
    mask = (my_display_data.index.values >= pd.Timestamp(start_date)) & (my_display_data.index.values <= pd.Timestamp(end_date))
df_filtered = my_display_data.loc[mask]

cols = st.columns(4)
for col, (title, column, color) in zip(cols, metrics):
    display_metric(col, title.split()[-1], df_filtered[column].sum(), df_filtered, column, color, time_frame)

# data display
with st.expander('Sampled DataFrame (Selected time frame)'):
    st.dataframe(df_filtered)