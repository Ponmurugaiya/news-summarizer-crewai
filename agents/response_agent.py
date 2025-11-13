# response_agent.py
from crewai import Agent

class ResponseAgent(Agent):
    def __init__(self, role, llm):
        super().__init__(
            role=role,
            goal="Summarize scraped news into readable paragraphs, ignoring irrelevant news",
            backstory="Creates concise, human-readable summaries from scraped news",
            llm=llm
        )

    def execute_task(self, task_input=None, **kwargs):
        """
        task_input should be a dictionary returned by ScraperAgent:
        {
            "search_terms": "user query",
            "candidate_headlines": [
                {"title": "...", "summary": "..."},
                {"title": "...", "summary": "..."}
            ]
        }
        """
        if not isinstance(task_input, dict):
            return "Invalid input for ResponseAgent. Expected a dictionary."

        scraped_news = task_input.get("candidate_headlines", [])
        search_terms = task_input.get("search_terms", "")

        if not scraped_news:
            return "No news found to summarize."

        # Convert each item to a string (title + optional summary)
        news_strings = []
        for item in scraped_news:
            if isinstance(item, dict):
                title = item.get("title", "").strip()
                summary = item.get("summary", "").strip()
                combined = f"{title} - {summary}" if summary else title
                news_strings.append(combined)
            elif isinstance(item, str):
                news_strings.append(item)

        if not news_strings:
            return "No news found to summarize."

        news_text = "\n".join(news_strings)

        prompt = f"""
You are an expert news summarization AI.
Search query: {search_terms}

Summarize the following candidate news snippets into a single, coherent paragraph.
⚠️ Ignore any headlines that are irrelevant to the search query.
Provide a detailed, understandable summary that conveys the main points clearly.

Candidate headlines:
{news_text}
        """

        result = self.llm.call(prompt)
        return result.strip()
