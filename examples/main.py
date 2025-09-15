from __future__ import annotations

import asyncio
import logging
import os
import sys
from datetime import time

from saic_ismart_client_ng import SaicApi
from saic_ismart_client_ng.model import SaicApiConfiguration
from saic_ismart_client_ng.api.vehicle.alarm.schema import AlarmType
from saic_ismart_client_ng.api.vehicle.locks.schema import VehicleLockId
from saic_ismart_client_ng.api.vehicle.windows.schema import VehicleWindowId
from saic_ismart_client_ng.api.vehicle_charging.schema import TargetBatteryCode, ScheduledChargingMode


def print_menu():
    """Affiche le menu principal"""
    print("\n" + "="*50)
    print("🚗 MENU CONTRÔLE VÉHICULE MG iSMART")
    print("="*50)
    print("📊 STATUT:")
    print("  1. Statut du véhicule")
    print("  2. Statut de charge")
    print("  3. Données de gestion de charge")
    print()
    print("🌡️  CLIMATISATION:")
    print("  4. Démarrer la climatisation")
    print("  5. Arrêter la climatisation")
    print("  6. Démarrer le dégivrage avant")
    print("  7. Contrôler les sièges chauffants")
    print("  8. Chauffage lunette arrière ON/OFF")
    print()
    print("🔒 VERROUILLAGE:")
    print("  9. Verrouiller le véhicule")
    print("  10. Déverrouiller le véhicule")
    print("  11. Ouvrir le coffre")
    print()
    print("🚨 ALARMES:")
    print("  12. Voir les alarmes actives")
    print("  13. Configurer les alarmes")
    print()
    print("🪟 FENÊTRES:")
    print("  14. Contrôler le toit ouvrant")
    print("  15. Fermer la fenêtre conducteur")
    print()
    print("🔋 CHARGE:")
    print("  16. Démarrer/Arrêter la charge")
    print("  17. Contrôler le verrouillage du port de charge")
    print("  18. Définir le niveau de charge cible")
    print("  19. Programmer la charge")
    print("  20. Contrôler le chauffage batterie")
    print()
    print("  0. Mode automatique (boucle)")
    print("  q. Quitter")
    print("="*50)


async def get_vehicle_info(saic_api: SaicApi):
    """Récupère les informations du véhicule"""
    vehicle_list = await saic_api.vehicle_list()
    if not vehicle_list.vinList:
        print("❌ Aucun véhicule trouvé!")
        return None
    
    car = vehicle_list.vinList[0]
    vin = car.vin
    print(f"🚗 Véhicule sélectionné: {vin}")
    return vin


async def handle_vehicle_status(saic_api: SaicApi, vin: str):
    """Affiche le statut du véhicule"""
    try:
        print("📊 Récupération du statut du véhicule...")
        vehicle_status = await saic_api.get_vehicle_status(vin)
        print(f"🔋 Tension batterie: {vehicle_status.basicVehicleStatus.batteryVoltage}V")
        print(f"🚗 Kilométrage: {vehicle_status.basicVehicleStatus.mileage}km")
        print(f"🔒 Véhicule verrouillé: {'Oui' if vehicle_status.basicVehicleStatus.lockStatus else 'Non'}")
    except Exception as e:
        print(f"❌ Erreur lors de la récupération du statut: {e}")


async def handle_charging_status(saic_api: SaicApi, vin: str):
    """Affiche le statut de charge"""
    try:
        print("🔋 Récupération du statut de charge...")
        charging_status = await saic_api.get_vehicle_charging_status(vin)
        print(f"🔋 Niveau de batterie: {charging_status.chrgMgmtData.bmsPackSOCDsp}%")
        print(f"⚡ Puissance de charge: {charging_status.chrgMgmtData.chrgngRmnngTime}kW")
        print(f"🔌 Statut de charge: {charging_status.chrgMgmtData.chargingType}")
    except Exception as e:
        print(f"❌ Erreur lors de la récupération du statut de charge: {e}")


async def handle_charging_management(saic_api: SaicApi, vin: str):
    """Affiche les données de gestion de charge"""
    try:
        print("📊 Récupération des données de gestion de charge...")
        mgmt_data = await saic_api.get_vehicle_charging_management_data(vin)
        print(f"⚡ Puissance en temps réel: {mgmt_data.rvsChargeStatus.realtimePower}kW")
        print(f"🔋 SOC de la batterie: {mgmt_data.rvsChargeStatus.bmsPackSOCDsp}%")
        print(f"🌡️ Température batterie: {mgmt_data.rvsChargeStatus.bmsPackCrnt}°C")
    except Exception as e:
        print(f"❌ Erreur lors de la récupération des données: {e}")


async def handle_climate_control(saic_api: SaicApi, vin: str, action: str):
    """Contrôle la climatisation"""
    try:
        if action == "start_ac":
            print("🌡️ Démarrage de la climatisation...")
            temp = int(input("Température (1-15, défaut 8): ") or "8")
            result = await saic_api.start_ac(vin, temperature_idx=temp)
        elif action == "stop_ac":
            print("🌡️ Arrêt de la climatisation...")
            result = await saic_api.stop_ac(vin)
        elif action == "defrost":
            print("❄️ Démarrage du dégivrage avant...")
            result = await saic_api.start_front_defrost(vin)
        elif action == "heated_seats":
            print("🪑 Contrôle des sièges chauffants...")
            left = int(input("Niveau siège gauche (0-3): ") or "0")
            right = int(input("Niveau siège droit (0-3): ") or "0")
            result = await saic_api.control_heated_seats(vin, left_side_level=left, right_side_level=right)
        elif action == "rear_window":
            enable = input("Activer le chauffage lunette arrière? (o/n): ").lower() == 'o'
            print(f"🪟 {'Activation' if enable else 'Désactivation'} du chauffage lunette arrière...")
            result = await saic_api.control_rear_window_heat(vin, enable=enable)
        
        print(f"✅ Commande envoyée avec succès! Event ID: {result.eventId}")
    except Exception as e:
        print(f"❌ Erreur lors du contrôle climatisation: {e}")


async def handle_locks_control(saic_api: SaicApi, vin: str, action: str):
    """Contrôle les verrous"""
    try:
        if action == "lock":
            print("🔒 Verrouillage du véhicule...")
            result = await saic_api.lock_vehicle(vin)
        elif action == "unlock":
            print("🔓 Déverrouillage du véhicule...")
            result = await saic_api.unlock_vehicle(vin)
        elif action == "tailgate":
            print("🚗 Ouverture du coffre...")
            result = await saic_api.open_tailgate(vin)
        
        print(f"✅ Commande envoyée avec succès! Event ID: {result.eventId}")
    except Exception as e:
        print(f"❌ Erreur lors du contrôle des verrous: {e}")


async def handle_alarm_control(saic_api: SaicApi, vin: str, action: str):
    """Contrôle les alarmes"""
    try:
        if action == "get":
            print("🚨 Récupération des alarmes actives...")
            alarms = await saic_api.get_alarm_switch(vin)
            print("Alarmes configurées:")
            for alarm in alarms.alarmSwitchList:
                print(f"  - Type {alarm.alarmType}: {'Activé' if alarm.alarmSwitch else 'Désactivé'}")
        elif action == "set":
            print("🚨 Configuration des alarmes...")
            print("Types d'alarmes disponibles:")
            for alarm_type in AlarmType:
                print(f"  {alarm_type.value}: {alarm_type.name}")
            
            alarm_types = []
            while True:
                choice = input("Entrez un type d'alarme (ou 'done' pour terminer): ")
                if choice.lower() == 'done':
                    break
                try:
                    alarm_types.append(AlarmType(int(choice)))
                except ValueError:
                    print("Type d'alarme invalide!")
            
            if alarm_types:
                await saic_api.set_alarm_switches(alarm_types, vin)
                print("✅ Alarmes configurées avec succès!")
    except Exception as e:
        print(f"❌ Erreur lors du contrôle des alarmes: {e}")


async def handle_windows_control(saic_api: SaicApi, vin: str, action: str):
    """Contrôle les fenêtres"""
    try:
        if action == "sunroof":
            should_open = input("Ouvrir le toit ouvrant? (o/n): ").lower() == 'o'
            print(f"🪟 {'Ouverture' if should_open else 'Fermeture'} du toit ouvrant...")
            result = await saic_api.control_sunroof(vin, should_open=should_open)
        elif action == "driver_window":
            print("🪟 Fermeture de la fenêtre conducteur...")
            result = await saic_api.close_driver_window(vin)
        
        print(f"✅ Commande envoyée avec succès! Event ID: {result.eventId}")
    except Exception as e:
        print(f"❌ Erreur lors du contrôle des fenêtres: {e}")


async def handle_charging_control(saic_api: SaicApi, vin: str, action: str):
    """Contrôle la charge"""
    try:
        if action == "control":
            stop = input("Arrêter la charge? (o/n): ").lower() == 'o'
            print(f"🔋 {'Arrêt' if stop else 'Démarrage'} de la charge...")
            result = await saic_api.control_charging(vin, stop_charging=stop)
        elif action == "port_lock":
            unlock = input("Déverrouiller le port de charge? (o/n): ").lower() == 'o'
            print(f"🔌 {'Déverrouillage' if unlock else 'Verrouillage'} du port de charge...")
            result = await saic_api.control_charging_port_lock(vin, unlock=unlock)
        elif action == "target_soc":
            print("🎯 Définition du niveau de charge cible...")
            print("Niveaux disponibles: 40%, 50%, 60%, 70%, 80%, 90%, 100%")
            soc = int(input("Niveau souhaité (40-100): ") or "80")
            target_map = {40: TargetBatteryCode.C_40, 50: TargetBatteryCode.C_50, 
                         60: TargetBatteryCode.C_60, 70: TargetBatteryCode.C_70,
                         80: TargetBatteryCode.C_80, 90: TargetBatteryCode.C_90, 
                         100: TargetBatteryCode.C_100}
            target = target_map.get(soc, TargetBatteryCode.C_80)
            result = await saic_api.set_target_battery_soc(vin, target)
        elif action == "schedule":
            print("⏰ Programmation de la charge...")
            start_hour = int(input("Heure de début (0-23): ") or "22")
            start_min = int(input("Minute de début (0-59): ") or "0")
            end_hour = int(input("Heure de fin (0-23): ") or "6")
            end_min = int(input("Minute de fin (0-59): ") or "0")
            
            start_time = time(start_hour, start_min)
            end_time = time(end_hour, end_min)
            result = await saic_api.set_schedule_charging(vin, start_time=start_time, 
                                                        end_time=end_time, 
                                                        mode=ScheduledChargingMode.ENABLE)
        elif action == "battery_heat":
            enable = input("Activer le chauffage batterie? (o/n): ").lower() == 'o'
            print(f"🌡️ {'Activation' if enable else 'Désactivation'} du chauffage batterie...")
            result = await saic_api.control_battery_heating(vin, enable=enable)
        
        print(f"✅ Commande envoyée avec succès!")
    except Exception as e:
        print(f"❌ Erreur lors du contrôle de charge: {e}")


async def interactive_mode(saic_api: SaicApi):
    """Mode interactif avec menu"""
    vin = await get_vehicle_info(saic_api)
    if not vin:
        return
    
    while True:
        print_menu()
        choice = input("\n👉 Votre choix: ").strip()
        
        if choice == 'q':
            print("👋 Au revoir!")
            break
        elif choice == '0':
            print("🔄 Passage en mode automatique...")
            break
        elif choice == '1':
            await handle_vehicle_status(saic_api, vin)
        elif choice == '2':
            await handle_charging_status(saic_api, vin)
        elif choice == '3':
            await handle_charging_management(saic_api, vin)
        elif choice == '4':
            await handle_climate_control(saic_api, vin, "start_ac")
        elif choice == '5':
            await handle_climate_control(saic_api, vin, "stop_ac")
        elif choice == '6':
            await handle_climate_control(saic_api, vin, "defrost")
        elif choice == '7':
            await handle_climate_control(saic_api, vin, "heated_seats")
        elif choice == '8':
            await handle_climate_control(saic_api, vin, "rear_window")
        elif choice == '9':
            await handle_locks_control(saic_api, vin, "lock")
        elif choice == '10':
            await handle_locks_control(saic_api, vin, "unlock")
        elif choice == '11':
            await handle_locks_control(saic_api, vin, "tailgate")
        elif choice == '12':
            await handle_alarm_control(saic_api, vin, "get")
        elif choice == '13':
            await handle_alarm_control(saic_api, vin, "set")
        elif choice == '14':
            await handle_windows_control(saic_api, vin, "sunroof")
        elif choice == '15':
            await handle_windows_control(saic_api, vin, "driver_window")
        elif choice == '16':
            await handle_charging_control(saic_api, vin, "control")
        elif choice == '17':
            await handle_charging_control(saic_api, vin, "port_lock")
        elif choice == '18':
            await handle_charging_control(saic_api, vin, "target_soc")
        elif choice == '19':
            await handle_charging_control(saic_api, vin, "schedule")
        elif choice == '20':
            await handle_charging_control(saic_api, vin, "battery_heat")
        else:
            print("❌ Choix invalide!")
        
        input("\n📱 Appuyez sur Entrée pour continuer...")
    
    return vin


async def automatic_mode(saic_api: SaicApi, vin: str):
    """Mode automatique (boucle originale)"""
    print("🔄 Mode automatique activé - Ctrl+C pour arrêter")
    while True:
        logging.info("Auth token expires at %s", saic_api.token_expiration)
        vehicle_list_rest = await saic_api.vehicle_list()
        cars = vehicle_list_rest.vinList
        for car in cars:
            vin_num = car.vin
            try:
                vehicle_status = await saic_api.get_vehicle_status(vin_num)
                logging.info("Battery voltage is %d", vehicle_status.basicVehicleStatus.batteryVoltage)
                charging_status = await saic_api.get_vehicle_charging_management_data(vin_num)
                logging.info("Current power is %d", charging_status.rvsChargeStatus.realtimePower)
            except Exception as e:
                logging.error("Error getting vehicle data: %s", e)
            logging.info("My VIN is %s", vin_num)
        await asyncio.sleep(10)


async def main() -> None:
    # Récupération sécurisée des identifiants depuis les variables d'environnement
    username = os.getenv('MG_USERNAME')
    password = os.getenv('MG_PASSWORD')
    
    if not username or not password:
        print("❌ ERREUR: Variables d'environnement manquantes!")
        print("Définissez MG_USERNAME et MG_PASSWORD")
        print("Exemple:")
        print("export MG_USERNAME='votre@email.com'")
        print("export MG_PASSWORD='votre_mot_de_passe'")
        sys.exit(1)
    
    config = SaicApiConfiguration(
        username=username,
        password=password,
    )
    saic_api = SaicApi(config)
    
    print("🔐 Connexion à l'API MG iSMART...")
    await saic_api.login()
    print("✅ Connexion réussie!")
    
    # Mode interactif
    vin = await interactive_mode(saic_api)
    
    # Si l'utilisateur choisit le mode automatique
    if vin:
        await automatic_mode(saic_api, vin)


if __name__ == "__main__":
    logging.basicConfig(
        stream=sys.stdout,
        format="%(levelname)s [%(asctime)s] %(name)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        level=logging.INFO,
    )

    asyncio.run(main())