import requests
import json

# Your HubSpot Private App Token
ACCESS_TOKEN = "pat-na2-66555ece-8539-4a1b-891e-878cfec6df86"
FILE_PATH = "HubSpot_Final_Cleaned.csv"
URL = "https://api.hubapi.com/crm/v3/imports"

headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}"
}

# The importRequest maps your CSV headers directly to HubSpot's internal properties
import_request = {
    "name": "PBA Bulk Companies Import via API",
    "files": [
        {
            "fileName": "HubSpot_Final_Cleaned.csv",
            "fileFormat": "CSV",
            "fileImportPage": {
                "hasHeader": True,
                "columnMappings": [
                    {
                        "columnObjectTypeId": "0-2", # 0-2 indicates Company Object
                        "columnName": "Company Name",
                        "propertyName": "name"
                    },
                    {
                        "columnObjectTypeId": "0-2",
                        "columnName": "Street Address",
                        "propertyName": "address"
                    },
                    {
                        "columnObjectTypeId": "0-2",
                        "columnName": "City",
                        "propertyName": "city"
                    },
                    {
                        "columnObjectTypeId": "0-2",
                        "columnName": "State/Region",
                        "propertyName": "state"
                    },
                    {
                        "columnObjectTypeId": "0-2",
                        "columnName": "Postal Code",
                        "propertyName": "zip"
                    },
                    {
                        "columnObjectTypeId": "0-2",
                        "columnName": "Phone Number",
                        "propertyName": "phone"
                    },
                    {
                        "columnObjectTypeId": "0-2",
                        "columnName": "Website URL",
                        "propertyName": "domain"
                    },
                    {
                        "columnObjectTypeId": "0-2",
                        "columnName": "Description",
                        "propertyName": "description"
                    }
                ]
            }
        }
    ]
}

# Prepare the multipart/form-data payload
files = {
    'importRequest': (None, json.dumps(import_request), 'application/json'),
    'files': (FILE_PATH, open(FILE_PATH, 'rb'), 'text/csv')
}

# Execute the API POST request
response = requests.post(URL, headers=headers, files=files)

if response.status_code == 200:
    import_data = response.json()
    print(f"SUCCESS! Import started. Import ID: {import_data.get('id')}")
    print(f"Check the HubSpot UI to watch the progress.")
else:
    print(f"FAILED with status code {response.status_code}")
    print(response.text)