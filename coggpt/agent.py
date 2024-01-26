import os
import random
random.seed(0)
import argparse
import traceback

from coggpt.update import UpdateAgent
from coggpt.distill import DistillAgent
from coggpt.memory import Memory
from coggpt.grade import GradeAgent
from utils.file_utils import load_json, dump_json, text_to_dict
from utils.chain_logger import *


class CogGPT:
    def __init__(
        self,
        resume=False,
        resume_path=os.path.join('datasets', 'english', 'cogbench_a.json'),
        resume_method='CogGPT',
        profile='',
        profile_path=os.path.join('datasets', 'english', 'profile.json'),
        iteration=0,
        topic='Gossip',
        max_iterations=10,
        cogbench_path=os.path.join('datasets', 'english', 'cogbench_a.json'),
        update_prompt='update',
        update_model_name='gpt-4',
        update_temperature=0,
        update_max_tries=20,
        distill_prompt='distill',
        distill_model_name='gpt-4',
        distill_temperature=0,
        distill_max_tries=20,
        memory_dir='memory',
        memory_folder='',
        openai_api_key=os.environ.get('OPENAI_API_KEY'),
        chunk_size=1000,
        chunk_overlap=100,
        grade_prompt='grade',
        grade_model_name='gpt-4',
        grade_temperature=0,
        grade_max_tries=20,
        logger=True
    ):
        self.logger = ChainMessageLogger() if logger else None

        if resume:
            self.initial_profile, self.profile, self.iteration, self.topic = self.load(resume_method, resume_path)
        else:
            self.profile = profile if profile else self.get_profile(profile_path)
            self.initial_profile = text_to_dict(self.profile)
            self.iteration = iteration
            self.topic = topic
        self.logger.put("observation", f'I am\n{self.profile}')
        self.logger.put("observation", f'I am perceiving information flows about {self.topic} in the {self.iteration}th iteration.')

        self.max_iterations = max_iterations
        self.information_flow = self.get_information_flow(cogbench_path)
        self.questionnaire = self.get_questionnaire(cogbench_path)

        self.update_agent = UpdateAgent(
            update_prompt=update_prompt,
            model_name=update_model_name,
            temperature=update_temperature,
            max_tries=update_max_tries,
            logger = self.logger
        )

        self.distill_agent = DistillAgent(
            distill_prompt=distill_prompt,
            model_name=distill_model_name,
            temperature=distill_temperature,
            max_tries=distill_max_tries,
            logger = self.logger
        )
        
        self.memory = Memory(
            memory_dir=memory_dir,
            memory_folder=os.path.join(self.topic, self.initial_profile['Name']) if not memory_folder else memory_folder,
            openai_api_key=openai_api_key,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )

        self.grade_agent = GradeAgent(
            grade_prompt=grade_prompt,
            model_name=grade_model_name,
            temperature=grade_temperature,
            max_tries=grade_max_tries,
            logger = self.logger
        )


    def run(self,
        update_keywords=['Assessments:', 'Thoughts:', 'Updated Profile:', 'Name: ', 'Future Outlook:'],
        grade_keywords=['Thoughts:', 'Rating:'],
        method_name='CogGPT',
        cogbench_path=os.path.join('datasets', 'english', 'cogbench_a.json'),
        results_path=os.path.join('datasets', 'english', 'eval_cogbench_a.json')
    ):
        try:
            while self.iteration <= self.max_iterations:
                self.perceive(update_keywords)
                results = self.interpret(grade_keywords)
                self.save(results, method_name, cogbench_path, results_path)
        except Exception as e:
            self.logger.put("observation", f"An unexpected error occurred: {str(e)}")
            traceback.print_exc()


    def perceive(self, keywords):
        try:
            short_term_memory = self.get_current_information_flow(self.information_flow[self.iteration])
            
            if short_term_memory:
                knowledge = self.distill_agent.distill(
                    profile=self.profile, 
                    memory=short_term_memory
                )
                self.memory.store(knowledge)

                self.profile = self.update_agent.update(
                    profile=self.profile, 
                    memory=short_term_memory, 
                    keywords=keywords
                )['updated']
                
            self.iteration += 1
        except Exception as e:
            self.logger.put("observation", f"An unexpected error occurred: {str(e)}")
            traceback.print_exc()


    def interpret(self, keywords):
        try:
            results = []
            for question in self.questionnaire:
                grade = self.grade_agent.grade(
                    profile=self.profile, 
                    memory='\n'.join(self.memory.recall(question['question'])) if self.iteration > 1 else '', 
                    question=question['question'], 
                    keywords=keywords
                )

                results.append({
                    'question': question['question'],
                    'rating': grade['rating'],
                    'reason': grade['thoughts']
                })
            return results
        except Exception as e:
            self.logger.put("observation", f"An unexpected error occurred: {str(e)}")
            traceback.print_exc()


    # Retrieves a random profile from the given file.
    def get_profile(self, profile_path):
        try:
            profile = random.sample(load_json(profile_path), 1)[0]
            return '\n'.join(f'{item[0]}: {item[1]}' for item in profile.items())
        except Exception as e:
            self.logger.put("observation", f"An unexpected error occurred: {str(e)}")
            traceback.print_exc()
        return ''


    # Retrieves the cognitive questionnaire for the given topic from CogBench.
    def get_questionnaire(self, cogbench_path):
        try:
            data = load_json(cogbench_path)
            for item in data:
                if item.get('topic') == self.topic:
                    return item.get('questionnaire')
        except Exception as e:
            self.logger.put("observation", f"An unexpected error occurred: {str(e)}")
            traceback.print_exc()
        return []


    # Retrieves the inforamtion flow for the given topic from CogBench.
    def get_information_flow(self, cogbench_path):
        information_flow = []
        try:
            data = load_json(cogbench_path)
            for item in data:
                if item.get('topic') == self.topic:
                    information_flow.append(item.get('information_flow'))
        except Exception as e:
            self.logger.put("observation", f"An unexpected error occurred: {str(e)}")
            traceback.print_exc()
        return information_flow


    # Retrieves the current inforamtion flow for the given topic from CogBench.
    def get_current_information_flow(self, current_information_flow):
        concatenated_information = []
        for item in current_information_flow:
            concatenated_information.append('\n'.join(str(value) for value in item.values() if value)) if isinstance(item, dict) else concatenated_information.append(item)
        return '\n\n'.join(concatenated_information)


    def get_current_iteration_settings(self, iteration, cogbench_path):
        try:
            data = load_json(cogbench_path)
            for item in data:
                if item.get('iteration') == iteration and item.get('topic') == self.topic:
                    return item
        except Exception as e:
            self.logger.put("observation", f"An unexpected error occurred: {str(e)}")
            traceback.print_exc()
        return {}


    def load(self, method_name, resume_path):
        try:
            data = load_json(resume_path)[-1]
            initial_profile = data['profile']
            profile = data['questionnaire'][0]['answer'][method_name].get('profile', '') if data['questionnaire'][0]['answer'][method_name].get('profile', '') else data['profile']
            iteration = data['iteration']
            topic = data['topic']
            return initial_profile, profile, iteration+1, topic
        except Exception as e:
            self.logger.put("observation", f"An unexpected error occurred: {str(e)}")
            traceback.print_exc()

        self.logger.put("observation", f"No eligible results.")


    def save(self, results, method_name, cogbench_path, results_path):
        data = load_json(results_path) if os.path.exists(results_path) else []

        for item in data:
            if item.get('iteration') == self.iteration-1 and item.get('topic') == self.topic and item.get('profile').get('Name') == self.initial_profile['Name']:
                for result_item, questionnaire_item in zip(results, item.get('questionnaire')):
                    assert result_item['question'] == questionnaire_item['question']

                    questionnaire_item['answer'][method_name] = {
                        "profile": self.profile,
                        "rating": result_item['rating'],
                        "reason": result_item['reason'],
                        "rationality": -1
                    }

                dump_json(data, results_path)
                self.logger.put("execute", f"Successfully save results in {results_path}.")
                return

        current_iteration_settings = self.get_current_iteration_settings(self.iteration-1, cogbench_path)
        current_iteration_settings['profile'] = self.initial_profile
        for result_item, questionnaire_item in zip(results, current_iteration_settings.get('questionnaire')):
            assert result_item['question'] == questionnaire_item['question']

            questionnaire_item['answer'] = {"human_rating": -1} # default value
            questionnaire_item['answer'][method_name] = {
                "profile": self.profile,
                "rating": result_item['rating'],
                "reason": result_item['reason'],
                "rationality": -1 # default value
            }
        
        data.append(current_iteration_settings)
        dump_json(data, results_path)
        self.logger.put("execute", f"Successfully save results in {results_path}.")


def add_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("--resume", action='store_true', default=False, help="Whether to resume from previous settings")
    parser.add_argument("--resume_path", type=str, default=os.path.join('datasets', 'english', 'eval_cogbench_a.json'), help="Path to resume previous settings")
    parser.add_argument("--resume_method", type=str, default='CogGPT', help="the method name of previous settings")
    parser.add_argument("--profile", type=str, default='', help="Profile. Will not be activated when resume is True.")
    parser.add_argument("--profile_path", type=str, default=os.path.join('datasets', 'english', 'profile.json'), help="Path to select a predefined profile. Will not be activated when resume is True.")
    parser.add_argument("--iteration", type=int, default=0, help="Current iteration(≤10). Will not be activated when resume is True.")
    parser.add_argument("--topic", type=str, default='Gossip', help="Topic selected from Cogbench. Will not be activated when resume is True.")
    parser.add_argument("--max_iterations", type=int, default=10, help="Maximum iterations(≤10)")
    parser.add_argument("--cogbench_path", type=str, default=os.path.join('datasets', 'english', 'cogbench_a.json'), help="Path to the Cogbench of article")
    parser.add_argument("--memory_dir", type=str, default='memory', help="Memory directory for memory.py")
    parser.add_argument("--memory_folder", type=str, default='', help="Memory folder for memory.py")
    parser.add_argument("--openai_api_key", type=str, default=os.environ.get('OPENAI_API_KEY'), help="OpenAI API key")
    parser.add_argument("--logger", type=bool, default=True, help="Enable or disable logging")

    parser.add_argument("--method_name", type=str, default='CogGPT', help="Method name of current settings")
    parser.add_argument("--results_path", type=str, default=os.path.join('datasets', 'english', 'test.json'), help="Path to save the results of current settings")

    return parser.parse_args()


def main():
    args = add_args()

    coggpt = CogGPT(
        resume=args.resume,
        resume_path=args.resume_path,
        resume_method=args.resume_method,
        profile=args.profile,
        profile_path=args.profile_path,
        iteration=args.iteration,
        topic=args.topic,
        max_iterations=args.max_iterations,
        cogbench_path=args.cogbench_path,
        memory_dir=args.memory_dir,
        memory_folder=args.memory_folder,
        openai_api_key=args.openai_api_key,
        logger=args.logger
    )
    coggpt.run(method_name=args.method_name, results_path=args.results_path)


if __name__ == '__main__':
    sys.exit(main())