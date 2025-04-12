# 📈 TradeMind AI Journal

Journal de trading intelligent avec analyse IA et intégration TradingView pour le trading de futures (ES/NQ).

## 🌟 Fonctionnalités

- 📊 **Capture des Trades**
  - Webhooks TradingView pour capture automatique
  - Support des screenshots
  - Calcul automatique du ratio R:R

- 🎯 **Analyse des Structures**
  - Détection BOS (Break of Structure)
  - Détection CHoCH (Change of Character)
  - Validation automatique des niveaux

- 🤖 **Analyse IA**
  - Feedback GPT-4 sur chaque trade
  - Analyse des structures de marché
  - Suggestions d'amélioration

- 🗄️ **Stockage Cloud**
  - Base de données Supabase
  - Stockage sécurisé des images
  - Backup automatique

## 🛠️ Technologies

- **Backend**: Flask (Python)
- **Base de données**: Supabase (PostgreSQL)
- **IA**: OpenAI GPT-4
- **Frontend**: Streamlit (à venir)
- **Trading**: TradingView Webhooks

## 📋 Prérequis

- Python 3.8+
- Compte Supabase
- Compte OpenAI
- Compte TradingView (Pro pour les webhooks)

## ⚙️ Installation

1. **Cloner le repository**
   ```bash
   git clone https://github.com/votre-username/trademind_ai_journal.git
   cd trademind_ai_journal
   ```

2. **Créer l'environnement virtuel**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Unix
   # ou
   .\venv\Scripts\activate  # Windows
   ```

3. **Installer les dépendances**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configuration Supabase**
   - Créer un projet sur [Supabase](https://app.supabase.com)
   - Créer les tables `trades` et `structures`
   - Créer un bucket `screenshots`

5. **Configuration des variables d'environnement**
   ```bash
   cp .env.example .env
   ```
   Remplir les variables dans `.env`:
   ```
   SUPABASE_URL=votre_url
   SUPABASE_KEY=votre_key
   OPENAI_API_KEY=votre_key
   ```

## 🚀 Démarrage

1. **Lancer le serveur**
   ```bash
   cd server
   python app.py
   ```
   Le serveur démarre sur `http://localhost:5001`

2. **Configuration TradingView**
   - Créer une alerte sur TradingView
   - Configurer le webhook vers `http://votre-serveur/webhook/trade`
   - Format JSON pour les trades:
     ```json
     {
         "instrument": "ES",
         "direction": "LONG",
         "entry_price": 4500.25,
         "stop_loss": 4480.50,
         "take_profit": 4550.75,
         "notes": "Description du trade"
     }
     ```

## 📝 Structure des Données

### Table `trades`
- `id`: UUID (Primary Key)
- `instrument`: TEXT
- `direction`: TEXT (LONG/SHORT)
- `entry_price`: DECIMAL
- `stop_loss`: DECIMAL
- `take_profit`: DECIMAL
- `screenshot_url`: TEXT
- `notes`: TEXT
- `risk_reward`: DECIMAL
- `created_at`: TIMESTAMPTZ
- `updated_at`: TIMESTAMPTZ

### Table `structures`
- `id`: UUID (Primary Key)
- `instrument`: TEXT
- `structure_type`: TEXT (BOS/CHoCH)
- `price_level`: DECIMAL
- `direction`: TEXT (BULLISH/BEARISH)
- `screenshot_url`: TEXT
- `notes`: TEXT
- `created_at`: TIMESTAMPTZ
- `updated_at`: TIMESTAMPTZ

## 📡 API Endpoints

### POST `/webhook/trade`
Enregistre un nouveau trade avec analyse IA optionnelle.

### POST `/webhook/structure`
Enregistre une nouvelle structure de marché avec analyse IA optionnelle.

### GET `/test-supabase`
Vérifie la connexion à Supabase.

## 🔒 Sécurité

- Validation des données entrantes
- Sanitization des entrées utilisateur
- Stockage sécurisé des clés API
- Gestion des erreurs robuste

## 🔄 Workflow de Trading

1. **Analyse de Structure**
   - Identifier BOS/CHoCH
   - Envoyer via webhook
   - Recevoir analyse IA

2. **Exécution de Trade**
   - Entrer les détails du trade
   - Capturer screenshot
   - Envoyer via webhook
   - Recevoir feedback IA

3. **Review et Amélioration**
   - Analyser feedback IA
   - Ajuster la stratégie
   - Suivre les métriques

## 📊 Prochaines Étapes

- [ ] Interface Streamlit
- [ ] Intégration des news économiques
- [ ] Statistiques avancées
- [ ] Backtesting automatisé
- [ ] Export de rapports

## 🤝 Contribution

Les contributions sont les bienvenues ! Voir [CONTRIBUTING.md](CONTRIBUTING.md) pour les détails.

## 📄 Licence

Ce projet est sous licence MIT - voir [LICENSE.md](LICENSE.md) pour les détails.

## 👥 Auteurs

- **Benjamin** - *Développement Initial* - [GitHub](https://github.com/votre-username)
