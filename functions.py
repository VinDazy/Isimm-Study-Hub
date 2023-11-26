from bs4 import BeautifulSoup
from PIL import Image
import random
import json
import requests
import pickle
import os
from google_auth_oauthlib.flow import Flow, InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
import datetime
import streamlit as st
from PIL import Image
from io import BytesIO



def Create_Service(client_secret_file, api_name, api_version, *scopes):
    #print(client_secret_file, api_name, api_version, scopes, sep='-')
    CLIENT_SECRET_FILE = client_secret_file
    API_SERVICE_NAME = api_name
    API_VERSION = api_version
    SCOPES = [scope for scope in scopes[0]]
    #print(SCOPES)

    cred = None

    pickle_file = f'token_{API_SERVICE_NAME}_{API_VERSION}.pickle'
    # print(pickle_file)

    if os.path.exists(pickle_file):
        with open(pickle_file, 'rb') as token:
            cred = pickle.load(token)

    if not cred or not cred.valid:
        if cred and cred.expired and cred.refresh_token:
            cred.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
            cred = flow.run_local_server()

        with open(pickle_file, 'wb') as token:
            pickle.dump(cred, token)

    try:
        service = build(API_SERVICE_NAME, API_VERSION, credentials=cred)
        #print(API_SERVICE_NAME, 'service created successfully')
        return service
    except Exception as e:
        print('Unable to connect.')
        print(e)
        return None

def convert_to_RFC_datetime(year=1900, month=1, day=1, hour=0, minute=0):
    dt = datetime.datetime(year, month, day, hour, minute, 0).isoformat() + 'Z'
    return dt

def scrape_quote():
    page_index=random.randint(1,10)
    quote_index=random.randint(1,10)
    data = {}
    index_counter = 0
    link = f"https://quotes.toscrape.com/page/{page_index}/"
    html_text = requests.get(link).text
    soup = BeautifulSoup(html_text, 'lxml')
    quotes = soup.find_all('div', class_='quote')
    for element in quotes:
        quote = element.find('span', class_='text').text
        author = element.find('small', class_='author').text
        data[index_counter+1] = {
            'quote': quote,
            'author': author,
        }
        index_counter += 1
    return data[quote_index]
def scrape_announcement() -> dict:
    base_url = 'http://www.isimm.rnu.tn'
    url = f'{base_url}/public/'
    html_text = requests.get(url=url).text
    soup = BeautifulSoup(html_text, 'lxml')
    announcements = soup.find_all('div', class_='actu grid_2 insa-lyon click')
    announcements_dict = {}

    for index, announcement in enumerate(announcements):
        announcement_image_url = announcement.find('img', id="img_post")['src']
        announcement_date = announcement.find('span', class_='date').text
        announcement_title = announcement.find('h4').find('a').text.strip()
        announcement_link = announcement.find('h4').find('a')['href']

        # Download image and convert to base64
        image_response = requests.get(f'{base_url}{announcement_image_url}')
        image = Image.open(BytesIO(image_response.content))
        buffered = BytesIO()
        image.save(buffered, format="JPEG")
        announcement_image_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")

        announcements_dict[index] = {
            'announcement_image': f"data:image/jpeg;base64,{announcement_image_base64}",
            'announcement_date': announcement_date,
            'announcement_title': announcement_title,
            'announcement_link': announcement_link
        }

    return announcements_dict


def get_subfolder_links(client_secret_file, api_name, api_version, scopes, folder_id):
    # Create the service
    service = Create_Service(client_secret_file, api_name, api_version, scopes)
    
    # Perform a file listing request for the specified folder
    query = f"parents = '{folder_id}'"
    response = service.files().list(q=query).execute()
    folders = response.get('files')
    
    # Dictionary to store folder names and their links
    folder_links = {}
    
    # Loop through each folder and obtain its link
    for folder in folders:
        folder_id = folder['id']
        folder_name = folder['name']
        
        # Generate a link for the folder
        folder_link = f"https://drive.google.com/drive/folders/{folder_id}"
        
        # Add folder name and link to the dictionary
        folder_links[folder_name] = folder_link
    
    return folder_links
def get_subfolder_files_download_links(client_secret_file, api_name, api_version, scopes, folder_id):
    # Create the service
    service = Create_Service(client_secret_file, api_name, api_version, scopes)
    
    # Perform a file listing request for the specified folder
    query = f"parents = '{folder_id}'"
    response = service.files().list(q=query).execute()
    folders = response.get('files')
    
    # Dictionary to store folder names and download links
    folder_download_links = {}
    
    # Loop through each folder and obtain download links for its files
    for folder in folders:
        folder_id = folder['id']
        folder_name = folder['name']
        
        # Perform a file listing request for the current folder
        query = f"parents = '{folder_id}'"
        response = service.files().list(q=query).execute()
        files = response.get('files')
        
        # List to store download links for files in the folder
        download_links = []
        
        # Generate download links for files in the folder
        for file in files:
            file_id = file['id']
            file_name = file['name']
            
            # Generate a download link for the file
            download_link = f"https://drive.google.com/uc?id={file_id}"
            
            # Add the download link to the list
            download_links.append({file_name: download_link})
        
        # Add folder name and download links to the dictionary
        folder_download_links[folder_name] = download_links
    
    return folder_download_links
def resize_images(directory, width, height):
    # Loop through each file in the directory
    for filename in os.listdir(directory):
        if filename.endswith(('.jpg', '.jpeg', '.png')):
            filepath = os.path.join(directory, filename)
            
            # Open the image using PIL
            img = Image.open(filepath)
            
            # Resize the image
            resized_img = img.resize((width, height), Image.ANTIALIAS)
            
            # Save the resized image, overwriting the original file
            resized_img.save(filepath)

def display_subfolder_links(folder_links):
    # Path to the image file
    columns = st.columns(3, gap="large")  # Creating three columns

    for index, (folder_name, folder_link) in enumerate(folder_links.items()):
        with columns[index % 3]: 
            if folder_name.endswith(' '):
                folder_name = folder_name[:-1]
            image_name = f"{folder_name}.png"
            image_path = os.path.join("media", "subject_logos", image_name)
            st.markdown(f"<b>Subject : </b> {folder_name}", unsafe_allow_html=True)
            st.image(image_path, width=350, caption="", use_column_width=False)  # Displaying the image
            st.markdown(f"📁 [Visit Folder]({folder_link})")  # Displaying the link
            st.markdown("---")


def get_subfolder_links(client_secret_file, api_name, api_version, scopes, folder_id):
    # Create the service
    service = Create_Service(client_secret_file, api_name, api_version, scopes)
    
    query = f"parents = '{folder_id}'"
    response = service.files().list(q=query).execute()
    folders = response.get('files')
    
    # Dictionary to store folder names and their links
    folder_links = {}
    
    # Loop through each folder and obtain its link
    for folder in folders:
        folder_id = folder['id']
        folder_name = folder['name']
        
        # Generate a link for the folder
        folder_link = f"https://drive.google.com/drive/folders/{folder_id}"
        
        # Add folder name and link to the dictionary
        folder_links[folder_name] = folder_link
    
    return folder_links