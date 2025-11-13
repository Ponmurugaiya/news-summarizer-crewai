# query_agent.py
from crewai import Agent

class QueryAgent(Agent):
    def __init__(self, role, llm):
        super().__init__(
            role=role,
            goal="Convert user question into concise search keywords",
            backstory="Generates short keyword strings for news searches",
            llm=llm
        )

    def execute_task(self, task_input=None, **kwargs):
        question = task_input.get("question") if isinstance(task_input, dict) else task_input
        prompt = f"""
        You are a helpful assistant that converts user news questions into concise search keywords.
        User question: "{question}"
        Return only a short keyword string suitable for a news search.
        """
        result = self.llm.call(prompt)
        return result.strip()
