FROM python:3.11-slim

WORKDIR /app

# Installer les dépendances système
RUN apt-get update && apt-get install -y \
    cron \
    && rm -rf /var/lib/apt/lists/*

# Copier les fichiers
COPY requirements.txt .
COPY climate_scheduler.py .
COPY src/ ./src/

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir -e .

# Créer le script cron
RUN echo "20 12 * * * cd /app && python climate_scheduler.py >> /var/log/climate.log 2>&1" > /etc/cron.d/climate-scheduler
RUN chmod 0644 /etc/cron.d/climate-scheduler
RUN crontab /etc/cron.d/climate-scheduler

# Script de démarrage
COPY docker/start.sh /start.sh
RUN chmod +x /start.sh

CMD ["/start.sh"]
