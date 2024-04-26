import pandas as pd
import streamlit as st
import numpy as np
from ydata_profiling import ProfileReport
from streamlit_pandas_profiling import st_profile_report

st.set_page_config(layout="wide")
st.title(":bar_chart: Dataset")

tab1, tab2 = st.tabs(["Data Description", "Dashboard Data"])
with tab1:
    df = pd.read_excel("df_dashboard.xlsx")
    df_profile = ProfileReport(df, explorative=True)
    st_profile_report(df_profile)
    #st.dataframe(df.head(20))
#with tab2:
    #df = pd.read_excel("df_dashboard.xlsx",index_col=0)
    #st.dataframe(df.head(20))
