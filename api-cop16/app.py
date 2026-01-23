from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import openai
import os
from PyPDF2 import PdfReader
import docx
from dotenv import load_dotenv
import joblib
import numpy as np
load_dotenv()

app = Flask(__name__)
CORS(app)

# Load trained models
try:
    regressor = joblib.load('random_forest_regressor.pkl')
    classifier = joblib.load('random_forest_classifier.pkl')
except Exception as e:
    print(f"Error loading models: {e}")
    exit(1)

# Load the OpenAI API key from environment variables
openai.api_key = os.getenv('OPENAI_API_KEY')

if not openai.api_key:
    print("Error: Failed to load OpenAI API key. Check the .env file.")

# Ensure the training-files directory exists
TRAINING_FILES_PATH = 'training_files'
if not os.path.exists(TRAINING_FILES_PATH):
    os.makedirs(TRAINING_FILES_PATH)

# Cache training file contents in memory
file_contents = {}

VARIABLE_RANGES = {
    'temperatura': [
        ('Poor', float('-inf'), 15),
        ('Stable', 15, 20),
        ('Optimal', 20, 30),
        ('Poor', 30, float('inf'))
    ],
    'humedad_suelo': [
        ('Poor', float('-inf'), 50),
        ('Stable', 50, 60),
        ('Optimal', 60, 70),
        ('Poor', 70, float('inf'))
    ],
    'humedad_ambiente': [
        ('Poor', float('-inf'), 50),
        ('Stable', 50, 60),
        ('Optimal', 60, 70),
        ('Poor', 70, float('inf'))
    ],
    'luz': [
        ('Poor', float('-inf'), 2000),
        ('Stable', 2000, 4000),
        ('Optimal', 4000, 8000),
        ('Poor', 8000, float('inf'))
    ],
    'ph_suelo': [
        ('Poor', float('-inf'), 5.5),
        ('Stable', 5.5, 6.0),
        ('Optimal', 6.0, 7.0),
        ('Poor', 7.0, float('inf'))
    ],
    'co2': [
        ('Poor', float('-inf'), 300),
        ('Stable', 300, 600),
        ('Optimal', 600, 1000),
        ('Poor', 1000, float('inf'))
    ],
    'nitrogeno': [
        ('Poor', float('-inf'), 10),
        ('Stable', 10, 20),
        ('Optimal', 20, 30),
        ('Poor', 30, float('inf'))
    ],
    'fosforo': [
        ('Poor', float('-inf'), 30),
        ('Stable', 30, 60),
        ('Optimal', 60, 70),
        ('Poor', 70, float('inf'))
    ],
    'potasio': [
        ('Poor', float('-inf'), 150),
        ('Stable', 150, 200),
        ('Optimal', 200, 300),
        ('Poor', 300, float('inf'))
    ]
}

VARIABLE_LABELS = {
    'temperatura': 'Temperature',
    'humedad_suelo': 'Soil Moisture',
    'humedad_ambiente': 'Ambient Humidity',
    'luz': 'Light',
    'ph_suelo': 'Soil pH',
    'co2': 'CO2',
    'nitrogeno': 'Nitrogen',
    'fosforo': 'Phosphorus',
    'potasio': 'Potassium'
}


def get_variable_status(value, variable):
    for label, lower, upper in VARIABLE_RANGES[variable]:
        if lower <= value < upper:
            return f"Within the {label.lower()} range"
    return "Within the poor range"

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        print(f"Received data: {data}")

        # Validate required input fields
        required_fields = ['temperatura', 'humedad_suelo', 'humedad_ambiente', 'luz', 'ph_suelo', 'co2', 'nitrogeno', 'fosforo', 'potasio']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing fields in input data'}), 400

        # Prepare the input array for the models
        input_data = np.array([
            data['temperatura'],
            data['humedad_suelo'],
            data['humedad_ambiente'],
            data['luz'],
            data['ph_suelo'],
            data['co2'],
            data['nitrogeno'],
            data['fosforo'],
            data['potasio']
        ]).reshape(1, -1)

        print(f"Prediction payload: {input_data}")

        # Run predictions
        predicted_survival_percentage = regressor.predict(input_data)[0]
        predicted_life_status = classifier.predict(input_data)[0]

        # Translate classifier output into human-friendly labels
        status_labels = {0: 'Dead', 1: 'Stable', 2: 'Optimal'}
        life_status = status_labels[predicted_life_status]

        # Build per-variable status report
        variable_status = {
            VARIABLE_LABELS.get(var, var): get_variable_status(value, var)
            for var, value in data.items()
        }

        # Compose payload for the frontend
        formatted_result = {
            'Predicted Survival Percentage': f"{predicted_survival_percentage:.2f}%",
            'Predicted Life Status': life_status,
            'Variable Statuses': {k: v for k, v in variable_status.items()}
        }

        # Build the prompt for the recommendation model
        prompt = "You are an agronomy expert focused on common bean crops. Using the following variable statuses, provide concise first-person recommendations (maximum 200 tokens) that move the plant toward optimal health.\n\n"
        for var, status in variable_status.items():
            prompt += f"{var}: {status}\n"

        # Query GPT for agronomic recommendations
        gpt_response = get_gpt4_response(prompt, file_contents)

        return jsonify({'prediction_result': formatted_result, 'gpt_response': gpt_response})

    except Exception as e:
        print(f"Prediction error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/')
def serve_index():
    return render_template('index.html')

def get_gpt4_response(user_input, file_contents):
    try:
        # Build conversation context from uploaded files
        context = "\n\n".join(file_contents.values())
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that responds in English."},
                {"role": "system", "content": f"File context:\n{context}"},
                {"role": "user", "content": user_input}
            ],
            max_tokens=200  # Adjust if a longer answer is required
        )
        return response.choices[0].message['content'].strip()
    except Exception as e:
        return f"Error retrieving response: {str(e)}"

@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    question = data.get('question')
    if not question:
        return jsonify({'error': 'No question provided'}), 400

    # Let GPT generate a response for additional questions
    answer = get_gpt4_response(question, file_contents)
    return jsonify({'answer': answer})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
