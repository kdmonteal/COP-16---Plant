
'''
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.metrics import mean_squared_error, accuracy_score, classification_report, confusion_matrix
import joblib

import pandas as pd
df = pd.read_csv('frijol.csv') 
df

# Definir las variables y la variable objetivo
X = df[['temperatura', 'humedad_suelo', 'humedad_ambiente', 'luz', 'ph_suelo', 'co2', 'nitrogeno', 'fosforo', 'potasio']]
y_regressor = df['porcentaje_supervivencia']
y_classifier = df['vive']

# Dividir los datos en conjunto de entrenamiento y prueba
X_train, X_test, y_train_regressor, y_test_regressor, y_train_classifier, y_test_classifier = train_test_split(
    X, y_regressor, y_classifier, test_size=0.3, random_state=42
)

# Entrenar el modelo RandomForestRegressor
regressor = RandomForestRegressor(n_estimators=100, random_state=42)
regressor.fit(X_train, y_train_regressor)

# Entrenar el modelo RandomForestClassifier para clasificación multiclase
classifier = RandomForestClassifier(n_estimators=100, random_state=42)
classifier.fit(X_train, y_train_classifier)

# Evaluar los modelos
y_pred_regressor = regressor.predict(X_test)
y_pred_classifier = classifier.predict(X_test)

# Métricas de evaluación para el regresor
mse = mean_squared_error(y_test_regressor, y_pred_regressor)
print(f"Regressor Mean Squared Error: {mse:.2f}")

# Métricas de evaluación para el clasificador
accuracy = accuracy_score(y_test_classifier, y_pred_classifier)
conf_matrix = confusion_matrix(y_test_classifier, y_pred_classifier)
class_report = classification_report(y_test_classifier, y_pred_classifier, target_names=['Muere', 'Estable', 'Óptimo'])

print(f"\nClassifier Accuracy: {accuracy:.2f}")
print("Confusion Matrix:")
print(conf_matrix)
print("\nClassification Report:")
print(class_report)

# Guardar los modelos
joblib.dump(regressor, 'random_forest_regressor.pkl')
joblib.dump(classifier, 'random_forest_classifier.pkl')

print("\nModelos guardados como 'random_forest_regressor.pkl' y 'random_forest_classifier.pkl'.")

# Función para determinar el estado de cada variable
def get_variable_status(value, variable):
    ranges = {
        'temperatura': {'Malo': (10, 35), 'Estable': (15, 20), 'Óptimo': (20, 30)},
        'humedad_suelo': {'Malo': (0, 50), 'Estable': (50, 70), 'Óptimo': (60, 70)},
        'humedad_ambiente': {'Malo': (0, 50), 'Estable': (50, 70), 'Óptimo': (50, 70)},
        'luz': {'Malo': (0, 2000), 'Estable': (2000, 4000), 'Óptimo': (4000, 8000)},
        'ph_suelo': {'Malo': (4.0, 5.5), 'Estable': (5.5, 6.0), 'Óptimo': (6.0, 7.0)},
        'co2': {'Malo': (0, 300), 'Estable': (300, 600), 'Óptimo': (800, 1000)},
        'nitrogeno': {'Malo': (0, 5), 'Estable': (10, 20), 'Óptimo': (20, 30)},
        'potasio': {'Malo': (0, 50), 'Estable': (150, 250), 'Óptimo': (200, 300)},
        'calcio': {'Malo': (0, 10), 'Estable': (10, 20), 'Óptimo': (20, 30)}
    }

    status = []
    for condition, rng in ranges[variable].items():
        if rng[0] <= value <= rng[1]:
            return f"Dentro del rango {condition}"
    return "Fuera del rango"

# Evaluar un nuevo registro
new_record = {
    'temperatura': 19.77,
    'humedad_suelo': 57.46,
    'humedad_ambiente': 60.15,
    'luz': 3669.81,
    'ph_suelo': 5.85,
    'co2': 388.31,
    'nitrogeno': 10.91,
    'potasio': 30.59,
    'calcio': 152.24
}

print("\nEstado del nuevo registro:")
for var, val in new_record.items():
    print(f"{var}: {val} - {get_variable_status(val, var)}")

# Realizar predicciones
predicted_survival_percentage = regressor.predict([list(new_record.values())])[0]
predicted_life_status = classifier.predict([list(new_record.values())])[0]

# Mapear el resultado de clasificación a las etiquetas
status_labels = {0: 'Muere', 1: 'Estable', 2: 'Óptimo'}

print("\nPredicciones para el nuevo registro:")
print(f"Porcentaje de Supervivencia Predicho: {predicted_survival_percentage:.2f}%")
print(f"Estado de Vida Predicho: {status_labels[predicted_life_status]}")
'''