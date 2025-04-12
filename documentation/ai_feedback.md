# Module de Feedback IA (ai_feedback.py)

## Description
Module qui utilise l'API OpenAI pour générer des analyses et des feedbacks sur les trades et les structures de marché.

## Fonctions Principales

### 1. `generate_trade_feedback(trade_data: Dict[str, Any]) -> str`

#### Description
Génère un feedback détaillé sur un trade en utilisant GPT-4.

#### Paramètres
- `trade_data` : Dictionnaire contenant les informations du trade
  ```python
  {
      "instrument": str,
      "direction": str,
      "entry_price": float,
      "stop_loss": float,
      "take_profit": float,
      "notes": str,
      "risk_reward": float
  }
  ```

#### Retour
- Analyse détaillée du trade avec recommandations

#### Aspects Analysés
- Gestion du risque
- Ratio risque/récompense
- Points d'entrée et de sortie
- Respect du plan de trading
- Psychologie du trader

### 2. `analyze_market_structure(structure_data: Dict[str, Any]) -> str`

#### Description
Analyse une structure de marché (BOS/ChoCH) et fournit des insights.

#### Paramètres
- `structure_data` : Dictionnaire contenant les informations de la structure
  ```python
  {
      "instrument": str,
      "structure_type": str,
      "price_level": float,
      "direction": str,
      "notes": str
  }
  ```

#### Retour
- Analyse détaillée de la structure de marché

#### Aspects Analysés
- Validité de la structure
- Contexte de marché
- Probabilité de réussite
- Points de surveillance

## Configuration

### Variables d'Environnement
- `OPENAI_API_KEY` : Clé API pour OpenAI

### Modèles Utilisés
- GPT-4 pour l'analyse détaillée
- Température et paramètres optimisés pour l'analyse financière

## Prompts

### Trade Analysis Prompt
- Évaluation de la qualité du trade
- Analyse du R:R ratio
- Suggestions d'amélioration
- Aspects psychologiques

### Structure Analysis Prompt
- Validation de la structure
- Contexte technique
- Niveaux importants
- Probabilités et risques

## Dépendances
- openai
- python-dotenv
- logging
- typing

## Gestion des Erreurs
- Retry sur erreurs API
- Logging des erreurs
- Réponses par défaut en cas d'échec
- Timeouts configurables 