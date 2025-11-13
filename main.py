# main.py
import os
from crewai import LLM
from agents.query_agent import QueryAgent
from agents.scraper_agent import ScraperAgent
from agents.response_agent import ResponseAgent

# ---------------------------
# Setup Gemini LLM
# ---------------------------
gemini_llm = LLM(
    model="gemini/gemini-2.5-flash",
    api_key=os.getenv("GEMINI_API_KEY"),
    temperature=0.7
)

# ---------------------------
# Instantiate Agents
# ---------------------------
query_agent = QueryAgent(role="Query Generator", llm=gemini_llm)
scraper_agent = ScraperAgent(role="Web Scraper", llm=gemini_llm)  # no LLM needed
response_agent = ResponseAgent(role="Response Generator", llm=gemini_llm)

# ---------------------------
# User input
# ---------------------------
user_question = "Latest AI developments in India"

# ---------------------------
# Step 1: Generate search keywords
# ---------------------------
search_terms = query_agent.execute_task({"question": user_question})
print(f"🔎 Search Keywords: {search_terms}")

# ---------------------------
# Step 2: Scrape news
# ---------------------------
scraped_news_dict = scraper_agent.execute_task({"search_terms": search_terms})
print(f"📰 Scraped News: {scraped_news_dict}")

# ---------------------------
# Step 3: Generate final response
# ---------------------------
final_reply = response_agent.execute_task(scraped_news_dict)
print(f"\n💬 Final News Summary:\n{final_reply}")
