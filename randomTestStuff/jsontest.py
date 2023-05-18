import pandas as pd

# Read the CSV file
df = pd.read_csv('studentData.csv', sep=',+', engine='python')

# Print the resulting DataFrame
print(df.loc[5])