BMI_THRESHOLD = 25.0
UNDERWEIGHT_THRESHOLD = 18.5
GENERAL_ASSESSMENT = "general"
OVERWEIGHT_ASSESSMENT = "overweight"

def calculate_bmi(height_cm, weight_kg):
    if height_cm <=0:
        raise ValueError('Height must be greater than 0')

    if weight_kg <=0:
        raise ValueError('Weight must be greater than 0')


    height_m = height_cm / 100
    bmi = weight_kg / (height_m ** 2)
    return round(bmi, 1)


def determine_assessment(bmi):
    if bmi>=BMI_THRESHOLD:
        return OVERWEIGHT_ASSESSMENT

    return GENERAL_ASSESSMENT

def bmi_category(bmi):
    if bmi < UNDERWEIGHT_THRESHOLD:
        return "Underweight"
    elif bmi < BMI_THRESHOLD:
        return "Normal"
    else:
        return "Overweight"