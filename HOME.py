import streamlit as st
import requests
from streamlit_lottie import st_lottie
from streamlit_plotly_events import plotly_events

st.set_page_config(layout="wide")
st.title(':blue[Tình trạng khách hàng rời bỏ trong ngành viễn thông] :satellite_antenna:')

def load_lottieurl(url: str):
 r = requests.get(url)
 if r.status_code != 200:
    return None
 return r.json()
lottie_school = load_lottieurl(
 "https://lottie.host/45210b36-862b-4682-b435-74ad382658d6/hnTOu4H4qg.json"
)
st_lottie(lottie_school, height=500)
