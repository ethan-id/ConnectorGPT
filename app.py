from flask import Flask, request, jsonify
import os
import tempfile
import shutil

from dotenv import load_dotenv

load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API")

from langchain.chains import ConversationalRetrievalChain
from langchain_community.chat_models import ChatOpenAI
from langchain_community.document_loaders import TextLoader, DirectoryLoader
from langchain_openai import OpenAIEmbeddings
from langchain.indexes.vectorstore import VectorStoreIndexWrapper, VectorstoreIndexCreator
from langchain_community.vectorstores import Chroma

app = Flask(__name__)

# Function to create an index from dynamic data
def create_dynamic_index(data_text):
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_file_path = os.path.join(temp_dir, "temp_data.txt")
        with open(temp_file_path, "w") as temp_file:
            temp_file.write(data_text)
        loader = TextLoader(temp_file_path)
        index = VectorstoreIndexCreator().from_loaders([loader])
        return index

# Function to check if a directory is empty
def is_directory_empty(directory):
    return not any(os.scandir(directory))

# Initialize components for static data if available
if not is_directory_empty("data/"):
    static_loader = DirectoryLoader("data/")
    static_index = VectorstoreIndexCreator().from_loaders([static_loader])
    static_chain = ConversationalRetrievalChain.from_llm(
        llm=ChatOpenAI(model="gpt-3.5-turbo"),
        retriever=static_index.vectorstore.as_retriever(search_kwargs={"k": 1}),
    )
else:
    static_chain = None

@app.route('/query', methods=['POST'])
def query():
    content = request.json
    question = content.get('question')
    additional_data = content.get('additional_data', None)
    
    if not question:
        return jsonify({"error": "No question provided"}), 400
    
    chat_history = content.get('chat_history', [])
    
    if additional_data:
        # Handle dynamic data case
        dynamic_index = create_dynamic_index(additional_data)
        selected_chain = ConversationalRetrievalChain.from_llm(
            llm=ChatOpenAI(model="gpt-3.5-turbo"),
            retriever=dynamic_index.vectorstore.as_retriever(search_kwargs={"k": 1}),
        )
    elif static_chain is not None:
        # Use static chain if initialized
        selected_chain = static_chain
    else:
        # Handle case where there's no static data and no dynamic data provided
        return jsonify({"error": "No data available for processing"}), 400
    
    result = selected_chain({"question": question, "chat_history": chat_history})
    return jsonify({"answer": result['answer']})


if __name__ == '__main__':
    app.run(port=int(os.environ.get("PORT", 8080)),host='0.0.0.0',debug=True)
