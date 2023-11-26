import streamlit as st
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
st.markdown("---")
st.header("Introduction 🌐")
st.write("""Welcome to ISIMM Study Hub, an unofficial platform dedicated to providing essential information for Computer Science students at Higher Institue of Informatics and Mathematics.
         \nMy aim is to assist students by gathering and organizing various resources, including timetables, teachers contacts information, subjects, and study resources, to streamline your academic experience.
           """)
st.markdown("---")
st.header("Purpose of this webiste 🎯")
st.write("""
My primary goal is to offer a centralized hub for students to access information necessary for our academic journey,by simplifying the process of finding timetables, locating teachers contact information, and obtaining subject-related details, all in one place.

At ISIMM Study Hub, you can find:

\n- Timetables for various courses and semesters.
\n- Contact information for professors and teaching staff.
\n- Details about different subjects, including course descriptions and resources.
""")
st.write("---")
st.header("Creator 🚀")
st.write("""
Khalyl Ebdelli, a Computer Science student at ISIMM
Contact info : 
""")
st.write("Email 📧 : ebdellikhalyl@outlook.com")
st.markdown("Linkedin 🤵: [Linkedin Profile ](https://www.linkedin.com/in/khalyl-ebdelli-3733ab1ba/)")
st.markdown("Github 👨‍💻: [GitHub Repository ](https://github.com/VinDazy)")
st.markdown("---")
st.header("Acknowledgment 🙏")
st.markdown("I extend my gratitude to [Khalil Ouali](https://www.linkedin.com/in/ouali-khalil) for the inspiration and originality of the idea.")
st.markdown("---")
col1,col2,col3,col4,col5=st.columns(5)
return_home=col3.button("🏠Return Home")
if return_home:
    switch_page("home")