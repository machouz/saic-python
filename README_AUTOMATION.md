# 🌡️ Automatisation Climatisation MG iSMART

Ce guide vous explique comment automatiser le démarrage de la climatisation tous les jours à 15h20 heure israélienne pendant 3 mois, **sans que votre ordinateur soit allumé**.

## 🎯 Objectif
- ⏰ Démarrage automatique à 15h20 (heure israélienne)
- 📅 Pendant 3 mois
- 🌐 Fonctionne sans votre ordinateur
- 🔒 Sécurisé et fiable

## 🚀 Solutions disponibles

### Option 1: GitHub Actions (GRATUIT) ⭐ Recommandé

**Avantages:**
- ✅ Totalement gratuit
- ✅ Aucune maintenance
- ✅ Très simple à configurer
- ✅ Logs accessibles

**Configuration:**

1. **Forkez ce repository** sur votre compte GitHub

2. **Ajoutez vos identifiants** dans les secrets GitHub:
   - Allez dans `Settings` → `Secrets and variables` → `Actions`
   - Ajoutez:
     - `MG_USERNAME`: votre email iSMART
     - `MG_PASSWORD`: votre mot de passe iSMART

3. **Activez les GitHub Actions** dans votre repository

4. **C'est tout!** Le workflow se lancera automatiquement tous les jours à 15h20 heure israélienne

**Surveillance:**
- Consultez l'onglet `Actions` pour voir les exécutions
- Téléchargez les logs si nécessaire

---

### Option 2: VPS/Serveur Cloud (~3-5€/mois)

**Avantages:**
- ✅ Contrôle total
- ✅ Très fiable
- ✅ Peut faire d'autres tâches

**Fournisseurs recommandés:**
- [DigitalOcean](https://digitalocean.com) - 4$/mois
- [Linode](https://linode.com) - 5$/mois  
- [OVH](https://ovh.com) - 3€/mois

**Configuration:**

1. **Créez un VPS** avec Ubuntu 20.04+

2. **Connectez-vous en SSH** et exécutez:
   ```bash
   wget https://raw.githubusercontent.com/VOTRE-USERNAME/saic-python-client-ng/master/deploy/vps-setup.sh
   chmod +x vps-setup.sh
   ./vps-setup.sh
   ```

3. **Suivez les instructions** du script

---

### Option 3: Docker (Pour les experts)

**Configuration:**

1. **Clonez le repository** sur votre serveur

2. **Créez le fichier .env:**
   ```bash
   echo "MG_USERNAME=votre@email.com" > .env
   echo "MG_PASSWORD=votre_mot_de_passe" >> .env
   ```

3. **Lancez avec Docker Compose:**
   ```bash
   cd docker
   docker-compose up -d
   ```

---

### Option 4: Raspberry Pi (Chez vous)

**Avantages:**
- ✅ Une seule fois payé (~50€)
- ✅ Contrôle total
- ✅ Peut faire d'autres tâches

**Configuration:**

1. **Installez Raspberry Pi OS**

2. **Suivez les étapes VPS** (même script)

---

## 🔧 Configuration avancée

### Modifier l'heure
Éditez `climate_scheduler.py`:
```python
TARGET_TIME = "16:30"  # Nouvelle heure
```

### Modifier la température
```python
TEMPERATURE_IDX = 10  # Plus chaud (1-15)
```

### Modifier la durée
```python
DURATION_MONTHS = 6  # 6 mois au lieu de 3
```

## 📊 Surveillance

### GitHub Actions
- Onglet `Actions` de votre repository
- Téléchargement des logs automatique

### VPS/Docker
```bash
# Voir les logs en temps réel
tail -f climate_scheduler.log

# Voir les exécutions passées
ls executed_*.flag

# Tester manuellement
python climate_scheduler.py
```

## 🔒 Sécurité

- ✅ Mots de passe stockés dans des secrets/variables d'environnement
- ✅ Logs ne contiennent pas d'informations sensibles
- ✅ Connexions HTTPS uniquement

## 🆘 Dépannage

### Le script ne s'exécute pas
1. Vérifiez les logs
2. Vérifiez l'heure du serveur: `date`
3. Vérifiez les identifiants

### Erreur de connexion
1. Vérifiez vos identifiants MG iSMART
2. Testez la connexion manuellement
3. Vérifiez que votre véhicule est connecté

### Questions fréquentes

**Q: Que se passe-t-il si mon véhicule n'est pas accessible?**
R: Le script réessaiera automatiquement et logguera l'erreur.

**Q: Puis-je arrêter l'automatisation?**
R: Oui, désactivez le workflow GitHub ou arrêtez le service.

**Q: Ça consomme beaucoup de ressources?**
R: Non, le script s'exécute en quelques secondes par jour.

## 📞 Support

En cas de problème:
1. Consultez les logs
2. Vérifiez la documentation MG iSMART
3. Ouvrez une issue sur GitHub
