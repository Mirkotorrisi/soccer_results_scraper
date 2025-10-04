# Usa un'immagine di base Python
FROM python:3.10-slim

# Installa Poetry
RUN pip install poetry

# Configura Poetry per non creare un virtual environment
ENV POETRY_VENV_IN_PROJECT=false \
    POETRY_NO_INTERACTION=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

# Imposta la working directory
WORKDIR /app

# Copia i file di configurazione Poetry
COPY pyproject.toml ./

# Installa le dipendenze (solo production)
RUN poetry install --only=main && rm -rf $POETRY_CACHE_DIR

# Copia il resto del codice
COPY . .

# Esponi la porta 8081
EXPOSE 8081

# Comando per avviare l'applicazione
CMD ["poetry", "run", "python", "run.py"]