# CrewAI News Summarizer

A multi-agent news summarization system powered by **CrewAI** and **Gemini LLM**, designed to collect, filter, and summarize the latest news from top online sources — all automatically.

---

## Features

- **Multi-Agent Architecture**
  - `QueryAgent` → Converts user question into concise search keywords.
  - `ScraperAgent` → Fetches and ranks relevant news articles using RSS + live web search.
  - `ResponseAgent` → Summarizes the collected articles into a single coherent response.

- **Powered by Gemini**
  - Uses **Gemini 2.5 Flash** for natural, context-aware summarization.

- **Smart Filtering**
  - Scores and ranks news based on keyword relevance.
  - Filters out unrelated or duplicate headlines.

- **Customizable**
  - Add or remove RSS/news sources easily.
  - Adjust number of results or keyword matching threshold.

---

## Architecture Overview

```mermaid
flowchart LR
    A[User Question] --> B[QueryAgent]
    B -->|Search Keywords| C[ScraperAgent]
    C -->|Scraped Articles| D[ResponseAgent]
    D -->|Final Summary| E[Console Output]
````

---

## Project Structure

```
news-summarizer-crewai/
├── main.py                  # Entry point for the app
├── agents/
│   ├── query_agent.py       # Converts user questions → keywords
│   ├── scraper_agent.py     # Fetches relevant articles
│   └── response_agent.py    # Summarizes scraped content
├── requirements.txt          # Python dependencies
└── README.md                 # Project documentation
```

---

## Setup & Installation

### Clone the repository

```bash
git clone https://github.com/Ponmurugaiya/news-summarizer-crewai.git
cd news-summarizer-crewai
```

### Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate     # (Linux/Mac)
venv\Scripts\activate        # (Windows)
(or)
uv venv
.venv\Scripts\activate
```

### Install dependencies

```bash
pip install -r requirements.txt
(or)
uv add -r requirements.txt
```

### Set your Gemini API key

You can export it as an environment variable:

```bash
export GEMINI_API_KEY="your_api_key_here"     # (Linux/Mac)
setx GEMINI_API_KEY "your_api_key_here"       # (Windows)
```

---

## Usage

Run the main script:

```bash
python main.py
```

---

## Future Improvements

* [ ] Schedule daily automatic summarization via cron or n8n.
* [ ] Serve results as a web API or Telegram bot.

---

*"Built with CrewAI — where multiple agents work together to make information intelligent."*

```
