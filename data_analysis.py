import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Saves charts to files instead of displaying
import matplotlib.pyplot as plt
import seaborn as sns
import os
from datetime import datetime

# Setup
os.makedirs('charts', exist_ok=True)
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print(f"\n{'='*55}")
print(f"  Nutritional Insights Analysis — {timestamp}")
print(f"{'='*55}\n")

# Load & Clean Data
df = pd.read_csv('All_Diets.csv')
print(f"Dataset loaded: {df.shape[0]} rows, {df.shape[1]} columns")
print(f"Missing values before cleaning:\n{df.isnull().sum()}\n")

# Fill missing numeric values with column mean
numeric_cols = ['Protein(g)', 'Carbs(g)', 'Fat(g)']
df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
print(f"Missing values after cleaning:\n{df.isnull().sum()}\n")

# Avg macronutrients per diet type
avg_macros = df.groupby('Diet_type')[['Protein(g)', 'Carbs(g)', 'Fat(g)']].mean().round(2)
print("Average Macronutrients per Diet Type:")
print(avg_macros.to_string())
print()

# Top 5 protein-rich recipes per diet type
top_protein = (df.sort_values('Protein(g)', ascending=False)
               .groupby('Diet_type')
               .head(5)[['Diet_type', 'Recipe_name', 'Protein(g)']])
print("Top 5 Protein-Rich Recipes per Diet Type:")
print(top_protein.to_string(index=False))
print()

# Diet type with highest avg protein
highest_protein_diet = avg_macros['Protein(g)'].idxmax()
highest_protein_val  = avg_macros['Protein(g)'].max()
print(f"Diet with highest avg protein: {highest_protein_diet} ({highest_protein_val:.2f}g)\n")

# Most common cuisine per diet type
common_cuisines = (df.groupby('Diet_type')['Cuisine_type']
                   .agg(lambda x: x.value_counts().index[0])
                   .reset_index()
                   .rename(columns={'Cuisine_type': 'Most_Common_Cuisine'}))
print("Most Common Cuisine per Diet Type:")
print(common_cuisines.to_string(index=False))
print()

# New ratios
df['Protein_to_Carbs_ratio'] = (df['Protein(g)'] / df['Carbs(g)']).replace([float('inf')], 0).round(4)
df['Carbs_to_Fat_ratio']     = (df['Carbs(g)']   / df['Fat(g)']).replace([float('inf')], 0).round(4)
print("Sample of computed ratios (first 5 rows):")
print(df[['Recipe_name','Protein_to_Carbs_ratio','Carbs_to_Fat_ratio']].head().to_string(index=False))
print()

# VISUALIZATIONS

sns.set_theme(style="whitegrid")

# Chart 1: Bar chart - avg macronutrients per diet type
fig, ax = plt.subplots(figsize=(12, 6))
avg_macros.plot(kind='bar', ax=ax, color=['#2196F3', '#FF9800', '#F44336'])
ax.set_title('Average Macronutrient Content by Diet Type', fontsize=14, pad=12)
ax.set_xlabel('Diet Type')
ax.set_ylabel('Average Amount (g)')
ax.set_xticklabels(ax.get_xticklabels(), rotation=35, ha='right')
ax.legend(title='Macronutrient')
plt.tight_layout()
plt.savefig('charts/bar_avg_macros.png', dpi=150)
plt.close()
print("Saved: charts/bar_avg_macros.png")

# Chart 2: Heatmap — macronutrient vs diet type
fig, ax = plt.subplots(figsize=(10, 6))
sns.heatmap(avg_macros, annot=True, fmt='.1f', cmap='YlOrRd', linewidths=0.5, ax=ax)
ax.set_title('Macronutrient Heatmap by Diet Type', fontsize=14, pad=12)
ax.set_xlabel('Macronutrient')
ax.set_ylabel('Diet Type')
plt.tight_layout()
plt.savefig('charts/heatmap_macros.png', dpi=150)
plt.close()
print("Saved: charts/heatmap_macros.png")

# Chart 3: Scatter plot — top 5 protein recipes by cuisine
top5_all = df.sort_values('Protein(g)', ascending=False).head(30)
fig, ax = plt.subplots(figsize=(12, 6))
sns.scatterplot(data=top5_all, x='Cuisine_type', y='Protein(g)',
                hue='Diet_type', s=120, ax=ax)
ax.set_title('Top Protein-Rich Recipes Across Cuisines', fontsize=14, pad=12)
ax.set_xlabel('Cuisine Type')
ax.set_ylabel('Protein (g)')
ax.set_xticklabels(ax.get_xticklabels(), rotation=40, ha='right')
ax.legend(title='Diet Type', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.savefig('charts/scatter_top_protein.png', dpi=150)
plt.close()
print("Saved: charts/scatter_top_protein.png")

print(f"\n{'='*55}")
print("  Analysis complete. Charts saved to /charts/")
print(f"{'='*55}\n")