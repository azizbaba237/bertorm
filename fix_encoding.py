# fix_encoding.py
print("Correction de l'encodage en cours...")

with open(r'C:\Users\user\Desktop\datadump.json', 'r', encoding='latin1') as f:
    data = f.read()

with open(r'C:\Users\user\Desktop\datadump_fixed.json', 'w', encoding='utf-8') as f:
    f.write(data)

print("Fichier corrigé créé : datadump_fixed.json")
print("Maintenant exécutez : python manage.py loaddata ../datadump_fixed.json")
input("Appuyez sur Entrée pour quitter...")