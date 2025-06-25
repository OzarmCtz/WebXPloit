FROM python:3.11-slim

WORKDIR /app

# Installer les dépendances système
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*


# Copier et installer les dépendances
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copier le code source
COPY . .

# Créer un utilisateur non-root
RUN useradd -m -u 1001 webxploit && \
    chown -R webxploit:webxploit /app
USER webxploit

# Exposer le port API
EXPOSE 8000

ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Commande par défaut
CMD ["python", "router.py"]