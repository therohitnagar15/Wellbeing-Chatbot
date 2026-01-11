# Wellbeing Chatbot TODO

## Completed
- [x] Integrate OpenAI GPT for natural chatbot responses
- [x] Add OpenAI API key management with .env file
- [x] Update requirements.txt with openai and python-dotenv
- [x] Create README.md with setup instructions
- [x] Add fallback responses if OpenAI fails
- [x] Maintain crisis detection and exercise recommendations
- [x] Fix 404 error for login page links (changed /login.html to /login)
- [x] Add dashboard button on main page
- [x] Make dashboard button attractive with CSS
- [x] Make usernames responsive
- [x] When clicking on username, show their report

## Remaining Tasks
- [x] Test the chatbot with OpenAI API - Issue identified: API key not working, falling back to rule-based responses
- [x] Fine-tune the GPT prompt for better wellbeing responses - Enhanced prompt with detailed guidelines for compassionate, professional responses
- [x] Add conversation history for context - Implemented with last 10 messages stored in database
- [x] Implement rate limiting for API calls - Added 20 API calls per hour per user limit
- [x] Add more wellbeing resources and exercises - Added 8 new exercises: progressive muscle relaxation, gratitude journaling, peaceful place visualization, body scan meditation, loving kindness meditation, mindful walking, positive affirmations, self-compassion, and nature connection
- [x] Deploy to a hosting platform - Prepared for Heroku deployment with Procfile, runtime.txt, updated requirements.txt, and deployment guide in README.md

## Notes
- The chatbot now uses GPT-3.5-turbo for natural conversations
- Fallback to rule-based responses if API fails
- User mood is included in the prompt for personalized responses
- Crisis keywords still trigger immediate professional help recommendations
