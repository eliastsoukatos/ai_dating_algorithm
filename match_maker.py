import os
import numpy as np
import pandas as pd
import psycopg2
from pgvector.psycopg2 import register_vector
from psycopg2.extras import execute_values
import openai
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

def get_top_similar_docs(query_embedding, conn, table_name):
    embedding_array = np.array(query_embedding)
    
    # Register pgvector extension
    register_vector(conn)
    cur = conn.cursor()
    
    # Get the top most similar profiles using the KNN <=> operator
    cur.execute(f"SELECT id, combined_text FROM {table_name} ORDER BY embedding <=> %s LIMIT 1", (embedding_array,))
    top_profile = cur.fetchone()
    return top_profile

def ask_questions_and_find_match(conn, table_name):
    questions = [
        "What is your Name?",
        "What is your Age?",
        "What is your Job?",
        "What is your Education degree?",
        "What are your top three hobbies and why do you enjoy them?",
        "Describe your ideal weekend. Are you out exploring the city or cozying up with a good book?",
        "What's your go-to comfort food and why?",
        "How would you describe your sense of humor? (Sarcastic, slapstick, dry, etc.)",
        "What's a cause or issue that you're passionate about?",
        "What's your favorite genre of music and how does it reflect your personality?",
        "How important is physical fitness to you and how do you incorporate it into your life?",
        "What are the top three qualities you're looking for in a partner?",
        "Are you a morning person or a night owl? How does this affect your daily routine?",
        "How do you handle stress or conflict? Are you more of a problem-solver or a peacemaker?"
    ]
    
    responses = []
    for question in questions:
        answer = input(question + " ")
        responses.append(answer)
    
    # Combine all the answers into a single string
    combined_text = ' '.join(responses)
    
    # Generate an embedding for the combined text
    user_embedding = get_embedding(combined_text)
    
    # Find the most similar profile in the database
    top_profile = get_top_similar_docs(user_embedding, conn, table_name)
    
    print(f"Your top match is profile ID {top_profile[0]} with the following details:")
    print(top_profile[1])

# Database connection
db_url = "postgresql://postgres:12345@localhost:5432/mydb"
table_name = input("Please enter the name of the table you want to query: ")
conn = psycopg2.connect(db_url)

# Ask questions and find the top match
ask_questions_and_find_match(conn, table_name)

# Close the database connection
conn.close()
