import xml.etree.ElementTree as ET
import sys
import time

"""
v1. --> Notes de modifications à apporter au programme
Le problème vient du fait que dans le cas où les deux éléments se trouvant aux indices n+1 sont différents alors les deux indices avancent en même temps
En réalité, il faut comparer les deux éléments et les faire avancer chacun de leur côté en fonction de l'ordre de supériorité (> ou <) jusqu'à ce que cet ordre s'inverse
On fera alors avancer l'autre élément là encore jusqu'à ce que l'ordre s'inverse, et ce jusqu'à la fin du programme. 

Affichage de comparaison intelligente de deux fichiers XML

Argument 1 : nom du programme. Exemple : xml-Parser.py
Argument 2 : nom du fichier le plus récent. Exemple ; fichier_recent.xml
Argument 3 : nom du fichier ancien. Exemple : fichier_ancien.xml

Exemple d'utilisation :
python Argument 1 Argument 2 Argument 3
Soit :
python xml-Parser.py fichier_recent.xml fichier_ancien.xml

"""

if len(sys.argv) != 3:
    print("Vous devez donner en premier argument le nom du fichier le plus récent et en deuxième argument le nom du fichier le plus ancien.")
    sys.exit()

start_time = time.time() # Début du timer pour déterminer à la fin, le temps d'exécution du programme

fichier_new = sys.argv[1]
fichier_old = sys.argv[2] # Récupération des fichiers XML à ouvrir et parcourir

arbre_new = ET.parse(fichier_new) # Lecture des fichiers
arbre_old = ET.parse(fichier_old)

root_new = arbre_new.getroot() # Puis récupération de la racine pour permettre la comparaison de leurs attributs
root_old = arbre_old.getroot()

gom1 = root_new[0][0] # On se place directement au premier niveau d'objets
gom2 = root_old[0][0]

diff = False # Variable permettant de déterminer le type d'exit() à effectuer en fin de programme

def xmlParserClassName(gom1,gom2): # Fonction de comparaison des attributs class-name
    global diff
    elements_new = [] # Liste qui va contenir les différentes valeurs des attributs récupérés lors du parcours de chacun des fichiers
    elements_old = []

    ecart_index_new = 0 # Variable d'écart, qui va permettre d'ajuster le parcours en fonction des types de différences détectées
    ecart_index_old = 0 # Une différence ne doit pas entraîner la différence du reste du fichier (à cause du décalage)

    for enfant in gom1 :
        class_name = enfant.get("class-name") # Récupération des attributs class-name du fichier récent
        elements_new.append(class_name)

    for enfant2 in gom2 :
        class_name = enfant2.get("class-name") # Récupération des attributs class-name du fichier ancien
        elements_old.append(class_name)

    for n in range(max(len(elements_new),len(elements_old))):
        if len(elements_new) - 1 <= n + ecart_index_new and len(elements_old) > n + ecart_index_old:
            #print("Fin nouveau fichier")
            if elements_new[-1] == elements_old[n+ecart_index_old]:
                #print("Classe " + str(elements_old[n+ecart_index_old]) + " identique dans le nouveau et l'ancien fichier")
                #print("Parcours des noms des objets de la classe " + str(elements_old[n+ecart_index_old])+ " et affichage des potentielles différences.\n")
                print("\nClasse : " + str(elements_new[-1]) + "\n")
                ecart_index_new -= 1
                xmlParserName(str(elements_old[n+ecart_index_old]),gom1,gom2)
            else :
                diff = True
                #print("Différence : " + str(elements_new[-1]) + " dans nouveau fichier et " + str(elements_old[n+ecart_index_old]) + " dans ancien fichier") # Si les classes sont différentes, pas besoin d'appeler la fonctiona de parsing par nom, puisqu'on sait déjà qu'initialement la classe n'existe pas dans un des deux fichiers, et donc son contenu également
                #print("Classe " + str(elements_new[-1]) + " dans nouveau fichier et " + str(elements_old[n+ecart_index_old]) + " dans ancien fichier")
                if elements_new[-1] < elements_old[n+ecart_index_old]:
                    print("Classe : " + str(elements_old[n+ecart_index_old]) + " seulement dans l'ancien fichier\n")
                    ecart_index_new -= 1
                else :
                    print("Classe : " + str(elements_new[-1]) + " seulement dans le nouveau fichier\n")
                    ecart_index_new -= 1
        elif len(elements_new) > n + ecart_index_new and len(elements_old) - 1 <= n + ecart_index_old : # Idem dans le cas si l'autre fichier est arrivé à sa fin
            #print("Fin ancien fichier")
            if elements_old[-1] == elements_new[n+ecart_index_new]:
                #print("Classe " + str(elements_new[n+ecart_index_new]) + " identique dans le nouveau et l'ancien fichier")
                #print("Parcours des noms des objets de la classe " + str(elements_new[n + ecart_index_new]) + " et affichage des potentielles différences.\n")
                print("\nClasse : " + elements_old[-1] + "\n")
                ecart_index_old -= 1
                xmlParserName(str(elements_new[n + ecart_index_new]),gom1,gom2)
            else:
                #print("Différence : " + str(elements_new[n+ecart_index_new]) + " dans nouveau fichier et " + str(elements_old[-1]) + " dans ancien fichier")
                #print("Classe " + str(elements_new[n+ecart_index_new]) + " dans nouveau fichier et " + str(elements_old[-1]) + " dans ancien fichier")
                diff = True
                if elements_old[-1] < elements_new[n + ecart_index_new]:
                    print("Classe : " + str(elements_new[n+ecart_index_new]) + " seulement dans l'ancien fichier\n")
                    ecart_index_old -= 1
                else :
                    print("Classe : " + str(elements_old[-1]) + " seulement dans le nouveau fichier\n")
                    ecart_index_old -= 1
        elif len(elements_new) <= n + ecart_index_new and len(elements_old) <= n + ecart_index_old :
            #print("Fin des deux fichiers")
            if elements_new[-1] == elements_old[-1]:
                #print("Classe " + elements_old[-1] + " identique dans le nouveau et l'ancien fichier")
                #print("Parcours des noms des objets de la classe " + str(elements_new[n + ecart_index_new]) + " et affichage des potentielles différences.\n")
                print("\nClasse : " + elements_new[-1] + "\n")
                xmlParserName(str(elements_old[-1]),gom1,gom2)
            else:
                #print("Différence : " + str(elements_new[-1]) + " dans nouveau fichier et " + str(elements_old[-1]) + " dans ancien fichier")
                #print("Classe " + str(elements_new[-1]) + " dans nouveau fichier et " + str(elements_old[-1]) + " dans ancien fichier")
                diff = True
                if elements_new[-1] < elements_old[-1]:
                    print("Classe : " + str(elements_old[-1]) + " seulement dans l'ancien fichier\n")
                else :
                    print("Classe : " + str(elements_new[-1]) + " seulement dans le nouveau fichier\n")
        elif elements_new[n+ecart_index_new] == elements_old[n+ecart_index_old]:
            #print("Classe "+str(elements_new[n+ecart_index_new])+" identique dans le nouveau et l'ancien fichier")
            #print("Parcours des noms des objets de la classe " + str(elements_new[n + ecart_index_new]) + " et affichage des potentielles différences.\n")
            print("\nClasse : " + elements_new[n+ecart_index_new] + "\n")
            xmlParserName(str(elements_new[n + ecart_index_new]),gom1,gom2)
        elif elements_old[n+ecart_index_old] != elements_new[n+ecart_index_new]:
            if elements_new[n+1+ecart_index_new] == elements_old[n+ecart_index_old] :
                #print("Différence : " + str(elements_new[n+ecart_index_new]) + " dans nouveau fichier et " + str(elements_old[n+ecart_index_old]) + " dans ancien fichier")
                #print("Classe " + str(elements_new[n+ecart_index_new]) + " dans nouveau fichier et " + str(elements_old[n+ecart_index_old]) + " dans ancien fichier")
                diff = True
                if elements_new[n+ecart_index_new] < elements_old[n+ecart_index_old]:
                    print("Classe : " + str(elements_old[n+ecart_index_old]) + " seulement dans l'ancien fichier\n")
                    ecart_index_new -= 1
                else :
                    print("Classe : " + str(elements_new[n + ecart_index_new]) + " seulement dans le nouveau fichier\n")
                    ecart_index_new -= 1

            elif elements_new[n+ ecart_index_new] == elements_old[n+1+ ecart_index_old]:
                #print("Différence : " + str(elements_new[n+ecart_index_new]) + " dans nouveau fichier et " + str(elements_old[n+ecart_index_old]) + " dans ancien fichier")
                #print("Classe " + str(elements_new[n+ecart_index_new]) + " dans nouveau fichier et " + str(elements_old[n+ecart_index_old]) + " dans ancien fichier")
                diff = True
                if elements_new[n+ ecart_index_new] < elements_old[n+ecart_index_old]:
                    print("Classe : " + str(elements_old[n+ecart_index_old]) + " seulement dans l'ancien fichier\n")
                    ecart_index_old -= 1
                else :
                    print("Classe : " + str(elements_new[n + ecart_index_new]) + " seulement dans le nouveau fichier\n")
                    ecart_index_old -= 1
            else :
                # print("Différence : " + str(elements_new[n+ecart_index_new]) + " dans nouveau fichier et " + str(elements_old[n+ecart_index_old]) + " dans ancien fichier")
                #print("Classe " + str(elements_new[n + ecart_index_new]) + " dans nouveau fichier et " + str(elements_old[n + ecart_index_old]) + " dans ancien fichier")
                diff = True
                if elements_new[n+ecart_index_new] < elements_old[n+ecart_index_old]:
                    print("Classe : " + str(elements_old[n+ecart_index_old]) + " seulement dans l'ancien fichier\n")
                else :
                    print("Classe : " + str(elements_new[n + ecart_index_new]) + " seulement dans le nouveau fichier\n")

def xmlParserName(class_name,gom1,gom2): # Fonction de comparaison des attributs name
    global diff
    elements_new2 = []
    elements_old2 = []

    ecart_index_new2 = 0
    ecart_index_old2 = 0

    for enfant in gom1.iter():
        if enfant.get("class-name") == class_name:
            for a in enfant.findall("fv"):
                elements_new2.append(a.get("nom"))

    for enfant in gom2.iter():
        if enfant.get("class-name") == class_name:
            for b in enfant.findall("fv"):
                elements_old2.append(b.get("nom"))

    for m in range(max(len(elements_new2),len(elements_old2))):
        if len(elements_new2) == 0:
            if len(elements_old2) == 0 :
                print("Classe " + class_name + " vide")
            else :
                print("Classe " + class_name + " vide dans nouveau fichier, Nom : " + str(elements_old2[m+ecart_index_old2]) + " dans ancien fichier\n")
        elif  len(elements_old2) == 0:
            if len(elements_new2) == 0 :
                print("Classe " + class_name + " vide")
            else :
                print("Classe " + class_name + " vide dans ancien fichier, Nom : " + str(elements_new2[m+ecart_index_new2]) + " dans nouveau fichier\n")
        elif len(elements_new2) - 1 <= m + ecart_index_new2 and len(elements_old2) > m + ecart_index_old2:
            #print("Fin nouveau fichier")
            if elements_new2[-1] == elements_old2[m + ecart_index_old2]:
                ecart_index_new2 -= 1
                #print("Nom : " + str(elements_old2[m + ecart_index_old2]) + " identique dans le nouveau et l'ancien fichier") # Si les fichiers sont identiques...
                #print("Parcours des valeurs des objets de la classe " + str(elements_new2[-1]) + " et affichage des potentielles différences.\n")
                xmlParserVal(str(elements_new2[-1]),gom1,gom2, class_name) # On va cette fois-ci appeler la fonction de comparaison par valeur. Son fonctionnement est identique des deux autres fonctions, seule l'instance de comparaison change
            else:
                #print("Différence : " + str(elements_new2[-1]) + " dans nouveau fichier et " + str(elements_old2[m + ecart_index_old2]) + " dans ancien fichier") # Si différence il y a, pas d'appel de fonction, puisqu'on sait déjà que l'instance est différente, pas besoin de comparer "l'intérieur" de l'objet
                #print("Nom " + str(elements_new2[-1]) + " dans nouveau fichier et " + str(elements_old2[m + ecart_index_old2]) + " dans ancien fichier")
                diff = True
                if elements_new2[-1] < elements_old2[m+ecart_index_old2]:
                    print("Nom : " + str(elements_old2[m+ecart_index_old2]) + " seulement dans l'ancien fichier")
                    ecart_index_new2 -= 1
                else :
                    print("Nom : " + str(elements_new2[-1]) + " seulement dans le nouveau fichier")
                    ecart_index_new2 -= 1
        elif len(elements_new2) > m + ecart_index_new2 and len(elements_old2) - 1 <= m + ecart_index_old2:
            #print("Fin ancien fichier")
            if elements_old2[-1] == elements_new2[m + ecart_index_new2]:
                ecart_index_old2 -= 1
                #print("Nom : " + str(elements_old2[-1]) + " identique dans le nouveau et l'ancien fichier")
                #print("Parcours des valeurs des objets de la classe " + str(elements_old2[-1]) + " et affichage des potentielles différences.\n")
                xmlParserVal(str(elements_old2[-1]),gom1,gom2, class_name)
            else:
                #print("Différence : " + str(elements_new2[m + ecart_index_new2]) + " dans nouveau fichier et " + str(elements_old2[-1]) + " dans ancien fichier")
                #print("Nom " + str(elements_new2[m + ecart_index_new2]) + " dans nouveau fichier et " + str(elements_old2[-1]) + " dans ancien fichier")
                diff = True
                if elements_new2[m+ecart_index_new2] < elements_old2[-1]:
                    print("Nom : " + str(elements_old2[-1]) + " seulement dans l'ancien fichier")
                    ecart_index_old2 -= 1
                else :
                    print("Nom : " + str(elements_new2[m + ecart_index_new2]) + " seulement dans le nouveau fichier")
                    ecart_index_old2 -= 1
        elif len(elements_new2) <= m + ecart_index_new2 and len(elements_old2) <= m + ecart_index_old2:
            #print("Fin des deux fichiers")
            if elements_new2[-1] == elements_old2[-1]:
                #print("Nom : " + str(elements_old2[m + ecart_index_old2]) + " identique dans le nouveau et l'ancien fichier")
                #print("Parcours des valeurs des objets de la classe " + str(elements_new2[-1]) + " et affichage des potentielles différences.\n")
                xmlParserVal(str(elements_old2[-1]),gom1,gom2, class_name)
            else:
                #print("Différence : " + str(elements_new2[-1]) + " dans nouveau fichier et " + str(elements_old2[-1]) + " dans ancien fichier")
                #print("Nom " + str(elements_new2[-1]) + " dans nouveau fichier et " + str(elements_old2[-1]) + " dans ancien fichier")
                diff = True
                if elements_new2[-1] < elements_old2[-1]:
                    print("Nom : " + str(elements_old2[-1]) + " seulement dans l'ancien fichier")
                else :
                    print("Nom : " + str(elements_new2[-1]) + " seulement dans le nouveau fichier")
        elif elements_new2[m + ecart_index_new2] == elements_old2[m + ecart_index_old2]:
            #print("Nom : " + str(elements_old2[m + ecart_index_old2]) + " identique dans le nouveau et l'ancien fichier")
            #print("Parcours des valeurs des objets de la classe " + str(elements_new2[m + ecart_index_new2]) + " et affichage des potentielles différences.\n")
            xmlParserVal(str(elements_old2[m + ecart_index_old2]),gom1,gom2, class_name)
        elif elements_old2[m + ecart_index_old2] != elements_new2[m + ecart_index_new2]:
            if elements_old2[m + ecart_index_old2] == elements_new2[m + 1 + ecart_index_new2]:
                #print("Différence : " + str(elements_new2[m + ecart_index_new2]) + " dans nouveau fichier et " + str(elements_old2[m + ecart_index_old2]) + " dans ancien fichier")
                #print("Nom " + str(elements_new2[m + ecart_index_new2]) + " dans nouveau fichier et " + str(elements_old2[m + ecart_index_old2]) + " dans ancien fichier")
                diff = True
                if elements_new2[m+ecart_index_new2] < elements_old2[m+ecart_index_old2]:
                    print("Nom : " + str(elements_old2[m+ecart_index_old2]) + " seulement dans l'ancien fichier")
                    ecart_index_new2 -= 1
                else :
                    print("Nom : " + str(elements_new2[m + ecart_index_new2]) + " seulement dans le nouveau fichier")
                    ecart_index_new2 -= 1
            elif elements_new2[m + ecart_index_new2] == elements_old2[m + 1 + ecart_index_old2]:  # Idem
                #print("Différence : " + str(elements_new2[m + ecart_index_new2]) + " dans nouveau fichier et " + str(elements_old2[m + ecart_index_old2]) + " dans ancien fichier")
                #print("Nom " + str(elements_new2[m + ecart_index_new2]) + " dans nouveau fichier et " + str(elements_old2[m + ecart_index_old2]) + " dans ancien fichier")
                diff = True
                if elements_new2[m+ecart_index_new2] < elements_old2[m+ecart_index_old2]:
                    print("Nom : " + str(elements_old2[m+ecart_index_old2]) + " seulement dans l'ancien fichier")
                    ecart_index_old2 -= 1
                else :
                    print("Nom : " + str(elements_new2[m + ecart_index_new2]) + " seulement dans le nouveau fichier")
                    ecart_index_old2 -= 1
            else :
                # print("Différence : " + str(elements_new2[m + ecart_index_new2]) + " dans nouveau fichier et " + str(elements_old2[m + ecart_index_old2]) + " dans ancien fichier")
                #print("Nom " + str(elements_new2[m + ecart_index_new2]) + " dans nouveau fichier et " + str(elements_old2[m + ecart_index_old2]) + " dans ancien fichier")
                diff = True
                if elements_new2[m+ecart_index_new2] < elements_old2[m+ecart_index_old2]:
                    print("Nom : " + str(elements_old2[m+ecart_index_old2]) + " seulement dans l'ancien fichier")
                else :
                    print("Nom : " + str(elements_new2[m + ecart_index_new2]) + " seulement dans le nouveau fichier")

def xmlParserVal(name,gom1,gom2, class_name): # Fonction de comparaison des attributs val
    global diff
    elements_new3 = []
    elements_old3 = []

    ecart_index_new3 = 0
    ecart_index_old3 = 0

    for enfant in gom1.iter():
        if enfant.get("class-name") == class_name:
            for a in enfant.findall("fv"):
                if a.get("nom") == name:
                    elements_new3.append(a.get("val"))

    for enfant in gom2.iter():
        if enfant.get("class-name") == class_name:
            for a in enfant.findall("fv"):
                if a.get("nom") == name:
                    elements_old3.append(a.get("val"))

    for g in range(max(len(elements_new3),len(elements_old3))):
        if len(elements_new3) - 1 <= g + ecart_index_new3 and len(elements_old3) > g + ecart_index_old3:
            #print("Fin nouveau fichier")
            if elements_new3[-1] == elements_old3[g + ecart_index_old3]:
                ecart_index_new3 -= 1
                #print("Valeur : " + str(elements_old3[g + ecart_index_old3]) + " identique dans le nouveau et l'ancien fichier")
                continue
            else:
                diff = True
                #print("Différence : " + str(elements_new3[-1]) + " dans nouveau fichier et " + str(elements_old3[g + ecart_index_old3]) + " dans ancien fichier")
                #print("Valeur " + str(elements_new3[-1]) + " dans nouveau fichier et " + str(elements_old3[g + ecart_index_old3]) + " dans ancien fichier")
                if elements_new3[-1] < elements_old3[g+ecart_index_old3]:
                    print("Valeur : " + str(elements_old3[g+ecart_index_old3]) + " seulement dans l'ancien fichier")
                    ecart_index_new3 -= 1
                else :
                    print("Valeur : " + str(elements_new3[-1]) + " seulement dans le nouveau fichier")
                    ecart_index_new3 -= 1
        elif len(elements_new3) > g + ecart_index_new3 and len(elements_old3) - 1 <= g + ecart_index_old3:
            #print("Fin ancien fichier")
            if elements_old3[-1] == elements_new3[g + ecart_index_new3]:
                ecart_index_old3 -= 1
                #print("Valeur : " + str(elements_old3[g + ecart_index_old3]) + " identique dans le nouveau et l'ancien fichier")
                continue
            else:
                diff = True
                #print("Différence : " + str(elements_new3[g + ecart_index_new3]) + " dans nouveau fichier et " + str(elements_old3[-1]) + " dans ancien fichier")
                #print("Valeur " + str(elements_new3[g + ecart_index_new3]) + " dans nouveau fichier et " + str(elements_old3[-1]) + " dans ancien fichier")
                if elements_new3[g+ecart_index_new3] < elements_old3[-1]:
                    print("Valeur : " + str(elements_old3[-1]) + " seulement dans l'ancien fichier")
                    ecart_index_old3 -= 1
                else :
                    print("Valeur : " + str(elements_new3[g+ecart_index_new3]) + " seulement dans le nouveau fichier")
                    ecart_index_old3 -= 1
        elif len(elements_new3) <= g + ecart_index_new3 and len(elements_old3) <= g + ecart_index_old3:
            #print("Fin des deux fichiers")
            if elements_new3[-1] == elements_old3[-1]:
                #print("Valeur : " + str(elements_old3[g + ecart_index_old3]) + " identique dans le nouveau et l'ancien fichier")
                continue
            else:
                diff = True
                #print("Différence : " + str(elements_new3[-1]) + " dans nouveau fichier et " + str(elements_old3[-1]) + " dans ancien fichier")
                #print("Valeur " + str(elements_new3[-1]) + " dans nouveau fichier et " + str(elements_old3[-1]) + " dans ancien fichier")
                if elements_new3[-1] < elements_old3[-1]:
                    print("Valeur : " + str(elements_old3[-1]) + " seulement dans l'ancien fichier")
                else :
                    print("Valeur : " + str(elements_new3[-1]) + " seulement dans le nouveau fichier")
        elif elements_new3[g + ecart_index_new3] == elements_old3[g + ecart_index_old3]:
            #print("Valeur : " + str(elements_old3[g + ecart_index_old3]) + " identique dans le nouveau et l'ancien fichier")
            continue
        elif elements_old3[g + ecart_index_old3] != elements_new3[g + ecart_index_new3]:
            if elements_old3[g + ecart_index_old3] == elements_new3[g + 1 + ecart_index_new3]:
                diff = True
                #print("Différence : " + str(elements_new3[g + ecart_index_new3]) + " dans nouveau fichier et " + str(elements_old3[g + ecart_index_old3]) + " dans ancien fichier")
                #print("Valeur " + str(elements_new3[g + ecart_index_new3]) + " dans nouveau fichier et " + str(elements_old3[g + ecart_index_old3]) + " dans ancien fichier")
                if elements_new3[g+ecart_index_new3] < elements_old3[g+ecart_index_old3]:
                    print("Valeur : " + str(elements_old3[g+ecart_index_old3]) + " seulement dans l'ancien fichier")
                    ecart_index_new3 -= 1
                else :
                    print("Valeur : " + str(elements_new3[g+ecart_index_new3]) + " seulement dans le nouveau fichier")
                    ecart_index_new3 -= 1
            elif elements_new3[g] == elements_old3[g + 1 + ecart_index_old3]:  # Idem
                diff = True
                #print("Différence : " + str(elements_new3[g + ecart_index_new3]) + " dans nouveau fichier et " + str(elements_old3[g + ecart_index_old3]) + " dans ancien fichier")
                #print("Valeur " + str(elements_new3[g + ecart_index_new3]) + " dans nouveau fichier et " + str(elements_old3[g + ecart_index_old3]) + " dans ancien fichier")
                if elements_new3[g+ecart_index_new3] < elements_old3[g+ecart_index_old3]:
                    print("Valeur : " + str(elements_old3[g+ecart_index_old3]) + " seulement dans l'ancien fichier")
                    ecart_index_old3 -= 1
                else :
                    print("Valeur : " + str(elements_new3[g+ecart_index_new3]) + " seulement dans le nouveau fichier")
                    ecart_index_old3 -= 1
            else :
                diff = True
                # print("Différence : " + str(elements_new3[g + ecart_index_new3]) + " dans nouveau fichier et " + str(elements_old3[g + ecart_index_old3]) + " dans ancien fichier")
                #print("Valeur " + str(elements_new3[g + ecart_index_new3]) + " dans nouveau fichier et " + str(elements_old3[g + ecart_index_old3]) + " dans ancien fichier")
                if elements_new3[g+ecart_index_new3] < elements_old3[g+ecart_index_old3]:
                    print("Valeur : " + str(elements_old3[g+ecart_index_old3]) + " seulement dans l'ancien fichier")
                else :
                    print("Valeur : " + str(elements_new3[g+ecart_index_new3]) + " seulement dans le nouveau fichier")
xmlParserClassName(gom1,gom2)

# Calcul du temps d'exécution du parcours
end_time = time.time()
execution_time = end_time - start_time
print(execution_time) # Et affichage
if diff: # Si le programme a au moins une différence
    exit(1) # Type d'exit 1
elif not diff: # Sinon
    exit(0) # Type d'exit 2
