from flask import Flask, request, jsonify
import os

# Assuming constants.py contains your API Key and possibly other settings
import constants

os.environ["OPENAI_API_KEY"] = constants.APIKEY

from langchain.chains import ConversationalRetrievalChain
from langchain_community.chat_models import ChatOpenAI
from langchain_community.document_loaders import DirectoryLoader
from langchain_openai import OpenAIEmbeddings
from langchain.indexes.vectorstore import VectorStoreIndexWrapper, VectorstoreIndexCreator
from langchain_community.vectorstores import Chroma

app = Flask(__name__)

# Initialize your components here
loader = DirectoryLoader("data/")
index = VectorstoreIndexCreator().from_loaders([loader])
chain = ConversationalRetrievalChain.from_llm(
    llm=ChatOpenAI(model="gpt-3.5-turbo"),
    retriever=index.vectorstore.as_retriever(search_kwargs={"k": 1}),
)

@app.route('/query', methods=['POST'])
def query():
    content = request.json
    question = content.get('question')
    if not question:
        return jsonify({"error": "No question provided"}), 400
    chat_history = content.get('chat_history', [])
    result = chain({"question": question, "chat_history": chat_history})
    return jsonify({"answer": result['answer']})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
