import pandas as pd

# read the data from the CSV file into a dataframe
df = pd.read_csv('studentData.csv')

# create a new column for IDs
df['ID'] = df['Course'].str.startswith('ID').cumsum()  # assign ID based on "ID" rows

# group the dataframe by ID
grouped = df.groupby('ID')

# create a dictionary of ID:data pairs
data_dict = {}
for name, group in grouped:
    data_dict[group['ID'].iloc[0]] = group.drop('ID', axis=1).values.tolist()
