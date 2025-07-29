from genagents.genagents import GenerativeAgent


#agent_folder = r"agent_bank\populations\single_agent\01fd7d2a-0357-4c1b-9f3e-8eade2d537ae"
agent_folder = r"agent_bank/populations/AGA_agents/Isabella Rodriguez"

agent = GenerativeAgent(agent_folder)

#agent.update_scratch({
#    "first_name": "John",
#    "last_name": "Doe",
#    "age": 30,
#    "occupation": "Software Engineer",
#    "interests": ["reading", "hiking", "coding"]
#})

dialogue = [
    ("Interviewer", "Tell me about your favorite hobby."),
]

response = agent.utterance(dialogue)
print(response)