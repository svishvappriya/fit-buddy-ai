import os
from google import genai


def demo_plan(p):
    return f"""
**Goal Summary**

Your current goal is **{p["goal"]}**.

This plan is designed based on your experience level, available equipment,
activity level and preferred workout schedule.

**Profile Overview**

Goal: {p["goal"]}
Experience: {p["experience"]}
Equipment: {p["equipment"] or "Bodyweight"}
Activity Level: {p["activity"]}
Diet Preference: {p["diet"]}

**7-Day Workout Schedule**

Monday

Full Body Workout

Squats, Push-ups and Glute Bridge

3 sets × 10–12 repetitions


Tuesday

Recovery Day

Light walking and mobility exercises

20–30 minutes


Wednesday

Upper Body Workout

Push-ups, Rows or Band Pulls and Plank

3 sets × 8–12 repetitions


Thursday

Rest and Recovery

Gentle stretching and relaxed walking

10–15 minutes


Friday

Lower Body Workout

Squats, Lunges and Calf Raises

3 sets × 10–15 repetitions


Saturday

Cardio

Brisk walking or cycling

25–35 minutes


Sunday

Recovery

Easy walking and mobility exercises

15–20 minutes


**Warm-up & Cool-down**

Start each workout with 5–8 minutes of light movement, arm circles
and leg movements.

After your workout, spend a few minutes doing gentle stretching
and slow breathing.


**General Nutrition Guidance**

Choose balanced meals containing vegetables or fruits, protein sources,
whole grains and adequate fluids.

Try to maintain regular meal timings and avoid making sudden extreme
changes to your food intake.


**Hydration & Recovery**

Drink water regularly throughout the day.

Maintain a consistent sleep schedule and allow your body enough time
to recover between workouts.


**Progress Tracking**

Track your weekly body weight, completed workouts, energy level
and exercise repetitions.

Focus on consistency and gradual improvement rather than rapid changes.


**Safety Notes**

Stop exercising if you experience significant pain, dizziness or
unusual symptoms.

If you have an injury or medical condition, consult a qualified
health professional before starting a new exercise program.
"""


def generate_plan(p):

    key = os.getenv("GEMINI_API_KEY")

    if not key:
        return demo_plan(p)

    client = genai.Client(api_key=key)

    prompt = f"""
You are Fit Buddy AI, an AI fitness assistant used in a college
software project.

Create a personalized, safe and practical general fitness plan based
on the following user profile.

USER PROFILE

Age: {p["age"]}
Gender: {p["gender"]}
Height: {p["height"]} cm
Weight: {p["weight"]} kg
Activity Level: {p["activity"]}
Fitness Goal: {p["goal"]}
Experience Level: {p["experience"]}
Workout Days: {p["workout_days"]}
Available Equipment: {p["equipment"] or "Bodyweight"}
Diet Preference: {p["diet"]}
BMI: {p["bmi"]}
BMR: {p["bmr"]}
Estimated Maintenance Calories: {p["maintenance_calories"]}

IMPORTANT OUTPUT FORMAT

Return ONLY the fitness plan.

Do NOT use:

# headings
## headings
### headings
Markdown tables
Markdown blockquotes
Numbered lists

Use this exact section structure:

**Goal Summary**

Write 2–3 short paragraphs explaining the user's goal and
how the plan is designed.

**Profile Overview**

Show the important profile information in short lines.

**7-Day Workout Schedule**

For every day, provide:

Day name

Workout focus

Exercises

Sets, repetitions or duration

Keep each day clearly separated with blank lines.

**Warm-up & Cool-down**

Give simple warm-up and cool-down instructions.

**General Nutrition Guidance**

Give practical general nutrition suggestions based on the
user's goal and diet preference.

Do not prescribe an extreme calorie restriction.

**Hydration & Recovery**

Give practical hydration, sleep and recovery suggestions.

**Progress Tracking**

Explain what the user can track weekly.

**AI Recommendations**

Give 3–5 practical recommendations specifically based on
the user's profile.

**Safety Notes**

Include a short safety section.

Do not diagnose medical conditions.

Do not prescribe medication.

Do not recommend starvation, extreme dieting or unsafe exercise.

Do not make guaranteed weight-loss claims.

BMI should not be presented as a complete measure of health.

STYLE

Write like a modern AI fitness assistant.

Keep the language simple and friendly.

Use short paragraphs.

Use blank lines between sections.

Do not use excessive emojis.

Do not add unnecessary introductions or conclusions.

Make the response easy to display in a web application.
"""

    response = client.models.generate_content(
        model=os.getenv(
            "GEMINI_MODEL",
            "gemini-2.5-flash"
        ),
        contents=prompt
    )

    return response.text