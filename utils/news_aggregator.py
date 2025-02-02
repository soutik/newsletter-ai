from newsapi import NewsApiClient
import pandas as pd
import os
from config import *
from datetime import datetime, timedelta

def fetch_articles(topics):
    newsapi = NewsApiClient(api_key=os.getenv('NEWSAPI_KEY'))
    date_to = datetime.today().date()
    date_from = date_to - timedelta(days=1)
    articles = newsapi.get_everything(
        q=" OR ".join(topics),
        # sources=NEWS_SOURCES,
        # excludeDomains=["bbc.co.uk"] # if you want to exclude a news provider
        language="en",
        sort_by="relevancy",
        page_size=50,  # Max for free tier
        from_param=date_from,
        to=date_to
    )
    return articles["articles"]

def deduplicate_articles(articles):
    # Simple title-based deduplication
    seen = set()
    unique_articles = []
    for article in articles:
        title = article["title"].lower().strip()
        if title not in seen:
            seen.add(title)
            unique_articles.append(article)
    return unique_articles