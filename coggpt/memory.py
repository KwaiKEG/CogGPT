import os
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma

from utils.file_utils import create_folder
from utils.chain_logger import *


class Memory:
    def __init__(
        self,
        memory_dir='./',
        memory_folder='memory',
        openai_api_key=os.environ.get('OPENAI_API_KEY'),
        chunk_size=1000,
        chunk_overlap=100,
        logger=ChainMessageLogger()
    ):
        create_folder(memory_dir, memory_folder)
        self.embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
        self.vectordb = Chroma(embedding_function=self.embeddings, persist_directory=os.path.join(memory_dir, memory_folder))
        self.text_splitter = CharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        self.logger = logger


    def forget(self, knowledge, forgetting_rate):
        num = round(len(knowledge) * (1-forgetting_rate))
        return sorted(knowledge, key=lambda x: x['score'], reverse=True)[:num]


    def store(self, knowledge, forgetting_rate=0.4):
        knowledge = self.forget(knowledge, forgetting_rate)
        for item in knowledge:
            documents = self.text_splitter.create_documents([item['knowledge']], metadatas=[{"score": item['score']}])
            self.vectordb.add_documents(documents)
        self.vectordb.persist()

        self.logger.put("execute", f"Successfully store {len(knowledge)} knowledge in my long-term memory.")
        for i, item in enumerate(knowledge, start=1):
            self.logger.put("execute", f"{i}. {item['knowledge']}")


    # Recalls Top 3 relevant knowledge.
    def recall(self, query, num=3):
        documents = sorted(self.vectordb.similarity_search_with_score(query), key=lambda x: x[1], reverse=True)
        results = [doc[0].page_content for doc in documents[:num]]

        self.logger.put("execute", f"Recall {len(results)} knowledge from my long-term memory.")
        for i, result in enumerate(results, start=1):
            self.logger.put("execute", f"{i}. {result}")

        return results