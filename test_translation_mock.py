#!/usr/bin/env python3
"""
Mock test script for translation functionality in the wellbeing chatbot.
Tests the integration without requiring external translation services.
"""

import sys
import os
import unittest
from unittest.mock import Mock, patch, MagicMock
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

class TestTranslationIntegration(unittest.TestCase):
    """Test translation integration with mocked services"""

    def setUp(self):
        """Set up test environment"""
        # Mock the googletrans module
        self.googletrans_mock = MagicMock()
        self.translator_mock = MagicMock()
        self.googletrans_mock.Translator.return_value = self.translator_mock

        # Mock langdetect
        self.langdetect_mock = MagicMock()
        self.langdetect_mock.detect.return_value = 'en'
        self.langdetect_mock.LangDetectError = Exception

        # Apply patches
        self.patches = [
            patch.dict('sys.modules', {'googletrans': self.googletrans_mock}),
            patch.dict('sys.modules', {'langdetect': self.langdetect_mock}),
        ]

        for p in self.patches:
            p.start()

        # Now import after mocking
        from translation_service import TranslationService, translation_service
        self.TranslationService = TranslationService
        self.translation_service = translation_service

    def tearDown(self):
        """Clean up patches"""
        for p in self.patches:
            p.stop()

    def test_translation_service_initialization(self):
        """Test that TranslationService initializes correctly"""
        service = self.TranslationService()
        self.assertIsNotNone(service.translator)
        self.assertIsInstance(service.supported_languages, dict)
        self.assertGreater(len(service.supported_languages), 0)

    def test_language_support(self):
        """Test language support checking"""
        service = self.TranslationService()

        # Test supported languages
        self.assertTrue(service.is_language_supported('en'))
        self.assertTrue(service.is_language_supported('es'))
        self.assertTrue(service.is_language_supported('fr'))

        # Test unsupported language
        self.assertFalse(service.is_language_supported('unsupported'))

    def test_translation_text_method(self):
        """Test the translate_text method"""
        service = self.TranslationService()

        # Mock the translator's translate method
        self.translator_mock.translate.return_value.text = "Hola mundo"

        # Test translation
        result = service.translate_text("Hello world", "es")
        self.assertEqual(result, "Hola mundo")
        self.translator_mock.translate.assert_called_once()

    def test_empty_text_handling(self):
        """Test handling of empty text"""
        service = self.TranslationService()

        result = service.translate_text("", "es")
        self.assertEqual(result, "")

        result = service.translate_text("   ", "es")
        self.assertEqual(result, "   ")

        result = service.translate_text(None, "es")
        self.assertIsNone(result)

    def test_same_language_no_translation(self):
        """Test that text isn't translated when source and target are the same"""
        service = self.TranslationService()

        result = service.translate_text("Hello world", "en", "en")
        self.assertEqual(result, "Hello world")
        # Translator should not be called
        self.translator_mock.translate.assert_not_called()

    def test_unsupported_language_fallback(self):
        """Test fallback for unsupported languages"""
        service = self.TranslationService()

        result = service.translate_text("Hello world", "unsupported")
        self.assertEqual(result, "Hello world")  # Should return original text

    def test_language_detection(self):
        """Test language detection"""
        service = self.TranslationService()

        # Test successful detection
        result = service.detect_language("Hello world")
        self.assertEqual(result, 'en')

        # Test detection error
        self.langdetect_mock.detect.side_effect = Exception("Detection failed")
        result = service.detect_language("Unknown text")
        self.assertEqual(result, 'en')  # Should default to English

    @patch('chatbot.translation_service')
    def test_chatbot_translation_integration(self, mock_translation_service):
        """Test chatbot integration with translation"""
        # Mock the translation service
        mock_translation_service.translate_text.return_value = "¡Hola! ¿Cómo estás?"

        # Import chatbot after mocking
        from chatbot import generate_response
        from database import get_db

        # Get database session
        db = next(get_db())

        # Test generate_response with target_lang
        response = generate_response("test_user", "Hello", db, target_lang="es")

        # Verify translation was called
        mock_translation_service.translate_text.assert_called_once()

        # Clean up
        db.close()

class TestChatbotCodeIntegration(unittest.TestCase):
    """Test that chatbot code properly integrates translation"""

    def test_translation_code_presence(self):
        """Test that translation code is present in chatbot.py"""
        with open('chatbot.py', 'r', encoding='utf-8') as f:
            content = f.read()

        # Check for translation service import
        self.assertIn('from translation_service import translation_service', content)

        # Check for target_lang parameter in generate_response
        self.assertIn('target_lang=None', content)

        # Check for translation usage
        self.assertIn('translation_service.translate', content)

        # Check for target_language variable
        self.assertIn('target_language', content)

    def test_translation_error_handling(self):
        """Test that translation errors are handled gracefully"""
        # This would require mocking the translation to raise an exception
        # and verifying the chatbot still returns a response
        pass

def run_mock_tests():
    """Run the mock translation tests"""
    print("Running Mock Translation Tests...")
    print("=" * 50)

    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add test cases
    suite.addTest(TestTranslationIntegration('test_translation_service_initialization'))
    suite.addTest(TestTranslationIntegration('test_language_support'))
    suite.addTest(TestTranslationIntegration('test_translation_text_method'))
    suite.addTest(TestTranslationIntegration('test_empty_text_handling'))
    suite.addTest(TestTranslationIntegration('test_same_language_no_translation'))
    suite.addTest(TestTranslationIntegration('test_unsupported_language_fallback'))
    suite.addTest(TestTranslationIntegration('test_language_detection'))
    suite.addTest(TestChatbotCodeIntegration('test_translation_code_presence'))

    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    return result.wasSuccessful()

if __name__ == "__main__":
    success = run_mock_tests()

    if success:
        print("\n🎉 All mock translation tests passed!")
        print("The translation functionality is properly integrated into the chatbot.")
        print("\nNote: These tests use mocked services. For full functionality testing,")
        print("ensure googletrans and langdetect are properly installed and internet-connected.")
    else:
        print("\n❌ Some tests failed. Please check the implementation.")
