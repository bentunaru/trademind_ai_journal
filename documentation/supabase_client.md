# Client Supabase (supabase_client.py)

## Description
Client personnalisé pour interagir avec la base de données Supabase. Gère l'insertion des trades et des structures de marché.

## Classes

### SupabaseClient

#### Méthodes

1. **`__init__(self)`**
   - Initialise le client Supabase avec les variables d'environnement
   - Utilise `SUPABASE_URL` et `SUPABASE_KEY`

2. **`insert_trade(self, ...)`**
   ```python
   def insert_trade(
       self,
       instrument: str,
       direction: str,
       entry_price: float,
       stop_loss: float,
       take_profit: float,
       screenshot_url: Optional[str] = None,
       notes: Optional[str] = None,
       risk_reward: Optional[float] = None
   ) -> Dict[str, Any]
   ```
   - Insère un nouveau trade dans la table 'trades'
   - Retourne les données du trade inséré

3. **`insert_structure(self, ...)`**
   ```python
   def insert_structure(
       self,
       instrument: str,
       structure_type: str,  # "BOS" ou "CHoCH"
       price_level: float,
       direction: str,  # "BULLISH" ou "BEARISH"
       screenshot_url: Optional[str] = None,
       notes: Optional[str] = None
   ) -> Dict[str, Any]
   ```
   - Insère une nouvelle structure dans la table 'structures'
   - Retourne les données de la structure insérée

4. **`upload_screenshot(self, ...)`**
   ```python
   def upload_screenshot(
       self,
       file: BinaryIO,
       filename: str
   ) -> str
   ```
   - Upload une capture d'écran dans le bucket 'screenshots'
   - Retourne l'URL publique de l'image

## Structure des Tables

### Table 'trades'
- id (UUID, Primary Key)
- instrument (TEXT)
- direction (TEXT)
- entry_price (DECIMAL)
- stop_loss (DECIMAL)
- take_profit (DECIMAL)
- screenshot_url (TEXT, Optional)
- notes (TEXT, Optional)
- risk_reward (DECIMAL, Optional)
- created_at (TIMESTAMPTZ)
- updated_at (TIMESTAMPTZ)

### Table 'structures'
- id (UUID, Primary Key)
- instrument (TEXT)
- structure_type (TEXT)
- price_level (DECIMAL)
- direction (TEXT)
- screenshot_url (TEXT, Optional)
- notes (TEXT, Optional)
- created_at (TIMESTAMPTZ)
- updated_at (TIMESTAMPTZ)

## Gestion des Erreurs
- Logging détaillé des erreurs
- Propagation des exceptions pour gestion au niveau supérieur
- Messages d'erreur descriptifs

## Dépendances
- supabase-py
- python-dotenv
- typing
- logging 