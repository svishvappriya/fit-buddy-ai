def calculate_metrics(age, gender, height_cm, weight_kg, activity):
    bmi = weight_kg / ((height_cm / 100) ** 2)
    if gender.lower() == 'male':
        bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age + 5
    elif gender.lower() == 'female':
        bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age - 161
    else:
        bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age - 78
    factor = {'Sedentary':1.20,'Lightly Active':1.375,'Moderately Active':1.55,'Very Active':1.725}.get(activity,1.2)
    return round(bmi,1), round(bmr), round(bmr * factor)
