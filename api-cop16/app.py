from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import openai
import os
from PyPDF2 import PdfReader
import docx
from dotenv import load_dotenv
import joblib
import numpy as np
import os
print(os.getenv('OPENAI_API_KEY'))
load_dotenv()

app = Flask(__name__)
CORS(app)

# Cargar los modelos guardados
try:
    regressor = joblib.load('random_forest_regressor.pkl')
    classifier = joblib.load('random_forest_classifier.pkl')
except Exception as e:
    print(f"Error al cargar los modelos: {e}")
    exit(1)

# Carga la clave de API de OpenAI desde una variable de entorno
openai.api_key = os.getenv('OPENAI_API_KEY')

if not openai.api_key:
    print("Error: No se pudo cargar la API Key. Verifica el archivo .env")

# Ruta de los archivos para entrenar el chatbot
TRAINING_FILES_PATH = 'training_files'
if not os.path.exists(TRAINING_FILES_PATH):
    os.makedirs(TRAINING_FILES_PATH)

# Variable para mantener el contenido de los archivos en memoria
file_contents = {}

# Definir los rangos para el estado de las variables
def get_variable_status(value, variable):
    ranges = {
        'temperatura': {'Malo': (float('-inf'), 15), 'Estable': (15, 20), 'Óptimo': (20, 30), 'Malo': (31, float('inf'))},
        'humedad_suelo': {'Malo': (float('-inf'), 50), 'Estable': (50, 60), 'Óptimo': (60, 70), 'Malo': (71, float('inf'))},
        'humedad_ambiente': {'Malo': (float('-inf'), 50), 'Estable': (50, 60), 'Óptimo': (60, 70), 'Malo': (71, float('inf'))},
        'luz': {'Malo': (float('-inf'), 2000), 'Estable': (2000, 4000), 'Óptimo': (4000, 8000), 'Malo': (8001, float('inf'))},
        'ph_suelo': {'Malo': (float('-inf'), 5.5), 'Estable': (5.5, 6.0), 'Óptimo': (6.0, 7.0), 'Malo': (7.0, float('inf'))},
        'co2': {'Malo': (float('-inf'), 300), 'Estable': (300, 600), 'Óptimo': (600, 999), 'Malo': (1000, float('inf'))},
        'nitrogeno': {'Malo': (float('-inf'), 10), 'Estable': (10, 20), 'Óptimo': (20, 30), 'Malo': (31, float('inf'))},
        'fosforo': {'Malo': (float('-inf'), 29), 'Estable': (30, 60), 'Óptimo': (61, 70), 'Malo': (71, float('inf'))},
        'potasio': {'Malo': (float('-inf'), 150), 'Estable': (150, 200), 'Óptimo': (200, 300), 'Malo': (301, float('inf'))}
    }

    for condition, rng in ranges[variable].items():
        if rng[0] <= value < rng[1]:
            return f"Dentro del rango {condition}"
    
    return "Dentro del rango Malo"

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        print(f"Datos recibidos: {data}")

        # Validar los datos de entrada
        required_fields = ['temperatura', 'humedad_suelo', 'humedad_ambiente', 'luz', 'ph_suelo', 'co2', 'nitrogeno', 'fosforo', 'potasio']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing fields in input data'}), 400

        # Convertir los datos en formato adecuado para los modelos
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

        print(f"Datos para predicción: {input_data}")

        # Realizar las predicciones
        predicted_survival_percentage = regressor.predict(input_data)[0]
        predicted_life_status = classifier.predict(input_data)[0]

        # Mapear el resultado de clasificación a las etiquetas
        status_labels = {0: 'Muere', 1: 'Estable', 2: 'Óptimo'}
        life_status = status_labels[predicted_life_status]

        # Obtener el estado de las variables
        variable_status = {var: get_variable_status(value, var) for var, value in data.items()}

        # Formatear resultados
        formatted_result = {
            'Porcentaje de Supervivencia Predicho': f"{predicted_survival_percentage:.2f}%",
            'Estado de Vida Predicho': life_status,
            'Estado de Variables': {k: v for k, v in variable_status.items()}
        }

        # Crear el prompt para el segundo modelo
        prompt = f"Según estos valores 'Estado de Variables:\n"
        for var, status in variable_status.items():
            prompt += f"{var}: {status}\n"
        prompt += "'Eres un experto y debes dar recomendaciones de cómo podría ayudar a que la planta de frijol sea óptima. Hazlo en maximo 200 tokens de gpt y escribe en  primera persona"

        # Obtener la respuesta del segundo modelo (GPT-4)
        gpt_response = get_gpt4_response(prompt, file_contents)

        return jsonify({'prediction_result': formatted_result, 'gpt_response': gpt_response})

    except Exception as e:
        print(f"Error en la predicción: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/')
def serve_index():
    return render_template('index.html')

def get_gpt4_response(user_input, file_contents):
    try:
        # Construir el contexto de la conversación a partir del contenido de los archivos
        context = "\n\n".join(file_contents.values())
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "system", "content": f"Contexto de los archivos:\n{context}"},
                {"role": "user", "content": user_input}
            ],
            max_tokens=200  # Ajusta el número de tokens según tus necesidades
        )
        return response.choices[0].message['content'].strip()
    except Exception as e:
        return f"Error al obtener respuesta: {str(e)}"

@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    question = data.get('question')
    if not question:
        return jsonify({'error': 'No question provided'}), 400

    # Llama a tu modelo GPT-4 para obtener una respuesta
    answer = get_gpt4_response(question, file_contents)
    return jsonify({'answer': answer})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
