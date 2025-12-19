# src/churn_gym/infrastructure/ml/features
# Liste des variables numériques (en excluant la target 'churn')
NUMERICAL_FEATURES = [
    'age', 
    'avg_workout_duration_min', 
    'avg_calories_burned', 
    'total_weight_lifted_kg', 
    'visits_per_month', 
    'tenure_days', 
    'days_since_last_visit', 
    'calories_per_minute', 
    'weight_per_visit', 
    'attendance_rate', 
    'recency_frequency_score', 
    'weight_intensity'
]

# Liste des variables catégorielles (en excluant 'member_id' qui est un identifiant)
CATEGORICAL_FEATURES = [
    'gender', 
    'membership_type', 
    'favorite_exercise', 
    'visit_recency_bucket', 
    'tenure_bucket'
]

# Colonnes à exclure lors de l'entraînement
ID_COLUMN = 'member_id'
TARGET_COLUMN = 'churn'

# Combinaison pour l'ordre complet des colonnes
FEATURES_ALL = NUMERICAL_FEATURES + CATEGORICAL_FEATURES