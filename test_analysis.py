import pandas as pd

df = pd.read_csv('All_Diets.csv')
avg = df.groupby('Diet_type')[['Protein(g)','Carbs(g)','Fat(g)']].mean()

assert not df.empty, "Dataset should not be empty"
assert 'Protein(g)' in df.columns, "Protein column missing"
assert avg['Protein(g)'].idxmax() == 'keto', "Keto should have highest protein"
print("All tests passed.")