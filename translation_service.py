import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TranslationService:
    def __init__(self):
        # Try to import external translation libraries, fallback to mock if not available
        self.translator_available = False
        self.mock_translations = {
            'es': {
                'Hello': 'Hola',
                'How are you?': '¿Cómo estás?',
                'I feel stressed': 'Me siento estresado',
                'I need help': 'Necesito ayuda',
                'Thank you': 'Gracias',
                'I feel anxious': 'Me siento ansioso',
                'I feel sad': 'Me siento triste',
                'I feel happy': 'Me siento feliz',
                'Good morning': 'Buenos días',
                'Good evening': 'Buenas noches'
            },
            'fr': {
                'Hello': 'Bonjour',
                'How are you?': 'Comment allez-vous?',
                'I feel stressed': 'Je me sens stressé',
                'I need help': 'J\'ai besoin d\'aide',
                'Thank you': 'Merci',
                'I feel anxious': 'Je me sens anxieux',
                'I feel sad': 'Je me sens triste',
                'I feel happy': 'Je me sens heureux',
                'Good morning': 'Bonjour',
                'Good evening': 'Bonsoir'
            },
            'de': {
                'Hello': 'Hallo',
                'How are you?': 'Wie geht es Ihnen?',
                'I feel stressed': 'Ich fühle mich gestresst',
                'I need help': 'Ich brauche Hilfe',
                'Thank you': 'Danke',
                'I feel anxious': 'Ich fühle mich ängstlich',
                'I feel sad': 'Ich fühle mich traurig',
                'I feel happy': 'Ich fühle mich glücklich',
                'Good morning': 'Guten Morgen',
                'Good evening': 'Guten Abend'
            },
            'hi': {
                'Hello': 'नमस्ते',
                'How are you?': 'आप कैसे हैं?',
                'I feel stressed': 'मैं तनाव महसूस कर रहा हूं',
                'I need help': 'मुझे मदद चाहिए',
                'Thank you': 'धन्यवाद',
                'I feel anxious': 'मैं चिंतित महसूस कर रहा हूं',
                'I feel sad': 'मैं दुखी महसूस कर रहा हूं',
                'I feel happy': 'मैं खुश महसूस कर रहा हूं',
                'Good morning': 'सुप्रभात',
                'Good evening': 'शुभ संध्या'
            }
        }

        try:
            from googletrans import Translator
            from langdetect import detect, LangDetectError
            self.translator = Translator()
            self.detect = detect
            self.LangDetectError = LangDetectError
            self.translator_available = True
            logger.info("External translation libraries loaded successfully")
        except ImportError as e:
            logger.warning(f"External translation libraries not available: {e}. Using mock translations.")
            self.translator_available = False

        # Supported languages for mental health content (ISO 639-1 codes)
        self.supported_languages = {
            'en': 'English',
            'es': 'Spanish',
            'fr': 'French',
            'de': 'German',
            'it': 'Italian',
            'pt': 'Portuguese',
            'ru': 'Russian',
            'ja': 'Japanese',
            'ko': 'Korean',
            'zh-cn': 'Chinese (Simplified)',
            'ar': 'Arabic',
            'hi': 'Hindi',
            'bn': 'Bengali',
            'ur': 'Urdu',
            'fa': 'Persian',
            'tr': 'Turkish',
            'pl': 'Polish',
            'nl': 'Dutch',
            'sv': 'Swedish',
            'da': 'Danish',
            'no': 'Norwegian',
            'fi': 'Finnish',
            'he': 'Hebrew',
            'th': 'Thai',
            'vi': 'Vietnamese',
            'id': 'Indonesian',
            'ms': 'Malay',
            'tl': 'Filipino'
        }

    def detect_language(self, text):
        """Detect the language of the input text"""
        if self.translator_available:
            try:
                detected_lang = self.detect(text)
                # Normalize language codes
                if detected_lang == 'zh':
                    detected_lang = 'zh-cn'
                elif detected_lang == 'zht':
                    detected_lang = 'zh-tw'
                return detected_lang
            except self.LangDetectError:
                logger.warning("Could not detect language, defaulting to English")
                return 'en'
        else:
            # Simple fallback language detection based on common patterns
            text_lower = text.lower()
            if any(word in text_lower for word in ['hola', 'gracias', 'español', '¿', '¡']):
                return 'es'
            elif any(word in text_lower for word in ['bonjour', 'merci', 'français']):
                return 'fr'
            elif any(word in text_lower for word in ['hallo', 'danke', 'deutsch']):
                return 'de'
            elif any(word in text_lower for word in ['नमस्ते', 'धन्यवाद', 'हिंदी']):
                return 'hi'
            else:
                return 'en'

    def translate_text(self, text, target_lang, source_lang='auto'):
        """Translate text to target language"""
        if not text or text.strip() == '':
            return text

        if target_lang not in self.supported_languages and target_lang != 'en':
            logger.warning(f"Unsupported language: {target_lang}, falling back to English")
            return text

        if target_lang == 'en' or source_lang == target_lang:
            return text

        # Use external translator if available
        if self.translator_available:
            try:
                translation = self.translator.translate(text, src=source_lang, dest=target_lang)
                return translation.text
            except Exception as e:
                logger.error(f"Translation failed: {str(e)}")
                return text  # Return original text if translation fails
        else:
            # Use mock translations
            if target_lang in self.mock_translations:
                # Simple exact match lookup
                if text in self.mock_translations[target_lang]:
                    return self.mock_translations[target_lang][text]
                else:
                    # For unmatched text, return original with a note
                    logger.info(f"Mock translation: '{text}' not found for {target_lang}, returning original")
                    return text
            else:
                logger.warning(f"No mock translations available for {target_lang}")
                return text

    def is_language_supported(self, lang_code):
        """Check if a language is supported"""
        return lang_code in self.supported_languages

    def get_supported_languages(self):
        """Get list of supported languages"""
        return self.supported_languages

    def translate_mental_health_content(self, text, target_lang):
        """
        Specialized translation for mental health content with cultural sensitivity
        """
        if target_lang not in ['es', 'fr', 'de', 'it', 'pt', 'ru', 'ja', 'ko', 'zh-cn', 'ar', 'hi']:
            # For unsupported languages, use standard translation
            return self.translate_text(text, target_lang)

        # For supported mental health languages, use standard translation
        # In a production system, you might want to use human-reviewed translations
        # for sensitive mental health content
        return self.translate_text(text, target_lang)

# Global translation service instance
translation_service = TranslationService()
