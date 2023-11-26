CLIENT_SECRET_FILE='download\client_secrets_file.json'
API_NAME='drive'
API_VERSION='v3'
SCOPES=['https://www.googleapis.com/auth/drive']
FOLDER_ID="1DFwSgOYhRCXzfbgCTAnT3g_UMMCFqPml"
from pprint import pprint
import json
with open('download\client_secrets_file.json', 'r') as file:
    data_dict = json.load(file)

# Display the resulting dictionary
pprint(data_dict)





