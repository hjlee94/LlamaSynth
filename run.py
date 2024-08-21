
def interview_example():
    from llama_synth import LlamaModerator, LlamaSpeaker
    from llama_synth.moderator import Topic
    from llama_synth.prompt import Prompt

    agent1 = LlamaSpeaker.from_card("./cards/sheldon.yaml")
    agent2 = LlamaSpeaker.from_card("./cards/harry.yaml")

    assistent = LlamaSpeaker(
        name="assistant",
        model_path="./models/llama-8b-v3.1-F16.gguf",
        prompt=Prompt(
            system_prompt="You are an interview assistant who generate a casual question",
            template=None
            )
        )
 
    topic = Topic(
        question = "Give me a question for interview",
        topic_list = ["Science", "Lord Voldemort"]
        )
    
    print(topic.get_question_getter()())
    
    moderator = LlamaModerator(topic=topic, log_path="./example.tsv")

    moderator.add_agent(agent1)
    moderator.add_agent(agent2)
    
    moderator.interview(assistant=assistent, n=2)

def relay_example():
    from llama_synth import LlamaModerator, LlamaSpeaker
    from llama_synth.moderator import Topic


    agent1 = LlamaSpeaker.from_card("./cards/sheldon.yaml")
    agent2 = LlamaSpeaker.from_card("./cards/harry.yaml")

    topic = Topic(
        question = "Let's start the discussion.",
        topic_list = ["Science", "Lord Voldemort"]
        )
    
    print(topic.get_question_getter()())
    
    moderator = LlamaModerator(topic=topic, log_path="./example.tsv")

    moderator.add_agent(agent1)
    moderator.add_agent(agent2)

    moderator.relay(n=1, n_toss=4)

def classify_label():
    from llama_synth import LlamaSpeaker
    from llama_synth.prompt import Prompt
    from llama_synth.prompt.template import get_classification_template

    prompt = Prompt.with_classification_template(
        system_prompt="You are a classifier for T personality and F personality of MBTI. You reponse only a label name",
        label_names=['T Personality', 'F Personality']
    )

    agent = LlamaSpeaker(
        model_path="./models/llama-8b-v3.1-F16.gguf",
        name="classifier",
        prompt=prompt
        )
    agent.set_classification_mode()
    
    # inp = "That is the world works. You should practice more"
    # inp = "You have a headache. Opening the door would be helpful."
    inp = "In real life, the probability of that happening is extremely low"
    # inp = "I'm sorry. You can get a first place next time"
    
    resp = agent(inp)

    print(resp)

if __name__ == '__main__':
    # classify_label()
    relay_example()
    # interview_example()
