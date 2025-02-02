from collections import defaultdict
from sqlalchemy.orm import Session
from models.user_model import *

def group_users_by_topics(engine):
    """Batch users with identical topics to minimize API calls"""
    with Session(engine) as session:
        users = session.query(User).all()
        topic_groups = defaultdict(list)
        for user in users:
            topics_key = ",".join(sorted(user.preferences["topics"]))
            topic_groups[topics_key].append(user)
        return topic_groups