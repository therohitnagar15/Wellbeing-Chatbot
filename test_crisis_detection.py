#!/usr/bin/env python3
"""Critical-path test for crisis detection in expanded CRISIS_WORDS list"""

from chatbot import generate_response, CRISIS_WORDS
from database import SessionLocal, engine
from models import Base

# Create tables
Base.metadata.create_all(bind=engine)

def test_crisis_detection():
    """Test critical crisis detection functionality"""
    print("=== CRITICAL-PATH TESTING: Crisis Detection ===\n")

    db = SessionLocal()

    # Test cases for crisis detection
    crisis_test_cases = [
        # Suicide and self-harm (from expanded list)
        ("I want to kill myself", "crisis"),
        ("I'm cutting myself", "crisis"),
        ("suicidal thoughts", "crisis"),
        ("end my life", "crisis"),

        # Crisis and emergency
        ("I'm in crisis", "crisis"),
        ("losing it completely", "crisis"),
        ("at my breaking point", "crisis"),

        # Severe mental health crisis
        ("hearing voices", "crisis"),
        ("going crazy", "crisis"),
        ("psychotic episode", "crisis"),

        # Violence and harm to others
        ("rage blackout", "crisis"),
        ("violent thoughts", "crisis"),

        # Severe depression and despair
        ("worthless and useless", "crisis"),
        ("burden to everyone", "crisis"),
        ("nothing matters anymore", "crisis"),

        # Addiction crisis
        ("can't stop drinking", "crisis"),
        ("hitting rock bottom", "crisis"),

        # Trauma and abuse
        ("being abused", "crisis"),
        ("in danger", "crisis"),
        ("threatened with violence", "crisis"),
    ]

    # Test cases for non-crisis (should NOT trigger crisis response)
    non_crisis_test_cases = [
        ("I'm feeling stressed", "non-crisis"),
        ("having a bad day", "non-crisis"),
        ("need help with anxiety", "non-crisis"),
        ("depressed about work", "non-crisis"),
        ("feeling worthless at job", "non-crisis"),  # This might be borderline, but should not trigger crisis
    ]

    print("Testing CRISIS detection (should trigger crisis response):")
    print("-" * 60)

    crisis_detected_correctly = 0
    total_crisis_tests = len(crisis_test_cases)

    for message, expected in crisis_test_cases:
        try:
            response = generate_response("test_user", message, db)
            # Check if crisis response is triggered
            is_crisis_response = "I'm really sorry you're feeling this way" in response or "reach out to a trusted person" in response

            if is_crisis_response:
                print(f"✓ PASS: '{message}' -> Crisis detected")
                crisis_detected_correctly += 1
            else:
                print(f"✗ FAIL: '{message}' -> No crisis response (got: {response[:50]}...)")

        except Exception as e:
            print(f"✗ ERROR: '{message}' -> {e}")

    print(f"\nCrisis Detection Results: {crisis_detected_correctly}/{total_crisis_tests} passed")
    print("-" * 60)

    print("\nTesting NON-CRISIS detection (should NOT trigger crisis response):")
    print("-" * 60)

    false_positives = 0
    total_non_crisis_tests = len(non_crisis_test_cases)

    for message, expected in non_crisis_test_cases:
        try:
            response = generate_response("test_user", message, db)
            # Check if crisis response is triggered
            is_crisis_response = "I'm really sorry you're feeling this way" in response or "reach out to a trusted person" in response

            if not is_crisis_response:
                print(f"✓ PASS: '{message}' -> No false positive")
            else:
                print(f"✗ FAIL: '{message}' -> False positive crisis response")
                false_positives += 1

        except Exception as e:
            print(f"✗ ERROR: '{message}' -> {e}")

    print(f"\nNon-Crisis Detection Results: {total_non_crisis_tests - false_positives}/{total_non_crisis_tests} passed (no false positives)")
    print("-" * 60)

    # Summary
    print("\n=== TEST SUMMARY ===")
    print(f"Crisis words in list: {len(CRISIS_WORDS)}")
    print(f"Crisis detection accuracy: {crisis_detected_correctly}/{total_crisis_tests}")
    print(f"False positive rate: {false_positives}/{total_non_crisis_tests}")

    if crisis_detected_correctly == total_crisis_tests and false_positives == 0:
        print("✅ CRITICAL-PATH TESTING PASSED: Crisis detection working correctly!")
    else:
        print("❌ CRITICAL-PATH TESTING FAILED: Issues detected with crisis detection")

    db.close()

if __name__ == "__main__":
    test_crisis_detection()
