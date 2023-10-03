import os
import numpy as np
import pandas as pd
from datetime import datetime
import openai
from pgvector.psycopg2 import register_vector
from psycopg2.extras import execute_values
import psycopg2

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve the API key from environment variables
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
if not OPENAI_API_KEY:
    raise ValueError("Please set the OPENAI_API_KEY in the .env file.")

# Set up the OpenAI API key
openai.api_key = OPENAI_API_KEY

def get_embedding(text, model="text-embedding-ada-002"):
    text = text.replace("\n", " ")
    return openai.Embedding.create(input=[text], model=model)['data'][0]['embedding']

def process_batch(df, conn, table_name):
    combined_texts = []
    embeddings = []

    # Concatenate selected columns into a single text string for each row and generate embeddings
    for index, row in df.iterrows():
        combined_text = ' '.join(row.astype(str))
        combined_texts.append(combined_text)
        embedding = get_embedding(combined_text)
        embeddings.append(embedding)

    # Create a new DataFrame to hold the combined text and embeddings
    new_df = pd.DataFrame({
        'combined_text': combined_texts,
        'embedding': embeddings
    })

    # Print the first 5 rows of combined text and embeddings
    print("First 5 combined texts:")
    print(new_df['combined_text'].head())
    print("\nFirst 5 embeddings:")
    print(new_df['embedding'].head())

    # Batch insert the new DataFrame into the PostgreSQL database
    cur = conn.cursor()
    data_list = [(row['combined_text'], np.array(row['embedding'])) for index, row in new_df.iterrows()]
    execute_values(cur, f"INSERT INTO {table_name} (combined_text, embedding) VALUES %s", data_list)
    conn.commit()


# Ask for user input
csv_file = "dating_app_data.csv"
db_url = "postgresql://postgres:12345@localhost:5432/mydb"
table_name = input("Please enter the name of the table you want to create: ")

# Connect to PostgreSQL database
conn = psycopg2.connect(db_url)

# Read the .csv file into a DataFrame
df = pd.read_csv(csv_file)

# Initialize the database and table
cur = conn.cursor()
cur.execute("CREATE EXTENSION IF NOT EXISTS vector")
conn.commit()
register_vector(conn)

table_create_command = f"""
CREATE TABLE IF NOT EXISTS {table_name} (
    id bigserial primary key, 
    combined_text text,
    embedding vector(1536)
);
"""
cur.execute(table_create_command)
conn.commit()

# Process the DataFrame
process_batch(df, conn, table_name)

# Close the database connection
conn.close()
