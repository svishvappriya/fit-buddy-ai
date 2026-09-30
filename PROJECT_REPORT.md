# FIT BUDDY — AI FITNESS PLAN GENERATOR USING GEMINI MODELS

## Abstract
Fit Buddy is a Python web application that generates general personalized fitness guidance using Google Gemini. It collects age, height, weight, activity, goal, experience, equipment and diet preference; calculates basic metrics; sends the structured profile to Gemini; and stores the generated plan in SQLite.

## Objectives
- Develop a simple AI-enabled fitness web application.
- Store user accounts and fitness profiles.
- Calculate BMI, BMR and estimated maintenance calories.
- Generate a 7-day fitness plan.
- Save plans for later viewing.
- Provide an admin dashboard.

## Functional Requirements
Registration, login, logout, profile entry, metric calculation, AI generation, plan history and admin statistics.

## Non-Functional Requirements
Usability, password hashing, responsive UI, maintainability and API-key protection.

## Database Tables
**User:** id, name, email, password_hash, role, created_at.

**FitnessProfile:** id, user_id, age, gender, height, weight, activity, goal, experience, workout_days, equipment, diet, bmi, bmr, maintenance_calories, created_at.

**FitnessPlan:** id, user_id, title, content, created_at.

## System Flow
Browser → Flask → Authentication/Profile → Calculator → Gemini Service → Fitness Plan → SQLite → Dashboard.

## Conclusion
The project demonstrates practical integration of Python, web development, database management and generative AI. It can later be extended with progress tracking, exercise media, PDF reports and a mobile client.

## Disclaimer
Generated content is general educational information and is not a substitute for professional medical or fitness advice.
