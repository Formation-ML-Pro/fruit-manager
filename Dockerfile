# Utiliser une image Python officielle
FROM python:3.12.3

# Créer un dossier de travail
WORKDIR /app

# Copier les dépendances
COPY requirements.txt .

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Copier le reste du code
COPY . .

# Exposer le port de Streamlit
EXPOSE 8501

# Lancer l'application Streamlit
CMD ["python", "-m", "streamlit", "run", "app.py", "--server.address=0.0.0.0", "--server.port=8501"]
