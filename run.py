
from llama_synth import LlamaModerator, LlamaSpeaker

def generate_synth_data_on_interview():

    moderator = LlamaModerator(log_path="./interview.tsv")

    # agent1 = LlamaSpeaker.from_card("./cards/sheldon.yaml")
    # agent2 = LlamaSpeaker.from_card("./cards/leslie.yaml")
    # agent3 = LlamaSpeaker.from_card("./cards/harry.yaml")
    assistant = LlamaSpeaker.from_card("./cards/assistant.yaml")

    agent1 = LlamaSpeaker.from_card("./cards/guest_T.yaml")
    agent2 = LlamaSpeaker.from_card("./cards/guest_F.yaml")

    moderator.add_agent(agent1)
    moderator.add_agent(agent2)

    # moderator.discuss_q(get_q=moderator.simulate_play_q, n=5, n_toss=6)
    moderator.interview(assistant=assistant, n=1000)

def classify_label():
    agent = LlamaSpeaker(
        model_path="./models/llama-8b-v3.1-F16.gguf",
        name="classifier",
        system_prompt="You are a classifier reponses only a label name",
        )
    agent.set_classification_mode(
        label_name=["T Personality", "F Personality"]
    )
    
    # inp = "That is the world works. You should practice more"
    inp = "You have a headache. Opening the door would be helpful."
    # inp = "I'm sorry. You can get a first place next time"
    # i =f"Classify the text into T(Thinking) Personality or F(Feeling) Personality in MBTI\nText:{inp}\nLabel:"
    resp = agent.generate(inp)

    print(resp)

if __name__ == '__main__':
    classify_label()
