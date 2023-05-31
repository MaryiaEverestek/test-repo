from flask import Flask, request, jsonify
import os
import pinecone

# from apikey import apikey, pinecone_apikey, pinecone_env

from langchain.vectorstores import Pinecone
from langchain.embeddings.openai import OpenAIEmbeddings


app = Flask(__name__)

# OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY', apikey)
# PINECONE_API_KEY = os.environ.get('PINECONE_API_KEY', pinecone_apikey)
# PINECONE_API_ENV = os.environ.get('PINECONE_API_ENV', pinecone_env)
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY', "N/A")
PINECONE_API_KEY = os.environ.get('PINECONE_API_KEY', "N/A")
PINECONE_API_ENV = os.environ.get('PINECONE_API_ENV', "N/A")



try:
    pinecone.init(
        api_key=PINECONE_API_KEY,
        environment=PINECONE_API_ENV
    )
except Exception as e:
    print(f"An error occurred while trying to initialize Pinecone: {e}")


embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
index_name = "langchaintest"


index = pinecone.Index(index_name=index_name)
vector_store = Pinecone(index=index, embedding_function=embeddings.embed_query, text_key="text")


@app.route('/api/v1/consume', methods=['POST'])
def consume():
    try:
        data = request.json['data']
        texts = []
        metadata_list = []

        for item in data:
            question = item.get("question", "N/A")
            response = item.get("response", "N/A")
            metadata = item.get("metadata", {})

            metadata.update({"question": question, "response": response})

            texts.append(response)
            metadata_list.append(metadata)

        vector_store.add_texts(texts=texts, metadatas=metadata_list)


        return jsonify({"message": "Data processed successfully"}), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/v1/semantic-search', methods=['POST'])
def semantic_search():
    try:
        question = request.json["question"]


        results = vector_store.similarity_search(question)
        valid_results = [result for result in results if result.metadata.get("question", None)]


        formatted_results = [
            {
                "question": result.metadata.get("question", "N/A"),
                "question": result.metadata.get("question", "N/A"),
                "metadata": result.metadata
            }
            for result in valid_results
            # for result in results

        ]

        return jsonify({"results": formatted_results}), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500




if __name__ == '__main__':
    # app.run(debug=True)
    app.run(host='0.0.0.0', debug=True)