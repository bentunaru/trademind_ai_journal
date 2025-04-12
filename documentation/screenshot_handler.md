# Gestionnaire de Screenshots (screenshot_handler.py)

## Description
Module qui gère le traitement et le stockage des captures d'écran pour les trades et les structures de marché.

## Fonctions

### `save_base64_screenshot(base64_string: str) -> str`

#### Description
Convertit une image en base64 en fichier et l'upload vers Supabase Storage.

#### Paramètres
- `base64_string` : Image encodée en base64

#### Retour
- URL publique de l'image stockée dans Supabase

#### Processus
1. Décode la chaîne base64
2. Génère un nom de fichier unique avec timestamp
3. Sauvegarde temporairement l'image
4. Upload vers Supabase Storage
5. Supprime le fichier temporaire
6. Retourne l'URL publique

## Gestion des Erreurs
- Validation du format base64
- Gestion des erreurs d'écriture fichier
- Gestion des erreurs d'upload
- Nettoyage des fichiers temporaires

## Dépendances
- base64
- os
- datetime
- tempfile
- logging

## Utilisation
```python
# Exemple d'utilisation
base64_image = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgA..."
try:
    public_url = save_base64_screenshot(base64_image)
    print(f"Image uploadée : {public_url}")
except Exception as e:
    print(f"Erreur lors de l'upload : {str(e)}")
```

## Sécurité
- Validation des types de fichiers
- Nettoyage automatique des fichiers temporaires
- Utilisation de noms de fichiers uniques
- Stockage sécurisé dans Supabase 