from typing import List, Callable, Optional

from . import LlamaSpeaker

import random

type QuestionGetter = Callable[[], str]

class Topic:
    def __init__(self, question, topic_list:List[str]=[]) -> None:
        self.question = question

        if topic_list:
            self.topic_list = topic_list
        else:
            self.topic_list = ["you choose"]

    def get_topic(self) -> str:
        idx = random.randint(0, len(self.topic_list)-1)
        return self.topic_list[idx]
    
    def get_question_getter(self) -> QuestionGetter:
        def get_q():
            return f"{self.question} The topic is {self.get_topic()}"
        
        return get_q
    
class LlamaModerator:

    def __init__(self, topic:Topic, log_path=None) -> None:
        self._agent_pool = []
        self._idx = 0

        self._topic = topic

        self._log_path = log_path
        
    def add_agent(self, agent:LlamaSpeaker) -> None:
        self._agent_pool.append(agent)

    def get_next_agent(self, is_first:bool=False) -> LlamaSpeaker:
        if is_first:
            self._idx = random.randint(0, len(self._agent_pool)-1)

        else:
            self._idx = (self._idx + 1) % len(self._agent_pool)

        agent = self._agent_pool[self._idx]

        return agent
    
    def log(self, *s:str) -> None:
        if not self._log_path:
            return
        
        contents = '\t'.join(s)
        with open(self._log_path, 'a', encoding='utf-8') as fd:
            fd.write(f"\n{contents}")
    
    def relay(self, n:int=5, n_toss:int=10) -> None:
        get_q = self._topic.get_question_getter()

        for _ in range(n):
            inp = get_q()

            for i in range(n_toss):
                agent = self.get_next_agent(is_first= i==0)
                answer = agent(inp).replace('\n', ' ')
                print(f'[{agent.name}] >> {answer}\n')

                self.log(agent.name, answer)

                inp = answer
            
            print(f"RING RING 🔔🔔")
            [agent.prompt.history.clear_history() for agent in self._agent_pool]

    def interview(self, assistant:LlamaSpeaker, n:int=5) -> None: 
        get_q = self._topic.get_question_getter()

        for _ in range(n):
            answer = assistant(get_q())
            answer = answer.replace('\n', ' ')
            print(f'[{assistant.name}] >> {answer}\n')

            inp = answer

            log_msg = []

            for agent in self._agent_pool:
                answer = agent(inp).replace('\n', ' ')
                print(f'[{agent.name}] >> {answer}\n')

                log_msg.append(agent.name)
                log_msg.append(answer)
            
            self.log(*log_msg)
            
            [agent.prompt.history.clear() for agent in self._agent_pool]
