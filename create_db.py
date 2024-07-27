import sqlite3
import pandas as pd

# Load Titanic dataset
titanic = pd.read_csv('data/titanic.csv')
movie_data = pd.read_csv('data/IMDB-Movie-Data.csv')
housing = pd.read_csv('data/USA Housing Dataset.csv')

# Create an SQLite database (or connect to an existing one)
conn = sqlite3.connect('test_db.db')

# Write the DataFrame to an SQLite table
titanic.to_sql('passengers', conn, if_exists='replace', index=False)
movie_data.to_sql('movies', conn, if_exists='replace', index=False)
housing.to_sql('houses', conn, if_exists='replace', index=False)

# Close the connection
conn.close()
