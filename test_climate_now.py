#!/usr/bin/env python3
"""
Script de test pour forcer l'exécution de la climatisation maintenant
"""

from __future__ import annotations

import asyncio
import logging
import sys
import os

from saic_ismart_client_ng import SaicApi
from saic_ismart_client_ng.model import SaicApiConfiguration


async def test_climate_now():
    """Test du démarrage de climatisation"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    try:
        print("🔐 Connexion à l'API MG iSMART...")
        
        username = os.getenv('MG_USERNAME')
        password = os.getenv('MG_PASSWORD')
        
        if not username or not password:
            print("❌ ERREUR: Variables d'environnement MG_USERNAME et MG_PASSWORD requises!")
            print("Définissez-les avant d'exécuter le script:")
            print("export MG_USERNAME='votre@email.com'")
            print("export MG_PASSWORD='votre_mot_de_passe'")
            return False
        
        config = SaicApiConfiguration(
            username=username,
            password=password,
        )
        saic_api = SaicApi(config)
        await saic_api.login()
        
        print("✅ Connexion réussie!")
        
        # Récupérer le véhicule
        vehicle_list = await saic_api.vehicle_list()
        if not vehicle_list.vinList:
            print("❌ Aucun véhicule trouvé!")
            return False
        
        vin = vehicle_list.vinList[0].vin
        print(f"🚗 Véhicule: {vin}")
        
        # Démarrer la climatisation
        print("🌡️ Test du démarrage de la climatisation...")
        result = await saic_api.start_ac(vin, temperature_idx=8)
        
        print(f"✅ Commande envoyée!")
        print(f"📊 Résultat: {result}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False


if __name__ == "__main__":
    success = asyncio.run(test_climate_now())
    if not success:
        sys.exit(1)
