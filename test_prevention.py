#!/usr/bin/env python3
"""Test script to verify prevention tips are available for all health conditions"""

from health_knowledge import get_health_info, HEALTH_CONDITIONS, MENTAL_HEALTH_CONDITIONS

def test_prevention_tips():
    """Test that all conditions have prevention tips"""
    print("Testing prevention tips for all health conditions...\n")

    all_conditions = {**HEALTH_CONDITIONS, **MENTAL_HEALTH_CONDITIONS}

    missing_prevention = []
    total_conditions = len(all_conditions)

    for condition_name, condition_data in all_conditions.items():
        prevention_tips = condition_data.get('prevention', [])
        if not prevention_tips:
            missing_prevention.append(condition_name)
        else:
            print(f"✓ {condition_name.replace('_', ' ').title()}: {len(prevention_tips)} prevention tips")

    print(f"\nSummary:")
    print(f"Total conditions: {total_conditions}")
    print(f"Conditions with prevention tips: {total_conditions - len(missing_prevention)}")
    print(f"Conditions missing prevention tips: {len(missing_prevention)}")

    if missing_prevention:
        print(f"\nConditions missing prevention tips: {missing_prevention}")
    else:
        print("\n✅ All conditions have prevention tips!")

    # Test a few specific conditions
    print("\nTesting specific conditions:")
    test_conditions = ['anxiety', 'depression', 'hypertension', 'diabetes', 'asthma', 'bipolar_disorder', 'ptsd', 'ocd', 'eating_disorders']

    for condition in test_conditions:
        info = get_health_info(condition)
        if info and 'prevention' in info:
            print(f"✓ {condition}: {len(info['prevention'])} prevention tips")
        else:
            print(f"✗ {condition}: No prevention tips found")

if __name__ == "__main__":
    test_prevention_tips()
