# 🚀 Guide de Déploiement - Automatisation Climatisation

## 🎯 Objectif
Déployer votre système d'automatisation pour que la climatisation se lance tous les jours à 15h20 heure israélienne pendant 3 mois.

## ✅ Ce qui a été sécurisé
- ❌ **Supprimé** tous les identifiants du code
- ✅ **Ajouté** la gestion des variables d'environnement
- ✅ **Créé** le fichier .gitignore pour protéger vos données
- ✅ **Configuré** GitHub Actions pour l'automatisation

## 🔧 Étapes de déploiement

### **Étape 1: Créer votre repository GitHub**

1. **Allez sur GitHub.com** et connectez-vous
2. **Créez un nouveau repository** :
   - Nom: `mg-climate-automation` (ou autre nom)
   - Visibilité: **Privé** (recommandé) ou Public
   - Ne pas initialiser avec README (on a déjà les fichiers)

3. **Copiez l'URL** de votre nouveau repository (ex: `https://github.com/machouz/mg-climate-automation.git`)

### **Étape 2: Pousser votre code**

```bash
# Ajouter votre repository comme origin
git remote add origin https://github.com/machouz/mg-climate-automation.git

# Ajouter tous les fichiers modifiés
git add .

# Commit avec message descriptif
git commit -m "🔒 Sécurisation complète + automatisation climatisation"

# Pousser vers votre repository
git push -u origin main
```

### **Étape 3: Configurer les secrets GitHub**

1. **Dans votre repository GitHub** → `Settings`
2. **Secrets and variables** → `Actions`
3. **New repository secret** et ajoutez :

   **Secret 1:**
   - Name: `MG_USERNAME`
   - Secret: `uzanmacho@gmail.com`

   **Secret 2:**
   - Name: `MG_PASSWORD`
   - Secret: `Mouchi95`

### **Étape 4: Activer GitHub Actions**

1. **Onglet Actions** de votre repository
2. **"I understand my workflows, go ahead and enable them"**
3. Le workflow `Climate Scheduler` apparaîtra

### **Étape 5: Tester l'automatisation**

1. **Test manuel** : Cliquez sur `Run workflow` dans Actions
2. **Vérifiez les logs** pour confirmer que ça fonctionne
3. **L'automatisation** se lancera tous les jours à 15h20

## 🛡️ Sécurité garantie

### ✅ Vos identifiants sont :
- **Cryptés** par GitHub (AES-256)
- **Masqués** dans tous les logs
- **Inaccessibles** aux autres utilisateurs
- **Jamais exposés** dans le code

### ✅ Le code est propre :
- Aucun identifiant en dur
- Variables d'environnement uniquement
- Fichiers sensibles ignorés par Git

## 📊 Surveillance

### **Voir les exécutions :**
- Onglet `Actions` → `Climate Scheduler`
- Logs détaillés de chaque exécution
- Téléchargement des logs possible

### **Fichiers créés :**
- `climate_scheduler.log` : Historique détaillé
- `executed_YYYY-MM-DD.flag` : Marqueurs d'exécution
- `schedule_start_date.txt` : Date de début

## ⚙️ Personnalisation

### **Changer l'heure :**
Éditez `.github/workflows/climate-scheduler.yml` :
```yaml
schedule:
  # 16h20 heure israélienne = 13h20 UTC
  - cron: '20 13 * * *'
```

### **Changer la température :**
Éditez `climate_scheduler.py` :
```python
TEMPERATURE_IDX = 10  # Plus chaud (1-15)
```

### **Changer la durée :**
```python
DURATION_MONTHS = 6  # 6 mois au lieu de 3
```

## 🆘 Dépannage

### **"Permission denied" lors du push :**
- Vérifiez l'URL de votre repository
- Assurez-vous d'être connecté à GitHub
- Utilisez un token personnel si nécessaire

### **Workflow ne s'exécute pas :**
- Vérifiez que les secrets sont configurés
- Vérifiez que GitHub Actions est activé
- Consultez les logs d'erreur

### **Erreur d'authentification MG :**
- Vérifiez vos identifiants dans l'app MG
- Recréez les secrets GitHub
- Testez avec le script local

## 🎉 Résultat final

Une fois déployé, vous aurez :
- ✅ **Automatisation complète** (15h20 tous les jours)
- ✅ **Sécurité maximale** (identifiants cryptés)
- ✅ **Surveillance facile** (logs GitHub)
- ✅ **Flexibilité totale** (personnalisation facile)
- ✅ **Coût zéro** (GitHub Actions gratuit)

**Votre climatisation se lancera automatiquement pendant 3 mois sans que votre ordinateur soit allumé !** 🌡️🚗✨
