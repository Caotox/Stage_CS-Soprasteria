import xml.etree.ElementTree as ET
import sys

"""
Documentation :
Programme de suppression d'objets en fonction de leurs attributs "class-name" et "nom".

Utilisation :
Argument 1 : nom du programme. Exemple : liaison_vpn.py
Argument 2 : nom du fichier. Exemple : conf.xml
Argument 3 : nom souhaité pour le nouveau fichier. Exemple : new.xml
Argument 4 : fichier txt contenant les classes. Exemple : classes.txt
Argument 5 : fichier txt contenant les noms. Exemple : noms.txt

Exemple d'utilisation : python liaisons_vpn.py conf.xml new.xml classes.txt noms.txt
"""

# Vérifier que le nombre correct d'arguments est passé
if len(sys.argv) != 5:
    print("Utilisation : python script.py <fichier> <new_file> <classes_file> <noms_file>")
    sys.exit(1)

# Récupération des arguments de la ligne de commande
fichier = sys.argv[1]
new_file = sys.argv[2]
classes_file = sys.argv[3]
noms_file = sys.argv[4]

# Fonction pour lire un fichier et le transformer en une liste d'éléments
def read_file_to_list(filename):
    with open(filename, 'r') as file:
        content = file.read()
    return [item.strip() for item in content.split(',')]

# Lire les fichiers de classes et de noms
classes = read_file_to_list(classes_file)
noms = read_file_to_list(noms_file)

# Lire et parser le fichier XML
arbre = ET.parse(fichier)
racine = arbre.getroot()

print("Classes:", classes)
print("Noms:", noms)

# Parcourir les éléments du modèle d'objet de groupe et supprimer les éléments correspondants
for p in racine[0].findall("groupe-object-model"):
    for element in list(p): # Convertir p en liste pour éviter les problèmes de modification pendant l'itération
        if element.get("class-name") in classes:
            for i in noms:
                if i in element.get("nom"):
                    p.remove(element)

# Sauvegarder le nouvel arbre XML dans un fichier
nouvel_arbre = ET.ElementTree(racine)
nouvel_arbre.write(new_file, encoding="UTF-8", xml_declaration=True)
print("Le fichier XML modifié a été sauvegardé sous "+new_file+".")
