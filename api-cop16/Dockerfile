# Usa la imagen base de Python
FROM python:3.9-slim

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia los archivos de la aplicación al contenedor
COPY . .

# Instala las dependencias del proyecto
RUN pip install --no-cache-dir -r requirements.txt

# Configura variables de entorno
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Expone el puerto en el que se ejecutará la aplicación
EXPOSE 5000

# Instala Gunicorn
RUN pip install gunicorn


# Comando para ejecutar la aplicación con Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
