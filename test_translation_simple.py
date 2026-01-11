#!/usr/bin/env python3
"""
Simple test script for translation functionality in the wellbeing chatbot.
Tests basic integration without requiring external translation services.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_translation_integration():
    """Test basic translation integration in chatbot"""
    print("Testing Translation Integration...")
    print("=" * 40)

    # Test 1: Check if translation_service can be imported
    try:
        from translation_service import TranslationService
        print("✓ TranslationService import successful")
    except ImportError as e:
        print(f"✗ TranslationService import failed: {e}")
        return False

    # Test 2: Check if chatbot can import translation_service
    try:
        from chatbot import translation_service
        print("✓ Chatbot translation_service import successful")
    except ImportError as e:
        print(f"✗ Chatbot translation_service import failed: {e}")
        return False

    # Test 3: Test TranslationService initialization
    try:
        service = TranslationService()
        print("✓ TranslationService initialization successful")
    except Exception as e:
        print(f"✗ TranslationService initialization failed: {e}")
        return False

    # Test 4: Test supported languages
    try:
        languages = service.get_supported_languages()
        print(f"✓ Supported languages loaded: {len(languages)} languages")
        print(f"  Sample languages: {list(languages.keys())[:5]}")
    except Exception as e:
        print(f"✗ Failed to get supported languages: {e}")
        return False

    # Test 5: Test language support checking
    try:
        assert service.is_language_supported('en') == True
        assert service.is_language_supported('es') == True
        assert service.is_language_supported('invalid') == False
        print("✓ Language support checking works")
    except Exception as e:
        print(f"✗ Language support checking failed: {e}")
        return False

    # Test 6: Test empty text handling
    try:
        result = service.translate_text("", "es")
        assert result == ""
        result = service.translate_text("   ", "es")
        assert result == "   "
        print("✓ Empty text handling works")
    except Exception as e:
        print(f"✗ Empty text handling failed: {e}")
        return False

    # Test 7: Test chatbot generate_response with target_lang parameter
    try:
        from chatbot import generate_response
        from database import get_db

        # Get database session
        db = next(get_db())

        # Test with target_lang parameter (should not crash)
        response = generate_response("test_user", "Hello", db, target_lang="en")
        print("✓ Chatbot generate_response with target_lang works")
        print(f"  Response length: {len(response)} characters")

    except Exception as e:
        print(f"✗ Chatbot generate_response test failed: {e}")
        return False

    print("\n" + "=" * 40)
    print("✓ All basic translation integration tests passed!")
    return True

def test_chatbot_translation_features():
    """Test specific chatbot translation features"""
    print("\nTesting Chatbot Translation Features...")
    print("=" * 40)

    # Test 1: Check if translation is called in generate_response
    try:
        from chatbot import generate_response
        from database import get_db
        import inspect

        # Check if the function accepts target_lang parameter
        sig = inspect.signature(generate_response)
        if 'target_lang' in sig.parameters:
            print("✓ generate_response accepts target_lang parameter")
        else:
            print("✗ generate_response missing target_lang parameter")
            return False

    except Exception as e:
        print(f"✗ Function signature check failed: {e}")
        return False

    # Test 2: Check if translation_service is used in the code
    try:
        with open('chatbot.py', 'r', encoding='utf-8') as f:
            content = f.read()

        if 'translation_service.translate' in content:
            print("✓ Translation service is called in chatbot code")
        else:
            print("✗ Translation service not found in chatbot code")
            return False

        if 'target_language' in content:
            print("✓ Target language handling found in code")
        else:
            print("✗ Target language handling not found in code")
            return False

    except Exception as e:
        print(f"✗ Code analysis failed: {e}")
        return False

    print("✓ All chatbot translation features tests passed!")
    return True

if __name__ == "__main__":
    print("Wellbeing Chatbot Translation Testing")
    print("====================================")

    success1 = test_translation_integration()
    success2 = test_chatbot_translation_features()

    if success1 and success2:
        print("\n🎉 All tests passed! Translation functionality is properly integrated.")
    else:
        print("\n❌ Some tests failed. Please check the implementation.")

    print("\nNote: Full translation testing requires internet connection and external APIs.")
    print("For complete testing, ensure googletrans and langdetect are properly installed.")
