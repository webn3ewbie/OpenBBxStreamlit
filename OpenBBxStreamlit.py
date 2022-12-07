import streamlit as st 
from openbb_terminal.sdk import openbb
import pandas as pd

st.set_page_config(
layout="wide"
)
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
    st.sidebar.write('Special thanks to the team at [Openbb](https://openbb.co/) Excited to see what the future holds as the lead the way in open source investment research!'
                     'Feel free to reach [out](https://twitter.com/DirtyDefi) I love talking anything markets and programming. '
                     'Please note this app is NOT financial advice. The dashboards is NOT intended to help guide financial decisions!')
    st.sidebar.write('')
    

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
    st.subheader('Congress Latest Trades')
    st.write(openbb.stocks.gov.lasttrades()) 
st.title('Short Data')
col1,col2=st.columns([35,55])
with col1:
    st.subheader('Highest cost to borrow')
    st.write("[Interactive Brokers]")
    st.dataframe(openbb.stocks.dps.ctb())
with col2:
    st.subheader('Stock with high short interest')
    st.write(openbb.stocks.dps.hsi())

col1,col2=st.columns([35,55]) 
with col1:
    st.subheader('% Float Short & Days to Cover')
    st.dataframe(openbb.stocks.dps.sidtc())
with col2:
    st.subheader('   Dark Pool Short Positions')
    st.dataframe(openbb.stocks.dps.pos())

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
    data = openbb.crypto.ov.markets()
    data['pct_change_24h'] = data['pct_change_24h' ].apply(pd.to_numeric)
    data['mcap_change_24h'] = data['mcap_change_24h' ].apply(pd.to_numeric)
    data['pct_change_1h'] = data['pct_change_1h' ].apply(pd.to_numeric)
    data['pct_from_ath'] = data['pct_from_ath' ].apply(pd.to_numeric)
    st.dataframe(data.style.applymap(color_negative_red, subset=['pct_change_24h','mcap_change_24h','pct_change_1h','pct_from_ath']))   
with col2:
    st.subheader('Crypto Hacks')
    st.dataframe(openbb.crypto.ov.crypto_hacks())
st.subheader('Enter a ticker below to get price chart, Government Contracts, Insider Activity, and list of suppliers and customers')  
text_input = st.text_input('Symbol')
if text_input:
    data = openbb.stocks.load(text_input)
    df_max_scaled = data.copy()
    st.pyplot(openbb.stocks.candle(symbol=text_input))
    
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
    
