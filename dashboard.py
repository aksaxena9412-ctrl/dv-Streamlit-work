import streamlit as st
import pandas as pd
import plotly.express as px

st.title("Environmental Pollution Dashboard")
st.write("Air quality data across Indian cities")

df = pd.read_csv(r"C:\Users\dell\OneDrive\Documents\Streamlit\city_day.csv", encoding='latin-1')
df['Date'] = pd.to_datetime(df['Date'])

st.dataframe(df.head())

st.sidebar.header("Filters")
cities = st.sidebar.multiselect("Select Cities", options=df["City"].unique(), default=list(df["City"].unique()[:2]))
date_range = st.sidebar.date_input("Select Date Range", value=[df["Date"].min(), df["Date"].max()])
pm25_range = st.sidebar.slider("PM2.5 Range", min_value=float(df["PM2.5"].min()), max_value=float(df["PM2.5"].max()), value=(float(df["PM2.5"].min()), float(df["PM2.5"].max())))

if len(date_range) == 2:
    filtered_df = df[(df["City"].isin(cities)) & (df["Date"] >= pd.to_datetime(date_range[0])) & (df["Date"] <= pd.to_datetime(date_range[1])) & (df["PM2.5"] >= pm25_range[0]) & (df["PM2.5"] <= pm25_range[1])]
else:
    filtered_df = df[(df["City"].isin(cities)) & (df["PM2.5"] >= pm25_range[0]) & (df["PM2.5"] <= pm25_range[1])]

col1, col2, col3 = st.columns(3)
col1.metric("Average PM2.5", f"{filtered_df['PM2.5'].mean():.2f}")
col2.metric("Highest PM2.5", f"{filtered_df['PM2.5'].max():.2f}")
col3.metric("Lowest PM2.5", f"{filtered_df['PM2.5'].min():.2f}")

st.subheader("PM2.5 Trend Over Time")
fig1 = px.line(filtered_df, x="Date", y="PM2.5", color="City")
st.plotly_chart(fig1)

st.subheader("Average PM2.5 by City")
avg_data = filtered_df.groupby("City")["PM2.5"].mean().reset_index()
fig2 = px.bar(avg_data, x="City", y="PM2.5", color="PM2.5")
st.plotly_chart(fig2)

st.subheader("PM2.5 vs Temperature")
fig3 = px.scatter(filtered_df, x="PM2.5", y="NO2", color="City")
st.plotly_chart(fig3)

st.subheader("Filtered Data")
st.dataframe(filtered_df)
csv = filtered_df.to_csv(index=False).encode('utf-8')
st.download_button("Download CSV", data=csv, file_name="data.csv")

st.subheader("Summary")
st.write(f"Total records: {len(filtered_df)}")
st.write(f"Cities: {', '.join(cities)}")
if len(filtered_df) > 0:
    worst = filtered_df.loc[filtered_df['PM2.5'].idxmax()]
    st.write(f"Highest pollution: {worst['City']} on {worst['Date'].strftime('%Y-%m-%d')}")
    
filtered_df["Level"] = filtered_df["PM2.5"].apply(lambda x: "Good" if x <= 30 else ("Moderate" if x <= 60 else ("Poor" if x <= 90 else "Hazardous")))
st.bar_chart(filtered_df["Level"].value_counts())
