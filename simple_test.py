#!/usr/bin/env python3
"""
Simple test script to verify greeting and routine functionality
"""

import sys
import os
import tempfile
import sqlite3

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_greeting_basic():
    """Test basic greeting functionality"""
    print("Testing basic greeting functionality...")

    try:
        from chatbot import generate_response
        from models import User, ChatHistory
        from database import init_db, get_db_session

        # Create temporary database
        db_fd, db_path = tempfile.mkstemp()
        init_db(db_path)
        db_session = get_db_session(db_path)

        # Create test user
        test_user = User(username="test_user", password_hash="test_hash")
        db_session.add(test_user)
        db_session.commit()

        # Test greetings
        greetings = ["hello", "hi", "hey", "good morning"]
        results = []

        for greeting in greetings:
            response = generate_response("test_user", greeting, db_session)
            results.append((greeting, response))

            # Check database
            chat_entry = db_session.query(ChatHistory).filter(
                ChatHistory.user_id == test_user.id,
                ChatHistory.user_message == greeting
            ).first()

            if chat_entry is None:
                print(f"❌ FAIL: No database entry for greeting '{greeting}'")
                return False

        print("✅ PASS: Basic greeting functionality works")
        for greeting, response in results:
            print(f"  '{greeting}' -> '{response[:50]}...'")

        # Cleanup
        db_session.close()
        os.close(db_fd)
        os.unlink(db_path)

        return True

    except Exception as e:
        print(f"❌ FAIL: Exception in greeting test: {e}")
        return False

def test_routine_basic():
    """Test basic routine functionality"""
    print("\nTesting basic routine functionality...")

    try:
        from chatbot import generate_response
        from models import User, ChatHistory
        from database import init_db, get_db_session

        # Create temporary database
        db_fd, db_path = tempfile.mkstemp()
        init_db(db_path)
        db_session = get_db_session(db_path)

        # Create test user
        test_user = User(username="test_user", password_hash="test_hash")
        db_session.add(test_user)
        db_session.commit()

        # Test routine questions
        routines = ["daily routine", "how is your day", "what's your routine"]
        results = []

        for routine in routines:
            response = generate_response("test_user", routine, db_session)
            results.append((routine, response))

            # Check database
            chat_entry = db_session.query(ChatHistory).filter(
                ChatHistory.user_id == test_user.id,
                ChatHistory.user_message == routine
            ).first()

            if chat_entry is None:
                print(f"❌ FAIL: No database entry for routine question '{routine}'")
                return False

        print("✅ PASS: Basic routine functionality works")
        for routine, response in results:
            print(f"  '{routine}' -> '{response[:50]}...'")

        # Cleanup
        db_session.close()
        os.close(db_fd)
        os.unlink(db_path)

        return True

    except Exception as e:
        print(f"❌ FAIL: Exception in routine test: {e}")
        return False

def test_no_interference():
    """Test that greeting/routine don't interfere with other features"""
    print("\nTesting no interference with other features...")

    try:
        from chatbot import generate_response
        from models import User
        from database import init_db, get_db_session

        # Create temporary database
        db_fd, db_path = tempfile.mkstemp()
        init_db(db_path)
        db_session = get_db_session(db_path)

        # Create test user
        test_user = User(username="test_user", password_hash="test_hash")
        db_session.add(test_user)
        db_session.commit()

        # Test crisis detection (should not be greeting/routine)
        crisis_msg = "I want to kill myself"
        response = generate_response("test_user", crisis_msg, db_session)

        if "Emergency Services" not in response:
            print("❌ FAIL: Crisis detection not working")
            return False

        # Test health query (should not be greeting/routine)
        health_msg = "symptoms of depression"
        # Mock the Gemini API call
        import chatbot
        original_genai = chatbot.genai
        chatbot.genai = type('MockGenai', (), {
            'GenerativeModel': lambda self, model: type('MockModel', (), {
                'generate_content': lambda self, prompt: type('MockResponse', (), {'text': 'Mock health response about depression'})()
            })()
        })()

        response = generate_response("test_user", health_msg, db_session)

        # Restore original
        chatbot.genai = original_genai

        if "depression" not in response.lower():
            print("❌ FAIL: Health query not working properly")
            return False

        print("✅ PASS: No interference with crisis detection and health queries")

        # Cleanup
        db_session.close()
        os.close(db_fd)
        os.unlink(db_path)

        return True

    except Exception as e:
        print(f"❌ FAIL: Exception in interference test: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Running Simple Tests for Greeting and Routine Features")
    print("=" * 60)

    tests = [
        test_greeting_basic,
        test_routine_basic,
        test_no_interference
    ]

    passed = 0
    total = len(tests)

    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ FAIL: Test {test.__name__} crashed: {e}")

    print("\n" + "=" * 60)
    print(f"📊 Test Results: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 All tests passed! The greeting and routine features are working correctly.")
        return 0
    else:
        print("⚠️  Some tests failed. Please review the implementation.")
        return 1

if __name__ == "__main__":
    # Set test environment
    os.environ['GEMINI_API_KEY'] = 'test_key_for_testing'
    sys.exit(main())
