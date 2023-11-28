from flask import Flask, request, jsonify, send_from_directory
from age_calculator import AgeCalculator
from flask_cors import CORS
from datetime import datetime
import os
import json

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

class AgeCalculator:
    def __init__(self, profiles_filename):
        self.profiles = self.load_profiles(profiles_filename)

    def load_profiles(self, filename):
        with open(filename, 'r') as file:
            profiles = json.load(file)
        return profiles

    def calculate_age(self, name):
        profile = next((p for p in self.profiles if p['name'] == name), None)

        if profile:
            # Check school education
            school_education_end = profile.get('school_education_end')
            if school_education_end:
                age = self.calculate_age_from_education(school_education_end, 18)
                return {'age': age}

            # Check college education
            college_education_end = profile.get('college_education_end')
            if college_education_end:
                age = self.calculate_age_from_education(college_education_end, 22)
                return {'age': age}

            # Check work experience
            work_experience = profile.get('work_experience')
            if work_experience:
                first_job_start = self.find_first_job_start(work_experience)
                if first_job_start:
                    age = self.calculate_age_from_education(first_job_start, 22)
                    return {'age': age}

            # If no education or work information is available, return an error
            return {'error': 'No education or work information available for age calculation'}
        else:
            return {'error': 'Profile not found'}

    def calculate_age_from_education(self, education_end, base_age):
        current_year = datetime.now().year
        age = current_year - education_end + base_age
        return age

    def find_first_job_start(self, work_experience):
        # Assuming work_experience is a list of jobs with start and end years
        first_job = min(work_experience, key=lambda job: job.get('start_year', float('inf')))
        return first_job.get('start_year')

age_calculator = AgeCalculator('cs_profiles.json')  # Assuming you've saved profiles as cs_profiles.json

@app.route('/')
def index():
    # Load and return the content of popup.html
    with open('popup.html', 'r') as file:
        content = file.read()
    return content

@app.route('/profiles', methods=['GET'])
def get_profiles():
    profiles = [{'name': profile['name']} for profile in age_calculator.profiles]
    return jsonify(profiles)

@app.route('/age', methods=['GET'])
def get_age():
    name = request.args.get('name')
    result = age_calculator.calculate_age(name)
    print('Profile Name:', name)
    print('Calculated Age:', result)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
