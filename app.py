import pandas as pd
import glob
import os

# 1. Map all possible client garbage variations to HubSpot's strict properties
hubspot_mapping = {
    'name': 'Company Name',
    'address': 'Street Address',
    'address1': 'Street Address',
    'city': 'City',
    'state': 'State/Region',
    'zip': 'Postal Code',
    'phone 1': 'Phone Number',
    'phone 2': 'Phone Number 2',
    'fax': 'Fax',
    'email': 'Company Email',
    'website': 'Website URL',
    'dis': 'Description',
    'disc': 'Description'
}

excel_files = glob.glob("*.xlsx") + glob.glob("*.xls")
master_list = []

for file in excel_files:
    try:
        # Use calamine for .xlsx to bypass the style fill crashes
        engine = 'calamine' if file.endswith('.xlsx') else None
        
        # read_excel with sheet_name=None reads all sheets into a dictionary
        xls = pd.read_excel(file, sheet_name=None, engine=engine)
        
        for sheet_name, df in xls.items():
            # Skip empty sheets (like Sheet2, Sheet3 in the TG files)
            if df.empty or len(df.columns) == 0:
                continue 
            
            # 2. Clean headers: make lowercase and strip hidden spaces (fixes "Fax ")
            df.columns = [str(col).lower().strip() for col in df.columns]
            
            # 3. Rename columns using the HubSpot mapping dictionary
            df.rename(columns=hubspot_mapping, inplace=True)
            
            # 4. Inject a custom column so your client knows which file a lead came from
            df['Original File Source'] = file 
            
            master_list.append(df)
            print(f"Successfully processed: {file} - {sheet_name}")
            
    except Exception as e:
        print(f"CRITICAL FAILURE on {file}: {e}")

# 5. Merge every valid sheet into one master table
if master_list:
    master_df = pd.concat(master_list, ignore_index=True)

    # Drop any entirely blank rows
    master_df.dropna(how='all', inplace=True)

    # Export to the final HubSpot-ready format
    master_df.to_csv("HubSpot_Ready_Master.csv", index=False)
    print(f"\nSUCCESS: Merged into 'HubSpot_Ready_Master.csv'. Total Rows: {len(master_df)}")
else:
    print("\nNo data was extracted.")