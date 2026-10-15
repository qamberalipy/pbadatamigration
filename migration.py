import pandas as pd
import requests
import json

ACCESS_TOKEN = "pat-na2-66555ece-8539-4a1b-891e-878cfec6df86"
CLEANED_FILE = "HubSpot_Final_Cleaned.csv"
API_READY_FILE = "HubSpot_API_Ready.csv"
URL = "https://api.hubapi.com/crm/v3/imports"

# 1. Load the 12-column CSV
df = pd.read_csv(CLEANED_FILE)

# 2. Safely merge the unmapped columns into the standard 'Description' property
# The Fax append logic has been removed so it stays in its own column
def build_description(row):
    extras = []
    if pd.notna(row.get('Description')) and str(row.get('Description')).strip():
        extras.append(str(row['Description']))
    if pd.notna(row.get('Original File Source')):
        extras.append(f"Source: {row['Original File Source']}")
    if pd.notna(row.get('Company Email')):
        extras.append(f"Email: {row['Company Email']}")
    if pd.notna(row.get('Phone Number 2')):
        extras.append(f"Phone 2: {row['Phone Number 2']}")
    return " | ".join(extras) if extras else ""

df['Description'] = df.apply(build_description, axis=1)

# 3. Strip the CSV down to 9 columns, now explicitly keeping 'Fax'
columns_to_keep = [
    'Company Name', 'Street Address', 'City', 'State/Region', 
    'Postal Code', 'Phone Number', 'Website URL', 'Fax', 'Description'
]
df_api = df[columns_to_keep]
df_api.to_csv(API_READY_FILE, index=False)

# 4. Fire the 9-column match to the API
headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}"
}

import_request = {
    "name": "PBA Bulk Companies Import via API",
    "files": [
        {
            "fileName": API_READY_FILE,
            "fileFormat": "CSV",
            "fileImportPage": {
                "hasHeader": True,
                "columnMappings": [
                    {"columnObjectTypeId": "0-2", "columnName": "Company Name", "propertyName": "name"},
                    {"columnObjectTypeId": "0-2", "columnName": "Street Address", "propertyName": "address"},
                    {"columnObjectTypeId": "0-2", "columnName": "City", "propertyName": "city"},
                    {"columnObjectTypeId": "0-2", "columnName": "State/Region", "propertyName": "state"},
                    {"columnObjectTypeId": "0-2", "columnName": "Postal Code", "propertyName": "zip"},
                    {"columnObjectTypeId": "0-2", "columnName": "Phone Number", "propertyName": "phone"},
                    {"columnObjectTypeId": "0-2", "columnName": "Website URL", "propertyName": "domain"},
                    {"columnObjectTypeId": "0-2", "columnName": "Fax", "propertyName": "fax"}, # <--- NEW FAX MAPPING
                    {"columnObjectTypeId": "0-2", "columnName": "Description", "propertyName": "description"}
                ]
            }
        }
    ]
}

files = {
    'importRequest': (None, json.dumps(import_request), 'application/json'),
    'files': (API_READY_FILE, open(API_READY_FILE, 'rb'), 'text/csv')
}

response = requests.post(URL, headers=headers, files=files)

if response.status_code == 200:
    import_data = response.json()
    print(f"SUCCESS! Import started. Import ID: {import_data.get('id')}")
    print(f"Check the HubSpot UI to watch the progress.")
else:
    print(f"FAILED with status code {response.status_code}")
    print(response.text)