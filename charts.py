import streamlit as st
import pandas as pd
import requests
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Instanciamos para obtener datos historicos
@st.cache(allow_output_mutation=True)
def data(coin):
    resolution = 60*60
    url = f'https://ftx.com/api/markets/{coin}/USD/candles?resolution={resolution}'
    request = requests.get(url).json()
    dfh = pd.DataFrame(request['result'])
    dfh['date'] = pd.to_datetime(dfh['startTime']).dt.date
    dfh = dfh.drop(columns=['startTime', 'time'])
    return dfh


#Instanciamos para generar los graficos de velas juntos
def get_candlestick_plot(
    df: pd.DataFrame,
    ma1: int,
    ticker: str):

    fig = make_subplots(
        rows = 2,
        cols = 1,
        shared_xaxes = True,
        vertical_spacing = 0.2,
        subplot_titles = (f'{ticker} Stock Price', 'Volume Chart'),
        row_width = [1.5, 2]
    )
    
    fig.add_trace(
        go.Candlestick(
            x = df['date'],
            open = df['open'], 
            high = df['high'],
            low = df['low'],
            close = df['close'],
            name = 'Candlestick chart'
        ),
        row = 1,
        col = 1,
    )
    fig.add_trace(
        go.Line(x = df['date'], y = df[f'{ma1}_ma'], name = f'{ma1} SMA'),
        row = 1,
        col = 1,
    )
    
    fig.add_trace(
        go.Bar(x = df['date'], y = round(df['volume'],2), name = 'Volume'),
        row = 2,
        col = 1,
    )
    
    fig['layout']['yaxis']['title'] = 'Price'
    fig['layout']['yaxis2']['title'] = 'Volume'
    
    fig.update_xaxes(
        rangeslider_visible = False,
    )
    
    return fig

