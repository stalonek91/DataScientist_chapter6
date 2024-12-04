import streamlit as st
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# Funkcje do konwertowania zakresu doswiadczenia do INT tak by filtering mogl zadzialac

def convert_experience_to_list(exp_str):
    if isinstance(exp_str, str):
        if exp_str.startswith(">="):
            return [16]  
        elif "-" in exp_str:
            start, end = map(int, exp_str.split("-"))
            return list(range(start, end + 1))  
        else:
            return [int(exp_str)]  
    return [0]  

def convert_age_to_numeric(age_str):
    if isinstance(age_str, str):
        if age_str.startswith(">="):
            return 65  
        elif age_str.startswith("<"):
            return 0  
        elif "-" in age_str:
            start, end = map(int, age_str.split("-"))
            return (start + end) / 2  
        elif age_str == "unknown":
            return None  
    return None  


#Definicja funkcji page_2 -> domyslnie miala byc jedna ze stron

def page_2():

    csv_file_path = Path('35__welcome_survey_cleaned.csv')
    df = pd.read_csv(csv_file_path, sep=';')

    age_tab, hobby_tab, prof_tab, other_tab = st.tabs(
        ["Participant Age", "Participant Hobby", "Participant career", 
         "Other"
                                            ])
    with age_tab:

        with st.sidebar:


            # Maping 0/1 na plec - mozna by to bylo zrobic w DFie bezposrednio ale wolalem sie pobawic

            st.write("Use following filters to every section")
            gender_options = ["Male", "Female"]
            gender_mapping = {"Male": 0, "Female": 1}
            selected_genders = st.multiselect(
                "Select data per gender",
                gender_options
            )
            
            #
            animal_options = ["Psy", "Koty", "Inne", "Brak ulubionych", "Koty i Psy"]
            selected_animals = st.multiselect(
                "Select favorite animals",
                animal_options
            )       

            
            edu_level_options = df['edu_level'].unique().tolist()  # Get unique education levels
            selected_edu_levels = st.multiselect(
                "Select education levels",
                edu_level_options
            )       

            # Slider dla doswiadczenia
            experience_slider = st.slider(
                "Select years of experience",
                min_value=0,
                max_value=16,
                value=(0, 16),  
                step=1
            )

        
        
        df['experience_list'] = df['years_of_experience'].apply(convert_experience_to_list)
        df['numeric_age'] = df['age'].apply(convert_age_to_numeric)

        
        age_bins = [0, 18, 25, 35, 45, 55, 65, 100] 
        age_labels = ['<18', '18-24', '25-34', '35-44', '45-54', '55-64', '65+']
        df['age_group'] = pd.cut(df['numeric_age'], bins=age_bins, labels=age_labels, right=False)

        st.title(":man-raising-hand: Participants survey data")
        with st.expander("Click to get brief overview of the data"):
            st.write("""
                    This dataset contains information about participants in a data science course, 
                     capturing diverse aspects of their demographics, preferences, and motivations. 
                     It includes 28 features, such as age, education level, and professional experience, 
                     as well as personal interests like favorite animals, places, and hobbies. 
                     Additionally, it explores participants' learning preferences, 
                     ranging from online courses to personal projects, and their motivations, 
                     including career growth and creativity. 
                     This rich dataset provides an opportunity to analyze patterns and trends among 
                     aspiring data scientists, offering insights into their backgrounds and aspirations.
                     """)


        # Zmienna title bedzie podmianiala na zywo tytul w glownym histogramie i dodawala inforamcje o filtrach
        title = 'Histogram of Age for:'

       
       #Filtry z sidebaru (kod sie powtarza w kazdej sekcji -> do usprawnienia i sprawdzenia czy da sie
       #zredukowac duplikaty)
        if selected_genders:
            title += '\n  ' + ', '.join(selected_genders)
            numeric_genders = [gender_mapping[gender] for gender in selected_genders]
            df = df[df['gender'].isin(numeric_genders)]
        else:
            title += '\n  Male, Female'  

        
        experience_min, experience_max = experience_slider
        experience_title = "All Years of Experience" if (experience_min == 0 and experience_max == 16) else f"Years of Experience: {experience_min} to {experience_max}"
        title += '\n  ' + experience_title

        
        df = df[df['experience_list'].apply(lambda x: any(year in range(experience_min, experience_max + 1) for year in x))]

        
        if selected_animals:
            title += '\n - Favorite animal: ' + ', '.join(selected_animals)
            df = df[df['fav_animals'].isin(selected_animals)]

        
        if selected_edu_levels:
            title += '\n - Education level: ' + ', '.join(selected_edu_levels)
            df = df[df['edu_level'].isin(selected_edu_levels)]

        

        # Histogram
        title = title.strip()

        fig, ax = plt.subplots(figsize=(10, 5))  
        sns.histplot(df['age_group'], discrete=True, ax=ax, alpha=0.7)  

        ax.set_xlabel('User Age')
        ax.set_ylabel('Number of Users in Age Range')
        ax.set_title(title)

        ax.set_xticks(range(len(age_labels)))
        ax.set_xticklabels(age_labels)

        st.pyplot(fig)
        


        # Summary Data sekcja: Kazda kolumna policzona tak by mozna bylo stworzyc agregacyjny DF z podsumowaniem.
        # Summary data jest na biezaco akutalizowany per filter

        summary_data = df.groupby(['age']).agg(
            Male=('gender', lambda x: (x == 0).sum()),  
            Female=('gender', lambda x: (x == 1).sum()),  
            Cat=('fav_animals', lambda x: (x == 'Koty').sum()),  
            Dog=('fav_animals', lambda x: (x == 'Psy').sum()),  
            Other=('fav_animals', lambda x: (x == 'Inne').sum()), 
            No_Favorite=('fav_animals', lambda x: (x == 'Brak ulubionych').sum()),  
            Both=('fav_animals', lambda x: (x == 'Koty i Psy').sum()),  
            Podstawowe=('edu_level', lambda x: (x == 'Podstawowe').sum()),  
            Srednie=('edu_level', lambda x: (x == 'Srednie').sum()),  
            Wyzsze=('edu_level', lambda x: (x == 'Wyzsze').sum())  
        ).reset_index()

        
        st.write("Summary Data:")
        st.dataframe(summary_data, hide_index=True)


    with hobby_tab:

        st.title(":table_tennis_paddle_and_ball: Hobbies")

        hobby_columns = ["hobby_art", "hobby_books", "hobby_movies", 
                        "hobby_other", "hobby_sport", "hobby_video_games"]

        hobby_title = 'Participants by Hobby'

        filter_option = st.radio(
                "Select filter type - feel free to use sidebar filters also!",
                ("Custom Filters", "Gender Filter", "Age Filter")
            )

        if filter_option == 'Custom Filters':
            #Filtry z sidebaru
            if selected_genders:
                numeric_genders = [gender_mapping[gender] for gender in selected_genders]
                df_filtered = df[df['gender'].isin(numeric_genders)]
                hobby_title += '\n - Gender: ' + ', '.join(selected_genders)

            else:
                df_filtered = df  

            
            df_filtered = df_filtered[df_filtered['experience_list'].apply(lambda x: any(year in range(experience_min, experience_max + 1) for year in x))]
            hobby_title += f' \n- Experience: {experience_min} to {experience_max}'

           
            if selected_animals:
                df_filtered = df_filtered[df_filtered['fav_animals'].isin(selected_animals)]
                hobby_title += ' \n- Favorite Animals: ' + ', '.join(selected_animals)

            
            if selected_edu_levels:
                df_filtered = df_filtered[df_filtered['edu_level'].isin(selected_edu_levels)]
                hobby_title += ' \n- Education Levels: ' + ', '.join(selected_edu_levels)

            
            hobby_counts = df_filtered[hobby_columns].sum()  

            
            fig, ax = plt.subplots(figsize=(10, 6))
            colors = sns.color_palette("Blues_d", len(hobby_counts))
            sns.barplot(
                y=hobby_counts.index,
                x=hobby_counts.values,
                ax=ax,
                palette=colors  
            )
            st.pyplot(fig)


        elif filter_option == 'Gender Filter':

            
            df_filtered = df[df['gender'].notna()]

            
            df_gender = df.copy()

            
            df_gender['gender'] = df_gender['gender'].map({0: "Male", 1: "Female"})

            # Uzyte transpose do lepszej reprezentacji per hobby .T
            hobby_counts_gender = df_gender.groupby('gender')[hobby_columns].sum().T  
            
            
            fig, ax = plt.subplots(figsize=(10, 6))
            hobby_counts_gender.plot(kind='barh', stacked=True, ax=ax, color=["grey", "silver"])  
            ax.set_title(hobby_title, fontsize=16)  
            ax.set_xlabel("Number of Participants")
            ax.set_ylabel("Hobby")

            st.pyplot(fig)


            fig, ax = plt.subplots(figsize=(10, 6))
            sns.heatmap(hobby_counts_gender, annot=True, fmt='d', cmap='Blues', ax=ax) 
            ax.set_title('Participants by Hobby and Gender', fontsize=16)
            ax.set_xlabel("Age Group")
            ax.set_ylabel("Gender")

            st.pyplot(fig)

        elif filter_option == 'Age Filter':
            
            hobby_counts_age = df.groupby('age_group')[hobby_columns].sum().T  
            
            # Plot
            fig, ax = plt.subplots(figsize=(10, 6))
            hobby_counts_age.plot(kind='barh', stacked=True, ax=ax, color=sns.color_palette("coolwarm", len(age_labels)))  
            ax.set_title('Participants by Hobby and Age Group', fontsize=16)  
            ax.set_xlabel("Number of Participants")
            ax.set_ylabel("Hobby")

            st.pyplot(fig)

            fig, ax = plt.subplots(figsize=(10, 6))
            sns.heatmap(hobby_counts_age, annot=True, fmt='d', cmap='Blues', ax=ax)  
            ax.set_title('Participants by Hobby and Age Group', fontsize=16)
            ax.set_xlabel("Age Group")
            ax.set_ylabel("Hobby")

            st.pyplot(fig)

    with other_tab:

        st.title(":dog2: Participants favourite pet, place and seasoning :salt:")
        new_df = df[['fav_animals', 'fav_place', 'sweet_or_salty']]


        
        filtered_df = df.copy()

        #Filtry z sidebaru
        if selected_genders:
            numeric_genders = [gender_mapping[gender] for gender in selected_genders]
            filtered_df = filtered_df[filtered_df['gender'].isin(numeric_genders)]

        
        experience_min, experience_max = experience_slider
        filtered_df = filtered_df[filtered_df['experience_list'].apply(
            lambda x: any(year in range(experience_min, experience_max + 1) for year in x)
        )]

        
        if selected_animals:
            filtered_df = filtered_df[filtered_df['fav_animals'].isin(selected_animals)]

        
        if selected_edu_levels:
            filtered_df = filtered_df[filtered_df['edu_level'].isin(selected_edu_levels)]

        
        animal_counts = filtered_df['fav_animals'].value_counts().reset_index()
        animal_counts.columns = ['fav_animals', 'count']

        place_counts = filtered_df['fav_place'].value_counts().reset_index()
        place_counts.columns = ['fav_place', 'count']

        seasoning_counts = filtered_df['sweet_or_salty'].value_counts().reset_index()
        seasoning_counts.columns = ['sweet_or_salty', 'count']

        
        fig1 = px.bar(animal_counts, x='fav_animals', y='count', title='Favorite Animals')
        st.plotly_chart(fig1, theme="streamlit", use_container_width=True)

        fig2 = px.bar(place_counts, x='fav_place', y='count', title='Favorite Places')
        st.plotly_chart(fig2, theme="streamlit", use_container_width=True)

        fig3 = px.bar(seasoning_counts, x='sweet_or_salty', y='count', title='Sweet or Salty Preference')
        st.plotly_chart(fig3, theme="streamlit", use_container_width=True)



    with prof_tab:
        st.title(":female-student: Career & learning")
        prof_tab_1, prof_tab_2, prof_tab_3 = st.tabs(["Industries", "Motivation", "Learning style"])

        with prof_tab_1:

            filtered_df = df.copy()

            #Filtry z sidebaru
            if selected_genders:
                numeric_genders = [gender_mapping[gender] for gender in selected_genders]
                filtered_df = filtered_df[filtered_df['gender'].isin(numeric_genders)]

            
            experience_min, experience_max = experience_slider
            filtered_df = filtered_df[filtered_df['experience_list'].apply(
                lambda x: any(year in range(experience_min, experience_max + 1) for year in x)
            )]

            
            if selected_animals:
                filtered_df = filtered_df[filtered_df['fav_animals'].isin(selected_animals)]

            
            if selected_edu_levels:
                filtered_df = filtered_df[filtered_df['edu_level'].isin(selected_edu_levels)]

            

            industry_counts = filtered_df['industry'].value_counts().reset_index()
            industry_counts.columns = ['industry', 'count']  # Rename columns for clarity

            

           
            fig = px.bar(
                industry_counts,
                y="industry",
                x="count",
                color="industry",  
                title="Industry split of the participants",
                labels={"count": "Occurrences"},
            )

            fig.update_layout(
                height=600,  
                width=1000,
                showlegend=False
            )
            

            st.plotly_chart(fig, theme="streamlit", use_container_width=True)

        with prof_tab_2:

            columns_list = [
            "motivation_career", 
            "motivation_challenges", 
            "motivation_creativity_and_innovation", 
            "motivation_money_and_job", 
            "motivation_personal_growth", 
            "motivation_remote"

            
        ]
            filtered_df = df.copy()

            #Filtry z sidebaru
            if selected_genders:
                numeric_genders = [gender_mapping[gender] for gender in selected_genders]
                filtered_df = filtered_df[filtered_df['gender'].isin(numeric_genders)]

            
            experience_min, experience_max = experience_slider
            filtered_df = filtered_df[filtered_df['experience_list'].apply(
                lambda x: any(year in range(experience_min, experience_max + 1) for year in x)
            )]

            
            if selected_animals:
                filtered_df = filtered_df[filtered_df['fav_animals'].isin(selected_animals)]

            
            if selected_edu_levels:
                filtered_df = filtered_df[filtered_df['edu_level'].isin(selected_edu_levels)]

            motivation_df = filtered_df[columns_list]
            motivation_counts = motivation_df.sum().reset_index()
            motivation_counts.columns = ['motivation', 'count']
            motivation_counts = motivation_counts.sort_values(by="count", ascending=False)

            
            fig = px.bar(
                motivation_counts,
                x="motivation",
                y="count",
                color="motivation",  
                title="Motivation of Data Science course",
                labels={"count": "Occurrences", "motivation": "Motivation"},
                
            )

            fig.update_layout(xaxis=dict(showticklabels=False))
            fig.update_layout(
                height=600,  
                width=1000,
            )

            st.plotly_chart(fig, theme="streamlit", use_container_width=True)

        with prof_tab_3:
            
                        
            learning_columns = [
                'learning_pref_books',
                'learning_pref_chatgpt',
                'learning_pref_offline_courses',
                'learning_pref_online_courses',
                'learning_pref_personal_projects',
                'learning_pref_teaching',
                'learning_pref_teamwork',
                'learning_pref_workshops'
            ]

            filtered_df = df.copy()

            
            if selected_genders:
                numeric_genders = [gender_mapping[gender] for gender in selected_genders]
                filtered_df = filtered_df[filtered_df['gender'].isin(numeric_genders)]

            
            experience_min, experience_max = experience_slider
            filtered_df = filtered_df[filtered_df['experience_list'].apply(
                lambda x: any(year in range(experience_min, experience_max + 1) for year in x)
            )]

            
            if selected_animals:
                filtered_df = filtered_df[filtered_df['fav_animals'].isin(selected_animals)]

            
            if selected_edu_levels:
                filtered_df = filtered_df[filtered_df['edu_level'].isin(selected_edu_levels)]
            
            learning_df = filtered_df[learning_columns]

            
            learning_counts = learning_df.sum().reset_index()
            learning_counts.columns = ['learning_preference', 'count']  
            learning_counts = learning_counts.sort_values(by="count", ascending=False)

            
            fig = px.bar(
                learning_counts,
                y="learning_preference",
                x="count",
                color="learning_preference", 
                title="Learning prefference of the participants",
                labels={"count": "Occurrences"},
            )

            fig.update_layout(
                height=600,  
                width=1000,
                showlegend=False  
            )

            st.plotly_chart(fig, theme="streamlit", use_container_width=True)







                   
                    


                



