
from llama_synth import LlamaModerator, LlamaSpeaker
if __name__ == '__main__':

    moderator = LlamaModerator(log_path="./chat.tsv")

    # agent1 = LlamaSpeaker.from_card("./cards/sheldon.yaml")
    # agent2 = LlamaSpeaker.from_card("./cards/leslie.yaml")
    # agent3 = LlamaSpeaker.from_card("./cards/harry.yaml")
    agent1 = LlamaSpeaker.from_card("./cards/man_T.yaml")
    agent2 = LlamaSpeaker.from_card("./cards/woman_F.yaml")

    moderator.add_agent(agent1)
    moderator.add_agent(agent2)
    # moderator.add_agent(agent3)

    moderator.role_play(n=5, n_toss=6)
