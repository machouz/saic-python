#!/bin/bash

# Démarrer le service cron
service cron start

# Créer le fichier de log
touch /var/log/climate.log

# Afficher les logs en temps réel
echo "🚀 Climate Scheduler démarré - Logs:"
tail -f /var/log/climate.log
