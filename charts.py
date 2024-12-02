import streamlit as st
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt


def page_2():

    age_tab, hobby_tab, prof_tab = st.tabs([
        "Age analysis",
        "Hobby analysis",
        "Career analysis"
    ])

    with age_tab:
        with st.sidebar:
            gender_options = ["Male", "Female"]
            gender_mapping = {"Male": 0, "Female": 1}
            selected_genders = st.multiselect(
                "Select data per gender",
                gender_options
            )
            
        csv_file_path = Path('35__welcome_survey_cleaned.csv')
        df = pd.read_csv(csv_file_path, sep=';')

        st.title(":man-raising-hand: Ankieta powitalna - dane")

        st.write("USE THE SIDEBAR FOR ADDITIONAL FILTERS")

        
        if selected_genders:
            title = 'Histogram of Age for ' + ', '.join(selected_genders)  
            numeric_genders = [gender_mapping[gender] for gender in selected_genders]
            df = df[df['gender'].isin(numeric_genders)]
        else:
            title = 'Histogram of Age for Male, Female' 

        fig, ax = plt.subplots()
        df['age'].hist(bins=10, alpha=0.7, ax=ax)
        
        ax.set_xlabel('Age')  # Use ax to set labels
        ax.set_ylabel('Frequency')
        ax.set_title(title)

        # Display the plot in Streamlit
        st.pyplot(fig)
    
    with hobby_tab:
        st.write('hobby')

    with prof_tab:
        st.write('Kariera')
        