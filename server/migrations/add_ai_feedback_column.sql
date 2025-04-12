-- Ajouter la colonne ai_feedback à la table trades
ALTER TABLE trades
ADD COLUMN IF NOT EXISTS ai_feedback TEXT;

-- Mettre à jour les trades existants avec une valeur par défaut
UPDATE trades
SET ai_feedback = NULL
WHERE ai_feedback IS NULL; 