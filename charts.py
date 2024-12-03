import streamlit as st
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns

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

    csv_file_path = Path('35__welcome_survey_cleaned.csv')
    df = pd.read_csv(csv_file_path, sep=';')

    age_tab, hobby_tab, prof_tab = st.tabs(
        ["Participant Age", "Participant Hobby", "Participant career"
                                            ])

    with age_tab:
        with st.sidebar:
            gender_options = ["Male", "Female"]
            gender_mapping = {"Male": 0, "Female": 1}
            selected_genders = st.multiselect(
                "Select data per gender",
                gender_options
            )
            
            # New multiselect for favorite animals
            animal_options = ["Psy", "Koty", "Inne", "Brak ulubionych", "Koty i Psy"]
            selected_animals = st.multiselect(
                "Select favorite animals",
                animal_options
            )       

            # New multiselect for education levels
            edu_level_options = df['edu_level'].unique().tolist()  # Get unique education levels
            selected_edu_levels = st.multiselect(
                "Select education levels",
                edu_level_options
            )       

            # Slider for years of experience
            experience_slider = st.slider(
                "Select years of experience",
                min_value=0,
                max_value=16,
                value=(0, 16),  # Default range
                step=1
            )

            

        

        # Create a new column for years of experience as lists
        df['experience_list'] = df['years_of_experience'].apply(convert_experience_to_list)

        st.title(":man-raising-hand: Participants survey data")
        st.write("USE THE SIDEBAR FOR ADDITIONAL FILTERS")

        # Initialize the title
        title = 'Histogram of Age for:'

        # Filter by gender and update the title
        if selected_genders:
            title += '\n - ' + ', '.join(selected_genders)
            numeric_genders = [gender_mapping[gender] for gender in selected_genders]
            df = df[df['gender'].isin(numeric_genders)]
        else:
            title += '\n - Male, Female'  # Default if no gender selected

        # Create a title for the selected years of experience
        experience_min, experience_max = experience_slider
        experience_title = "All Years of Experience" if (experience_min == 0 and experience_max == 16) else f"Years of Experience: {experience_min} to {experience_max}"
        title += '\n - ' + experience_title

        # Filter by years of experience using the new list column
        df = df[df['experience_list'].apply(lambda x: any(year in range(experience_min, experience_max + 1) for year in x))]

        # New filtering based on selected favorite animals
        if selected_animals:
            title += '\n - Favorite animal: ' + ', '.join(selected_animals)
            df = df[df['fav_animals'].isin(selected_animals)]

        # New filtering based on selected education levels
        if selected_edu_levels:
            title += '\n - Education level: ' + ', '.join(selected_edu_levels)
            df = df[df['edu_level'].isin(selected_edu_levels)]

        # Remove the last newline character for cleaner output
        title = title.strip()

        fig, ax = plt.subplots()
        sns.histplot(df['age'], bins=10, kde=False, ax=ax, alpha=0.7)
        
        ax.set_xlabel('User age')  # Use ax to set labels
        ax.set_ylabel('Number of users in age range')
        ax.set_title(title)  # Updated title

        # Display the plot in Streamlit
        st.pyplot(fig)
        
        st.write("Sample of data")

        st.dataframe(df.sample(n=min(10, len(df))))


    with hobby_tab:
        # Extract hobby-related columns
        hobby_columns = ["hobby_art", "hobby_books", "hobby_movies", 
                        "hobby_other", "hobby_sport", "hobby_video_games"]

        # Initialize the title
        hobby_title = 'Participants by Hobby'

        filter_option = st.radio(
            "Select filter type",
            ("Custom Filters", "Gender Filter")
        )

        if filter_option == 'Custom Filters':

            # Apply the same filtering as in the histogram
            # Filter by gender
            if selected_genders:
                numeric_genders = [gender_mapping[gender] for gender in selected_genders]
                df_filtered = df[df['gender'].isin(numeric_genders)]
                hobby_title += '\n - Gender: ' + ', '.join(selected_genders)

            else:
                df_filtered = df  # No gender filter applied

            # Filter by years of experience
            df_filtered = df_filtered[df_filtered['experience_list'].apply(lambda x: any(year in range(experience_min, experience_max + 1) for year in x))]
            hobby_title += f' \n- Experience: {experience_min} to {experience_max}'

            # Filter by favorite animals
            if selected_animals:
                df_filtered = df_filtered[df_filtered['fav_animals'].isin(selected_animals)]
                hobby_title += ' \n- Favorite Animals: ' + ', '.join(selected_animals)

            # Filter by education levels
            if selected_edu_levels:
                df_filtered = df_filtered[df_filtered['edu_level'].isin(selected_edu_levels)]
                hobby_title += ' \n- Education Levels: ' + ', '.join(selected_edu_levels)

            # Calculate hobby counts
            hobby_counts = df_filtered[hobby_columns].sum()  # Use filtered DataFrame

            # Plot
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.barplot(y=hobby_counts.index, x=hobby_counts.values, ax=ax, palette="Blues_d")
            ax.set_title(hobby_title, fontsize=16)  # Updated title
            ax.set_xlabel("Number of Participants")
            ax.set_ylabel("Hobby")

            st.pyplot(fig)

        elif filter_option == 'Gender Filter':
            # Filter out NaN values in the gender column
            df_filtered = df[df['gender'].notna()]

            # Create a copy of the main DataFrame for gender
            df_gender = df.copy()

            # Replace numeric gender values with text labels
            df_gender['gender'] = df_gender['gender'].map({0: "Male", 1: "Female"})

            # Calculate hobby counts split by gender
            hobby_counts_gender = df_gender.groupby('gender')[hobby_columns].sum().T  # Transpose for easier plotting
            
            # Plot
            fig, ax = plt.subplots(figsize=(10, 6))
            hobby_counts_gender.plot(kind='barh', stacked=True, ax=ax, color=["grey", "silver"])  # Stacked horizontal bar plot
            ax.set_title(hobby_title, fontsize=16)  # Updated title
            ax.set_xlabel("Number of Participants")
            ax.set_ylabel("Hobby")

            st.pyplot(fig)

