from onyx.agents.base import Agent


class Coordinator(Agent):
    name = "coordinator"
    role = "Releases the scenario events in stages and routes information between agents."
