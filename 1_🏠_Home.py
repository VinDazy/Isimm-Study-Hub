import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from functions import *
from streamlit_extras.stylable_container import stylable_container
st.set_page_config(page_title='ISIMM Study Hub',
                   page_icon='media/isimm logo/isimm logo.jpg', layout='wide')
hide_streamlit_style = """
            <style>
            
            footer {visibility: hidden;}
            </style>
            """
#!To hide hamburger menu add " #MainMenu {visibility: hidden;} " to the <style>
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
img, bg = st.columns([0.2, 0.8], gap="large")
img.image("media/isimm logo/isimm logo _ 20.png", width=270)
bg.image("media/banner.jpeg", use_column_width=True)
st.markdown("----")
#quote_column,announcement_column=st.columns(2)
st.subheader("🔔 Quote of the day 🔔 ")
@st.cache_data
def Scrape_Quote():
    return scrape_quote()
quote=Scrape_Quote()
#!This is for caching the quote so it won't change when switching between pages
@st.cache_data
def Scrape_Announcement():
    return scrape_announcement()
announcements_dict=Scrape_Announcement()
#!This is for caching the announcements so it won't load again when switching between pages
quote_container = st.empty()
with quote_container:
    st.markdown(
        f'<div style="border: 1px solid rgba(49, 51, 63, 1); border-radius: 0.6rem; padding: 1em;">'
        f'{quote["quote"]} - {quote["author"]}'
        '</div>',
        unsafe_allow_html=True,
        )
st.markdown("----")
st.subheader("📢 Announcements 📢")
announcements_per_row = 3

# Initialize HTML content for the grid
html_content = '<div style="display: flex; flex-wrap: wrap;">'

# Iterate through announcements and generate HTML content for each announcement
for announcement in announcements_dict.values():
    styled_container = (
        '<div style="border: 1px solid rgba(49, 51, 63, 0.9); border-radius: 0.5rem; padding: 1em; margin: 0.5em;">'
        f'<b>Title:</b> {announcement["announcement_title"]}<br>'
        f'<b>Date:</b> {announcement["announcement_date"]}<br>'
        f'<img src="{announcement["announcement_image"]}" alt="Announcement Image" style="width: 200px; height: 150px;"><br>'
        f'<b></b> <a href="{announcement["announcement_link"]}">Visit Anouncement</a> 📢<br>'
        '</div>'
    )
    html_content += styled_container

# Close the grid layout HTML
html_content += '</div>'

st.markdown(html_content, unsafe_allow_html=True)
st.markdown("---")
subjectResources, schedule, subject_info = st.columns(3)

# Container for Subject Resources
with subjectResources:
    st.image("media/menu/info.png")
    resources_button = st.button("Check Course Materials",use_container_width=True)
    if resources_button:
        switch_page("subjects")

# Container for Schedule
with schedule:
    st.image("media/menu/sched.png")
    schedule_button = st.button("Check Time Table",use_container_width=True)
    if schedule_button:
        switch_page("time tables")

# Container for Subject Information
with subject_info:
    st.image("media/menu/resources.png")
    subject_info_button = st.button("Check useful information", use_container_width=True)
    if subject_info_button:
        switch_page("useful resources")


