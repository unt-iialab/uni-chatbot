import openai
import random
import os
import re
import requests

# Set up OpenAI API key
openai.api_key = "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"

# API_Key: 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

# Define a function to handle user input
def get_input():
    user_input = input("How can I help you today?")
    return user_input

# Define a function to search for relevant information in your documents
def search_docs(query):
    # Replace with your own path to your documents
    docs_path = "/Users/haihuachen/Documents/Code/countryReputation/documents"
    relevant_docs = []
    for filename in os.listdir(docs_path):
        if filename.endswith(".txt"):
            with open(os.path.join(docs_path, filename), "r") as f:
                text = f.read()
                if re.search(query, text):
                    relevant_docs.append(filename)
    return relevant_docs

# Define a function to search the internet for relevant information
def search_web(query):
    # Replace with your own Google Custom Search API key and search engine ID
    API_KEY = "AIzaSyCohSLwtXqDTpHYZtEB1ICaryC1rEb6WEU"
    SEARCH_ENGINE_ID = "135f827a753be4273"
    url = f"https://www.googleapis.com/customsearch/v1?key={API_KEY}&cx={SEARCH_ENGINE_ID}&q={query}"
    response = requests.get(url)
    if response.status_code == 200:
        results = response.json().get("items", [])
        return [result["link"] for result in results]
    else:
        return []

# Define a function to generate a response using GPT
def generate_response(prompt):
    response = openai.Completion.create(
        engine="davinci",
        prompt=prompt,
        temperature=0.7,
        max_tokens=1024,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    return response.choices[0].text.strip()

# Define a loop to handle user input and generate responses
while True:
    user_input = get_input()
    if user_input == "quit":
        break
    else:
        # Search for relevant information in your documents
        relevant_docs = search_docs(user_input)

        # If no relevant information is found in your documents, search the internet
        if not relevant_docs:
            relevant_web = search_web(user_input)
        else:
            relevant_web = []

        # Generate a prompt for GPT that includes the user's input and any relevant information from the documents or internet
        prompt = f"User: {user_input}"
        if relevant_docs:
            prompt += f"\nDocuments: {', '.join(relevant_docs)}\n"
        if relevant_web:
            prompt += f"\nWeb: {', '.join(relevant_web)}\n"

        # Generate a response using GPT
        response = generate_response(prompt)

        print(response)
