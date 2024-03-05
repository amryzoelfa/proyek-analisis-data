import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from datetime import datetime

sns.set(style='darkgrid')

# Load data
df = pd.read_csv("main_data.csv", parse_dates=['dteday'])

# Menentukan tanggal awal dan tanggal akhir
min_date = df['dteday'].min().date()
max_date = df['dteday'].max().date()

# Sidebar untuk pemilihan rentang tanggal
with st.sidebar:
    st.title("Bike Sharing Dashboard")
    st.image("dicoding.png")
    start_date = st.date_input("Pilih tanggal mulai", min_value=min_date, max_value=max_date, value=min_date)
    end_date = st.date_input("Pilih tanggal akhir", min_value=min_date, max_value=max_date, value=max_date)

df_filtered = df[(df['dteday'] >= pd.to_datetime(start_date)) & (df['dteday'] <= pd.to_datetime(end_date))]


def create_daily_rentals_df(df):
    daily_rentals_df = df.resample(rule='D', on='dteday').agg({
        "cnt": "sum"
    }).reset_index()
    daily_rentals_df.rename(columns={"cnt": "total_peminjaman"}, inplace=True)
    return daily_rentals_df

def create_weather_comparison_df(df):
    weather_comparison_df = df.groupby("weathersit").agg({"cnt": "sum"}).reset_index()
    weather_comparison_df.rename(columns={"cnt": "total_peminjaman", "weathersit": "kondisi_cuaca"}, inplace=True)
    return weather_comparison_df

# Peminjaman Harian
daily_rentals_df = create_daily_rentals_df(df_filtered)

st.subheader('Peminjaman Sepeda Harian')
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(daily_rentals_df['dteday'], daily_rentals_df['total_peminjaman'], marker='o', linestyle='-')
ax.set_xlabel('Tanggal')
ax.set_ylabel('Jumlah Peminjaman')
ax.set_title('Peminjaman Sepeda Harian')
st.pyplot(fig)

# Kondisi Cuaca
weather_comparison_df = create_weather_comparison_df(df_filtered)

st.subheader('Peminjaman berdasarkan Kondisi Cuaca')
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(data=weather_comparison_df, x='kondisi_cuaca', y='total_peminjaman', ax=ax)
ax.set_xlabel('Kondisi Cuaca')
ax.set_ylabel('Jumlah Peminjaman')
ax.set_title('Peminjaman Sepeda berdasarkan Kondisi cuaca')
st.pyplot(fig)

st.caption('Copyright © 2023')
