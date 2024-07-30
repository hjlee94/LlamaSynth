
from llama_synth import LlamaModerator, LlamaSpeaker

if __name__ == '__main__':

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
    moderator.interview(assistant=assistant, n=5)


