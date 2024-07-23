import xml.etree.ElementTree as ET
import sys

"""
Créé un fichier XML à partir d'un autre, en ne gardant que certains éléments choisis par l'utilisateur

 Argument 1 : nom du programme. Exemple : xml-Parser.py
 Argument 2 : nom de la conf xml à parcourir. Exemple : MDO-Conf.xml
 Argument 3 : nom souhaité pour le nouveau fichier renvoyé. Exemple : nouvelle_conf.xml
 Argument 4 : Trigramme. Exemple : MDO
 Argument 5 : nom du fichier texte contenant les classes à inclure
 Les arguments peuvent être mis entre guillemets ou non, cela ne gêne pas le fonctionnement du programme.
 Un exemple d'utilisation serait le suivant :
 python Argument 1 Argument 2 Argument 3 Argument 4 soit :
 python xml-Parser.py MDO-Conf.xml nouvelle_conf.xml MLV
 Il faut inclure les 5 arguments, dans le cas contraire le programme ne fonctionnera pas
"""

def parcours(root,classe):
    resultats = []
    for element in root.findall(".//*[@class-name='%s']" % classe):
        resultats.append(element)
    return resultats

if len(sys.argv) != 5:
    print("Vous devez donner en premier argument le nom du fichier à traiter, en deuxième argument le nom souhaité pour le nouveau fichier, en troisième argument le trigramme, et en quatrième argument le nom du fichier texte contenant les class-name des objets à inclure.")
    sys.exit()
else :
    nom_fichier=str(sys.argv[1])
    nom_nouveau_fichier=str(sys.argv[2])
    trigramme=str(sys.argv[3])
    arg4=str(sys.argv[4])

temp=open(arg4,'r')
fichier_classes=temp.read()
classes_a_rechercher=fichier_classes.split(",")

try:
    arbre = ET.parse(nom_fichier)
    racine = arbre.getroot()
    if len(racine) == 0:
        print("L'arbre est vide")
        sys.exit()
except ET.ParseError:
    print("Le fichier est vide ou n'a pas pu être lu correctement")
    sys.exit()
except IndexError:
    print("Vous devez donner en premier argument le nom du fichier à traiter, en deuxième argument le nom souhaité pour le nouveau fichier, en troisième argument le fichier texte.")
    sys.exit()

nouvelle_racine=ET.Element("configurations",version="3")
nouvelle_version=ET.Element("configuration", tag =trigramme+" - Configuration de travail", description= "Configuration de travail", nom= "")
element_nouveau=ET.Element("groupe-object-model")
nouvelle_racine.append(nouvelle_version)
nouvelle_version.append(element_nouveau)

for classe in classes_a_rechercher:
    elements=parcours(racine,classe)
    for element in elements:
        element_nouveau.append(element)

nouvel_arbre=ET.ElementTree(nouvelle_racine)
nouvel_arbre.write(nom_nouveau_fichier,encoding="utf-8",xml_declaration=True)
