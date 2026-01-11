#!/usr/bin/env python3
"""Test script to verify symptom prevention tips are accessible via search"""

from health_knowledge import search_health_database

def test_symptom_prevention_search():
    """Test that symptom prevention tips are found via search"""
    print("Testing symptom prevention search...\n")

    test_symptoms = ['headache', 'diarrhea', 'sadness', 'fever', 'nausea', 'dizziness', 'fatigue']

    for symptom in test_symptoms:
        results = search_health_database(symptom)
        prevention_results = [r for r in results if r.get('type') == 'prevention']

        if prevention_results:
            prevention_tips = prevention_results[0].get('prevention_tips', [])
            print(f"✓ {symptom}: {len(prevention_tips)} prevention tips found")
            # Show first 2 tips as example
            for tip in prevention_tips[:2]:
                print(f"  - {tip}")
        else:
            print(f"✗ {symptom}: No prevention tips found")

        print()

if __name__ == "__main__":
    test_symptom_prevention_search()
