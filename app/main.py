from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from .extensions import db
from .models import FitnessProfile, FitnessPlan, User
from .calculator import calculate_metrics
from .services.gemini_service import generate_plan
import os

from google import genai

main_bp = Blueprint('main', __name__)
@main_bp.route('/')
def home(): return render_template('home.html')


@main_bp.route('/dashboard')
@login_required
def dashboard():
    profile = FitnessProfile.query.filter_by(user_id=current_user.id).order_by(
        FitnessProfile.created_at.desc()).first()
    plans = FitnessPlan.query.filter_by(user_id=current_user.id).order_by(
        FitnessPlan.created_at.desc()).all()
    return render_template('dashboard.html', profile=profile, plans=plans)


@main_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        age = int(request.form['age'])
        gender = request.form['gender']
        height = float(request.form['height'])
        weight = float(request.form['weight'])
        activity = request.form['activity']
        goal = request.form['goal']
        experience = request.form['experience']
        days = int(request.form['workout_days'])
        equipment = ', '.join(request.form.getlist('equipment'))
        diet = request.form['diet']
        bmi, bmr, maintenance = calculate_metrics(
            age, gender, height, weight, activity)
        db.session.add(FitnessProfile(user_id=current_user.id, age=age, gender=gender, height=height, weight=weight, activity=activity, goal=goal,
                       experience=experience, workout_days=days, equipment=equipment, diet=diet, bmi=bmi, bmr=bmr, maintenance_calories=maintenance))
        db.session.commit()
        flash('Fitness profile saved successfully.', 'success')
        return redirect(url_for('main.dashboard'))
    return render_template('profile.html')


@main_bp.route('/generate', methods=['POST'])
@login_required
def generate():
    p = FitnessProfile.query.filter_by(user_id=current_user.id).order_by(
        FitnessProfile.created_at.desc()).first()
    if not p:
        flash('Please complete your fitness profile first.', 'warning')
        return redirect(url_for('main.profile'))
    data = {'age': p.age, 'gender': p.gender, 'height': p.height, 'weight': p.weight, 'activity': p.activity, 'goal': p.goal, 'experience': p.experience,
            'workout_days': p.workout_days, 'equipment': p.equipment, 'diet': p.diet, 'bmi': p.bmi, 'bmr': p.bmr, 'maintenance_calories': p.maintenance_calories}
    plan = FitnessPlan(user_id=current_user.id,
                       title=f'{p.goal} - AI Plan', content=generate_plan(data))
    db.session.add(plan)
    db.session.commit()
    flash('AI fitness plan generated.', 'success')
    return redirect(url_for('main.plan', plan_id=plan.id))


@main_bp.route('/plan/<int:plan_id>')
@login_required
def plan(plan_id):
    p = FitnessPlan.query.filter_by(
        id=plan_id, user_id=current_user.id).first_or_404()
    return render_template('plan.html', plan=p)


@main_bp.route('/admin')
@login_required
def admin():
    if current_user.role != 'admin':
        flash('Admin access required.', 'danger')
        return redirect(url_for('main.dashboard'))
    return render_template('admin.html', users=User.query.order_by(User.created_at.desc()).all(), profiles=FitnessProfile.query.count(), plans=FitnessPlan.query.count())



@main_bp.route("/plan/<int:plan_id>/ask", methods=["POST"])
@login_required
def ask_plan_ai(plan_id):

    plan = FitnessPlan.query.get_or_404(plan_id)

    # Make sure user can access this plan
    if plan.user_id != current_user.id and current_user.role != "admin":
        return jsonify({
            "success": False,
            "message": "You are not allowed to access this plan."
        }), 403

    data = request.get_json()

    question = (data.get("question") or "").strip()

    if not question:
        return jsonify({
            "success": False,
            "message": "Please enter a question."
        }), 400

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        return jsonify({
            "success": True,
            "answer": (
                "Gemini AI is not configured yet. "
                "Please add GEMINI_API_KEY to your .env file."
            )
        })

    client = genai.Client(api_key=api_key)

    prompt = f"""
You are Fit Buddy AI, a friendly fitness assistant.

The user already has the following personalized fitness plan:

--- FITNESS PLAN ---
{plan.content}
--- END FITNESS PLAN ---

The user is asking:

{question}

Answer the user's question based on their fitness plan.

Rules:

- Give simple and practical answers.
- Keep the answer concise.
- Do not diagnose medical conditions.
- Do not prescribe medication.
- Do not recommend starvation or extreme dieting.
- Do not make guaranteed weight-loss claims.
- If the question is outside the fitness plan, explain it briefly.
- Encourage professional medical advice for injuries or medical conditions.
- Do not repeat the entire fitness plan.
- Answer naturally like an AI fitness assistant.
"""

    try:

        response = client.models.generate_content(
            model=os.getenv(
                "GEMINI_MODEL",
                "gemini-2.5-flash"
            ),
            contents=prompt
        )

        return jsonify({
            "success": True,
            "answer": response.text
        })

    except Exception as e:

        return jsonify({
            "success": False,
            "message": "Unable to get an AI response right now."
        }), 500
