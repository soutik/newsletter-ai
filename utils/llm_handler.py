from openai import OpenAI
import tiktoken
from config import *

client = OpenAI()

def summarize_article(article_text, max_tokens=150):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Summarize this article in 2-3 sentences. Include key names, numbers, and conclusions."},
            {"role": "user", "content": article_text[:3000]}  # Truncate to save tokens
        ],
        max_tokens=max_tokens
    )
    return response.choices[0].message.content

def rank_articles(articles):
    # Use LLM to rank articles by relevance to user topics
    articles_str = "\n".join([f"{i+1}. {a['title']}" for i, a in enumerate(articles)])
    prompt = f"""
    Rank these articles by relevance to {USER_TOPICS}. Prioritize novelty and impact.
    Return ONLY the top 10 numbers in order, like "3,1,5,...":
    {articles_str}
    """
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )
    ranked_indices = [int(x)-1 for x in response.choices[0].message.content.split(",")]
    return [articles[i] for i in ranked_indices]