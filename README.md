# Wellbeing Chatbot

A compassionate AI-powered wellbeing chatbot designed for individuals suffering from psychological diseases, helping users track their mood, engage in supportive conversations, and access mental health resources tailored to their emotional states.

## Features

- User registration and authentication
- Daily mood tracking with psychological insights
- AI-powered chatbot conversations using OpenAI GPT, customized for psychological conditions
- Breathing and mindfulness exercises adapted for mood management
- Mood history and export (CSV/PDF) for therapeutic tracking
- Admin dashboard for user management
- Responsive web interface
- Mood-based quick access tools for anxiety, depression, stress, overwhelm, motivation, and loneliness

## Setup

1. Clone or download the project files.

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Get an OpenAI API key from [OpenAI](https://platform.openai.com/api-keys).

4. Create a `.env` file in the project root and add your API key:
   ```
   OPENAI_API_KEY=your-api-key-here
   ```

5. Run the application:
   ```
   python main.py
   ```

6. Open your browser and go to `http://127.0.0.1:8001`.

7. Login with username: `test`, password: `test` (or register a new account).

## Usage

- **Login/Register**: Create an account or login with existing credentials.
- **Track Mood**: Select your current mood from the dropdown to get personalized insights.
- **Chat**: Type messages to the chatbot. It will respond empathetically and offer exercises tailored to your mood and psychological needs.
- **Mood Support Tools**: Use quick-access buttons for common psychological challenges like anxiety relief, depression support, stress management, etc.
- **View History**: Check your mood history and export reports for personal or professional review.
- **Dashboard**: Admins can view all users and their mood logs.

## Technologies Used

- **Backend**: FastAPI, SQLAlchemy, SQLite
- **AI**: OpenAI GPT-3.5-turbo
- **Frontend**: HTML, CSS, JavaScript
- **Other**: TextBlob for sentiment analysis, ReportLab for PDF generation

## Safety Features

- Crisis detection: Automatically responds to crisis keywords with professional help recommendations.
- Fallback responses: If AI fails, uses rule-based responses tailored for psychological support.
- Supportive content: All responses are designed to be empathetic, encouraging, and psychologically informed.

## Contributing

Feel free to contribute improvements, bug fixes, or new features focused on mental health support!

## Deployment to Heroku

1. **Install Heroku CLI** (if not already installed):
   - Download and install from https://devcenter.heroku.com/articles/heroku-cli
   - Or use package manager: `winget install heroku` (Windows)

2. **Login to Heroku**:
   ```
   heroku login
   ```

3. **Create a new Heroku app**:
   ```
   heroku create your-app-name
   ```

4. **Set environment variables**:
   ```
   heroku config:set OPENAI_API_KEY=your-openai-api-key-here
   ```

5. **Deploy to Heroku**:
   ```
   git init
   git add .
   git commit -m "Initial commit"
   heroku git:remote -a your-app-name
   git push heroku main
   ```

6. **Open your deployed app**:
   ```
   heroku open
   ```

## License

This project is open-source. Use responsibly and prioritize user mental health.
