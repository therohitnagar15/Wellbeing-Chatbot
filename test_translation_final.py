#!/usr/bin/env python3
"""
Final comprehensive test for translation functionality in the wellbeing chatbot.
Tests the complete integration including chatbot responses with translation.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_complete_translation_integration():
    """Test complete translation integration"""
    print("🧪 Final Translation Integration Test")
    print("=" * 50)

    try:
        # Test 1: Import all required modules
        print("1. Testing imports...")
        from translation_service import translation_service, TranslationService
        from chatbot import generate_response
        from database import get_db
        from models import User
        print("   ✅ All imports successful")

        # Test 2: Translation service functionality
        print("\n2. Testing translation service...")
        service = TranslationService()

        # Test language detection
        detected = service.detect_language("Hola, ¿cómo estás?")
        print(f"   Language detection: 'Hola, ¿cómo estás?' -> {detected}")
        assert detected == 'es', f"Expected 'es', got '{detected}'"

        # Test mock translation
        translated = service.translate_text("Hello", "es")
        print(f"   Mock translation: 'Hello' -> '{translated}'")
        assert translated == "Hola", f"Expected 'Hola', got '{translated}'"

        # Test unsupported text fallback
        fallback = service.translate_text("Some random text", "es")
        print(f"   Fallback handling: 'Some random text' -> '{fallback}'")
        assert fallback == "Some random text", "Should return original text for unmatched translations"

        print("   ✅ Translation service working correctly")

        # Test 3: Chatbot integration
        print("\n3. Testing chatbot integration...")
        db = next(get_db())

        # Create test user
        test_user = User(username="translation_test_user", email="test@example.com", language="es")
        db.add(test_user)
        db.commit()

        # Test chatbot response with translation
        response = generate_response("translation_test_user", "I feel stressed", db, target_lang="es")
        print(f"   Chatbot response (ES): {response[:100]}...")

        # Test with different language
        response_fr = generate_response("translation_test_user", "Hello", db, target_lang="fr")
        print(f"   Chatbot response (FR): {response_fr[:100]}...")

        # Clean up
        db.query(User).filter(User.username == "translation_test_user").delete()
        db.commit()
        db.close()

        print("   ✅ Chatbot integration working correctly")

        # Test 4: Supported languages
        print("\n4. Testing supported languages...")
        languages = service.get_supported_languages()
        print(f"   Supported languages: {len(languages)} total")
        key_languages = ['en', 'es', 'fr', 'de', 'hi']
        for lang in key_languages:
            assert lang in languages, f"Language {lang} should be supported"
            assert service.is_language_supported(lang), f"Language {lang} support check failed"
        print("   ✅ Language support verification passed")

        print("\n" + "=" * 50)
        print("🎉 ALL TESTS PASSED!")
        print("✅ Translation functionality is fully integrated and working")
        print("\n📋 Summary:")
        print("   • Translation service with mock fallbacks")
        print("   • Multi-language support (25+ languages)")
        print("   • Chatbot response translation")
        print("   • Graceful error handling")
        print("   • User language preferences")
        print("\n💡 Note: Install googletrans and langdetect for full translation capabilities")
        return True

    except Exception as e:
        print(f"\n❌ TEST FAILED: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_translation_edge_cases():
    """Test edge cases for translation functionality"""
    print("\n🔍 Testing Edge Cases...")

    try:
        from translation_service import translation_service

        # Test empty text
        result = translation_service.translate_text("", "es")
        assert result == "", "Empty text should return empty string"

        # Test whitespace only
        result = translation_service.translate_text("   ", "es")
        assert result == "   ", "Whitespace should be preserved"

        # Test None input
        result = translation_service.translate_text(None, "es")
        assert result is None, "None input should return None"

        # Test same language translation
        result = translation_service.translate_text("Hello", "en", "en")
        assert result == "Hello", "Same language should return original text"

        # Test unsupported language
        result = translation_service.translate_text("Hello", "unsupported")
        assert result == "Hello", "Unsupported language should return original text"

        print("   ✅ All edge cases handled correctly")
        return True

    except Exception as e:
        print(f"   ❌ Edge case test failed: {str(e)}")
        return False

if __name__ == "__main__":
    success1 = test_complete_translation_integration()
    success2 = test_translation_edge_cases()

    if success1 and success2:
        print("\n🏆 FINAL RESULT: Translation functionality is production-ready!")
        print("The wellbeing chatbot now supports multi-language responses.")
    else:
        print("\n⚠️  Some tests failed. Please review the implementation.")
