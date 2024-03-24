from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_openai import ChatOpenAI
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.llms import OpenAI
from langchain.chains import VectorDBQA
from langchain.document_loaders import TextLoader

import os
import json
from load_dotenv import load_dotenv






class ChainManager:
    def __init__(self):
        load_dotenv()
        self.load_models()
        self.setup_chains()

    def load_models(self):
        self.llm = ChatOpenAI(model='gpt-3.5-turbo')
        self.embedding = OpenAIEmbeddings()

    def setup_chains(self):
        self.setup_plan_chain()
        self.setup_execute_chain()
        self.setup_qa_chain()

    def setup_plan_chain(self):
        PLAN_PROMPT = PromptTemplate.from_file('./prompts/plan.jinja2')
        self.plan_chain = LLMChain(llm=self.llm, prompt=PLAN_PROMPT)

    def setup_execute_chain(self):
        EXECUTE_PROMPT = PromptTemplate.from_file('./prompts/execute.jinja2')
        self.execute_chain = LLMChain(llm=self.llm, prompt=EXECUTE_PROMPT)

    def setup_qa_chain(self):
        persist_dir = f"{os.getcwd()}/data/store"
        self.vectordb = Chroma(persist_directory=persist_dir, embedding_function=self.embedding)
        self.qa_chain = VectorDBQA.from_chain_type(llm=OpenAI(), chain_type="stuff", vectorstore=self.vectordb)
        
        
    def get_relevant_docs(self, query, n=3):
        return self.vectordb.similarity_search(query)[:n]
        

    def answer_question(self, query):
        return self.qa_chain.run(query),self.get_relevant_docs(query)

    def generate_execution_plan(self, previous_2):
        plan = self.plan_chain.run(previous_3=previous_2)
        return json.loads(plan)

    def execute_plan(self, plan, questions_for_minute):
        context = ""
        for question in questions_for_minute:
            answer, source =  self.answer_question(question)
            context +=  answer + "\n" + "\n".join([page.page_content for page in source[:2]]) + "\n"
        execution = self.execute_chain.run(plan=plan, text=context)
        return execution