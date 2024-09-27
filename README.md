# Amazon Book Data Scraper and Chatbot with Semantic Search

## Overview
This project involves scraping book data from Amazon, storing it in a MySQL database, and leveraging Cohere's Embed API to create vector embeddings of the book data. These embeddings are stored in Pinecone and used to perform semantic search, integrated into a Flask-based chatbot web app.

The main features of the project include:
1. **Scraping Amazon Book Data** using Scrapy.
2. **Storing Data** in a MySQL database and exporting it to a JSON file.
3. **Data Cleaning** to format book details for embedding.
4. **Embedding Text Data** using the Cohere Embed API.
5. **Storing and Indexing Vector Embeddings** in Pinecone.
6. **Flask Web App with Chatbot Interface** using Cohere's chatbot API and Pinecone for semantic search.

## Technologies Used
- **Python** for scripting and development.
- **Scrapy** for web scraping Amazon book data.
- **MySQL** for data storage.
- **Cohere API** for generating vector embeddings from text data and chatbot functionality.
- **Pinecone** for storing and indexing embeddings for semantic search.
- **Flask** for creating the web interface for the chatbot.
- **HTML/CSS** for building the front-end interface.
  
## Project Structure
- **/spiders/** - Scrapy spiders for scraping Amazon books.
- **/database/** - SQLAlchemy models for MySQL database storage.
- **/embeddings/** - Scripts for cleaning, embedding, and indexing data with Cohere and Pinecone.
- **/flask_app/** - Flask app for the chatbot interface, utilizing the Cohere chatbot API and Pinecone for semantic search.
- **amazon_books_data.json** - JSON file storing the scraped Amazon book data.
  
## Project Workflow
1. **Scraping Amazon Data**: Used Scrapy to scrape book details (name, authors, ratings, etc.) from Amazon. Data is saved into a MySQL database and exported as a JSON file (`amazon_books_data.json`).
  
2. **Data Processing**: Cleaned and structured the scraped data into meaningful sentences combining book attributes like title, author, and reviews.

3. **Embedding and Storage**: 
   - Used Cohere's Embed API to convert the book information into vector embeddings.
   - Stored these embeddings in Pinecone for efficient retrieval and indexing.

4. **Flask Web App**: Developed a web interface with Flask, allowing users to interact with a chatbot named **Bookie**. Users can ask for book recommendations or information, and the chatbot responds based on the embeddings indexed in Pinecone.

5. **Semantic Search**: When a user queries the chatbot, the query is embedded and compared with the stored embeddings in Pinecone to retrieve relevant book data, which is then used to generate a detailed response via Cohere’s chatbot API.

## How to Run the Project
### Pre-requisites:
- Python 3.x
- MySQL
- Scrapy
- Cohere API key
- Pinecone API key
- Flask

### Steps:
1. **Clone the repository**:
    ```bash
    git clone <repository-url>
    ```
2. **Install required dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
3. **Run the Scrapy spider to scrape Amazon data**:
    ```bash
    scrapy crawl amazon_books_spider
    ```
4. **Run the Flask app**:
    ```bash
    python app.py
    ```

## Future Improvements
- Enhance chatbot interaction for more natural and dynamic responses.
- Add support for additional book data sources.
- Improve the efficiency of semantic search by refining embedding techniques.
