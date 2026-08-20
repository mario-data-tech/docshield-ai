FROM python:3.12-slim

WORKDIR /app

# Instalar dependencias del sistema necesarias
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Instalar el código y dependencias
COPY . .
RUN pip install --no-cache-dir .[nlp]
RUN python -m spacy download en_core_web_sm

# Punto de entrada para el CLI
ENTRYPOINT ["docshield"]
