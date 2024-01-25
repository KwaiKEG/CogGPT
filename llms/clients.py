import os
import time
import random
import openai
import traceback

from utils.file_utils import loads_json, find_ratings

def make_gpt_messages(query, system, history):
    msgs = list()
    if system:
        msgs.append({
            "role": "system",
            "content": system
        })
    for q, a in history:
        msgs.append({
            "role": "user",
            "content": str(q)
        })
        msgs.append({
            "role": "assistant",
            "content": str(a)
        })
    msgs.append({
        "role": "user",
        "content": query
    })
    return msgs


class OpenAIClient(object):
    def __init__(self, model="gpt-3.5-turbo"):
        self.model = model
        openai.api_type = os.environ.get("OPENAI_API_TYPE", "open_ai")
        openai.api_key = os.environ["OPENAI_API_KEY"]
        if openai.api_type == "azure":
            openai.api_version = os.environ["OPENAI_API_VERSION"]
            openai.api_base = os.environ["OPENAI_API_BASE"]
    
    
    def chat(self, query, history=list(), system="", temperature=0.0, stop="", *args, **kwargs):
        msgs = make_gpt_messages(query, system, history)

        try:
            if openai.api_type == "open_ai":
                response = openai.ChatCompletion.create(
                    model=self.model,
                    messages=msgs,
                    temperature = temperature,
                    stop=stop
                )
            elif openai.api_type == "azure":
                response = openai.ChatCompletion.create(
                    engine = self.model,
                    messages=msgs,
                    temperature = temperature,
                    stop=stop
                )
            response_text = response['choices'][0]['message']['content']
        except:
            print(traceback.format_exc())
            response_text = ""

        new_history = history[:] + [[query, response_text]]
        return response_text, new_history


    def chat_and_check_keywords(self, query, keywords, temperature=0.0, max_tries=20):
        response = []
        while max_tries > 0:
            try:
                response, _ = self.chat(
                    query=query,
                    temperature=temperature
                )
                
                assert all(w in response for w in keywords)
                if 'Rating: ' in keywords:
                    assert len(find_ratings(response[response.find('Rating: ')+len('Rating: '):].strip())) == 1
                    
                return response
                break
            except Exception:
                time.sleep(random.uniform(0, 5))
                max_tries -= 1
        return response


    def chat_and_check_json(self, query, temperature=0.0, max_tries=20):
        response = []
        while max_tries > 0:
            try:
                response, _ = self.chat(
                    query=query,
                    temperature=temperature
                )
                return loads_json(response)
                break
            except Exception:
                time.sleep(random.uniform(0, 5))
                max_tries -= 1
        return response