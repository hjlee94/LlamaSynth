# LlamaSynth


## 1. Introduction
It is to generate synthetic text data, using Llama language model. Currently, It has below features.
* "Relay" to generate synthetic data, talking to each other.
* "Interview" to generate a pair of synthetic data in a topic.
* "Classification" to classify text data into specific label.

## 2. Overview
(TBD)


## 3. Example

### 1. Relay
```python
    from llama_synth import LlamaModerator, LlamaSpeaker
    from llama_synth.moderator import Topic

    agent1 = LlamaSpeaker.from_card("./cards/sheldon.yaml")
    agent2 = LlamaSpeaker.from_card("./cards/harry.yaml")

    topic = Topic(
        question = "Let's start the discussion.",
        topic_list = ["Science", "Lord Voldemort"]
        )
        
    moderator = LlamaModerator(topic=topic, log_path="./example.tsv")

    moderator.add_agent(agent1)
    moderator.add_agent(agent2)

    moderator.relay(n=5, n_toss=10)
```

```
[Sheldon] >> Science is the pursuit of knowledge through empirical evidence and systematic observation. What's the most fascinating scientific discovery of the past century, in your opinion?  (Note: I'll respond with a brief answer, followed by a question related to the topic.)

[Harry] >> I think it's the discovery of dark matter! It's like this invisible magic that's all around us, but we can't see it.  Do you think the wizarding world's understanding of magic would be similar to our understanding of dark matter if we didn't study it with our Muggle science?

[Sheldon] >> A delightful topic. While the analogy between dark matter and magic is intriguing, I think our understanding of dark matter is more akin to understanding a complex mathematical equation. The wizarding world's understanding of magic would likely be based on observation and tradition, whereas our understanding of dark matter is grounded in empirical evidence and theoretical frameworks. Do you think the scientific community would be more accepting of magic if it were proven to exist in the same way we're accepting of dark matter's existence?

[Harry] >> That's a good point. I think scientists would be more interested in understanding magic if it were proven to exist. They'd want to study the underlying mechanisms and forces behind it, just like they do with dark matter. Do you think the discovery of magic would lead to a greater emphasis on the study of the supernatural in the scientific community?

RING RING 🔔🔔
```

### 2. Interview

```python
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
```

```
[assistant] >> Let's say the topic is "Travel". Here's a casual question for you:  "If you could travel anywhere in the world right now, where would you go and what's the first thing you'd do when you get there?"

[Sheldon] >> A straightforward question. I'd go to CERN in Switzerland, as it's the European Organization for Nuclear Research. The first thing I'd do upon arrival is visit the ATLAS experiment, to observe the Large Hadron Collider in action. What's the most efficient mode of transportation to get there from Pasadena?

[Leslie] >> I've always dreamed of visiting the Pacific Northwest, specifically the Columbia River Gorge in Oregon. The natural beauty and serenity of that place would be so rejuvenating for me. The first thing I'd do is hike to the top of Multnomah Falls and take in the breathtaking views. Wouldn't it be amazing to combine that with a trip to a small town to help them develop their local park system? Have you ever visited the Pacific Northwest?
```

### 3. Classification

```python
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
```

```
[input] >> This hotel is not good for a business. The bed is the worst I'd ever seen
[prediction] >> Bad
[input] >> The room is so clean. House-keeping is the best in the world. It makes my day happy
[prediction] >> Good
[input] >> A rat comes out in the bathroom.
[prediction] >> Bad
[input] >> The most of staffs were kind but few were very rude
[prediction] >> Good
```