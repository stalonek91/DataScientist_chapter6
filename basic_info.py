import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import missingno as msno
from pathlib import Path
st.set_page_config(layout="centered")

csv_file_path = Path('35__welcome_survey_cleaned.csv')
df = pd.read_csv(csv_file_path, sep=';')

st.title(':file_cabinet: Data scientist pandas data')

t1,t2 = st.tabs(["Generic Data", "Missing values"])

with t1:
    c1,c2,c3 = st.columns([1,1,1])

    with c1:
        
        st.metric("Ilosc wierszy", len(df))

    with c2:
        st.metric("Ilosc kolumn", len(df.columns))

    with c3:
        st.metric("Kolumny z brakujacymi wartosciami", df.isnull().any().sum())

    st.write('df.sample(8)')
    st.dataframe(df.sample(8), hide_index=True)
    st.write('DF.describe()')
    st.dataframe(df.describe())
    st.write('df.columns')
    st.dataframe(df.columns)

with t2:
    col1, col2 = st.columns([2,1])
    with col1:
        missing_columns_df = df[df.columns[df.isnull().any()]]

        # Streamlit App Title
        st.title("Missing Values Matrix (Filtered)")

        # Create the nullity matrix and display it in Streamlit
        fig, ax = plt.subplots(figsize=(12, 8))  # Create a figure
        msno.matrix(missing_columns_df, ax=ax, sparkline=False)  # Generate missingno plot
        ax.set_title("Missing Values Matrix (Filtered)", fontsize=16)  # Add title

        # Render the plot in Streamlit
        st.pyplot(fig)

    with col2:
        missing_count = df.isnull().sum()

        # Compute the percentage of missing values per column
        missing_percent = (missing_count / len(df)) * 100

        # Create a DataFrame to display missing values and percentages
        missing_summary = pd.DataFrame({
            "Missing Values Count": missing_count,
            "Missing Values (%)": missing_percent
        })

        # Display the DataFrame in Streamlit
        st.title("Missing Values Summary")
        st.dataframe(missing_summary)

            
