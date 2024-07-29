import xml.etree.ElementTree as ET
import sys
"""Documentation :
Programme de suppression d'objets en fonction de leurs attributs "class-name" et "nom".

Utilisation :
Argument 1 : nom du programme. Exemple : liaison_vpn.py
Argument 2 : nom du fichier. Exemple : conf.xml
Argument 3 : fichier txt contenant les classes. Exemple : classes.txt
Argument 4 : fichier txt contenant les noms. Exemple : noms.txt

Exemple d'utilisation : python liaisons_vpn.py conf.xml classes.txt noms.txt
"""
# Vérifier que le nombre correct d'arguments est passé
if len(sys.argv) != 5:
    print("Usage: python script.py <fichier> <new_file> <classes_file> <noms_file>")
    sys.exit(1)

fichier = sys.argv[1]
new_file = sys.argv[2]
classes_file = sys.argv[3]
noms_file = sys.argv[4]

# Lire et parser le fichier XML
try:
    arbre = ET.parse(fichier)
except ET.ParseError as e:
    print(f"Erreur lors du parsing du fichier XML: {e}")
    sys.exit(1)
except FileNotFoundError:
    print(f"Le fichier {fichier} n'a pas été trouvé.")
    sys.exit(1)

racine = arbre.getroot()
if not racine:
    print("Erreur: le fichier XML est vide ou mal formé.")
    sys.exit(1)

# Se déplacer au premier élément enfant de la racine
racine = racine[0]

# Fonction pour lire un fichier et le transformer en une liste d'éléments
def read_file_to_list(filename):
    try:
        with open(filename, 'r') as file:
            content = file.read()
        return [item.strip() for item in content.split(',')]
    except FileNotFoundError:
        print(f"Le fichier {filename} n'a pas été trouvé.")
        sys.exit(1)
    except Exception as e:
        print(f"Erreur lors de la lecture du fichier {filename}: {e}")
        sys.exit(1)

# Lire les fichiers de classes et de noms
classes = read_file_to_list(classes_file)
noms = read_file_to_list(noms_file)

print("Classes:", classes)
print("Noms:", noms)

# Parcourir les éléments du modèle d'objet de groupe et supprimer les éléments correspondants
for p in racine.findall("groupe-object-model"):
    for element in list(p):  # Convertir p en liste pour éviter les problèmes de modification pendant l'itération
        if element.get("class-name") in classes:
            for nom in noms:
                if nom in element.get("nom"):
                    p.remove(element)  # Supprimer l'élément de son parent direct

# Sauvegarder le nouvel arbre XML dans un fichier
try:
    nouvel_arbre = ET.ElementTree(racine)
    nouvel_arbre.write(new_file, encoding="utf-8", xml_declaration=True)
    print(f"Le fichier XML modifié a été sauvegardé sous {new_file}.")
except Exception as e:
    print(f"Erreur lors de la sauvegarde du fichier XML: {e}")
    sys.exit(1)
