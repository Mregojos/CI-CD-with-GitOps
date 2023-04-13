# Main.py

#------------------Libraries----------------------------------------#
import streamlit as st
import pandas as pd
import numpy as np
import time
import streamlit_option_menu as menu
import matplotlib.pyplot as plt
import plotly.express as px

#------------------Page Set-up--------------------------------------#
st.set_page_config(
    page_title="Data Analysis Web App",
    page_icon="",
    layout="wide"
)

#-----------------Title and Info------------------------------------#
st.title("Data Analysis Web App")
st.subheader("🍁 Canada TFWP's Positive LMIA Employers List of 2022")

#-----------------Menu------------------------------------#
menu_style = { 'background-color': 'red'}
selected_option = menu.option_menu("", options=["Data", "Visualization", "Analysis", "Search", "About"], icons=["bi-table", "bi-bar-chart", "bi-graph-up", "bi-search", "bi-question-circle", "bi-info-circle"], orientation='horizontal', menu_icon='bi-table', styles=menu_style)

#----------------Variable-------------------------------------------#
progress_text = "Operation in progress. Please wait."

#----------------Dataframes-----------------------------------------#
@st.cache_data
def dataframe():
    df_2022 = pd.read_csv("processed-data/df_2022_cleaned.csv")
    df_2022q1 = pd.read_csv("processed-data/df_2022q4_cleaned.csv")
    df_2022q2 = pd.read_csv("processed-data/df_2022q3_cleaned.csv")
    df_2022q3 = pd.read_csv("processed-data/df_2022q2_cleaned.csv")
    df_2022q4 = pd.read_csv("processed-data/df_2022q1_cleaned.csv")
    return df_2022, df_2022q4, df_2022q3, df_2022q2, df_2022q1

df_2022, df_2022q4, df_2022q3, df_2022q2, df_2022q1 = dataframe()

file = {"df_2022": df_2022,
"df_2022q4": df_2022q4,
"df_2022q3": df_2022q3,
"df_2022q2": df_2022q2,
"df_2022q1": df_2022q1}

title = {"df_2022": "2022 Dataset",
"df_2022q4": "2022 Q4 Dataset",
"df_2022q3": "2022 Q3 Dataset",
"df_2022q2": "2022 Q2 Dataset",
"df_2022q1": "2022 Q1 Dataset"}

#----------------Show Dataframe-----------------------------------------#
if selected_option == "Data":
    st.title("Dataset")
    data = st.multiselect("What data to show?", ("df_2022", "df_2022q4", "df_2022q3", "df_2022q2", "df_2022q1"))
    if data:
        column = st.multiselect("What column to show?", ["Program Stream", "Province/Territory", "Employer", "Address", "Occupation", "Code", "Job Title", "Incorporate Status", "Approved LMIAs", "Approved Positions", "Quarter"], ["Program Stream", "Province/Territory", "Employer", "Address", "Occupation", "Code", "Job Title", "Incorporate Status", "Approved LMIAs", "Approved Positions", "Quarter"])
        if column:
            my_bar = st.progress(0, text=progress_text)
            for df in data:
                operation = True
                my_bar.progress(50, text=progress_text)
                st.write("---")
                st.subheader(title[df])
                while operation == True:
                    my_bar.progress(50, text=progress_text)
                    st.dataframe(file[df][column])
                    operation = False
                st.write("Rows :", str(len(file[df])), ",",
                         "Columns :", str(len(file[df][column].columns.tolist())))
            my_bar.progress(100, text="Completed!")
        
            

#----------------Visualization-----------------------------------------#
if selected_option == "Visualization":

    progress_text = "Operation in progress. Please wait."

    st.title("Data Visualization")
    st.info("Here are some useful data visualizations!")
    # st.warning("The only available data is 2022!")

    data = st.selectbox("What data to visualize?", ("", "df_2022", "df_2022q4", "df_2022q3", "df_2022q2", "df_2022q1"))


    if data:
        my_bar = st.progress(0, text=progress_text)
        st.subheader(title[data])
        col1, col2 = st.columns([2, 2]) 
        with col1:
            fig1 = px.bar(file[data], x='Province/Territory', y='Approved Positions', title='Approved Positions by Province/Territory')
            st.plotly_chart(fig1)
            my_bar.progress(25, text=progress_text)
        with col2:
            fig2 = px.bar(file[data], x=['Approved Positions', 'Approved LMIAs'], y='Program Stream', title='Approved Positions and LMIAs by Program Stream')
            st.plotly_chart(fig2)
            my_bar.progress(50, text=progress_text)
        with col1:
            top_employer=file[data].groupby('Employer')[['Approved LMIAs', 'Approved Positions']].sum().nlargest(100, 'Approved LMIAs').reset_index()
            st.write('Top Employers with the most Approved LMIAs and Approved Positions')
            st.write(top_employer)
            my_bar.progress(75, text=progress_text)
        with col2:
            top_occupation=file[data].groupby('Occupation')['Approved Positions'].sum().nlargest(10).reset_index()
            fig4 = px.bar(top_occupation, x='Approved Positions', y='Occupation', title='Top 10 Occupations per Approved Positions', orientation = 'h')
            st.plotly_chart(fig4)
            my_bar.progress(100, text="Completed!")
        
#----------------Analysis-----------------------------------------#
Analysis = ['Descriptive Analysis',
            'How many employers got LMIA in 2022?',
            'Top 10 Employer',
            'LMIA percentage by program stream',
            'Average Approved Positions per Employer',
            'Approved positions per quarter',
            'Average LMIAs per occupation']
            
if selected_option == "Analysis":
    st.title("Analyzing the Data!")
    st.info("Here are some analyses about the data!")
    analyses = st.multiselect('Choose an analysis:', Analysis)
    if analyses:
        for analysis in analyses:
            if analysis == Analysis[0]:
                st.write(f"{analysis}")
                st.write(df_2022.describe())
            elif analysis == Analysis[1]:
                st.write(f"{analysis}")
                st.success(len(df_2022['Employer'].unique()))
            elif analysis == Analysis[2]:
                st.write(f"{analysis}")
                st.write(df_2022.groupby('Employer')['Approved LMIAs'].sum().nlargest(10))
            elif analysis == Analysis[3]:
                st.write(f"{analysis}")
                lmia_percentage = df_2022.groupby('Program Stream')['Approved LMIAs'].sum() / df_2022['Approved LMIAs'].sum() * 100
                st.write(lmia_percentage)
            elif analysis == Analysis[4]:
                st.write(f"{analysis}")
                st.write(df_2022['Approved Positions'].mean())
            elif analysis == Analysis[5]:
                st.write(f"{analysis}")
                st.write(df_2022.groupby('Quarter')['Approved Positions'].sum())
            elif analysis == Analysis[6]:
                st.write(f"{analysis}")
                st.write(df_2022.groupby('Occupation')['Approved LMIAs'].mean())

#----------------Search-----------------------------------------#
if selected_option == "Search":
    st.title("Search the Dataset!")
    data = st.selectbox("What data to show?", ("", "df_2022", "df_2022q4", "df_2022q3", "df_2022q2", "df_2022q1"))
    if data:
        df = file[data]
        columns = st.multiselect("What column to show?", ["Program Stream", "Province/Territory", "Employer", "Address", "Occupation", "Code", "Job Title", "Incorporate Status", "Approved LMIAs", "Approved Positions", "Quarter"])
        selections = {}
        if columns:
            for col in columns: 
                selections[col] = st.multiselect(f"Choose the value for {col}:", df[col].unique())
        if st.button("Search"):
            df_selection = df.copy()
            for col, selection in selections.items():
                df_selection = df_selection[df_selection[col].isin(selection)]
            st.dataframe(df_selection)
            st.write("Rows :", str(len(df_selection)), ",", "Columns :", str(len(df_selection.columns.tolist())))

#----------------About-----------------------------------------#
if selected_option == "About":
    st.title("Data Analysis Web App")
    st.info("Canada Temporary Foreign Worker Program (TFWP)'s Positive Labour Market Impact Assessment (LMIA) Employers List of 2022")
    st.info('[Github Repository](https://github.com/Mregojos/Data-Analysis-App)')
