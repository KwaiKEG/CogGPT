from llms.clients import OpenAIClient
from utils.file_utils import load_prompt
from utils.chain_logger import *


class DistillAgent:
    def __init__(
        self,
        distill_prompt='distill',
        model_name='gpt-4',
        temperature=0,
        max_tries=20,
        logger=ChainMessageLogger()
    ):
        self.distill_prompt = load_prompt(distill_prompt)
        self.llm = OpenAIClient(model=model_name)
        self.temperature = temperature
        self.max_tries = max_tries
        self.logger = logger
    
    
    def distill(self, profile, memory):
        self.logger.put("thinking", '')
        
        query = self.distill_prompt.format(
            profile=profile,
            memory=memory
        )
        
        response = []
        while not response:
            response = self.llm.chat_and_check_json(
                query=query, 
                temperature=self.temperature, 
                max_tries=self.max_tries
            )        
        
        return response