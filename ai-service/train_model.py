import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import joblib

# 1. Имитация исторических данных продаж б/у техники CHG-MERIDIAN
np.random.seed(42)
n_samples = 2000

categories = ['Laptop', 'Desktop', 'Server']
brands = ['Dell', 'HP', 'Lenovo', 'Apple']
grades = ['Grade A', 'Grade B', 'Grade C']

data = {
    'category': np.random.choice(categories, n_samples),
    'brand': np.random.choice(brands, n_samples),
    'initial_price_eur': np.random.uniform(800, 3500, n_samples),
    'age_months': np.random.randint(6, 60, n_samples),
    'ram_gb': np.random.choice([8, 16, 32, 64], n_samples),
    'storage_gb': np.random.choice([256, 512, 1024, 2048], n_samples),
    'grade': np.random.choice(grades, n_samples),
}

df = pd.DataFrame(data)

# Логика обесценивания
grade_mult = {'Grade A': 1.0, 'Grade B': 0.85, 'Grade C': 0.70}
depreciation = (1 - 0.018) ** df['age_months']
df['residual_value_eur'] = (
    df['initial_price_eur'] * depreciation * 
    df['grade'].map(grade_mult) + 
    df['ram_gb'] * 3 + 
    np.random.normal(0, 40, n_samples)
)
df['residual_value_eur'] = df['residual_value_eur'].clip(lower=50)

# 2. Подготовка пайплайна обучения
X = df.drop(columns=['residual_value_eur'])
y = df['residual_value_eur']

categorical_features = ['category', 'brand', 'grade']
numerical_features = ['initial_price_eur', 'age_months', 'ram_gb', 'storage_gb']

preprocessor = ColumnTransformer(
    transformers=[
        ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features),
        ('num', 'passthrough', numerical_features)
    ]
)

pipeline = Pipeline([
    ('preprocessor', preprocessor),
    ('regressor', RandomForestRegressor(n_estimators=100, random_state=42))
])

# 3. Обучение и сохранение
pipeline.fit(X, y)
joblib.dump(pipeline, 'residual_value_model.pkl')
print("✅ Успешно! Файл 'residual_value_model.pkl' создан.")
