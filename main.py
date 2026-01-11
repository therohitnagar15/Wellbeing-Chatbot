import uvicorn
from fastapi import FastAPI, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import User, MoodLog, ChatHistory, Base
from chatbot import generate_response
from pydantic import BaseModel
from datetime import date
import csv
from io import StringIO, BytesIO
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from dotenv import load_dotenv
import os

load_dotenv()
 
Base.metadata.create_all(bind=engine)

from fastapi.responses import FileResponse

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def read_root():
    return FileResponse("index.html")

@app.get("/login")
def read_login():
    return FileResponse("static/login.html")

@app.get("/index")
def read_index():
    return FileResponse("static/index.html")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class Login(BaseModel):
    username: str
    password: str

class Chat(BaseModel):
    username: str
    message: str

class Mood(BaseModel):
    username: str
    mood: str

class FeedbackData(BaseModel):
    username: str
    feedback_text: str
    rating: int

@app.post("/register")
def register(data: Login, db: Session = Depends(get_db)):
    if db.query(User).filter(User.username == data.username).first():
        return {"error": "User already exists"}
    db.add(User(username=data.username, password=data.password))
    db.commit()
    return {"message": "Registered successfully"}

@app.post("/login")
def login(data: Login, db: Session = Depends(get_db)):
    user = db.query(User).filter(
        User.username == data.username,
        User.password == data.password
    ).first()
    if not user:
        return {"error": "Invalid credentials"}
    return {"message": "Login success", "role": user.role}

@app.post("/mood")
def save_mood(data: Mood, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == data.username).first()
    today = date.today()

    record = db.query(MoodLog).filter(
        MoodLog.user_id == user.id,
        MoodLog.log_date == today
    ).first()

    if record:
        record.mood = data.mood
    else:
        db.add(MoodLog(user_id=user.id, mood=data.mood))

    db.commit()
    return {"message": "Mood saved"}

@app.get("/moods/{username}")
def mood_history(username: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    moods = db.query(MoodLog).filter(
        MoodLog.user_id == user.id
    ).order_by(MoodLog.log_date).all()
    return [{"date": m.log_date, "mood": m.mood} for m in moods]

@app.post("/chat")
def chat(data: Chat, db: Session = Depends(get_db)):
    return {"reply": generate_response(data.username, data.message, db)}

@app.get("/export/csv/{username}")
def export_csv(username: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    moods = db.query(MoodLog).filter(MoodLog.user_id == user.id).all()

    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(["Date", "Mood"])
    for m in moods:
        writer.writerow([m.log_date, m.mood])
    output.seek(0)

    return StreamingResponse(
        output,
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename={username}_mood.csv"}
    )

@app.get("/export/pdf/{username}")
def export_pdf(username: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    moods = db.query(MoodLog).filter(MoodLog.user_id == user.id).order_by(MoodLog.log_date).all()
    chats = db.query(ChatHistory).filter(ChatHistory.user_id == user.id).order_by(ChatHistory.timestamp).all()

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    elements = []

    # Title
    elements.append(Paragraph(f"Wellbeing Report: {username}", styles["Title"]))
    elements.append(Paragraph(" ", styles["Normal"]))  # Spacer

    # Mood Summary
    elements.append(Paragraph("Mood Tracking Summary", styles["Heading2"]))
    if moods:
        mood_data = [["Date", "Mood"]] + [[str(m.log_date), m.mood] for m in moods]
        mood_table = Table(mood_data)
        elements.append(mood_table)
    else:
        elements.append(Paragraph("No mood data recorded.", styles["Normal"]))
    elements.append(Paragraph(" ", styles["Normal"]))  # Spacer

    # Conversation History
    elements.append(Paragraph("Conversation History", styles["Heading2"]))
    if chats:
        chat_data = [["Date/Time", "User Message", "Bot Response"]]
        for c in chats:
            chat_data.append([str(c.timestamp), c.user_message, c.bot_response])
        chat_table = Table(chat_data)
        elements.append(chat_table)
    else:
        elements.append(Paragraph("No conversation history available.", styles["Normal"]))

    # Summary Statistics
    elements.append(Paragraph(" ", styles["Normal"]))  # Spacer
    elements.append(Paragraph("Summary Statistics", styles["Heading2"]))
    total_moods = len(moods)
    total_chats = len(chats)
    elements.append(Paragraph(f"Total mood entries: {total_moods}", styles["Normal"]))
    elements.append(Paragraph(f"Total conversations: {total_chats}", styles["Normal"]))

    doc.build(elements)
    buffer.seek(0)

    return StreamingResponse(
        buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={username}_wellbeing_report.pdf"}
    )

@app.get("/dashboard")
def dashboard():
    return FileResponse("static/dashboard.html")

@app.get("/users")
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return [{"username": u.username, "role": u.role} for u in users]

@app.post("/feedback")
def submit_feedback(data: FeedbackData, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == data.username).first()
    if not user:
        return {"error": "User not found"}
    db.add(Feedback(user_id=user.id, feedback_text=data.feedback_text, rating=data.rating))
    db.commit()
    return {"message": "Feedback submitted successfully"}

@app.get("/doctors")
def doctors_page():
    return FileResponse("static/doctors.html")

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=5000)
