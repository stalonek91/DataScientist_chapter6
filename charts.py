import streamlit as st
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt

def convert_experience_to_list(exp_str):
    if isinstance(exp_str, str):
        if exp_str.startswith(">="):
            return [16]  # Treat ">=16" as [16]
        elif "-" in exp_str:
            start, end = map(int, exp_str.split("-"))
            return list(range(start, end + 1))  # Create a list from start to end
        else:
            return [int(exp_str)]  # Handle single values
    return [0]  # Treat NaN or non-string as [0]

def page_2():
    with st.sidebar:
        gender_options = ["Male", "Female"]
        gender_mapping = {"Male": 0, "Female": 1}
        selected_genders = st.multiselect(
            "Select data per gender",
            gender_options
        )
        
        # Slider for years of experience
        experience_slider = st.slider(
            "Select years of experience",
            min_value=0,
            max_value=16,
            value=(0, 16),  # Default range
            step=1
        )

    csv_file_path = Path('35__welcome_survey_cleaned.csv')
    df = pd.read_csv(csv_file_path, sep=';')

    # Create a new column for years of experience as lists
    df['experience_list'] = df['years_of_experience'].apply(convert_experience_to_list)

    st.title(":man-raising-hand: Ankieta powitalna - dane")
    st.write("USE THE SIDEBAR FOR ADDITIONAL FILTERS")

    if selected_genders:
        title = 'Histogram of Age for ' + ', '.join(selected_genders)  
        numeric_genders = [gender_mapping[gender] for gender in selected_genders]
        df = df[df['gender'].isin(numeric_genders)]
    else:
        title = 'Histogram of Age for Male, Female' 

    # Filter by years of experience using the new list column
    df = df[df['experience_list'].apply(lambda x: any(year in range(experience_slider[0], experience_slider[1] + 1) for year in x))]

    fig, ax = plt.subplots()
    df['age'].hist(bins=10, alpha=0.7, ax=ax)
    
    ax.set_xlabel('User age')  # Use ax to set labels
    ax.set_ylabel('Number of users in age range')
    ax.set_title(title)

    # Display the plot in Streamlit
    st.pyplot(fig)
    