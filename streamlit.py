import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
pd.options.mode.chained_assignment = None

csv_file = {
   'aotizhongxin' : 'PRSA_Data_Aotizhongxin_20130301-20170228.csv',
   'changping' :  'PRSA_Data_Changping_20130301-20170228.csv',
   'dingling' :  'PRSA_Data_Dingling_20130301-20170228.csv',
   'dongsi' :  'PRSA_Data_Dongsi_20130301-20170228.csv',
   'guanyuan' :  'PRSA_Data_Guanyuan_20130301-20170228.csv',
   'gucheng' :  'PRSA_Data_Gucheng_20130301-20170228.csv',
   'huairou' :  'PRSA_Data_Huairou_20130301-20170228.csv',
   'nongzhanguan' :  'PRSA_Data_Nongzhanguan_20130301-20170228.csv',
   'shunyi' :  'PRSA_Data_Shunyi_20130301-20170228.csv',
   'tiantan' :  'PRSA_Data_Tiantan_20130301-20170228.csv',
   'wanliu' :  'PRSA_Data_Wanliu_20130301-20170228.csv',
   'wanshouxigong' :  'PRSA_Data_Wanshouxigong_20130301-20170228.csv',
}
df_list = {}
for key,file in csv_file.items():
    df_list[key] = pd.read_csv('Data/'+file, delimiter=",")
    df_list[key].bfill(inplace = True)
    df_list[key]['datetime'] = pd.to_datetime(df_list[key][['year', 'month', 'day']])
    df_list[key] = df_list[key].groupby(['station', 'datetime']).agg({
        'year'  : lambda x: x.iloc[0],
        'month'  : lambda x: x.iloc[0],
        'day'  : lambda x: x.iloc[0],
        'PM2.5' : 'mean',
        'PM10' : 'mean',
        'SO2' : 'mean',
        'NO2' : 'mean',
        'CO' : 'mean',
        'O3' : 'mean',
        'TEMP' : 'mean',
        'PRES' : 'mean',
        'DEWP' : 'mean',
        'RAIN' : 'mean',
        'wd' : lambda x: x.mode().iloc[0],
        'WSPM' : 'mean',
        }).reset_index()

combined_df = pd.concat(df_list, ignore_index=True)


min_date = combined_df["datetime"].min()
max_date = combined_df["datetime"].max()
with st.sidebar:
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )
    grouping = st.radio(
        label="Jarak Waktu",
        options=('Tahunan', 'Bulanan', 'Harian'),
        horizontal=True,
        help="Pilih jarak waktu",
        index = 1
    )

    main_df = combined_df[(combined_df['datetime'] >= pd.to_datetime(start_date)) & 
                        (combined_df['datetime'] <= pd.to_datetime(end_date))].copy()
    if grouping == 'Tahunan':
        main_df['datetime'] = pd.to_datetime(main_df[['year', 'month', 'day']]).dt.to_period('Y')
        main_df = main_df.groupby(['station', 'datetime']).agg({
            'PM2.5' : 'mean',
            'PM10' : 'mean',
            'SO2' : 'mean',
            'NO2' : 'mean',
            'CO' : 'mean',
            'O3' : 'mean',
            'TEMP' : 'mean',
            'PRES' : 'mean',
            'DEWP' : 'mean',
            'RAIN' : 'mean',
            'wd' : lambda x: x.mode().iloc[0],
            'WSPM' : 'mean',
        }).reset_index()
    elif grouping == 'Bulanan':
        main_df['datetime'] = pd.to_datetime(main_df[['year', 'month', 'day']]).dt.to_period('M')
        main_df = main_df.groupby(['station', 'datetime']).agg({
            'PM2.5' : 'mean',
            'PM10' : 'mean',
            'SO2' : 'mean',
            'NO2' : 'mean',
            'CO' : 'mean',
            'O3' : 'mean',
            'TEMP' : 'mean',
            'PRES' : 'mean',
            'DEWP' : 'mean',
            'RAIN' : 'mean',
            'wd' : lambda x: x.mode().iloc[0],
            'WSPM' : 'mean',
        }).reset_index()
    elif grouping == 'Harian':
        main_df['datetime'] = pd.to_datetime(main_df[['year', 'month', 'day']]).dt.to_period('D')
        main_df = main_df.groupby(['station', 'datetime']).agg({
            'PM2.5' : 'mean',
            'PM10' : 'mean',
            'SO2' : 'mean',
            'NO2' : 'mean',
            'CO' : 'mean',
            'O3' : 'mean',
            'TEMP' : 'mean',
            'PRES' : 'mean',
            'DEWP' : 'mean',
            'RAIN' : 'mean',
            'wd' : lambda x: x.mode().iloc[0],
            'WSPM' : 'mean',
        }).reset_index()
st.header('Air Quality Dashboard :wind_blowing_face:')
with st.container():
    st.subheader('Data per station')
    per_station = st.radio(
        label="Pilih station",
        options=('Aotizhongxin', 'Changping', 'Dingling', 'Dongsi', 'Guanyuan', 'Gucheng',
                    'Huairou', 'Nongzhanguan', 'Shunyi', 'Tiantan', 'Wanliu', 'Wanshouxigong'),
        horizontal=True,
        help="Pilih stasiun untuk menampilkan data.",
        index = 0
    )
    with st.expander('Pilih variabel'):
        per_station_variable = {}
        per_station_selected_variable = []
        for i in ('PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3', 'TEMP', 'PRES', 'DEWP', 'RAIN', 'WSPM'):
            per_station_variable[i] = st.checkbox(i)
            if per_station_variable[i]:
                per_station_selected_variable.append(i)
    station_df = main_df[main_df['station'] == per_station].copy()
    station_df = station_df[['datetime', 'station'] + per_station_selected_variable]
    station_df['datetime'] = pd.to_datetime(station_df['datetime'].dt.to_timestamp())
    fig, ax = plt.subplots(figsize=(12, 5))
    for variable in per_station_selected_variable:
        ax.plot(station_df['datetime'], station_df[variable],label=variable, marker='o')
    ax.legend()
    st.pyplot(fig)

with st.container():
    st.subheader('Data per variabel')
    per_variable = st.radio(
        label="Pilih variable",
        options=('PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3', 'TEMP', 'PRES', 'DEWP', 'RAIN', 'wd', 'WSPM'),
        horizontal=True,
        help="Pilih variable untuk menampilkan data.",
        index = 0
    )

    with st.expander('Pilih station'):
        per_variable_station = {}
        per_variable_selected_station = []
        for i in ('Aotizhongxin', 'Changping', 'Dingling', 'Dongsi', 'Guanyuan', 'Gucheng',
                     'Huairou', 'Nongzhanguan', 'Shunyi', 'Tiantan', 'Wanliu', 'Wanshouxigong'):
            per_variable_station[i] = st.checkbox(i)
            if per_variable_station[i]:
                per_variable_selected_station.append(i)
    variable_df = main_df[main_df['station'].isin(per_variable_selected_station)].copy()
    variable_df = variable_df[['datetime', 'station', per_variable]]
    variable_df['datetime'] = pd.to_datetime(variable_df['datetime'].dt.to_timestamp())
    for station in per_variable_selected_station:
        ax.plot(variable_df[variable_df['station'] == station]['datetime'], variable_df[variable_df['station'] == station][per_variable], label=station, marker='o')
    ax.legend()
    st.pyplot(fig)
   