#!/usr/bin/env python3
"""
Test script for the enhanced fallback response function.
Tests various combinations of user input, sentiment, and mood to ensure proper responses.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from chatbot import get_enhanced_fallback_response

def test_fallback_responses():
    """Test the enhanced fallback response function with various inputs"""

    test_cases = [
        # Test cases: (input_text, current_mood, expected_contains_keywords)
        # Negative sentiment with different moods
        ("I'm feeling really sad and down today", "sad", ["sadness", "breathing exercise"]),
        ("I'm so anxious about everything", "anxious", ["anxiety", "breathing exercise"]),
        ("Work is overwhelming me completely", "stressed", ["stress", "care for yourself"]),
        ("I feel so lonely all the time", "lonely", ["lonely", "mindfulness exercise"]),

        # Positive sentiment with different moods
        ("Despite feeling sad, I'm grateful for my friends", "sad", ["positivity", "lift your spirits"]),
        ("I'm happy even though I'm stressed", "stressed", ["positivity", "energy boost"]),
        ("Feeling content despite being tired", "tired", ["positivity", "energy boost"]),

        # Neutral sentiment with different moods
        ("How are you doing today?", "happy", ["great that you're tracking", "day been overall"]),
        ("What's the weather like?", "sad", ["mixed emotions", "mindfulness techniques"]),
        ("Can you help me with something?", "anxious", ["happy to help", "bit more about what"]),

        # Questions and help-seeking
        ("What should I do when I'm feeling anxious?", None, ["breathing exercise", "help with that"]),
        ("Can you recommend some stress relief techniques?", None, ["breathing exercise", "help with that"]),

        # Emotional expressions without specific mood
        ("I'm feeling really depressed", None, ["sorry you're feeling sad", "breathing exercise"]),
        ("I'm so stressed out", None, ["stress can make everything feel heavier", "care for yourself"]),
        ("I'm grateful for everything", None, ["wonderful to hear gratitude", "thankful for today"]),
        ("I'm feeling happy today", None, ["glad you're feeling positive", "contributing to this good feeling"]),

        # Edge cases
        ("Hello", None, ["Thanks for sharing", "overall day been"]),
        ("This is neutral text", None, ["Thanks for sharing", "overall day been"]),
    ]

    print("Testing Enhanced Fallback Response Function")
    print("=" * 50)

    passed = 0
    total = len(test_cases)

    for i, (text, mood, expected_keywords) in enumerate(test_cases, 1):
        print(f"\nTest {i}: Input: '{text}' | Mood: {mood}")
        print("-" * 40)

        try:
            response = get_enhanced_fallback_response(text, mood)
            print(f"Response: {response}")

            # Check if response contains expected keywords
            keywords_found = []
            for keyword in expected_keywords:
                if keyword.lower() in response.lower():
                    keywords_found.append(keyword)

            if len(keywords_found) == len(expected_keywords):
                print(f"✓ PASSED - All expected keywords found: {keywords_found}")
                passed += 1
            else:
                print(f"✗ FAILED - Missing keywords. Expected: {expected_keywords}, Found: {keywords_found}")

        except Exception as e:
            print(f"✗ ERROR - Exception occurred: {e}")

    print("\n" + "=" * 50)
    print(f"Test Results: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 All tests passed! The enhanced fallback response function is working correctly.")
    else:
        print(f"⚠️  {total - passed} tests failed. Please review the implementation.")

    return passed == total

if __name__ == "__main__":
    success = test_fallback_responses()
    sys.exit(0 if success else 1)
