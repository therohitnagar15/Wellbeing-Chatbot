#!/usr/bin/env python3
"""Critical path testing for Gemini API integration in chatbot.py"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from chatbot import generate_response, gemini_model
from database import SessionLocal, engine
from models import Base
import google.generativeai as genai

# Create tables
Base.metadata.create_all(bind=engine)

def test_gemini_initialization():
    """Test 1: Verify Gemini client initialization"""
    print("Test 1: Gemini Client Initialization")
    try:
        # Check if gemini_model is properly initialized
        if gemini_model is None:
            print("❌ FAIL: Gemini model is None")
            return False

        # Try a simple generation to verify API key and model work
        test_prompt = "Hello, this is a test."
        response = gemini_model.generate_content(test_prompt)
        if response and response.text:
            print("✅ PASS: Gemini client initialized and responding")
            return True
        else:
            print("❌ FAIL: Gemini client not responding properly")
            return False
    except Exception as e:
        print(f"❌ FAIL: Gemini initialization error - {str(e)}")
        return False

def test_basic_response_generation():
    """Test 2: Test basic response generation with Gemini"""
    print("\nTest 2: Basic Response Generation")
    try:
        db = SessionLocal()
        test_message = "Hello, I'm feeling stressed today."

        response = generate_response("test_user", test_message, db)

        if response and len(response.strip()) > 0:
            print("✅ PASS: Response generated successfully")
            print(f"Response length: {len(response)} characters")
            print(f"Response preview: {response[:100]}...")
            db.close()
            return True
        else:
            print("❌ FAIL: Empty or invalid response")
            db.close()
            return False
    except Exception as e:
        print(f"❌ FAIL: Response generation error - {str(e)}")
        return False

def test_conversation_formatting():
    """Test 3: Test conversation history formatting"""
    print("\nTest 3: Conversation Formatting")
    try:
        db = SessionLocal()

        # Create a user and add some chat history
        from models import User, ChatHistory
        user = db.query(User).filter(User.username == "test_user").first()
        if not user:
            user = User(username="test_user", password="test")
            db.add(user)
            db.commit()

        # Add test conversation history
        chat1 = ChatHistory(user_id=user.id, user_message="Hi", bot_response="Hello!")
        chat2 = ChatHistory(user_id=user.id, user_message="I'm stressed", bot_response="I understand")
        db.add(chat1)
        db.add(chat2)
        db.commit()

        # Test response with conversation history
        response = generate_response("test_user", "What can I do?", db)

        if response and len(response.strip()) > 0:
            print("✅ PASS: Response generated with conversation history")
            db.close()
            return True
        else:
            print("❌ FAIL: Failed to generate response with history")
            db.close()
            return False
    except Exception as e:
        print(f"❌ FAIL: Conversation formatting error - {str(e)}")
        return False

def test_error_handling():
    """Test 4: Test error handling and fallback"""
    print("\nTest 4: Error Handling")
    try:
        db = SessionLocal()

        # Test with invalid input
        response = generate_response("test_user", "", db)

        if response and len(response.strip()) > 0:
            print("✅ PASS: Error handling working (fallback response generated)")
            db.close()
            return True
        else:
            print("❌ FAIL: No fallback response for invalid input")
            db.close()
            return False
    except Exception as e:
        print(f"❌ FAIL: Error handling failed - {str(e)}")
        return False

def run_critical_path_tests():
    """Run all critical path tests"""
    print("🔍 Running Critical Path Tests for Gemini API Integration\n")
    print("=" * 60)

    tests = [
        test_gemini_initialization,
        test_basic_response_generation,
        test_conversation_formatting,
        test_error_handling
    ]

    passed = 0
    total = len(tests)

    for test in tests:
        if test():
            passed += 1

    print("\n" + "=" * 60)
    print(f"📊 Test Results: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 All critical path tests PASSED! Gemini integration is working correctly.")
        return True
    else:
        print("⚠️  Some tests failed. Please check the Gemini API configuration.")
        return False

if __name__ == "__main__":
    success = run_critical_path_tests()
    sys.exit(0 if success else 1)
