import sys
import os

# Get the absolute path of the project root (parent of main/)
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Add it to sys.path
if project_root not in sys.path:
    sys.path.append(project_root)

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session
from services.user_manager import SessionLocal, get_db
from models.user_model import User

app = FastAPI()

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class UserCreate(BaseModel):
    email: str
    preferences: dict  # {"topics": ["AI", "Climate"]}

@app.post("/api/users")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # Check if email exists
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    print(f"preferences: {user.preferences}")
    # Create new user
    new_user = User(
        email=user.email,
        preferences=user.preferences,
    )
    db.add(new_user)
    db.commit()
    return {"message": "User created successfully"}