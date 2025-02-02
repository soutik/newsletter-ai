# scripts/init_test_data.py
from services.user_manager import *

def create_test_users():
    test_users = [
        {"email": "linkinp0123@gmail.com", "topics": ["AI", "Climate"]},
        {"email": "prsoman92@gmail.com", "topics": ["AI"]},
    ]
    
    with SessionLocal() as session:
        for user_data in test_users:
            user = User(
                email=user_data["email"],
                preferences={"topics": user_data["topics"]},
            )
            session.add(user)
        session.commit()
    print("Created test users!")

if __name__ == "__main__":
    create_test_users()