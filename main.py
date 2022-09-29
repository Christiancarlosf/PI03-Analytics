import streamlit as st
import pandas as pd
import numpy as np
import requests
from charts import get_candlestick_plot, data
import plotly.graph_objects as go


#Configuramos pag
st.set_page_config(page_title = 'ChrisDS03-PI03' ,layout='wide')



# Monedas a visualizar 
coins = ['BTC', 'ETH', 'BNB', 'AXS', 'DOGE', 'MATIC','SOL', 'DOT', 'LTC', 'TRX']

coin = st.sidebar.selectbox('Search', coins)


#Configuramos el request

url = f'https://ftx.com/api/markets/{coin}/USD'
request = requests.get(url).json()
df = pd.Series(request['result'])

#Añadimos metricas

st.sidebar.metric("Price", round(df['price'],3))
st.sidebar.metric("24h Low", round(df['priceLow24h'],3))
st.sidebar.metric("24h High", round(df['priceHigh24h'],3))
st.sidebar.metric("24h Volume(USD)",(round(df['volumeUsd24h'],3)))
#variance = np.var(df['close'])
#st.sidebar.metric("Variance", f'{variance:f}')
#df



#Configuramos y agregamos charts
st.title(f"{coin}/USD - Chart")



dfh = data(coin)

ma1 = st.sidebar.number_input(
    'Moving Average #1 Length',
    value = 10,
    min_value = 1,
    max_value = 120,
    step = 1,    )

dfh[f'{ma1}_ma'] = dfh['close'].rolling(ma1).mean()


st.plotly_chart(get_candlestick_plot(dfh, ma1, coin),use_container_width = True)



