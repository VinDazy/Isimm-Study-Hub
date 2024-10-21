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


def validateEmail(email):
    regex = '^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}'
    return re.match(regex, email) is not None


def get_email_docs():
    teachers_emailList = firestore.client().collection("teacherEmailList")
    emailDocs = teachers_emailList.stream()
    return emailDocs


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

data = []
for doc in emailDocs:
    row = doc.to_dict()
    data.append(row)

df = pd.DataFrame(data)
df=df.drop("Approved",axis=1)
st.table(df)

st.markdown("---")
col1, col2, col3, col4, col5 = st.columns(5)

return_home = col3.button("🏠Return Home")
if return_home:
    switch_page("home")
