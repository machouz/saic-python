#!/bin/bash

# Script de déploiement pour VPS
# Usage: ./vps-setup.sh

set -e

echo "🚀 Configuration du Climate Scheduler sur VPS..."

# Mise à jour du système
sudo apt update && sudo apt upgrade -y

# Installation de Python et dépendances
sudo apt install -y python3 python3-pip python3-venv git cron

# Clonage du projet (remplacez par votre repo)
if [ ! -d "saic-python-client-ng" ]; then
    git clone https://github.com/VOTRE-USERNAME/saic-python-client-ng.git
fi

cd saic-python-client-ng

# Création de l'environnement virtuel
python3 -m venv venv
source venv/bin/activate

# Installation des dépendances
pip install -r requirements.txt
pip install -e .

# Configuration des variables d'environnement
echo "📝 Configuration des identifiants..."
read -p "Email MG iSMART: " MG_USERNAME
read -s -p "Mot de passe MG iSMART: " MG_PASSWORD
echo

# Création du fichier .env
cat > .env << EOF
MG_USERNAME=$MG_USERNAME
MG_PASSWORD=$MG_PASSWORD
EOF

# Configuration du cron job
SCRIPT_PATH=$(pwd)/climate_scheduler.py
VENV_PATH=$(pwd)/venv

# Création du script wrapper
cat > run_climate.sh << EOF
#!/bin/bash
cd $(pwd)
source $VENV_PATH/bin/activate
export \$(cat .env | xargs)
python $SCRIPT_PATH
EOF

chmod +x run_climate.sh

# Ajout du cron job (15:20 heure israélienne = 12:20 UTC)
CRON_JOB="20 12 * * * $(pwd)/run_climate.sh >> $(pwd)/climate.log 2>&1"

# Vérifier si le cron job existe déjà
if ! crontab -l 2>/dev/null | grep -q "run_climate.sh"; then
    (crontab -l 2>/dev/null; echo "$CRON_JOB") | crontab -
    echo "✅ Cron job ajouté: $CRON_JOB"
else
    echo "ℹ️ Cron job déjà existant"
fi

# Test du script
echo "🧪 Test du script..."
source venv/bin/activate
export $(cat .env | xargs)
python climate_scheduler.py

echo "✅ Configuration terminée!"
echo "📋 Commandes utiles:"
echo "  - Voir les logs: tail -f $(pwd)/climate.log"
echo "  - Voir les cron jobs: crontab -l"
echo "  - Tester manuellement: $(pwd)/run_climate.sh"
