# Usa un'immagine di base Python
FROM python:3.9-slim

# Imposta la working directory
WORKDIR /app

# Copia i file necessari
COPY . .

# Installa le dipendenze
RUN pip install --no-cache-dir -r requirements.txt

# Esponi la porta 8080
EXPOSE 8081

# Comando per avviare l'applicazione
CMD ["python", "run.py"]