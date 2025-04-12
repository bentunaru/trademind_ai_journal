# Flask Server Application (app.py)

## Description
Serveur Flask qui gère les webhooks pour le journal de trading. Il reçoit les signaux de TradingView et les enregistre dans une base de données Supabase.

## Endpoints

### 1. `/webhook/structure` (POST)
Endpoint pour recevoir les signaux de structure de marché (BOS/ChoCH).

**Format JSON attendu :**
```json
{
    "instrument": "ES",
    "structure_type": "BOS" | "CHoCH",
    "price_level": 4500.25,
    "direction": "BULLISH" | "BEARISH",
    "screenshot": "optional_base64_image",
    "notes": "optional_notes"
}
```

**Validations :**
- Champs requis : instrument, structure_type, price_level, direction
- structure_type doit être "BOS" ou "ChoCH"
- direction doit être "BULLISH" ou "BEARISH"

### 2. `/webhook/trade` (POST)
Endpoint pour recevoir les signaux d'exécution de trades.

**Format JSON attendu :**
```json
{
    "instrument": "ES",
    "direction": "LONG" | "SHORT",
    "entry_price": 4500.25,
    "stop_loss": 4480.50,
    "take_profit": 4550.75,
    "screenshot": "optional_base64_image",
    "notes": "optional_notes",
    "risk_reward": 2.5
}
```

**Validations :**
- Champs requis : instrument, direction, entry_price, stop_loss, take_profit
- direction doit être "LONG" ou "SHORT"

### 3. `/test-supabase` (GET)
Endpoint de test pour vérifier la connexion à Supabase.

### 4. `/test-tables` (GET)
Endpoint de test pour vérifier la création des tables.

## Fonctionnalités

1. **Gestion des Screenshots**
   - Conversion et sauvegarde des images en base64
   - Stockage dans Supabase Storage
   - Génération d'URLs publiques

2. **Analyse IA**
   - Génération de feedback pour les trades
   - Analyse des structures de marché
   - TODO: Implémentation de la mise à jour avec l'analyse IA

3. **Logging**
   - Logging détaillé des opérations
   - Format : timestamp, nom, niveau, message

## Configuration

Le serveur utilise les variables d'environnement suivantes :
- `SUPABASE_URL`
- `SUPABASE_KEY`

## Démarrage
```bash
python app.py
```
Le serveur démarre sur le port 5001 en mode debug. 