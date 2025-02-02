import time
from utils.news_aggregator import fetch_articles, deduplicate_articles
from utils.llm_handler import summarize_article, rank_articles
from config import *

from services.batch_processor import group_users_by_topics
from services.user_manager import engine
from utils.vector_db import VectorDB
from sqlalchemy.orm import Session
from services.email_renderer import *
from services.email_sender import *
import os

vector_db = VectorDB()

def process_group(topics, users):
    # 1. Fetch articles for topic group
    print("- Fetching artciles...")
    articles = fetch_articles(topics)
    
    # 2. Filter duplicates using vector DB
    unique_articles = [
        article for article in articles
        if not any(vector_db.is_duplicate(article["content"], user.id) for user in users)
    ]
    
    # 3. Summarize & rank once per group
    print("- Summarizing...")
    ranked_articles = rank_articles(unique_articles)
    for article in ranked_articles:
        article["summary"] = summarize_article(article["content"])
        vector_db.add_article(article["content"])  # Store in vector DB
    
    # 4. Generate personalized emails for each user
    print("- Sending emails...")
    with Session(engine) as session:
        for user in users:
            email_html = EmailRenderer().render_newsletter(user, ranked_articles)
            send_email(user.email, email_html)

def main():
    topic_groups = group_users_by_topics(engine)
    for topics, users in topic_groups.items():
        process_group(topics.split(","), users)

if __name__ == "__main__":
    start_time = time.time()
    main()
    print(f"Done in {time.time() - start_time:.2f}s")