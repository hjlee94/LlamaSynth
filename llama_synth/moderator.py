import random
import os

class LlamaModerator:

    def __init__(self, topic=[], log_path=None) -> None:
        self._speaker_pool = []
        self._idx = 0

        self._topic = topic
        if not topic:
            self._topic = ['you choose']

        self._log_path = log_path
        
    def add_agent(self, agent):
        self._speaker_pool.append(agent)

    def get_next_agent(self, is_first=False):
        if is_first:
            self._idx = random.randint(0, len(self._speaker_pool)-1)

        else:
            self._idx = (self._idx + 1) % len(self._speaker_pool)

        agent = self._speaker_pool[self._idx]

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
    
    def discuss(self, n=5, n_toss=10):
        def get_q():
            return f"let's start the discussion with the topic {self.get_topic()}"

        self._start(get_q, n, n_toss)

    def role_play(self, n=5, n_toss=10):
        def get_q():
            return f"let's start role-playing with situation {self.get_topic()}"
        
        self._start(get_q, n, n_toss)

    def simulate_play(self, n=5, n_toss=10):
        def get_q():
            return f"let's start discussion how we should act when we are im a situation {self.get_topic()}"
        
        self._start(get_q, n, n_toss)

    def _start(self, get_q, n=5, n_toss=10):
        for _ in range(n):
            inp = get_q()

            for i in range(n_toss):
                agent = self.get_next_agent(is_first= i==0)
                answer = agent.generate(inp).replace('\n', ' ')
                print(f'[{agent.name}] >> {answer}\n')

                self.log(agent.name, answer)

                inp = answer
            
            print(f"RING RING 🔔🔔")
            [agent.clear_history() for agent in self._speaker_pool]