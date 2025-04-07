
import numpy as np
import pandas as pd # type: ignore
from sklearn.ensemble import RandomForestClassifier # type: ignore
from datetime import datetime, timedelta


class MaternalHealthRecommender:
    def __init__(self):
        # This would normally be trained on a dataset
        self.nutrition_model = RandomForestClassifier()
        self.exercise_model = RandomForestClassifier()

        # Pre-defined recommendations by pregnancy stage and risk factors
        self.nutrition_recommendations = {
            'first_trimester': {
                'normal': [
                    "Focus on folate-rich foods like leafy greens and fortified cereals",
                    "Stay hydrated with at least 8-10 glasses of water daily",
                    "Small, frequent meals can help manage morning sickness"
                ],
                'diabetes': [
                    "Monitor carbohydrate intake carefully",
                    "Choose complex carbohydrates over simple sugars",
                    "Regular protein with each meal helps stabilize blood sugar"
                ],
                'hypertension': [
                    "Limit sodium intake to less than 2,300mg daily",
                    "Include potassium-rich foods like bananas and sweet potatoes",
                    "Avoid caffeine and processed foods"
                ]
            },
            'second_trimester': {
                'normal': [
                    "Increase calcium intake with dairy or fortified alternatives",
                    "Add an extra 300 calories daily from nutrient-dense foods",
                    "Iron-rich foods like lean meats and beans help prevent anemia"
                ],
                'diabetes': [
                    "Continue monitoring carbohydrates closely",
                    "Increase protein intake to 75-100g daily",
                    "Include healthy fats from sources like avocados and nuts"
                ],
                'hypertension': [
                    "Maintain your low-sodium eating pattern",
                    "Increase calcium-rich foods to support blood pressure regulation",
                    "Focus on magnesium-rich foods like nuts, seeds, and whole grains"
                ]
            },
            'third_trimester': {
                'normal': [
                    "Focus on omega-3 fatty acids for baby's brain development",
                    "Increase protein intake to support baby's growth",
                    "Small, frequent meals help manage heartburn and indigestion"
                ],
                'diabetes': [
                    "Maintain consistent meal timing to stabilize blood sugar",
                    "Be vigilant about carbohydrate portions as insulin resistance increases",
                    "Ensure adequate protein with each meal and snack"
                ],
                'hypertension': [
                    "Continue with low-sodium foods and potassium-rich options",
                    "Stay well-hydrated with water rather than sugary drinks",
                    "Consider adding more beets and leafy greens to support blood pressure"
                ]
            }
        }

        self.exercise_recommendations = {
            'first_trimester': {
                'normal': [
                    "Aim for 30 minutes of moderate activity most days",
                    "Walking and swimming are excellent low-impact options",
                    "Focus on maintaining rather than increasing fitness"
                ],
                'diabetes': [
                    "Regular exercise helps control blood sugar - aim for 30 minutes daily",
                    "Walking after meals can help regulate blood glucose",
                    "Stay hydrated during exercise"
                ],
                'hypertension': [
                    "Gentle exercise like walking is recommended",
                    "Avoid high-intensity workouts",
                    "Monitor your blood pressure before and after exercise"
                ]
            },
            'second_trimester': {
                'normal': [
                    "Continue with regular moderate exercise",
                    "Consider prenatal yoga or swimming",
                    "Add pelvic floor exercises to your routine"
                ],
                'diabetes': [
                    "Maintain regular physical activity",
                    "Swimming is excellent for managing blood sugar without strain",
                    "Monitor blood glucose before and after exercise"
                ],
                'hypertension': [
                    "Water exercises are ideal for reducing strain",
                    "Aim for 20-30 minutes of gentle activity daily",
                    "Avoid exercises that require lying flat on your back"
                ]
            },
            'third_trimester': {
                'normal': [
                    "Continue gentle exercise like walking and swimming",
                    "Practice pelvic tilts to ease back pain",
                    "Focus on stretching and maintaining mobility"
                ],
                'diabetes': [
                    "Continue with gentle exercise as tolerated",
                    "Walking remains beneficial for blood sugar control",
                    "Consider seated exercises if mobility becomes limited"
                ],
                'hypertension': [
                    "Gentle walking is still beneficial",
                    "Listen to your body and rest when needed",
                    "Swimming or water exercises can help reduce swelling"
                ]
            }
        }

    def get_trimester(self, pregnancy_week):
        if pregnancy_week is None:
            return 'first_trimester'  # Default if no pregnancy week is available
        if pregnancy_week <= 13:
            return 'first_trimester'
        elif pregnancy_week <= 26:
            return 'second_trimester'
        else:
            return 'third_trimester'

    def get_risk_category(self, patient):
        # Simple risk categorization - would be more complex in real app
        if patient.has_diabetes:
            return 'diabetes'
        elif patient.has_hypertension:
            return 'hypertension'
        else:
            return 'normal'

    def get_bmi_category(self, height, weight):
        if not height or not weight:
            return 'unknown'
        bmi = weight / ((height / 100) ** 2)
        if bmi < 18.5:
            return 'underweight'
        elif bmi < 25:
            return 'normal'
        elif bmi < 30:
            return 'overweight'
        else:
            return 'obese'

    def calculate_weight_gain_recommendation(self, pre_pregnancy_bmi, current_week):
        if pre_pregnancy_bmi is None or current_week is None:
            return 0, 0, 'unknown'

        # Recommended weight gain ranges by BMI category for entire pregnancy
        weight_ranges = {
            'underweight': (12.5, 18),  # in kg
            'normal': (11.5, 16),
            'overweight': (7, 11.5),
            'obese': (5, 9)
        }

        # Determine BMI category
        if pre_pregnancy_bmi < 18.5:
            bmi_category = 'underweight'
        elif pre_pregnancy_bmi < 25:
            bmi_category = 'normal'
        elif pre_pregnancy_bmi < 30:
            bmi_category = 'overweight'
        else:
            bmi_category = 'obese'

        lower_range, upper_range = weight_ranges[bmi_category]

        # Calculate expected weight gain for current week (assuming linear progression)
        # 40 weeks is full term
        lower_expected = (lower_range / 40) * current_week
        upper_expected = (upper_range / 40) * current_week

        return lower_expected, upper_expected, bmi_category

    def get_personalized_recommendations(self, patient, nutrition_logs=None):
        """
        Generate personalized recommendations based on patient and logs
        """
        # Handle potentially missing data
        if not patient.height or not patient.pre_pregnancy_weight or not patient.current_weight:
            return {
                "nutrition": [
                    "Please complete your profile with height, pre-pregnancy weight, and current weight to receive personalized recommendations."],
                "exercise": ["Basic exercise recommendations will be available once your profile is complete."],
                "weight_guidance": {
                    "status": "incomplete_data"
                }
            }

        trimester = self.get_trimester(patient.pregnancy_week)
        risk_category = self.get_risk_category(patient)

        # Calculate BMI and weight gain recommendations
        pre_pregnancy_bmi = patient.pre_pregnancy_weight / ((patient.height / 100) ** 2)
        current_bmi = patient.current_weight / ((patient.height / 100) ** 2)

        weight_lower, weight_upper, bmi_category = self.calculate_weight_gain_recommendation(
            pre_pregnancy_bmi, patient.pregnancy_week
        )

        actual_weight_gain = patient.current_weight - patient.pre_pregnancy_weight

        # Get base recommendations from our pre-defined sets
        try:
            nutrition_recs = self.nutrition_recommendations[trimester][risk_category][:]  # Copy the list
        except KeyError:
            # Fallback to normal recommendations if specific category not found
            nutrition_recs = self.nutrition_recommendations[trimester]['normal'][:]

        try:
            exercise_recs = self.exercise_recommendations[trimester][risk_category][:]
        except KeyError:
            exercise_recs = self.exercise_recommendations[trimester]['normal'][:]

        # Add personalized weight guidance
        if actual_weight_gain < weight_lower:
            nutrition_recs.append(f"Consider adding an additional 200 calories daily from nutritious sources")
        elif actual_weight_gain > weight_upper:
            nutrition_recs.append(f"Focus on nutrient-dense foods rather than calorie-dense options")

        # If we have nutrition logs, analyze for deficiencies
        if nutrition_logs and len(nutrition_logs) > 0:
            # Calculate averages
            avg_protein = sum(log.protein for log in nutrition_logs) / len(nutrition_logs)
            avg_iron = sum(log.iron for log in nutrition_logs) / len(nutrition_logs)
            avg_calcium = sum(log.calcium for log in nutrition_logs) / len(nutrition_logs)
            avg_folate = sum(log.folate for log in nutrition_logs) / len(nutrition_logs)

            # Add recommendations based on nutritional analysis
            if avg_protein < 60:  # Example threshold, would be based on medical guidelines
                nutrition_recs.append("Increase protein intake with lean meats, beans, or plant-based alternatives")

            if avg_iron < 27:  # Pregnancy RDA
                nutrition_recs.append(
                    "Your iron intake appears low. Consider iron-rich foods like spinach and lean red meat")

            if avg_calcium < 1000:
                nutrition_recs.append("Boost calcium intake with dairy products or fortified plant milks")

            if avg_folate < 600:  # Pregnancy RDA in mcg
                nutrition_recs.append("Increase folate intake with leafy greens, citrus fruits, and beans")

        return {
            "nutrition": nutrition_recs,
            "exercise": exercise_recs,
            "weight_guidance": {
                "pre_pregnancy_bmi": round(pre_pregnancy_bmi, 1),
                "bmi_category": bmi_category,
                "current_week": patient.pregnancy_week,
                "recommended_weight_gain_range": [round(weight_lower, 1), round(weight_upper, 1)],
                "actual_weight_gain": round(actual_weight_gain, 1),
                "status": "on_track" if weight_lower <= actual_weight_gain <= weight_upper else
                "below" if actual_weight_gain < weight_lower else "above"
            }
        }