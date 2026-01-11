#!/usr/bin/env python3
"""Test script to verify headache prevention tips are triggered in chatbot"""

from chatbot import generate_response
from models import User, MoodLog, ChatHistory
from database import SessionLocal

def test_headache_response():
    """Test that headache mentions trigger prevention tips"""
    print("Testing headache response in chatbot...\n")

    # Create a test user
    db = SessionLocal()
    test_user = db.query(User).filter(User.username == "test_user").first()
    if not test_user:
        test_user = User(username="test_user", password="test")
        db.add(test_user)
        db.commit()

    # Test phrases that should trigger headache prevention tips
    test_phrases = [
        "I have a headache",
        "headache",
        "my head hurts",
        "headache pain",
        "migraine",
        "severe headache"
    ]

    for phrase in test_phrases:
        print(f"Testing: '{phrase}'")
        response = generate_response("test_user", phrase, db)
        print(f"Response: {response[:200]}...")  # Show first 200 chars

        # Check if response contains prevention tips
        if "prevention tips" in response.lower() or "stay hydrated" in response.lower() or "manage stress" in response.lower():
            print("✓ Prevention tips found")
        else:
            print("✗ No prevention tips found")

        print("-" * 50)

    db.close()

if __name__ == "__main__":
    test_headache_response()
