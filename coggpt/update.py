from llms.clients import OpenAIClient
from utils.file_utils import load_prompt
from utils.chain_logger import *


class UpdateAgent:
    def __init__(
        self,
        update_prompt='update',
        model_name='gpt-4',
        temperature=0,
        max_tries=20,
        logger=ChainMessageLogger()
    ):
        self.update_prompt = load_prompt(update_prompt)
        self.llm = OpenAIClient(model=model_name)
        self.temperature = temperature
        self.max_tries = max_tries
        self.logger = logger
    
    
    def update(self, profile, memory, keywords=['Assessments:', 'Thoughts:', 'Updated Profile:', 'Name:', 'Future Outlook:']):
        self.logger.put("thinking", '')
        
        query = self.update_prompt.format(
            profile=profile,
            memory=memory
        )
        
        response = ''
        while not response:
            response = self.llm.chat_and_check_keywords(
                query=query, 
                keywords=keywords,
                temperature=self.temperature, 
                max_tries=self.max_tries
            )

        result = {
            'assessments': response[response.find('Assessments:')+len('Assessments:'):response.find('Thoughts:')].strip(),
            'thoughts': response[response.find('Thoughts:')+len('Thoughts:'):response.find('Updated Profile:')].strip(),
            'updated': response[response.find('Updated Profile:')+len('Updated Profile:'):].strip()
        }

        self.logger.put("thought", result['assessments'])
        self.logger.put("thought", result['thoughts'])
        self.logger.put("execute", 'I am\n' + result['updated'])

        return result