from llms.clients import OpenAIClient
from utils.file_utils import load_prompt, find_ratings
from utils.chain_logger import *


class GradeAgent:
    def __init__(
        self,
        grade_prompt='grade',
        model_name='gpt-4',
        temperature=0,
        max_tries=20,
        logger=ChainMessageLogger()
    ):
        self.grade_prompt = load_prompt(grade_prompt)
        self.llm = OpenAIClient(model=model_name)
        self.temperature = temperature
        self.max_tries = max_tries
        self.logger = logger
    
    
    def grade(self, profile, memory, question, keywords=['Thoughts:', 'Rating:']):
        self.logger.put("thinking", '')
        
        query = self.grade_prompt.format(
            profile=profile,
            memory=memory,
            question=question
        )
        
        response = ''
        while not response:
            response = self.llm.chat_and_check_keywords(
                query=query, 
                keywords=keywords,
                temperature=self.temperature, 
                max_tries=self.max_tries
            )

        results = {
            'thoughts': response[response.find('Thoughts:')+len('Thoughts:'):response.find('Rating:')].strip(),
            'rating': eval(find_ratings(response[response.find('Rating:')+len('Rating:'):].strip())[0])
        }

        self.logger.put("thought", f'Q: {question}')
        self.logger.put("thought", results['thoughts'])
        self.logger.put("execute", results['rating'])

        return results