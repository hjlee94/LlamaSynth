import random

class LlamaModerator:
    # TODO: Logging feature required

    def __init__(self) -> None:
        self._agent_pool = []
        self._idx = 0

        self._topic = ['ice-breaking']

    def add_agent(self, agent):
        self._agent_pool.append(agent)

    def get_next_agent(self):
        idx = (self._idx + 1) % len(self._agent_pool)
        agent = self._agent_pool[idx]
        self._idx += 1

        return agent
    
    def get_topic(self):
        idx = random.randint(0, len(self._topic)-1)
        return self._topic[idx]

    
    def run(self, n=10):
        inp = f"let's start the discussion with the topic of {self.get_topic()}"

        for _ in range(n):
            agent = self.get_next_agent()
            answer = agent._generate(inp)
            print(f'[{agent.name}] >> {answer}\n')

            inp = answer