# Documentation du Journal de Trading IA

## Vue d'Ensemble
Documentation complète du projet de Journal de Trading avec intégration Supabase et analyse IA.

## Structure du Projet

```
trademind_ai_journal/
├── server/
│   ├── app.py                 # Serveur Flask principal
│   ├── supabase_client.py     # Client Supabase personnalisé
│   ├── ai_feedback.py         # Module d'analyse IA
│   └── screenshot_handler.py  # Gestionnaire de captures d'écran
├── documentation/
│   ├── app.md                # Documentation du serveur
│   ├── supabase_client.md    # Documentation du client Supabase
│   ├── ai_feedback.md        # Documentation du module IA
│   └── screenshot_handler.md # Documentation du gestionnaire d'images
├── .env                      # Variables d'environnement
└── requirements.txt          # Dépendances Python
```

## Composants Principaux

### 1. Serveur Flask (app.py)
- Gestion des webhooks TradingView
- Endpoints pour trades et structures
- Intégration Supabase

### 2. Client Supabase (supabase_client.py)
- Gestion de la base de données
- Stockage des images
- CRUD operations

### 3. Module IA (ai_feedback.py)
- Analyse des trades
- Feedback sur les structures
- Intégration OpenAI

### 4. Gestionnaire Screenshots (screenshot_handler.py)
- Traitement des images
- Upload vers Supabase Storage
- Gestion des URLs publiques

## Configuration

1. **Variables d'Environnement**
   ```env
   SUPABASE_URL=votre_url_supabase
   SUPABASE_KEY=votre_cle_supabase
   OPENAI_API_KEY=votre_cle_openai
   ```

2. **Installation**
   ```bash
   pip install -r requirements.txt
   ```

3. **Démarrage**
   ```bash
   cd server
   python app.py
   ```

## Webhooks TradingView

### Structure de Marché
```json
{
    "instrument": "ES",
    "structure_type": "BOS",
    "price_level": 4500.25,
    "direction": "BULLISH"
}
```

### Trade
```json
{
    "instrument": "ES",
    "direction": "LONG",
    "entry_price": 4500.25,
    "stop_loss": 4480.50,
    "take_profit": 4550.75
}
```

## Base de Données

### Table 'trades'
- Enregistrement des trades
- Métriques de performance
- Screenshots et notes

### Table 'structures'
- Structures de marché
- Points de référence
- Analyse technique

## Sécurité
- Validation des données
- Gestion sécurisée des clés
- Stockage sécurisé des images

## Maintenance
- Logging détaillé
- Gestion des erreurs
- Backups automatiques 