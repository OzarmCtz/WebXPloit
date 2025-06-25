FROM python:3.11-slim

# Définir le répertoire de travail
WORKDIR /app

# Installer les dépendances système nécessaires
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
    && rm -rf /var/lib/apt/lists/*


# Copier le fichier requirements.txt
COPY requirements.txt .

# Installer les dépendances Python
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copier tout le code source
COPY . .

# 🔁 Ajouter ici le script d’attente AVANT de changer d’utilisateur
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Créer un utilisateur non-root pour la sécurité
RUN useradd -m -u 1001 webxploit && \
    chown -R webxploit:webxploit /app
USER webxploit

# Exposer le port (à ajuster selon votre configuration)
EXPOSE 5000

# Variables d'environnement
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Commande par défaut
CMD ["python", "run.py"]
