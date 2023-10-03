import csv
import openai
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize the OpenAI API
openai.api_key = os.getenv("OPENAI_API_KEY")

# Define the questions (columns)
columns = [
    "What is your Name? Write a random name of a person:",
    "What is your Age? Write a random age of a person:",
    "What is your Job? Write a random job of a person:",
    "What is your Education degree? Write a random education degree of a person:",
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

# Open a new CSV file for writing
with open('dating_app_data.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    
    # Write the header (questions)
    writer.writerow(columns)
    
    # Generate 200 rows of answers
    for i in range(200):
        row = []
        for question in columns:
            prompt = f"You are a user creating a profile for a new Dating app. PLEASE ADD A LOT OF RANDOMNESS TO YOUR ANSWERS. You will be asked a question and need to respond the question asked and nothing else. Answer the dating app question: {question}"
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=prompt,
                max_tokens=50,
                temperature=1.0
            )
            row.append(response.choices[0].text.strip())
        writer.writerow(row)
