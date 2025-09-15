#!/usr/bin/env python3
"""
Script de contrôle manuel de la climatisation via GitHub Actions
"""

from __future__ import annotations

import asyncio
import logging
import os
import sys
from datetime import datetime

from saic_ismart_client_ng import SaicApi
from saic_ismart_client_ng.model import SaicApiConfiguration


def setup_logging():
    """Configure le logging"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('manual_climate.log'),
            logging.StreamHandler(sys.stdout)
        ]
    )


async def get_vehicle_vin(saic_api: SaicApi) -> str | None:
    """Récupère le VIN du véhicule"""
    try:
        vehicle_list = await saic_api.vehicle_list()
        if not vehicle_list.vinList:
            logging.error("❌ Aucun véhicule trouvé!")
            return None
        
        vin = vehicle_list.vinList[0].vin
        logging.info(f"🚗 Véhicule trouvé: {vin}")
        return vin
    except Exception as e:
        logging.error(f"❌ Erreur lors de la récupération du véhicule: {e}")
        return None


async def execute_climate_action(saic_api: SaicApi, vin: str, action: str, **params) -> bool:
    """Exécute l'action climatisation demandée"""
    try:
        result = None
        
        if action == "start_ac":
            temp = int(params.get('temperature', 8))
            logging.info(f"🌡️ Démarrage de la climatisation (température: {temp})...")
            result = await saic_api.start_ac(vin, temperature_idx=temp)
            
        elif action == "stop_ac":
            logging.info("🌡️ Arrêt de la climatisation...")
            result = await saic_api.stop_ac(vin)
            
        elif action == "start_defrost":
            logging.info("❄️ Démarrage du dégivrage avant...")
            result = await saic_api.start_front_defrost(vin)
            
        elif action == "start_heated_seats":
            left = int(params.get('heated_seats_left', 0))
            right = int(params.get('heated_seats_right', 0))
            logging.info(f"🪑 Contrôle des sièges chauffants (gauche: {left}, droit: {right})...")
            result = await saic_api.control_heated_seats(vin, left_side_level=left, right_side_level=right)
            
        elif action == "rear_window_heat_on":
            logging.info("🪟 Activation du chauffage lunette arrière...")
            result = await saic_api.control_rear_window_heat(vin, enable=True)
            
        elif action == "rear_window_heat_off":
            logging.info("🪟 Désactivation du chauffage lunette arrière...")
            result = await saic_api.control_rear_window_heat(vin, enable=False)
            
        else:
            logging.error(f"❌ Action inconnue: {action}")
            return False
        
        if result:
            logging.info(f"✅ Commande exécutée avec succès!")
            logging.info(f"📊 Résultat: {result}")
            return True
        else:
            logging.error("❌ Aucun résultat retourné")
            return False
            
    except Exception as e:
        logging.error(f"❌ Erreur lors de l'exécution de l'action {action}: {e}")
        return False


async def main():
    """Fonction principale"""
    setup_logging()
    
    # Récupération des paramètres
    action = os.getenv('ACTION', 'start_ac')
    temperature = os.getenv('TEMPERATURE', '8')
    heated_seats_left = os.getenv('HEATED_SEATS_LEFT', '0')
    heated_seats_right = os.getenv('HEATED_SEATS_RIGHT', '0')
    
    # Récupération des identifiants
    username = os.getenv('MG_USERNAME')
    password = os.getenv('MG_PASSWORD')
    
    if not username or not password:
        logging.error("❌ ERREUR: Variables d'environnement MG_USERNAME et MG_PASSWORD requises!")
        sys.exit(1)
    
    logging.info(f"🚀 Contrôle manuel climatisation - {datetime.now()}")
    logging.info(f"🎯 Action demandée: {action}")
    
    try:
        # Connexion à l'API
        logging.info("🔐 Connexion à l'API MG iSMART...")
        config = SaicApiConfiguration(username=username, password=password)
        saic_api = SaicApi(config)
        await saic_api.login()
        logging.info("✅ Connexion réussie!")
        
        # Récupération du véhicule
        vin = await get_vehicle_vin(saic_api)
        if not vin:
            sys.exit(1)
        
        # Exécution de l'action
        params = {
            'temperature': temperature,
            'heated_seats_left': heated_seats_left,
            'heated_seats_right': heated_seats_right,
        }
        
        success = await execute_climate_action(saic_api, vin, action, **params)
        
        if success:
            logging.info("🎉 Mission accomplie!")
        else:
            logging.error("❌ Échec de la mission")
            sys.exit(1)
            
    except Exception as e:
        logging.error(f"❌ Erreur inattendue: {e}")
        sys.exit(1)
    
    logging.info("🏁 Fin du contrôle manuel")


if __name__ == "__main__":
    asyncio.run(main())
