import sqlite3
import pandas as pd

# Load Titanic dataset
titanic = pd.read_csv('titanic.csv')

# Create an SQLite database (or connect to an existing one)
conn = sqlite3.connect('titanic.db')

# Write the DataFrame to an SQLite table
titanic.to_sql('passengers', conn, if_exists='replace', index=False)

# Close the connection
conn.close()
