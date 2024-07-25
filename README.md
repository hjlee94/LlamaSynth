# LlamaSynth
It is to generate synthetic text data, making Llama agents to chat each other

```python
    from llama_synth import LlamaModerator, LlamaSpeaker

    moderator = LlamaModerator(log_path="./chat.tsv")

    agent1 = LlamaSpeaker.from_card("./cards/man_T.yaml")
    agent2 = LlamaSpeaker.from_card("./cards/woman_F.yaml")

    moderator.add_agent(agent1)
    moderator.add_agent(agent2)

    moderator.role_play(n=5, n_toss=6)
```

```
[F Person] >> I'd like to role-play a situation where we're on a team at work, and we're discussing a new project proposal. I'll start by saying:  "I'm really concerned about the impact this new project will have on our team's workload. We're already stretched thin, and I don't want to compromise the quality of our work. How do you think we can balance the new project's demands with our existing responsibilities?"  Your turn!

[T Person] >> I see your point, but what's the exact data on our current workload and team capacity? Have we quantified the potential impact of this new project on our output and efficiency? I'd like to see some hard numbers to make a more informed decision.

[F Person] >> Numbers and data can be helpful, but I'm worried that we might be forgetting the human side of this project. How will it affect the team's morale and stress levels? Won't it be hard on the team members who already have a lot on their plates?

[T Person] >> You're bringing up the emotional aspect of this project. I'm not sure how to respond to that, as it seems to be based on feelings rather than facts. Can you provide data on how team morale and stress levels have been affected by similar projects in the past?

[F Person] >> I'm not sure I agree that it's all about facts and figures. Don't you think that people's emotions and well-being play a big role in how successful a project can be? How do you think our team members will feel if they're not considered in the decision-making process?

[T Person] >> I see what you're getting at. You're saying that people's feelings and emotions are a crucial factor in decision-making. But don't you think that's subjective and unreliable? How can we ensure that our decisions are based on consistent and objective standards, rather than just trying to accommodate everyone's feelings?

RING RING 🔔🔔
```

