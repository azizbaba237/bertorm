# convert.py
try:
    with open('datadump.json', 'r', encoding='latin1') as f:
        data = f.read()
    
    with open('datadump_fixed.json', 'w', encoding='utf-8') as f:
        f.write(data)
    
    print("Conversion réussie! Fichier créé: datadump_fixed.json")
except Exception as e:
    print("Erreur:", e)
input("Appuyez sur Entrée pour quitter...")