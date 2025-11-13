# scraper_agent.py
from crewai import Agent
import feedparser
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote

# Expanded and relevant news sources
NEWS_SOURCES = [
    {"name": "Times of India", "rss": "https://timesofindia.indiatimes.com/rssfeedstopstories.cms", "search_url": "https://timesofindia.indiatimes.com/topic/{query}"},
    {"name": "NDTV", "rss": "https://www.ndtv.com/rss/news", "search_url": "https://www.ndtv.com/topic/{query}"},
    {"name": "The Hindu", "rss": "https://www.thehindu.com/news/national/feeder/default.rss", "search_url": "https://www.thehindu.com/search/?q={query}"},
    {"name": "TechRadar", "rss": "https://www.techradar.com/rss", "search_url": "https://www.techradar.com/search?searchTerm={query}"},
    {"name": "Analytics India Magazine", "rss": "https://analyticsindiamag.com/feed/", "search_url": None},
    {"name": "TechCrunch", "rss": "https://techcrunch.com/feed/", "search_url": None},
    {"name": "The Verge", "rss": "https://www.theverge.com/rss/index.xml", "search_url": None},
    {"name": "YourStory Tech", "rss": "https://yourstory.com/feed", "search_url": None}
]

class ScraperAgent(Agent):
    def __init__(self, role, llm=None):
        super().__init__(
            role=role,
            goal="Fetch latest news using search keywords from multiple sources",
            backstory="Scrapes news from RSS feeds and search URLs, ranks by relevance, filters irrelevant news automatically",
            llm=llm
        )

    def clean_text(self, text):
        """Remove HTML tags and extra whitespace."""
        return BeautifulSoup(text, "html.parser").get_text().strip()

    def keyword_score(self, text, keywords):
        """Compute relevance score by counting keyword occurrences."""
        text_lower = text.lower()
        return sum(text_lower.count(k) for k in keywords)

    def fetch_full_article(self, url):
        """Fetch full article text from a URL."""
        try:
            headers = {"User-Agent": "Mozilla/5.0"}
            response = requests.get(url, headers=headers, timeout=5)
            soup = BeautifulSoup(response.text, "html.parser")
            paragraphs = soup.find_all("p")
            content = " ".join([p.get_text().strip() for p in paragraphs])
            return content
        except Exception:
            return ""

    def execute_task(self, task_input=None, **kwargs):
        search_terms = task_input.get("search_terms") if isinstance(task_input, dict) else task_input
        if not search_terms:
            return {"search_terms": "", "candidate_headlines": []}

        keywords = search_terms.lower().split()
        scored_articles = []

        for source in NEWS_SOURCES:
            # 1️⃣ RSS feed parsing
            feed = feedparser.parse(source["rss"])
            for entry in feed.entries[:30]:  # top 30 per feed
                title = self.clean_text(entry.get("title", ""))
                summary = self.clean_text(entry.get("summary", ""))
                combined_text = f"{title} {summary}"

                score = self.keyword_score(combined_text, keywords)
                link = entry.get("link")

                # Boost score by full article text if possible
                if link:
                    full_text = self.fetch_full_article(link)
                    score += self.keyword_score(full_text, keywords)

                if score > 0:
                    scored_articles.append((score, title, link))

            # 2️⃣ Dynamic search URL scraping
            search_url = source.get("search_url")
            if search_url:
                try:
                    url = search_url.format(query=quote(search_terms))
                    headers = {"User-Agent": "Mozilla/5.0"}
                    response = requests.get(url, headers=headers, timeout=5)
                    soup = BeautifulSoup(response.text, "html.parser")
                    for h in soup.find_all(["h2", "h3"]):
                        headline = self.clean_text(h.get_text())
                        score = self.keyword_score(headline, keywords)
                        if score > 0:
                            scored_articles.append((score, headline, None))
                except Exception:
                    continue

        # 3️⃣ Sort by relevance
        scored_articles.sort(key=lambda x: x[0], reverse=True)

        # 4️⃣ Return top 5 relevant headlines
        top_articles = [{"title": t, "link": l} for score, t, l in scored_articles[:5]]

        return {
            "search_terms": search_terms,
            "candidate_headlines": top_articles
        }
