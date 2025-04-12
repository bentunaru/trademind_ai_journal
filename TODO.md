# ✅ To-Do List – Agent IA Journal de Trading (avec Supabase)

## 🔧 Phase 1 – Setup général

- [x] Créer un projet Supabase
- [x] Créer deux tables dans la base PostgreSQL :
  - `trades`
  - `structures`
- [x] Créer un bucket public `screenshots` dans Supabase Storage
- [x] Récupérer l'URL du projet Supabase + la clé API
- [x] Créer un fichier `.env` avec `SUPABASE_URL` et `SUPABASE_KEY`
- [x] Configurer `.gitignore` pour les fichiers sensibles
- [x] Créer `.env.example` comme template de configuration

## 🧠 Phase 2 – Serveur Flask

- [x] Créer un serveur Flask dans `server/`
- [x] Ajouter une route `/webhook/structure` pour recevoir les BOS/ChoCH
- [x] Ajouter une route `/webhook/trade` pour enregistrer un trade réel
- [x] Ajouter insertion dans Supabase via `supabase-py`
- [x] Ajouter l'upload de screenshots dans Supabase Storage
- [x] Générer un lien public à insérer dans la ligne de trade
- [x] Créer fonction `generate_feedback()` (OpenAI API ou GPT local)

## 🧪 Phase 3 – Interface utilisateur (Streamlit)

- [x] Afficher les trades depuis Supabase
- [x] Ajouter un champ pour uploader une capture d'écran
- [ ] Ajouter un champ texte pour écrire une note personnelle
- [ ] Afficher la note de discipline + feedback IA
- [ ] Ajouter filtres : par date, instrument, direction, etc.

## 🧲 Phase 4 – Webhooks TradingView

- [ ] Créer un message JSON type pour BOS/ChoCH (structure)
- [ ] Créer un message JSON type pour les trades réels
- [ ] Créer les alertes dans TradingView avec ces messages JSON
- [ ] Tester en local avec webhook sur `http://localhost:5001/webhook/...`
- [ ] Ajouter validation des données entrantes
- [ ] Implémenter rate limiting pour les webhooks

## 🌍 Phase 5 – Intégration des news économiques

- [ ] Explorer les options : API Forex Factory, scraping ou API tierce
- [ ] Ajouter récupération des news du jour dans Supabase
- [ ] Afficher les news dans le dashboard Streamlit
- [ ] Intégrer les news dans le feedback IA

## 🔒 Phase 6 – Sécurité et Monitoring

- [x] Configurer la gestion sécurisée des secrets
- [x] Mettre en place le système de variables d'environnement
- [ ] Ajouter logging des actions critiques
- [ ] Implémenter monitoring des erreurs
- [ ] Mettre en place backup automatique des données
- [ ] Ajouter authentification pour les webhooks
