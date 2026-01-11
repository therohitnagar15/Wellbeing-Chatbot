#!/usr/bin/env python3
"""Test script to verify the updated chatbot logic"""

from chatbot import generate_response
from database import SessionLocal, engine
from models import Base

# Create tables
Base.metadata.create_all(bind=engine)

def test_chatbot_responses():
    """Test various chatbot responses to verify the updated logic"""
    print("Testing chatbot responses with updated logic...\n")

    # Create a mock db session
    db = SessionLocal()

    test_cases = [
        # Health information queries (should be prioritized first)
        ("What are the symptoms of anxiety?", "health_info"),
        ("Tell me about diabetes", "health_info"),
        ("What causes hypertension?", "health_info"),

        # Prevention and solution-focused queries (second priority)
        ("How to prevent stress?", "prevention"),
        ("What can I do to avoid depression?", "prevention"),
        ("Solutions for insomnia", "prevention"),

        # Intent-based responses (third priority)
        ("I'm feeling sad", "intent"),
        ("I have anxiety", "intent"),
        ("I'm stressed out", "intent"),

        # Professor exercises
        ("I'm a professor, give me exercises", "professor"),
        ("Professor exercises", "professor"),

        # Crisis words
        ("I want to die", "crisis"),
        ("Suicide thoughts", "crisis"),

        # OpenAI fallback
        ("Random question about weather", "fallback"),
    ]

    for message, expected_type in test_cases:
        print(f"Testing: '{message}'")
        try:
            response = generate_response("test_user", message, db)
            print(f"Response: {response[:100]}..." if len(response) > 100 else f"Response: {response}")
            print(f"Expected type: {expected_type}")
            print("-" * 50)
        except Exception as e:
            print(f"Error: {e}")
            print("-" * 50)

    db.close()

if __name__ == "__main__":
    test_chatbot_responses()
