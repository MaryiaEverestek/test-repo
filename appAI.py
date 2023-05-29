import os
import pinecone

from apikey import apikey, pinecone_apikey, pinecone_env

from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Pinecone
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.llms import OpenAI
from langchain.chains.question_answering import load_qa_chain



OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY', apikey)

PINECONE_API_KEY = os.environ.get('PINECONE_API_KEY', pinecone_apikey)
PINECONE_API_ENV = os.environ.get('PINECONE_API_ENV', pinecone_env)

url = 'URL OF THE PDF'

# LOAD OUR DATA
loader = PyPDFLoader(url)

data = loader.load()

print (f'You have {len(data)} document(s) in your data')
print (f'There are {len(data[0].page_content)} characters in your document')

'''
!!! need this if the pdf is very big like a book !!!

# CHUNK OUR DATA INTO SMALLER PIECES
# We need to split the documents into smaller chunks to be able to embed them.
text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=0)

# Parse the data that we loaded earlier into smaller chunks
texts = text_splitter.split_documents(data)
# print (f'Now you have {len(texts)} documents')
+ change the data to texts in the docsearch = Pinecone.from_texts...
'''


# CREATE EMBEDDINGS OF OUR DOCUMENTS TO GET READY FOR SEMANTIC SEARCH
# OpenAIEmbeddings will take our docs and returns them into vectors
embeddings = OpenAIEmbeddings(openai_api_key=apikey)


# initialize pinecone
pinecone.init(
    api_key=PINECONE_API_KEY,  # find at app.pinecone.io
    environment=PINECONE_API_ENV  # next to api key in console
)

# ! with OpenAIEmbeddings dimensions == 1536
index_name = "langchaintest" # put in the name of your pinecone index here



# It is taking all texts, it's creating embeddings about them, 
# and it's passing them to Pinecone which is the external data source
docsearch = Pinecone.from_texts([t.page_content for t in data], embeddings, index_name=index_name)

# do similarity/semantic search
query = "What is the name of the applicant?" # 'Your query goes here'
docs = docsearch.similarity_search(query)
# it returns the list of the documents (5) that has highest cosine similarity to our query




llm = OpenAI(temperature=0, openai_api_key=apikey)

# it's going to take all our docs, put them into a prompt and return finally the answer for us
chain = load_qa_chain(llm, chain_type="stuff")
chain.run(input_documents=docs, question=query)
# we'll get the natural answer from opneai