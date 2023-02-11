import streamlit as st 
import pandas as pd
from openbb_terminal.sdk import openbb
from openbb_terminal.config_terminal import theme  # noqa: F401
from openbb_terminal.helper_classes import TerminalStyle
from openbb_terminal import helper_funcs as helper  # noqa: F401
from openbb_terminal.reports import widget_helpers as widgets  # noqa: F401
from openbb_terminal.cryptocurrency.due_diligence.pycoingecko_model import (  # noqa: F401
    Coin,
)
from openbb_terminal.core.library.breadcrumb import Breadcrumb
from openbb_terminal.core.library.trail_map import TrailMap
from openbb_terminal.core.library.breadcrumb import MetadataBuilder

TerminalStyle().applyMPLstyle()
trail = ""
trail_map = TrailMap()
metadata = MetadataBuilder.build(trail=trail, trail_map=trail_map)

openbb = Breadcrumb(
    metadata=metadata,
    trail=trail,
    trail_map=trail_map,
)
st.set_page_config(
layout="wide",
page_title="Joseph Biancamano", 
)
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 
st.set_option('deprecation.showPyplotGlobalUse', False)
col1, col2, col3, col4 = st.columns([25,11,4,10])
with col1:
   st.title('Dashboard Powered By')
   st.write('Built by [Joseph B](https://twitter.com/DirtyDefi)')

with col2:
    st.image("https://raw.githubusercontent.com/OpenBB-finance/OpenBBTerminal/main/images/openbb_logo.png",width=120)
    
with col3:
    st.markdown(""" 
  
    # &
                """)
       
with col4:
    st.image("https://raw.githubusercontent.com/mesmith027/streamlit-roboflow-demo/master/images/streamlit_logo.png",width=180)


with st.container():
    st.sidebar.write('Special thanks to the team at [Openbb](https://openbb.co/) Excited to see what the future holds as the lead the way in open source investment research!')
                     
    st.sidebar.write('Feel free to reach [out](https://twitter.com/DirtyDefi) I love talking anything markets and programming.')
                     
    st.sidebar.write('Please note this app is NOT financial advice. The dashboards is NOT intended to help guide financial decisions!')   

def color_negative_red(val):
    if type(val) != 'str':
        color = 'green' if val >0 else 'red'
        return f'color: {color}'

col1, col2, col3 = st.columns([30,30,30])
with col1:
    st.subheader('World Currencies')
    data = openbb.economy.currencies()
    data[['Chng']] = data[['Chng']].apply(pd.to_numeric)
    data[['%Chng']] = data[['%Chng']].apply(pd.to_numeric)
    st.dataframe(data.style.applymap(color_negative_red, subset=['Chng','%Chng']))
with col2:
    st.subheader('US Indices')
    data = openbb.economy.indices()
    data[['Chg','%Chg']] = data[['Chg','%Chg']].apply(pd.to_numeric)
    st.dataframe(data.style.applymap(color_negative_red, subset=['Chg','%Chg']))   
with col3:
    st.subheader('US Bonds')
    data = openbb.economy.usbonds()
    data[data.columns[1]] = data[data.columns[1]].apply(pd.to_numeric)
    data[data.columns[2]] = data[data.columns[2]].apply(pd.to_numeric)
    data[data.columns[3]] = data[data.columns[3]].apply(pd.to_numeric)
    columns = data.columns[3]
    st.dataframe(data.style.applymap(color_negative_red, subset=[columns]))   
col1, col2=st.columns([22,30])
with col1:
    st.subheader('Commodities')
    data = openbb.economy.futures()
    data[['Chg','%Chg']] = data[['Chg','%Chg']].apply(pd.to_numeric)
    st.dataframe(data.style.applymap(color_negative_red, subset=['Chg','%Chg'])) 
with col2:
    st.subheader('Sectors') 
    st.pyplot(openbb.economy.rtps_chart())
st.title('Economy')
col1,col2=st.columns([55,55]) 
with col1:
    st.pyplot(openbb.economy.inf_chart()) 
with col2:
    st.pyplot(openbb.economy.cpi_chart())   
col1,col2=st.columns([55,55]) 
with col1:
    st.pyplot(openbb.economy.gdp_chart()) 
with col2:
    st.pyplot(openbb.economy.unemp_chart())
st.title('Government Trading & Contracts')
col1, col2=st.columns([50,50])
with col1:
    st.subheader('Government contracts')
    st.dataframe(openbb.stocks.gov.lastcontracts())
    
with col2:
    st.subheader('Congress Latest Trades')
    st.write(openbb.stocks.gov.lasttrades()) 
    
col1, col2=st.columns([50,50])
with col1:
    st.subheader('Senate Latest Trades')
    st.pyplot(openbb.stocks.gov.topbuys_chart(gov_type = "senate", past_transactions_months  = 6))
    
with col2:
    st.subheader('Senate Latest Trades')
    st.pyplot(openbb.stocks.gov.topsells_chart(gov_type = "senate", past_transactions_months  = 6))
    
col1, col2=st.columns([50,50])
with col1:
    st.subheader('Congress Latest Trades')
    st.pyplot(openbb.stocks.gov.topbuys_chart(gov_type = "congress", past_transactions_months  = 6))
    
with col2:
    st.subheader('Congress Latest Trades')
    st.pyplot(openbb.stocks.gov.topsells_chart(gov_type = "congress", past_transactions_months  = 6)) 
st.title('Short Data')
col1,col2=st.columns([35,55]) 
with col1:
    st.subheader('% Float Short & Days to Cover')
    st.dataframe(openbb.stocks.dps.sidtc())
with col2:
    st.subheader('   Dark Pool Short Positions')
    st.dataframe(openbb.stocks.dps.pos())   
st.title('Crypto') 
col1,col2=st.columns([55,55]) 
with col1:
    st.subheader('Bitcoin Circulating Supply')
    st.pyplot(openbb.crypto.onchain.btc_supply_chart()) 
with col2:
    st.subheader('Daily Bitcoin Transactions')
    st.pyplot(openbb.crypto.onchain.btc_transac_chart())

col1,col2=st.columns([55,55]) 
with col1:
    st.subheader('Altcoin Index')
    st.pyplot(openbb.crypto.ov.altindex_chart()) 
with col2:
    st.subheader('Defi TVL')
    st.pyplot(openbb.crypto.defi.stvl_chart(limit=730))
   
col1,col2=st.columns([50,50])
with col1: 
    st.subheader('Top Cryptos') 
    st.dataframe(openbb.crypto.disc.top_coins(source="CoinGecko", limit=50))
with col2:
    st.subheader('Crypto Hacks')
    st.dataframe(openbb.crypto.ov.crypto_hacks())
st.subheader('Enter a ticker below to get price chart, Government Contracts, Insider Activity, and list of suppliers and customers')  
text_input = st.text_input('Symbol')
if text_input:
    data = openbb.stocks.load(text_input)
    df_max_scaled = data.copy()
    st.pyplot(openbb.stocks.candle(symbol=text_input,ma = [50,150,200]))
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader('Government Contracts for {}'.format(text_input))
        st.dataframe(openbb.stocks.gov.contracts(symbol=text_input))

    with col2:
        st.subheader('Insider Activity for {}'.format(text_input))
        st.dataframe(openbb.stocks.ins.act(symbol=text_input))
   
col1, col2 = st.columns(2)
with col1:
    st.subheader('Suppliers of {}'.format(text_input))
    st.dataframe(openbb.stocks.dd.supplier(text_input))

with col2:
    st.subheader('Customers of {}'.format(text_input))
    st.dataframe(openbb.stocks.dd.customer(text_input))
    
col1, col2 = st.columns(2)
with col1:
    st.subheader('Put/Call Ratio of {}'.format(text_input))
    st.pyplot(openbb.stocks.options.pcr_chart(symbol=text_input))

with col2:
    st.subheader('Vol Surface of {}'.format(text_input))
    st.pyplot(openbb.stocks.options.vsurf_chart(symbol=text_input))
    
st.pyplot(openbb.stocks.gov.gtrades_chart(symbol=text_input, gov_type = 'congress'))
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 
