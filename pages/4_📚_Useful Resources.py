import streamlit as st
import pandas as pd
import json
import re
from streamlit_extras.switch_page_button import switch_page
import firebase_admin
from firebase_admin import credentials, firestore

st.set_page_config(page_title='ISIMM Study Hub',
                   page_icon='media/isimm logo/isimm logo.jpg', layout='wide')
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
img, bg = st.columns([0.2, 0.8], gap="large")

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
        index=0  
    )

l2_s1_df = pd.DataFrame(getFormatedData(json_file="credits/creds_sem_1.json"))
l2_s2_df = pd.DataFrame(getFormatedData(json_file="credits/creds_sem_2.json"))
l3_s1_df = pd.DataFrame(getFormatedData(json_file="credits/creds_l3_s1.json"))
l3_s2_df = pd.DataFrame(getFormatedData(json_file="credits/creds_pfe.json"))


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

def validateEmail(email):
    regex = '^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}'
    return re.match(regex, email) is not None


@st.cache_data()
def get_email_docs():
    teachers_emailList = firestore.client().collection("teacherEmailList")
    emailDocs = teachers_emailList.stream()
    data = [doc.to_dict() for doc in emailDocs]
    return data  


services_data = json.loads(st.secrets["json_data"]["services_data"])
storage_bucket = json.loads(st.secrets["storage"]["storage_bucket"])
cred = credentials.Certificate(services_data)

if not firebase_admin._apps:  
    app = firebase_admin.initialize_app(cred, storage_bucket)

teachers_waitlist = firestore.client().collection("teacherWaitList")



with st.sidebar:
    st.header("Add Teachers Email 📧")

    # Use session_state to maintain inputs
    if 'name' not in st.session_state:
        st.session_state['name'] = ""
    if 'email' not in st.session_state:
        st.session_state['email'] = ""

    name = st.text_input("Teacher's Name", value=st.session_state['name'])
    email = st.text_input("Teacher's Email", value=st.session_state['email'])
    button = st.button("Add Teacher")

    # Email validation
    if not validateEmail(email) and email:
        st.error("Invalid email format!")
    else:
        if button:
            if validateEmail(email):
                try:
                    row = {
                        "teacherEmail": email,
                        "teacherFullName": name,
                        "Validated": False
                    }
                    teachers_waitlist.add(row)
                    st.success("Teacher added successfully!")

                    # Clear inputs
                    st.session_state['name'] = ""
                    st.session_state['email'] = ""
                    



                except Exception as e:
                    st.error("Error adding teacher: " + str(e))
            else:
                st.error("Please provide a valid email address.")

emailDocs = get_email_docs()
df = pd.DataFrame(emailDocs)
df=df.drop(columns=["Approved","Validated"],axis=1)


st.table(df)

st.markdown("---")
col1, col2, col3, col4, col5 = st.columns(5)

return_home = col3.button("🏠Return Home")
if return_home:
    switch_page("home")
