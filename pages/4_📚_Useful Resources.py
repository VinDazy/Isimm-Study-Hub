import streamlit as st
import pandas as pd 
import json
import csv 
from streamlit_extras.switch_page_button import switch_page
st.set_page_config(page_title='ISIMM Study Hub',page_icon='media/isimm logo/isimm logo.jpg',layout='wide')
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
img,bg=st.columns([0.2,0.8],gap="large")

img.image("media/isimm logo/isimm logo _ 20.png", width=270)
bg.image("media/banner.jpeg", use_column_width=True)


def getFormatedData(json_file):
    with open(f'{json_file}', 'r') as file:
        data = json.load(file)
    formatted_data = []
    for unit_data in data:
        unit_name = unit_data['Unit']
        coefficient_total = unit_data['Coefficient(Total)']
        credit_total = unit_data['Credit(Total)']
        
        # Extracting subjects' details within the same unit
        subject_names = "<br>".join([subject['Subject'] for subject in unit_data['Subjects']])
        subject_coefficients = "<br>".join([str(subject['Coefficient']) for subject in unit_data['Subjects']])
        subject_credits = "<br>".join([str(subject['Credit']) for subject in unit_data['Subjects']])
        
        formatted_data.append({
            'Unit Name': unit_name,
            'Unit Total Coefficient': coefficient_total,
            'Unit Total Credit': credit_total,
            'Subject Name': subject_names,
            'Subject Coefficient': subject_coefficients,
            'Subject Credit': subject_credits
        })
    return formatted_data

with st.sidebar:

    year = st.radio(
        label="Choose Year : ", 
        options=["L3", "L2"], 
        index=0  # Default to L3 (first option)
    )
    
l2_s1_df = pd.DataFrame(getFormatedData(json_file="credits\\creds_sem_1.json"))
l2_s2_df = pd.DataFrame(getFormatedData(json_file="credits\\creds_sem_2.json"))
l3_s1_df= pd.DataFrame(getFormatedData(json_file="credits\\creds_l3_s1.json"))
l3_s2_df= pd.DataFrame(getFormatedData(json_file="credits\\creds_pfe.json"))












st.write("")

if year == "L2":
            st.header("Semester 1 classes")
            st.write(l2_s1_df.to_markdown(index=False), unsafe_allow_html=True)
            st.write(" ")
            st.markdown("---")
            st.header("Semester 2 classes")
            st.write(l2_s2_df.to_markdown(index=False), unsafe_allow_html=True)
else:
            st.header("Semester 1 classes")
            st.write(l3_s1_df.to_markdown(index=False), unsafe_allow_html=True)
            st.write(" ")
            st.markdown("---")
            st.header("Semester 2 classes")
            st.write(l3_s2_df.to_markdown(index=False), unsafe_allow_html=True)






st.markdown("---")
st.header("Teachers Emails 📧")




def read_csv_to_dict(csv_file):
    teachers_dict = {}
    with open(csv_file, mode='r') as file:
        csv_reader = csv.DictReader(file)
        rows = list(csv_reader)
        if not rows:  # Check if the CSV is empty
            return teachers_dict
        
        # Get the columns from the first row of the CSV
        columns = list(rows[0].keys())
        
        # Transpose the data
        for col in columns:
            # Center align column names
            col_length = max(len(col), max(len(row[col]) for row in rows))
            centered_col = col.center(col_length)
            teachers_dict[centered_col] = [row[col].center(col_length) for row in rows]

    return teachers_dict



# Example usage:
file_path = 'resources/teachersEmails.csv'  
teachers_data = read_csv_to_dict(file_path)

df = pd.DataFrame(teachers_data)


st.write(df.to_html(index=False), unsafe_allow_html=True)







st.markdown("---")
col1,col2,col3,col4,col5=st.columns(5)

return_home=col3.button("🏠Return Home")
if return_home:
    switch_page("home")