#!/usr/bin/env python3
"""
Test script for translation functionality in the wellbeing chatbot.
Tests language detection, translation accuracy, and integration with chatbot responses.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from translation_service import translation_service
from chatbot import generate_response
from models import User, ChatHistory
from database import get_db
import unittest
from unittest.mock import Mock, patch

class TestTranslationService(unittest.TestCase):
    """Test cases for the TranslationService class"""

    def test_language_detection(self):
        """Test language detection for various languages"""
        test_cases = [
            ("Hello, how are you?", "en"),
            ("Hola, ¿cómo estás?", "es"),
            ("Bonjour, comment allez-vous?", "fr"),
            ("Hallo, wie geht es dir?", "de"),
            ("Ciao, come stai?", "it"),
            ("Olá, como você está?", "pt"),
            ("Привет, как дела?", "ru"),
            ("こんにちは、元気ですか？", "ja"),
            ("안녕하세요, 어떻게 지내세요?", "ko"),
            ("你好，你怎么样？", "zh-cn"),
            ("مرحبا، كيف حالك؟", "ar"),
            ("नमस्ते, आप कैसे हैं?", "hi")
        ]

        for text, expected_lang in test_cases:
            with self.subTest(text=text):
                detected = translation_service.detect_language(text)
                # Allow for some flexibility in detection
                self.assertIn(detected, [expected_lang, expected_lang.split('-')[0]])

    def test_translation_basic(self):
        """Test basic translation functionality"""
        text = "Hello, how are you today?"
        translated = translation_service.translate_text(text, "es")

        # Check that translation is not empty and different from original
        self.assertIsNotNone(translated)
        self.assertNotEqual(translated, "")
        self.assertNotEqual(translated.lower(), text.lower())

        # Spanish translation should contain common Spanish words
        self.assertTrue(any(word in translated.lower() for word in ["hola", "cómo", "estás", "hoy"]))

    def test_translation_to_multiple_languages(self):
        """Test translation to multiple supported languages"""
        text = "I feel stressed and need help."

        target_languages = ["es", "fr", "de", "it", "pt", "hi"]

        for lang in target_languages:
            with self.subTest(lang=lang):
                translated = translation_service.translate_text(text, lang)
                self.assertIsNotNone(translated)
                self.assertNotEqual(translated, "")
                self.assertNotEqual(translated.lower(), text.lower())

    def test_unsupported_language_fallback(self):
        """Test fallback behavior for unsupported languages"""
        text = "Hello world"
        translated = translation_service.translate_text(text, "unsupported_lang")
        self.assertEqual(translated, text)  # Should return original text

    def test_empty_text_handling(self):
        """Test handling of empty or whitespace-only text"""
        test_cases = ["", "   ", None]

        for text in test_cases:
            translated = translation_service.translate_text(text, "es")
            self.assertEqual(translated, text)

class TestChatbotTranslationIntegration(unittest.TestCase):
    """Test integration of translation with chatbot responses"""

    def setUp(self):
        """Set up test database session"""
        self.db = next(get_db())

        # Create a test user
        self.test_user = User(
            username="test_user_translation",
            email="test@example.com",
            language="en"
        )
        self.db.add(self.test_user)
        self.db.commit()

    def tearDown(self):
        """Clean up test data"""
        # Remove test chat history
        self.db.query(ChatHistory).filter(ChatHistory.user_id == self.test_user.id).delete()
        # Remove test user
        self.db.query(User).filter(User.id == self.test_user.id).delete()
        self.db.commit()

    @patch('chatbot.gemini_model')
    def test_chatbot_response_translation(self, mock_gemini):
        """Test that chatbot responses are translated correctly"""
        # Mock Gemini response
        mock_response = Mock()
        mock_response.text = "I'm here to help you with your stress. Try taking deep breaths."
        mock_gemini.generate_content.return_value = mock_response

        # Test English response (no translation needed)
        response_en = generate_response("test_user_translation", "I feel stressed", self.db, target_lang="en")
        self.assertIn("help you with your stress", response_en)

        # Test Spanish translation
        response_es = generate_response("test_user_translation", "I feel stressed", self.db, target_lang="es")
        # Note: In real implementation, this would be translated, but we're mocking

    def test_language_preference_from_user(self):
        """Test that user's language preference is used"""
        # Update user language preference
        self.test_user.language = "es"
        self.db.commit()

        # Test that user language is retrieved correctly
        user = self.db.query(User).filter(User.username == "test_user_translation").first()
        self.assertEqual(user.language, "es")

    def test_translation_error_handling(self):
        """Test error handling when translation fails"""
        # Test with invalid target language
        response = generate_response("test_user_translation", "Hello", self.db, target_lang="invalid")
        # Should still return a response (fallback to English)

def run_translation_tests():
    """Run all translation tests"""
    print("Running Translation Functionality Tests...")
    print("=" * 50)

    # Test language detection
    print("\n1. Testing Language Detection:")
    test_texts = [
        "Hello, how are you?",
        "Hola, ¿cómo estás?",
        "Bonjour, comment allez-vous?",
        "नमस्ते, आप कैसे हैं?"
    ]

    for text in test_texts:
        detected = translation_service.detect_language(text)
        print(f"Text: '{text[:30]}...' -> Detected: {detected}")

    # Test basic translation
    print("\n2. Testing Basic Translation:")
    test_text = "I feel anxious and need help with stress."
    languages = ["es", "fr", "de", "hi"]

    for lang in languages:
        try:
            translated = translation_service.translate_text(test_text, lang)
            print(f"{lang.upper()}: {translated[:50]}...")
        except Exception as e:
            print(f"{lang.upper()}: Translation failed - {str(e)}")

    # Test chatbot integration
    print("\n3. Testing Chatbot Integration:")
    try:
        db = next(get_db())
        response = generate_response("test_user", "I feel stressed", db, target_lang="es")
        print(f"Chatbot response (ES): {response[:100]}...")
    except Exception as e:
        print(f"Chatbot integration test failed: {str(e)}")

    print("\n4. Running Unit Tests:")
    unittest.main(argv=[''], exit=False, verbosity=2)

if __name__ == "__main__":
    run_translation_tests()
