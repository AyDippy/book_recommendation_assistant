from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np
import cohere
import pinecone
from pinecone import Pinecone
from pinecone import ServerlessSpec
import json

#setting up my cohere API using API key
co = cohere.Client("API_KEY")

# initializing connection to pinecone
pc = Pinecone(api_key='API_KEY')

# Specify the index name and host

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
        # Get the query from the request JSON body
        data = request.get_json()
        query = data.get('query')

        if not query:
            return jsonify({"status": "error", "message": "Query not provided"}), 400

        # Call the chat_bot_response function with the query
        bot_response = chat_bot_response(query)

        # Return success and the bot's response
        return jsonify({"status": "success", "response": bot_response}), 200

def chat_bot_response(query):
    index_name = 'cohere-pinecone-amazon-books'
    host = 'https://cohere-pinecone-amazon-books-fogaie8.svc.aped-4627-b74a.pinecone.io'

    # Connect to the index with the correct host
    index = pc.Index(index_name, host=host)
    # create the query embedding
    xq = co.embed(
        texts=[query],
        model='embed-multilingual-v3.0',
        input_type='search_query'
    ).embeddings

    # query, returning the top 5 most similar results
    res = index.query(vector=xq, top_k=10, include_metadata=True)

    book_knowledge = []
    for match in res['matches']:
        book_knowledge.append(match['metadata']['text'])

    # Load chat history from a file if it exists
    try:
        with open('chat_history.json', 'r') as f:
            chat_history = json.load(f)
    except FileNotFoundError:
        chat_history = []

    prompt = f"""
You're a book recommendation assistant. Your goal is to assist users with book-related queries concisely. You cover genres like 'Literature & Fiction', 'Self-Help', 'Comics & Graphic Novels', and many more.

## Instructions
Below is a list of book summaries and reviews related to the user's query. Each entry includes information such as book name, authors, production date, category, hard cover price, book rating, user ratings, number of pages, and a selection of user reviews.

The user's query is: "{query}"

Respond briefly and naturally, without lengthy paragraphs. Keep it casual and conversational. Avoid recommending a book unless the user explicitly asks for one.

## Book Summaries and Reviews:
{book_knowledge}

## Rules
1. Greet the user briefly if the query is a greeting (e.g., "Good morning!", "Hi!"). Do not recommend books when responding to greetings. Introduce yourself politely, but keep it concise (e.g., "Hi, I can help with book recommendations.").
2. If the query involves book-related questions, provide a concise response based on the book knowledge. 
3. For non-book queries, acknowledge the user's request politely and suggest your area of expertise (e.g., "I can help with book recommendations.").
4. Be clear, concise, and conversational in all responses. Avoid creating long paragraphs.

# Example Outputs:
- User: "Can you suggest a self-help book?"
  * Response: "I have some great self-help books like X and Y. Would you like more info?"
- User: "Hi"
  * Response: "Hello! I can assist with book recommendations. Let me know what you're looking for."
- User: "I need books on history"
  * Response: "I found some history books like A and B. Let me know if you'd like more details."
"""


    response = co.chat(
        model="command-r-plus-08-2024",
        message=prompt,
        conversation_id = '001'
    )

    return response.text

if __name__ == '__main__':
    app.run(debug=True)

