#!/usr/bin/env python3
"""
Script d'automatisation pour démarrer la climatisation quotidiennement
Heure: 15h20 heure israélienne
Durée: 3 mois
"""

from __future__ import annotations

import asyncio
import logging
import sys
from datetime import datetime, timedelta
import pytz
import os
from pathlib import Path

from saic_ismart_client_ng import SaicApi
from saic_ismart_client_ng.model import SaicApiConfiguration


# Configuration
ISRAEL_TZ = pytz.timezone('Asia/Jerusalem')
TARGET_TIME = "15:20"  # Heure de démarrage souhaitée
DURATION_MONTHS = 3    # Durée en mois
TEMPERATURE_IDX = 8    # Température par défaut (peut être ajustée)

# Variables d'environnement pour la sécurité - OBLIGATOIRES
USERNAME = os.getenv('MG_USERNAME')
PASSWORD = os.getenv('MG_PASSWORD')

if not USERNAME or not PASSWORD:
    print("❌ ERREUR: Variables d'environnement MG_USERNAME et MG_PASSWORD requises!")
    print("Définissez-les avant d'exécuter le script:")
    print("export MG_USERNAME='votre@email.com'")
    print("export MG_PASSWORD='votre_mot_de_passe'")
    sys.exit(1)


def setup_logging():
    """Configure le logging avec timestamp"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('climate_scheduler.log'),
            logging.StreamHandler(sys.stdout)
        ]
    )


def is_within_schedule_period() -> bool:
    """Vérifie si nous sommes dans la période de 3 mois"""
    now = datetime.now(ISRAEL_TZ)
    
    # Date de début (aujourd'hui si c'est le premier lancement)
    start_date_file = Path('schedule_start_date.txt')
    
    if not start_date_file.exists():
        # Premier lancement, on enregistre la date de début
        start_date = now.date()
        start_date_file.write_text(start_date.isoformat())
        logging.info(f"🗓️ Début de la programmation: {start_date}")
    else:
        # On lit la date de début existante
        start_date = datetime.fromisoformat(start_date_file.read_text().strip()).date()
    
    # Calcul de la date de fin (3 mois après le début)
    end_date = start_date + timedelta(days=90)  # Approximation de 3 mois
    current_date = now.date()
    
    logging.info(f"📅 Période: {start_date} → {end_date} (aujourd'hui: {current_date})")
    
    if current_date > end_date:
        logging.info("⏰ Période de 3 mois terminée")
        return False
    
    return True


def should_run_today() -> bool:
    """Vérifie si on doit exécuter aujourd'hui"""
    now = datetime.now(ISRAEL_TZ)
    
    # Vérifier si on est dans la période
    if not is_within_schedule_period():
        return False
    
    # Vérifier l'heure
    target_hour, target_minute = map(int, TARGET_TIME.split(':'))
    current_time = now.time()
    target_time = now.replace(hour=target_hour, minute=target_minute, second=0, microsecond=0).time()
    
    # On exécute si l'heure actuelle est >= heure cible et < heure cible + 1h
    end_time = (now.replace(hour=target_hour, minute=target_minute) + timedelta(hours=1)).time()
    
    if target_time <= current_time < end_time:
        # Vérifier qu'on n'a pas déjà exécuté aujourd'hui
        today_file = Path(f'executed_{now.date().isoformat()}.flag')
        if today_file.exists():
            logging.info("✅ Déjà exécuté aujourd'hui")
            return False
        
        return True
    
    logging.info(f"⏰ Pas encore l'heure (actuel: {current_time}, cible: {target_time})")
    return False


async def start_climate_control():
    """Démarre la climatisation"""
    try:
        logging.info("🔐 Connexion à l'API MG iSMART...")
        
        config = SaicApiConfiguration(
            username=USERNAME,
            password=PASSWORD,
        )
        saic_api = SaicApi(config)
        await saic_api.login()
        
        logging.info("✅ Connexion réussie!")
        
        # Récupérer le véhicule
        vehicle_list = await saic_api.vehicle_list()
        if not vehicle_list.vinList:
            logging.error("❌ Aucun véhicule trouvé!")
            return False
        
        vin = vehicle_list.vinList[0].vin
        logging.info(f"🚗 Véhicule: {vin}")
        
        # Démarrer la climatisation
        logging.info(f"🌡️ Démarrage de la climatisation (température: {TEMPERATURE_IDX})...")
        result = await saic_api.start_ac(vin, temperature_idx=TEMPERATURE_IDX)
        
        logging.info(f"✅ Climatisation démarrée! Event ID: {result.eventId}")
        
        # Marquer comme exécuté aujourd'hui
        today = datetime.now(ISRAEL_TZ).date()
        today_file = Path(f'executed_{today.isoformat()}.flag')
        today_file.write_text(f"Executed at {datetime.now(ISRAEL_TZ).isoformat()}")
        
        return True
        
    except Exception as e:
        logging.error(f"❌ Erreur lors du démarrage de la climatisation: {e}")
        return False


async def main():
    """Fonction principale"""
    setup_logging()
    
    now = datetime.now(ISRAEL_TZ)
    logging.info(f"🚀 Démarrage du scheduler climatisation - {now}")
    
    if should_run_today():
        logging.info("🎯 Conditions remplies, démarrage de la climatisation...")
        success = await start_climate_control()
        
        if success:
            logging.info("✅ Mission accomplie!")
        else:
            logging.error("❌ Échec de la mission")
            sys.exit(1)
    else:
        logging.info("⏭️ Pas d'action nécessaire aujourd'hui")
    
    logging.info("🏁 Fin du script")


if __name__ == "__main__":
    asyncio.run(main())
