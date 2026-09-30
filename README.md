# Fit Buddy AI — College Student Project

**Project Title:** Fit Buddy – AI Fitness Plan Generator Using Gemini Models

**Project Type:** College Mini Project / Final Year Mini Project

## Problem Statement
Beginners often do not know how to organize a weekly workout routine based on their goal, experience and available equipment. Fit Buddy collects these inputs and uses Gemini to generate general fitness guidance.

## Main Modules
1. User Registration / Login
2. Fitness Profile
3. BMI, BMR and maintenance calculation
4. Gemini AI 7-day plan generation
5. Plan history
6. Admin dashboard

## Technology Stack
- Python Flask
- HTML5 / CSS3 / Bootstrap 5
- SQLite
- Flask-SQLAlchemy
- Flask-Login
- Google Gemini API

## Windows Setup
```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Copy `.env.example` to `.env` and add:
```env
SECRET_KEY=my-secret-key
GEMINI_API_KEY=YOUR_GEMINI_API_KEY
GEMINI_MODEL=gemini-2.5-flash
```

Run:
```powershell
python run.py
```
Open `http://127.0.0.1:5000`.

## Demo Admin
Email: `admin@fitbuddy.local`
Password: `admin123`

Change this credential before deployment.

## Viva Points
- Flask is lightweight and suitable for a student web project.
- SQLite is serverless and easy to demonstrate.
- Gemini converts structured user inputs into natural-language fitness guidance.
- Passwords are hashed before storage.
- `.env` keeps the API key out of source code.

## Future Enhancements
Exercise videos, progress charts, PDF export, reminders, mobile app, PostgreSQL deployment, AI chat and wearable integration.

## Safety
This is an educational fitness assistant and is not a medical diagnosis or treatment system.


## UI Style
The interface intentionally uses a simple, clean student-project style: Bootstrap, soft colors, cards, icons and straightforward navigation. It avoids an overly commercial enterprise look while remaining presentable for a college demo.
