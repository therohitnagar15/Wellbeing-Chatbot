from sqlalchemy import Column, Integer, String, Date, DateTime
from database import Base
from datetime import date, datetime

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password = Column(String)
    role = Column(String, default="user")  # user or admin
    language = Column(String, default="en")

class MoodLog(Base):
    __tablename__ = "moods"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    mood = Column(String)
    log_date = Column(Date, default=date.today)

class ChatHistory(Base):
    __tablename__ = "chat_history"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    user_message = Column(String)
    bot_response = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)

class Feedback(Base):
    __tablename__ = "feedback"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    feedback_text = Column(String)
    rating = Column(Integer)  # 1-5 scale
    timestamp = Column(DateTime, default=datetime.utcnow)
