#!/usr/bin/env python3
"""Test script to verify the chatbot modification: prevention tips only on explicit request"""

from chatbot import generate_response
from models import User, MoodLog, ChatHistory
from database import SessionLocal

def test_modification():
    """Test that prevention tips are only provided when explicitly requested"""
    print("Testing chatbot modification: prevention tips only on explicit request\n")

    # Create a test user
    db = SessionLocal()
    test_user = db.query(User).filter(User.username == "test_user").first()
    if not test_user:
        test_user = User(username="test_user", password="test")
        db.add(test_user)
        db.commit()

    print("=" * 60)
    print("TEST 1: Headache mention should NOT include prevention tips automatically")
    print("=" * 60)

    # Test phrases that mention headache but don't ask for prevention
    headache_phrases = [
        "I have a headache",
        "headache",
        "my head hurts",
        "headache pain",
        "migraine",
        "severe headache"
    ]

    for phrase in headache_phrases:
        print(f"\nTesting: '{phrase}'")
        response = generate_response("test_user", phrase, db)
        print(f"Response: {response[:300]}...")

        # Check if response contains prevention tips (should NOT)
        has_prevention = ("prevention tips" in response.lower() or
                         "stay hydrated" in response.lower() or
                         "manage stress" in response.lower() or
                         "Prevention tips:" in response)

        if has_prevention:
            print("❌ FAIL: Prevention tips found (should not be automatic)")
        else:
            print("✅ PASS: No automatic prevention tips")

    print("\n" + "=" * 60)
    print("TEST 2: Explicit prevention requests should include prevention tips")
    print("=" * 60)

    # Test phrases that explicitly ask for prevention
    prevention_phrases = [
        "how to prevent headaches",
        "prevention tips for headaches",
        "how can I avoid headaches",
        "headache prevention",
        "tips to prevent migraines"
    ]

    for phrase in prevention_phrases:
        print(f"\nTesting: '{phrase}'")
        response = generate_response("test_user", phrase, db)
        print(f"Response: {response[:300]}...")

        # Check if response contains prevention tips (should YES)
        has_prevention = ("prevention tips" in response.lower() or
                         "stay hydrated" in response.lower() or
                         "manage stress" in response.lower() or
                         "Prevention tips:" in response)

        if has_prevention:
            print("✅ PASS: Prevention tips provided when requested")
        else:
            print("❌ FAIL: No prevention tips provided when requested")

    print("\n" + "=" * 60)
    print("TEST 3: Other responses should remain unaffected")
    print("=" * 60)

    # Test other responses to ensure they still work
    other_phrases = [
        "I'm feeling stressed",
        "I need a breathing exercise",
        "how are you",
        "tell me about anxiety"
    ]

    for phrase in other_phrases:
        print(f"\nTesting: '{phrase}'")
        response = generate_response("test_user", phrase, db)
        print(f"Response: {response[:200]}...")

        if response and len(response) > 10:  # Basic check that response exists
            print("✅ PASS: Response generated")
        else:
            print("❌ FAIL: No response generated")

    db.close()
    print("\n" + "=" * 60)
    print("TESTING COMPLETE")
    print("=" * 60)

if __name__ == "__main__":
    test_modification()
