#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from chatbot import generate_response
from database import SessionLocal

def test_chatbot():
    try:
        db = SessionLocal()
        response = generate_response('testuser', 'hello', db)
        print("Chatbot Response:", response)
        print("SUCCESS: Chatbot is working!")
        db.close()
        return True
    except Exception as e:
        print(f"ERROR: Chatbot failed with error: {str(e)}")
        return False

if __name__ == "__main__":
    test_chatbot()
