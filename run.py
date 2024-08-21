
def interview_example():
    from llama_synth import LlamaModerator, LlamaSpeaker
    from llama_synth.moderator import Topic
    from llama_synth.prompt import Prompt

    agent1 = LlamaSpeaker.from_card("./cards/sheldon.yaml")
    agent2 = LlamaSpeaker.from_card("./cards/leslie.yaml")

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
        topic_list = None
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
        system_prompt="You are a classifier for Review Preference (Bad or Good). You reponse only a label name",
        label_names=['Bad', 'Good']
    )

    agent = LlamaSpeaker(
        model_path="./models/llama-8b-v3.1-F16.gguf",
        name="classifier",
        prompt=prompt
        )
    agent.set_classification_mode()
    
    inp_list = [
        "This hotel is not good for a business. The bed is the worst I'd ever seen",
        "The room is so clean. House-keeping is the best in the world. It makes my day happy",
        "A rat comes out in the bathroom.",
        "The most of staffs were kind but few were very rude."
    ]
    
    for inp in inp_list:
        resp = agent(inp)
        print(f"[input] >> {inp}")
        print(f"[prediction] >> {resp}")

if __name__ == '__main__':
    classify_label()
    # relay_example()
    # interview_example()
