# Semantic Search Application with Flask, OpenAI, and Pinecone

This application is built to perform semantic search on a collection of documents using the power of OpenAI's GPT model and Pinecone's vector database.

## Getting Started

### Prerequisites
- OpenAI API Key
- Pinecone API Key
- Pinecone API Environment Variable

These keys and variables can either be stored as environment variables or inside the `apikey.py` file.

### Installation
1. Clone this repository and navigate into the project directory.
```sh
git clone <repository-link>
cd <repository-folder>
```

2. Install the required Python dependencies from the requirements.txt file:
```sh
pip install -r requirements.txt
```

3. You need API keys for OpenAI and Pinecone services. Store these keys securely in your environment variables or, alternatively, in an `apikey.py` file which should contain:

```sh
apikey = "YOUR_OPENAI_API_KEY"
pinecone_apikey = "YOUR_PINECONE_API_KEY"
pinecone_env = "PINECONE_ENVIRONMENT"
```

<br>
<br>

## Running the Application
Start the application by running the main Python script:\
```sh
python app.py
```
The application will start a Flask server on localhost:5000.

<br>
<br>

## Running the Application with Docker
To run the application with Docker, follow these steps:
1. Build the Docker image. Navigate to the directory with your Dockerfile and run the following command:
```sh
docker build -t semantic-search-app .
```
In the command above, __`semantic-search-app`__ is the name of the Docker image. You can replace it with a name of your choice.

2. After building the Docker image, you can run the application using Docker with the following command:
```sh
docker run -p 5000:5000 -e "apikey=YOUR_OPENAI_API_KEY" -e "pinecone_apikey=YOUR_PINECONE_API_KEY" -e "pinecone_env=PINECONE_ENVIRONMENT" semantic-search-app
```
This command will run the Docker container and expose port 5000 for the Flask application. Replace __`YOUR_OPENAI_API_KEY`__, __`YOUR_PINECONE_API_KEY`__ and __`PINECONE_ENVIRONMENT`__ with your actual API keys and Pinecone environment variable.

Please note that if you want to run the Flask application on a different port, change the first number in the `-p` option. For example, if you want to run it on port `8080`, you would use `-p 8080:5000` instead.

<br>
<br>

## Usage
There are two endpoints you can interact with:

* __Document Indexing__: Index your documents using the __`/api/v1/consume`__ endpoint. This endpoint accepts POST requests with JSON data that includes the question, response, and additional metadata.

Here's an example curl command for indexing a new document:

```sh
curl -X POST -H "Content-Type: application/json" -d '{"data": [{"question": "What is AI?", "response": "AI stands for Artificial Intelligence.", "metadata": {"id": 1231}}, {"question": "What is ML?", "response": "ML stands for Machine Learning.", "metadata": {"id": 323423}}]}' http://localhost:5000/api/v1/consume
```

* __Semantic Search__: Perform semantic search using the __`/api/v1/semantic-search`__ endpoint. This endpoint accepts POST requests with JSON data that is used to ask questions. The application will search for the most similar question in the vector store and return its corresponding answer.

Here's an example curl command for performing a semantic search:

```sh
curl -X POST -H "Content-Type: application/json" -d '{"question": "What is AI?"}' http://localhost:5000/api/v1/semantic-search
```

The search will return a list of relevant responses along with their metadata.
