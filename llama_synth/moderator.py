import random
import os

class LlamaModerator:

    def __init__(self, topic=[], log_path=None) -> None:
        self._agent_pool = []
        self._idx = 0

        self._topic = topic
        if not topic:
            self._topic = ['you choose']

        self._log_path = log_path
        
    def add_agent(self, agent):
        self._agent_pool.append(agent)

    def get_next_agent(self, is_first=False):
        if is_first:
            self._idx = random.randint(0, len(self._agent_pool)-1)

        else:
            self._idx = (self._idx + 1) % len(self._agent_pool)

        agent = self._agent_pool[self._idx]

        return agent
    
    def get_topic(self):
        idx = random.randint(0, len(self._topic)-1)
        return self._topic[idx]
    
    def log(self, name, sentence):
        if not self._log_path:
            return
        
        if not os.path.exists(self._log_path):
            with open(self._log_path, 'w', encoding='utf-8') as fd:
                fd.write(f"name\tlines")

        with open(self._log_path, 'a', encoding='utf-8') as fd:
            fd.write(f"\n{name}\t{sentence}")
    
    def discuss_q(self):
        def get_q():
            return f"let's start the discussion with the topic {self.get_topic()}"

        return get_q

    def role_play_q(self):
        def get_q():
            return f"let's start role-playing with situation {self.get_topic()}"
        
        return get_q

    def simulate_play_q(self):
        def get_q():
            return f"let's start discussion how we should act when we are in a situation {self.get_topic()}"
        
        return get_q

    def relay(self, get_q=None, n=5, n_toss=10):
        if not get_q:
            get_q = self.discuss_q

        for _ in range(n):
            inp = get_q()

            for i in range(n_toss):
                agent = self.get_next_agent(is_first= i==0)
                answer = agent.generate(inp).replace('\n', ' ')
                print(f'[{agent.name}] >> {answer}\n')

                self.log(agent.name, answer)

                inp = answer
            
            print(f"RING RING 🔔🔔")
            [agent.clear_history() for agent in self._agent_pool]

    def situation_q(self):
        return f"give me a situation about {self.get_topic()}"

    def interview(self, assistant, get_q=None, n=5):
        if not get_q:
            get_q = self.situation_q

        for _ in range(n):
            answer = assistant.generate(get_q())
            answer = answer.replace('\n', ' ')
            print(f'[{assistant.name}] >> {answer}\n')

            inp = answer

            for agent in self._agent_pool:
                answer = agent.generate(inp).replace('\n', ' ')
                print(f'[{agent.name}] >> {answer}\n')

                self.log(agent.name, answer)
            
            [agent.clear_history() for agent in self._agent_pool]
