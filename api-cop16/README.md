# Predicción de Supervivencia de la Planta

Este proyecto es una aplicación web que predice la supervivencia de una planta de frijol en función de varias variables ambientales y del suelo. La aplicación utiliza un modelo de aprendizaje automático para hacer las predicciones y también ofrece recomendaciones basadas en GPT-4.

el modelo de regresión de encuentra en https://drive.google.com/file/d/1olX-KrMm_O-yM1fI9Y2pCS2gppHb0NbP/view?usp=sharing

## Estructura del Proyecto

### 1. Backend: Flask API

El backend del proyecto está desarrollado en Flask y expone dos endpoints principales:

- `/predict`: Recibe un JSON con los valores de las variables ambientales y del suelo, y devuelve una predicción de la supervivencia de la planta.
- `/ask`: Permite hacer preguntas adicionales sobre la planta de frijol y obtener respuestas basadas en GPT-4.

#### Archivos principales del backend:

- `app.py`: Contiene la lógica principal del servidor Flask y los endpoints.
- `model.pkl`: Archivo del modelo de aprendizaje automático entrenado.
- `requirements.txt`: Lista de dependencias necesarias para ejecutar el backend.

### 2. Frontend: HTML + JavaScript

El frontend está desarrollado en HTML y JavaScript. Incluye un formulario para ingresar los valores de las variables y muestra los resultados de la predicción.

#### Archivos principales del frontend:

- `index.html`: Contiene el formulario y la lógica de presentación de resultados.
- `style.css`: Define los estilos del formulario y la tabla de resultados (integrado en `index.html`).
- `script.js`: Contiene la lógica para manejar las solicitudes al backend y mostrar los resultados (integrado en `index.html`).

## Requisitos

Para ejecutar este proyecto, necesitarás:

- Python 3.7 o superior
- Flask
- scikit-learn
- OpenAI API (para obtener respuestas de GPT-4)

## Instalación

1. Clona este repositorio en tu máquina local:
    ```bash
    git clone https://github.com/tu_usuario/tu_repositorio.git
    cd tu_repositorio
    ```

2. Crea un entorno virtual e instala las dependencias:
    ```bash
    python3 -m venv env
    source env/bin/activate   # En Windows usa `env\Scripts\activate`
    pip install -r requirements.txt
    ```

3. Coloca tu archivo `model.pkl` en el directorio principal del proyecto.

4. Configura tus credenciales de OpenAI en un archivo `.env`:
    ```bash
    OPENAI_API_KEY=tu_clave_api_de_openai
    ```

## Ejecución

1. Inicia el servidor Flask:
    ```bash
    flask run
    ```

2. Abre `index.html` en tu navegador web.

## Uso

1. Ingresa los valores de las variables ambientales y del suelo en el formulario.
2. Los resultados de la predicción se mostrarán automáticamente debajo del formulario.
3. Para hacer preguntas adicionales sobre la planta de frijol, usa el campo de entrada de texto que aparece después de la predicción.

## Contribuciones

Las contribuciones son bienvenidas. Si deseas contribuir, por favor sigue estos pasos:

1. Haz un fork del proyecto.
2. Crea una nueva rama (`git checkout -b nueva-rama`).
3. Realiza tus cambios y haz commit (`git commit -am 'Agrega nueva funcionalidad'`).
4. Sube tus cambios a tu rama (`git push origin nueva-rama`).
5. Abre un Pull Request.

## Licencia

Este proyecto está licenciado bajo la [MIT License](LICENSE).

## Contacto

Para cualquier pregunta o sugerencia, puedes contactarme a través de [tu_email@dominio.com](mailto:cgioidalgo@gmail.com).

---

¡Gracias por utilizar la Predicción de Supervivencia de la Planta! 

by GHS
