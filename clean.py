import pandas as pd

# Load the master file you just generated
df = pd.read_csv("HubSpot_Ready_Master.csv")

# 1. Merge 'school name' into 'Company Name'
if 'school name' in df.columns:
    df['Company Name'] = df['Company Name'].fillna(df['school name'])
    df.drop(columns=['school name'], inplace=True)

# 2. Merge 'phone no' into 'Phone Number' and strip out the junk text
if 'phone no' in df.columns:
    df['Phone Number'] = df['Phone Number'].fillna(df['phone no'])
    # Remove the weird "Call-->" artifacts from the school lists
    df['Phone Number'] = df['Phone Number'].astype(str).str.replace('Call-->', '', regex=False).str.strip()
    df.drop(columns=['phone no'], inplace=True)

# 3. Drop useless system export columns
cols_to_drop = ['latest activity', 'actions']
df.drop(columns=[c for c in cols_to_drop if c in df.columns], inplace=True)

# Save the absolute final version
output_file = "HubSpot_Final_Cleaned.csv"
df.to_csv(output_file, index=False)
print(f"Data unified and cleaned! Ready for upload: {output_file}")