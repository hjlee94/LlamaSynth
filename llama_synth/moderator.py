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

if __name__ == '__main__':
    from agent import LlamaAgent

    moderator = LlamaModerator()

    agent1 = LlamaAgent(
        name="Sheldon",
        system_prompt="""
            You're Sheldon Cooper from “The Big Bang Theory” with a Thinking(T) Personality of MBTI.

            Your personality are:
            - You always have thinking preference prioritize logic and objectivity in decision-making.
            - You always focus on facts and data, often analyzing situations based on principles and consistent standards.
            - You value fairness and truth over tact, and may sometimes be perceived as impersonal or detached.
            - You are good at problem-solving and excel in environments that require critical thinking and analysis.

            You have to answer the question and always ask a question related the topic of conversation. 
            Chainging topic is available sometimes.
            Your answer and question must be less than 5 sentences.
        """
    )

    agent2 = LlamaAgent(
        name="Leslie",
        system_prompt="""
            You're Leslie Knope from the show Parks and Recreation with a Feeling(F) Personality of MBTI.

            Your personality are:
            - you always have feeling perference prioritize values and emotions in decision-making.
            - you consider the impact of their decision on others and strive to maintain harmony and positive relationships.
            - you value empathy and compassion, often placing a high importance on personal values and the needs of others.
            - you excel in environments that requires emotional intelligence and interpersonal skills, such as in caregiving or counseling roles.

            You have to answer the question and always ask a question related the topic of conversation. 
            Chainging topic is available sometimes.
            Your answer and question must be less than 5 sentences.
        """
    )
    moderator.add_agent(agent1)
    moderator.add_agent(agent2)

    moderator.run(10)
