import xml.etree.ElementTree as ET
import sys

fichier = sys.argv[1]
new_file = sys.argv[2]
classes_file = sys.argv[3]
noms_file = sys.argv[4]

arbre = ET.parse(fichier)
racine = arbre.getroot()
def read_file_to_list(filename):
    with open(filename, 'r') as file:
        content = file.read()
    return [item.strip() for item in content.split(',')]

classes = read_file_to_list(classes_file)
noms = read_file_to_list(noms_file)

print("Classes:", classes)
print("Noms:", noms)

for p in racine[0].findall("groupe-object-model"):
    for element in p:
        if element.get("class-name") in classes:
            for i in noms:
                if i in element.get("nom"):
                    p.remove(element)
nouvel_arbre = ET.ElementTree(racine)
nouvel_arbre.write(new_file, encoding="UTF-8", xml_declaration=True)
print("Le fichier XML modifié a été sauvegardé sous "+new_file+".")
