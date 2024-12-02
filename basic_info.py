import streamlit as st
import pandas as pd
from pathlib import Path

csv_file_path = Path('35__welcome_survey_cleaned.csv')
df = pd.read_csv(csv_file_path, sep=';')

st.title("Page 1")


st.title(':file_cabinet: Data scientist pandas data')

c1,c2,c3 = st.columns([1,1,1])

with c1:
    
    st.metric("Ilosc wierszy", len(df))

with c2:
    st.metric("Ilosc kolumn", len(df.columns))

with c3:
    st.metric("Kolumny z brakujacymi wartosciami", df.isnull().any().sum())

st.write('DataFrame data analytics info')
st.dataframe(df.sample(8), hide_index=True)
st.dataframe(df.describe())
st.dataframe(df.columns)
