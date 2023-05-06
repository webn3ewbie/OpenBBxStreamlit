import os
import pandas as pd
import streamlit as st
from openbb_terminal.core.plots.plotly_helper import OpenBBFigure, theme  # noqa: F401
from openbb_terminal.sdk import openbb

pd.options.plotting.backend = "plotly"

FRED_KEY = os.environ.get("FRED_KEY", "REPLACE_ME")
openbb.keys.fred(key=FRED_KEY, persist=True)

st.set_page_config(
    layout="wide",
    page_title="OpenBB X Streamlit",
)

hide_streamlit_style = """
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)


def display_chart(fig: OpenBBFigure, nticks: bool = True):
    if not isinstance(fig, OpenBBFigure):
        return st.write("No data available")

    if len(fig.layout.title.text) > 40:
        font_size = 14 if len(fig.layout.title.text) < 70 else 12
        fig.update_layout(title=dict(font=dict(size=font_size)))

    if nticks:
        fig.update_layout(xaxis=dict(nticks=5))

    fig.update_layout(
        legend=dict(
            bgcolor="rgba(0,0,0,0.5)",
            bordercolor="#F5EFF3",
            borderwidth=1,
            x=0.99,
            xanchor="right",
        ),
    )

    st.plotly_chart(
        fig.show(external=True),
        use_container_width=True,
        config=dict(
            scrollZoom=True,
            displaylogo=False,
            displayModeBar=False,
        ),
    )


col1, col2, col3, col4 = st.columns([25, 11, 4, 10])
with col1:
    st.title("Dashboard Powered By")
    st.write("Built by [Joseph B](https://twitter.com/DirtyDefi)")

with col2:
    st.image(
        "https://raw.githubusercontent.com/OpenBB-finance/OpenBBTerminal/main/images/openbb_logo.png",
        width=120,
    )

with col3:
    st.markdown(
        """

    # &
                """
    )

with col4:
    st.image(
        "https://raw.githubusercontent.com/mesmith027/streamlit-roboflow-demo/master/images/streamlit_logo.png",
        width=180,
    )


with st.container():
    st.sidebar.write(
        "Special thanks to the team at [Openbb](https://openbb.co/) Excited to see "
        "what the future holds as the lead the way in open source investment research!"
    )

    st.sidebar.write(
        "Feel free to reach [out](https://twitter.com/DirtyDefi) I love talking anything markets and programming."
    )

    st.sidebar.write(
        "Please note this app is NOT financial advice. The dashboards is NOT intended to help guide financial decisions!"
    )


def color_negative_red(val):
    if type(val) != "str":
        color = "green" if val > 0 else "red"
        return f"color: {color}"


@st.cache_resource(ttl=300, show_spinner=False)
def cached_data():
    col1, col2, col3 = st.columns([30, 30, 30])
    with col1:
        st.subheader("World Currencies")
        data = openbb.economy.currencies()
        data[["Chng"]] = data[["Chng"]].apply(pd.to_numeric)
        data[["%Chng"]] = data[["%Chng"]].apply(pd.to_numeric)
        data = data.set_index(data.columns[0])
        st.dataframe(data.style.applymap(color_negative_red, subset=["Chng", "%Chng"]))

    with col2:
        st.subheader("US Indices")
        data = openbb.economy.indices()
        data[["Chg", "%Chg"]] = data[["Chg", "%Chg"]].apply(pd.to_numeric)
        data = data.set_index(data.columns[0])
        st.dataframe(data.style.applymap(color_negative_red, subset=["Chg", "%Chg"]))

    with col3:
        st.subheader("US Bonds")
        data = openbb.economy.usbonds()
        data[data.columns[1]] = data[data.columns[1]].apply(pd.to_numeric)
        data[data.columns[2]] = data[data.columns[2]].apply(pd.to_numeric)
        data[data.columns[3]] = data[data.columns[3]].apply(pd.to_numeric)
        columns = data.columns[3]
        data = data.set_index(data.columns[0])
        st.dataframe(data.style.applymap(color_negative_red, subset=[columns]))

    col1, col2, col3 = st.columns([30, 30, 30])
    with col1:
        st.subheader("Commodities")
        data = openbb.economy.futures()
        data[["Chg", "%Chg"]] = data[["Chg", "%Chg"]].apply(pd.to_numeric)
        data = data.set_index(data.columns[0])
        st.dataframe(data.style.applymap(color_negative_red, subset=["Chg", "%Chg"]))

    with col2:
        st.subheader("Sectors")
        display_chart(openbb.economy.rtps_chart(external_axes=True))

    with col3:
        st.subheader("Economic Events")
        data = openbb.economy.events()
        data = data.set_index(data.columns[0])
        st.dataframe(data)

    st.title("Economy")
    col1, col2 = st.columns([55, 55])
    with col1:
        display_chart(
            openbb.economy.fred_chart(series_ids=["CPIAUCSL"], external_axes=True)
        )
    with col2:
        display_chart(
            openbb.economy.fred_chart(series_ids=["FPCPITOTLZGUSA"], external_axes=True)
        )

    col1, col2 = st.columns([55, 55])
    with col1:
        display_chart(
            openbb.economy.fred_chart(series_ids=["UNRATE"], external_axes=True)
        )

    with col2:
        display_chart(
            openbb.economy.fred_chart(series_ids=["FEDFUNDS"], external_axes=True)
        )
    st.title("Government Trading & Contracts")
    col1, col2 = st.columns([50, 50])
    with col1:
        st.subheader("Government Latest Contracts")
        data = openbb.stocks.gov.lastcontracts()
        data = data.set_index(data.columns[0])
        st.dataframe(data)

    with col2:
        st.subheader("Congress Latest Trades")
        data = openbb.stocks.gov.lasttrades()
        data = data.set_index(data.columns[0])
        st.write(data)

    col1, col2 = st.columns([50, 50])
    with col1:
        st.subheader("Senate Latest Trades")
        display_chart(
            openbb.stocks.gov.topbuys_chart(
                gov_type="senate", past_transactions_months=6, external_axes=True
            ),
            False,
        )

    with col2:
        st.subheader("Senate Latest Trades")
        display_chart(
            openbb.stocks.gov.topsells_chart(
                gov_type="senate", past_transactions_months=6, external_axes=True
            ),
            False,
        )

    col1, col2 = st.columns([50, 50])
    with col1:
        st.subheader("Congress Latest Trades")
        display_chart(
            openbb.stocks.gov.topbuys_chart(
                gov_type="congress", past_transactions_months=6, external_axes=True
            ),
            False,
        )

    with col2:
        st.subheader("Congress Latest Trades")
        display_chart(
            openbb.stocks.gov.topsells_chart(
                gov_type="congress", past_transactions_months=6, external_axes=True
            ),
            False,
        )

    st.title("Short Data")
    col1, col2 = st.columns([35, 55])
    with col1:
        st.subheader("% Float Short & Days to Cover")
        data = openbb.stocks.dps.sidtc()
        data = data.set_index(data.columns[0])
        st.dataframe(data)
    with col2:
        st.subheader("   Dark Pool Short Positions")
        data = openbb.stocks.dps.pos()
        data = data.set_index(data.columns[0])
        st.dataframe(data)

    st.title("Crypto")
    col1, col2 = st.columns([55, 55])
    with col1:
        st.subheader("Bitcoin Circulating Supply")
        display_chart(openbb.crypto.onchain.btc_supply_chart(external_axes=True))
    with col2:
        st.subheader("Daily Bitcoin Transactions")
        display_chart(openbb.crypto.onchain.btc_transac_chart(external_axes=True))

    col1, col2 = st.columns([55, 55])
    with col1:
        st.subheader("Altcoin Index")
        display_chart(openbb.crypto.ov.altindex_chart(external_axes=True))
    with col2:
        st.subheader("Defi TVL")
        display_chart(openbb.crypto.defi.stvl_chart(limit=730, external_axes=True))

    col1, col2 = st.columns([50, 50])
    with col1:
        st.subheader("Top Cryptos")
        data = openbb.crypto.disc.top_coins(source="CoinGecko", limit=50)
        data = data.set_index(data.columns[0])
        st.dataframe(data)

    with col2:
        st.subheader("Crypto Hacks")
        data = openbb.crypto.ov.crypto_hacks()
        data = data.set_index(data.columns[0])
        st.dataframe(data)


cached_data()

st.subheader(
    "Enter a ticker below to get price chart, "
    "Government Contracts, Insider Activity, and list of suppliers and customers"
)
text_input = st.text_input("Symbol").upper()


def valid_dataframe(obj):
    if not isinstance(obj, pd.DataFrame) or obj.empty:
        st.write("No data available")
    return isinstance(obj, pd.DataFrame) and not obj.empty


if text_input:
    data = openbb.stocks.load(text_input)
    df_max_scaled = data.copy()

    col1, col2 = st.columns(2)
    with col1:
        st.subheader(f"Government Contracts for {text_input}")
        data = openbb.stocks.gov.contracts(symbol=text_input)
        if valid_dataframe(data):
            data = data.set_index(data.columns[0])
            st.dataframe(data)

    with col2:
        st.subheader(f"Insider Activity for {text_input}")
        data = openbb.stocks.ins.act(symbol=text_input)
        if valid_dataframe(data):
            data = data.set_index(data.columns[0])
            st.dataframe(data)

    col1, col2 = st.columns(2)
    with col1:
        st.subheader(f"Suppliers of {text_input}")
        data = openbb.stocks.fa.supplier(symbol=text_input)
        if valid_dataframe(data):
            data = data.set_index(data.columns[0])
            st.dataframe(data)

    with col2:
        st.subheader(f"Customers of {text_input}")
        data = openbb.stocks.fa.customer(symbol=text_input)
        if valid_dataframe(data):
            data = data.set_index(data.columns[0])
            st.dataframe(data)

    col1, col2 = st.columns(2)
    with col1:
        st.subheader(f"Put/Call Ratio of {text_input}")
        display_chart(
            openbb.stocks.options.pcr_chart(symbol=text_input, external_axes=True)
        )

    with col2:
        st.subheader(f"Vol Surface of {text_input}")
        display_chart(
            openbb.stocks.options.vsurf_chart(symbol=text_input, external_axes=True)
        )

    with st.container():
        display_chart(
            openbb.stocks.gov.gtrades_chart(
                symbol=text_input, gov_type="congress", external_axes=True
            )
        )

