#!/usr/bin/env python3
"""
Comprehensive test suite for greeting and daily routine handling features
in the Wellbeing Chatbot.
"""

import sys
import os
import unittest
from unittest.mock import Mock, patch, MagicMock
import tempfile
import sqlite3
from datetime import datetime

# Add the current directory to the path so we can import modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from chatbot import generate_response
from models import User, MoodLog, ChatHistory
from database import init_db, get_db_session

class TestGreetingRoutineFeatures(unittest.TestCase):
    """Test cases for greeting and daily routine handling features."""

    def setUp(self):
        """Set up test database and mock user."""
        # Create a temporary database for testing
        self.db_fd, self.db_path = tempfile.mkstemp()
        self.db_session = None

        # Initialize test database
        init_db(self.db_path)
        self.db_session = get_db_session(self.db_path)

        # Create a test user
        self.test_user = User(username="test_user", password_hash="test_hash")
        self.db_session.add(self.test_user)
        self.db_session.commit()

        # Store original database path to restore later
        self.original_db_path = os.environ.get('DATABASE_URL')

    def tearDown(self):
        """Clean up test database."""
        if self.db_session:
            self.db_session.close()
        os.close(self.db_fd)
        os.unlink(self.db_path)
        if self.original_db_path:
            os.environ['DATABASE_URL'] = self.original_db_path

    def test_greeting_detection_basic(self):
        """Test basic greeting detection with short messages."""
        greeting_inputs = [
            "hello",
            "hi there",
            "good morning",
            "hey",
            "greetings",
            "sup",
            "yo"
        ]

        for greeting in greeting_inputs:
            with self.subTest(greeting=greeting):
                response = generate_response("test_user", greeting, self.db_session)

                # Check that response is one of the expected greeting responses
                expected_responses = [
                    "Hi there! How's your day going?",
                    "Hello! It's great to hear from you. What's new?",
                    "Hey! How are you feeling today?",
                    "Hi! I'm here whenever you need to talk. How's everything?"
                ]

                self.assertIn(response, expected_responses)

                # Check that database entry was created
                chat_entry = self.db_session.query(ChatHistory).filter(
                    ChatHistory.user_id == self.test_user.id,
                    ChatHistory.user_message == greeting
                ).first()

                self.assertIsNotNone(chat_entry, f"No database entry found for greeting: {greeting}")
                self.assertEqual(chat_entry.bot_response, response)

    def test_greeting_detection_case_insensitive(self):
        """Test that greeting detection works with different cases."""
        greeting_variations = [
            "HELLO",
            "Hi There",
            "Good Morning",
            "HEY",
            "Greetings",
            "SUP",
            "Yo"
        ]

        for greeting in greeting_variations:
            with self.subTest(greeting=greeting):
                response = generate_response("test_user", greeting, self.db_session)
                self.assertIsInstance(response, str)
                self.assertGreater(len(response), 0)

                # Check database entry
                chat_entry = self.db_session.query(ChatHistory).filter(
                    ChatHistory.user_id == self.test_user.id,
                    ChatHistory.user_message == greeting
                ).first()
                self.assertIsNotNone(chat_entry)

    def test_greeting_detection_long_messages(self):
        """Test that long messages with greetings are not treated as simple greetings."""
        long_greeting_messages = [
            "hello, I hope you're doing well today",
            "hi there, I wanted to talk about something important",
            "good morning, how has your day been so far",
            "hey, I need some advice about stress management"
        ]

        for message in long_greeting_messages:
            with self.subTest(message=message):
                # Mock Gemini API to avoid actual API calls
                with patch('chatbot.genai.GenerativeModel') as mock_model:
                    mock_response = Mock()
                    mock_response.text = "This is a mock response for long messages."
                    mock_model.return_value.generate_content.return_value = mock_response

                    response = generate_response("test_user", message, self.db_session)

                    # Should not be a simple greeting response
                    greeting_responses = [
                        "Hi there! How's your day going?",
                        "Hello! It's great to hear from you. What's new?",
                        "Hey! How are you feeling today?",
                        "Hi! I'm here whenever you need to talk. How's everything?"
                    ]

                    self.assertNotIn(response, greeting_responses)

    def test_daily_routine_detection(self):
        """Test daily routine question detection."""
        routine_questions = [
            "daily routine",
            "how is your day",
            "what's your routine",
            "tell me about your day",
            "how was your day",
            "what do you do daily",
            "your daily life"
        ]

        for question in routine_questions:
            with self.subTest(question=question):
                response = generate_response("test_user", question, self.db_session)

                # Check that response contains expected elements
                expected_phrases = [
                    "My day usually involves helping people like you",
                    "As an AI wellbeing companion",
                    "My 'routine' is being available 24/7",
                    "My purpose is to support wellbeing"
                ]

                response_lower = response.lower()
                has_expected_content = any(phrase.lower() in response_lower for phrase in expected_phrases)
                self.assertTrue(has_expected_content, f"Response doesn't contain expected content for: {question}")

                # Check database entry
                chat_entry = self.db_session.query(ChatHistory).filter(
                    ChatHistory.user_id == self.test_user.id,
                    ChatHistory.user_message == question
                ).first()
                self.assertIsNotNone(chat_entry)

    def test_daily_routine_case_insensitive(self):
        """Test daily routine detection with different cases."""
        routine_variations = [
            "DAILY ROUTINE",
            "How Is Your Day",
            "What's Your Routine",
            "Tell Me About Your Day"
        ]

        for question in routine_variations:
            with self.subTest(question=question):
                response = generate_response("test_user", question, self.db_session)
                self.assertIsInstance(response, str)
                self.assertGreater(len(response), 0)

                # Check database entry
                chat_entry = self.db_session.query(ChatHistory).filter(
                    ChatHistory.user_id == self.test_user.id,
                    ChatHistory.user_message == question
                ).first()
                self.assertIsNotNone(chat_entry)

    def test_no_interference_with_crisis_detection(self):
        """Test that greeting/routine features don't interfere with crisis detection."""
        crisis_messages = [
            "I want to kill myself",
            "I'm feeling suicidal",
            "I can't go on anymore",
            "I'm having suicidal thoughts"
        ]

        for message in crisis_messages:
            with self.subTest(message=message):
                response = generate_response("test_user", message, self.db_session)

                # Should trigger crisis response, not greeting/routine
                crisis_indicators = [
                    "I'm really concerned about what you're going through",
                    "Please reach out immediately",
                    "🚨 Emergency Services",
                    "🆘 Mental Health Crisis Helplines"
                ]

                response_lower = response.lower()
                has_crisis_content = any(indicator.lower() in response_lower for indicator in crisis_indicators)
                self.assertTrue(has_crisis_content, f"Crisis detection not working for: {message}")

    def test_no_interference_with_health_queries(self):
        """Test that greeting/routine features don't interfere with health queries."""
        health_queries = [
            "symptoms of depression",
            "how to prevent anxiety",
            "what causes stress",
            "treatment for headache"
        ]

        for query in health_queries:
            with self.subTest(query=query):
                # Mock Gemini API
                with patch('chatbot.genai.GenerativeModel') as mock_model:
                    mock_response = Mock()
                    mock_response.text = "This is a mock health response."
                    mock_model.return_value.generate_content.return_value = mock_response

                    response = generate_response("test_user", query, self.db_session)

                    # Should not be greeting or routine response
                    greeting_responses = [
                        "Hi there! How's your day going?",
                        "Hello! It's great to hear from you. What's new?",
                        "Hey! How are you feeling today?",
                        "Hi! I'm here whenever you need to talk. How's everything?"
                    ]

                    routine_indicators = [
                        "My day usually involves helping people",
                        "As an AI wellbeing companion"
                    ]

                    self.assertNotIn(response, greeting_responses)
                    response_lower = response.lower()
                    has_routine_content = any(indicator.lower() in response_lower for indicator in routine_indicators)
                    self.assertFalse(has_routine_content, f"Routine response triggered for health query: {query}")

    def test_edge_cases(self):
        """Test edge cases for greeting and routine detection."""
        edge_cases = [
            "",  # Empty string
            "   ",  # Whitespace only
            "h",  # Very short
            "hello world this is a long message with greeting",  # Long with greeting
            "daily routine is important for health",  # Routine in longer context
            "hi!",  # With punctuation
            "Hello.",  # With period
            "hey?",  # With question mark
        ]

        for case in edge_cases:
            with self.subTest(case=repr(case)):
                try:
                    response = generate_response("test_user", case, self.db_session)
                    self.assertIsInstance(response, str)
                    self.assertGreater(len(response), 0)
                except Exception as e:
                    self.fail(f"Edge case {repr(case)} caused exception: {e}")

    def test_database_integrity(self):
        """Test that database operations work correctly."""
        # Test multiple interactions
        interactions = [
            ("hello", "greeting"),
            ("how is your day", "routine"),
            ("hello again", "greeting"),
            ("what's your routine", "routine")
        ]

        for message, interaction_type in interactions:
            with self.subTest(message=message, interaction_type=interaction_type):
                initial_count = self.db_session.query(ChatHistory).count()

                response = generate_response("test_user", message, self.db_session)

                final_count = self.db_session.query(ChatHistory).count()
                self.assertEqual(final_count, initial_count + 1, f"Database entry not created for: {message}")

                # Verify the entry
                chat_entry = self.db_session.query(ChatHistory).filter(
                    ChatHistory.user_id == self.test_user.id,
                    ChatHistory.user_message == message
                ).first()

                self.assertIsNotNone(chat_entry)
                self.assertEqual(chat_entry.bot_response, response)
                self.assertIsNotNone(chat_entry.timestamp)

    def test_conversation_flow(self):
        """Test that greeting/routine features work in conversation context."""
        # Simulate a conversation
        conversation = [
            "hi",
            "how is your day",
            "thanks for asking",
            "hello again"
        ]

        responses = []

        for message in conversation:
            response = generate_response("test_user", message, self.db_session)
            responses.append(response)

        # Check that we have responses for all messages
        self.assertEqual(len(responses), len(conversation))

        # Check database has all entries
        chat_count = self.db_session.query(ChatHistory).filter(
            ChatHistory.user_id == self.test_user.id
        ).count()
        self.assertEqual(chat_count, len(conversation))

if __name__ == '__main__':
    # Set up environment for testing
    os.environ['GEMINI_API_KEY'] = 'test_key_for_testing'

    # Run the tests
    unittest.main(verbosity=2)
