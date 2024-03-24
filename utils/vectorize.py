import chromadb
import os


from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.llms import OpenAI
from langchain.chains import VectorDBQA
from langchain.document_loaders import TextLoader

from load_dotenv import load_dotenv

load_dotenv()

cwd = os.getcwd()
persist_dir= f"{os.getcwd()}/data/store"
client = chromadb.PersistentClient(path=persist_dir)


in_dir_path = f"{os.getcwd()}/data/txt/composed"
for filename in os.listdir(in_dir_path):
    if filename.endswith('.txt'):
        file_path = os.path.join(in_dir_path, filename)
        loader = TextLoader(file_path)
        documents = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
        texts = text_splitter.split_documents(documents)
        embedding = OpenAIEmbeddings()
        vectordb = Chroma.from_documents(documents=texts, embedding=embedding, persist_directory=persist_dir)
            