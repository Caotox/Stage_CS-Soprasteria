import xml.etree.ElementTree as ET
import sys

diff = False

def xmlParserClassName():
    elements_new = [] # Liste qui va contenir toutes les classes du fichier récent
    elements_old = [] # Liste qui va contenir toutes les classes du fichier ancien

    # Ecart qui va permettre d'ajuster le parcours pour éviter qu'une différence rende toute les autres comparaisons différentes également.
    # Va également servir pour éviter les erreurs d'index
    ecart_index_new = 0
    ecart_index_old = 0

    fichier_new = sys.argv[1]
    fichier_old = sys.argv[2]

    # Création des deux arbres, un venant du fichier récent et un venant du fichier ancien
    arbre_new = ET.parse(fichier_new)
    arbre_old = ET.parse(fichier_old)

    # On récupère les deux racines
    root_new = arbre_new.getroot()
    root_old = arbre_old.getroot()

    # Puis on se place dans le premier niveau (en dur pour l'instant, implémentation de manière dynamique plus tard)
    gom1 = root_new[0][0]
    gom2 = root_old[0][0]

    # Boucle pour ajouter à une liste toute les classes du premier niveau du fichier récent
    for enfant in gom1 :
        class_name = enfant.get("class-name")
        elements_new.append(class_name)

    # Boucle pour ajouter à une liste toute les classes du premier niveau du fichier ancien
    for enfant2 in gom2 :
        class_name = enfant2.get("class-name")
        elements_old.append(class_name)

    for n in range(max(len(elements_new),len(elements_old))): # On parcours autant de fois que le max de la longueur d'un des deux fichiers, pour : éviter certains problèmes d'index et éviter d'avoir besoin d'une condition d'arrêt propre
        if len(elements_new) - 1 <= n and len(elements_old) > n: # Si un des deux fichiers est arrivé à sa fin, on ne peut plus appeler element[n], on crée donc une condition pour appeler element[-1]
            ecart_index_new-=1 # Selon le fichier arrivé à sa fin, à chaque entrée dans cette boucle (normalement depuis la première entrée dans la boucle jusqu'à la fin du fichier), on ajoute -1 à l'écart index pour que les premières comparaisons ne renvoient pas une erreur
            print("Fin nouveau fichier")
            if elements_new[-1] == elements_old[n+ecart_index_old]: # On répète alors les comparaisons et affichages
                #print("Classe " + str(elements_old[n+ecart_index_old]) + " identique dans le nouveau et l'ancien fichier")
                #print("Parcours des noms des objets de la classe " + str(elements_old[n+ecart_index_old])+ " et affichage des potentielles différences.\n")
                xmlParserName(str(elements_old[n+ecart_index_old])) # A chaque fois que les fichiers sont identiques on va appeler la fonction de parsing mais qui va parser les noms ("nom") et non pas la classe ("class-name"). Son fonctionnement reste identique à cette fonction de parsing par classes
            else :
                print("Différence : " + str(elements_new[-1]) + " dans nouveau fichier et " + str(elements_old[n+ecart_index_old]) + " dans ancien fichier") # Si les classes sont différentes, pas besoin d'appeler la fonctiona de parsing par nom, puisqu'on sait déjà qu'initialement la classe n'existe pas dans un des deux fichiers, et donc son contenu également
                diff = True
        elif len(elements_new) > n and len(elements_old) - 1 <= n: # Idem dans le cas si l'autre fichier est arrivé à sa fin
            ecart_index_old -= 1
            print("Fin ancien fichier")
            if elements_old[-1] == elements_new[n+ecart_index_new]:
                print("Classe " + str(elements_new[n+ecart_index_new]) + " identique dans le nouveau et l'ancien fichier")
                #print("Parcours des noms des objets de la classe " + str(elements_new[n + ecart_index_new]) + " et affichage des potentielles différences.\n")
                xmlParserName(str(elements_new[n + ecart_index_new])) # Ainsi, à chaque détéction d'égalité, on appelle la fonction de comparaisons de noms
            else:
                print("Différence : " + str(elements_new[n+ecart_index_new]) + " dans nouveau fichier et " + str(elements_old[-1]) + " dans ancien fichier")
                diff = True
        elif len(elements_new) <= n and len(elements_old) <= n:
            print("Fin des deux fichiers")
            if elements_new[-1] == elements_old[-1]:  # On répète alors les comparaisons et affichages
                #print("Classe " + elements_old[-1] + " identique dans le nouveau et l'ancien fichier")
                #print("Parcours des noms des objets de la classe " + str(elements_new[n + ecart_index_new]) + " et affichage des potentielles différences.\n")
                xmlParserName(str(elements_old[-1]))
            else:
                print("Différence : " + str(elements_new[-1]) + " dans nouveau fichier et " + str(elements_old[-1]) + " dans ancien fichier")
                diff = True
        elif elements_new[n+ecart_index_new] == elements_old[n+ecart_index_old]: # Si les éléments sont identiques, on l'affiche
            #print("Classe "+str(elements_new[n+ecart_index_new])+" identique dans le nouveau et l'ancien fichier")
            #print("Parcours des noms des objets de la classe " + str(elements_new[n + ecart_index_new]) + " et affichage des potentielles différences.\n")
            xmlParserName(str(elements_new[n + ecart_index_new]))
        elif elements_old[n+ecart_index_old] != elements_new[n+ecart_index_new]: # Si ils sont différents, on va regarder chaque élément à l'indice n+1 pour ajuster la suite du parcours
            if elements_old[n+1+ecart_index_old] == elements_new[n+1+ecart_index_new] : # Si un des éléments n+1 et égal à l'élément actuel n, alors on va ajouter -1 à l'écart index, ce qui va permettre de faire stagner l'élément, en attendant que l'autre lui soit égal. De cette manière le parcours est "ajusté"
                print("Différence : " + str(elements_new[n+ecart_index_new]) + " dans nouveau fichier et " + str(elements_old[n+ecart_index_old]) + " dans ancien fichier")
                ecart_index_new -= 1
                diff = True
            elif elements_old[n] == elements_old[n+1]: # Idem
                print("Différence : " + str(elements_new[n+ecart_index_new]) + " dans nouveau fichier et " + str(elements_old[n+ecart_index_old]) + " dans ancien fichier")
                ecart_index_old -=1
                diff = True

def xmlParserName(class_name):
    elements_new2 = []
    elements_old2 = []

    ecart_index_new2 = 0
    ecart_index_old2 = 0

    # --> Implémentation future, défini en dur pour l'instant
    # fichier_new = sys.argv[1]
    # fichier_old = sys.argv[2]

    # ATTENTION : Ajuster le nom des fichiers selon ceux présents dans le dossier
    fichier_new2 = "ccmar_cuers-skeleton-cmoip_new.xml"
    fichier_old2 = "ccmar_cuers-skeleton-cmoip.xml"

    arbre_new2 = ET.parse(fichier_new2)
    arbre_old2 = ET.parse(fichier_old2)

    # On récupère les deux racines
    root_new2 = arbre_new2.getroot()
    root_old2 = arbre_old2.getroot()

    # Puis on se place dans le deuxième niveau cette fois ci, puisqu'on va comparer les noms et non pas les class-name
    gom3 = root_new2[0][0]
    gom4 = root_old2[0][0]

    # Boucle qui va chercher chaque objet (donc chaque élément commencant par fv) dont la classe correspond à celle entrée en argument. Cela permet d'obtenir tous les objets d'une seule classe pour isoler et sectionner le traitement
    for enfant in gom3.iter():
        if enfant.get("class-name") == class_name:
            for a in enfant.findall("fv"):
                elements_new2.append(a.get("nom"))

    for enfant in gom4.iter():
        if enfant.get("class-name") == class_name:
            for b in enfant.findall("fv"):
                elements_old2.append(b.get("nom"))

    for m in range(max(len(elements_new2),len(elements_old2))):
        if len(elements_new2) - 1 <= m and len(elements_old2) > m:
            ecart_index_new2 -= 1
            print("Fin nouveau fichier")
            if elements_new2[-1] == elements_old2[m + ecart_index_old2]:
                #print("Nom : " + str(elements_old2[m + ecart_index_old2]) + " identique dans le nouveau et l'ancien fichier") # Si les fichiers sont identiques...
                #print("Parcours des valeurs des objets de la classe " + str(elements_new2[-1]) + " et affichage des potentielles différences.\n")
                xmlParserVal(str(elements_new2[-1])) # On va cette fois-ci appeler la fonction de comparaison par valeur. Son fonctionnement est identique des deux autres fonctions, seule l'instance de comparaison change
            else:
                #print("Différence : " + str(elements_new2[-1]) + " dans nouveau fichier et " + str(elements_old2[m + ecart_index_old2]) + " dans ancien fichier") # Si différence il y a, pas d'appel de fonction, puisqu'on sait déjà que l'instance est différente, pas besoin de comparer "l'intérieur" de l'objet
                diff = True
        elif len(elements_new2) > m and len(elements_old2) - 1 <= m:
            ecart_index_old2 -= 1
            print("Fin ancien fichier")
            if elements_old2[-1] == elements_new2[m + ecart_index_new2]:
                print("Nom : " + str(elements_old2[-1]) + " identique dans le nouveau et l'ancien fichier")
                #print("Parcours des valeurs des objets de la classe " + str(elements_old2[-1]) + " et affichage des potentielles différences.\n")
                xmlParserVal(str(elements_old2[-1]))
            else:
                print("Différence : " + str(elements_new2[m + ecart_index_new2]) + " dans nouveau fichier et " + str(elements_old2[-1]) + " dans ancien fichier")
                diff = True
        elif len(elements_new2) <= m and len(elements_old2) <= m:
            print("Fin des deux fichiers")
            if elements_new2[-1] == elements_old2[-1]:
                print("Nom : " + str(elements_old2[m + ecart_index_old2]) + " identique dans le nouveau et l'ancien fichier")
                #print("Parcours des valeurs des objets de la classe " + str(elements_new2[-1]) + " et affichage des potentielles différences.\n")
                xmlParserVal(str(elements_old2[-1]))
            else:
                print("Différence : " + str(elements_new2[-1]) + " dans nouveau fichier et " + str(elements_old2[-1]) + " dans ancien fichier")
                diff = True
        elif elements_new2[m + ecart_index_new2] == elements_old2[m + ecart_index_old2]:
            print("Nom : " + str(elements_old2[m + ecart_index_old2]) + " identique dans le nouveau et l'ancien fichier")
            #print("Parcours des valeurs des objets de la classe " + str(elements_new2[m + ecart_index_new2]) + " et affichage des potentielles différences.\n")
            xmlParserVal(str(elements_old2[m + ecart_index_old2]))
        elif elements_old2[m + ecart_index_old2] != elements_new2[m + ecart_index_new2]:
            if elements_old2[m + ecart_index_old2] == elements_new2[m + 1 + ecart_index_new2]:
                print("Différence : " + str(elements_new2[m + ecart_index_new2]) + " dans nouveau fichier et " + str(elements_old2[m + ecart_index_old2]) + " dans ancien fichier")
                ecart_index_new2 -= 1
                diff = True
            elif elements_new2[m] == elements_old2[m + 1 + ecart_index_old2]:  # Idem
                print("Différence : " + str(elements_new2[m + ecart_index_new2]) + " dans nouveau fichier et " + str(elements_old2[m + ecart_index_old2]) + " dans ancien fichier")
                ecart_index_old2 -= 1
                diff = True

def xmlParserVal(name):
    elements_new3 = []
    elements_old3 = []

    ecart_index_new3 = 0
    ecart_index_old3 = 0

    # --> Implémentation future, défini en dur pour l'instant
    # fichier_new3 = sys.argv[1]
    # fichier_old3 = sys.argv[2]

    # ATTENTION : Ajuster le nom des fichiers selon ceux présents dans le dossier
    fichier_new3 = "ccmar_cuers-skeleton-cmoip_new.xml"
    fichier_old3 = "ccmar_cuers-skeleton-cmoip.xml"

    arbre_new3 = ET.parse(fichier_new3)
    arbre_old3 = ET.parse(fichier_old3)

    root_new2 = arbre_new3.getroot()
    root_old2 = arbre_old3.getroot()

    # Puis on se place dans le deuxième niveau cette fois ci, puisqu'on va comparer les val et non pas les class-name ni les noms
    gom5 = root_new2[0][0]
    gom6 = root_old2[0][0]

    # Boucle qui va chercher chaque objet (donc chaque élément commencant par fv) dont le nom correspond à celui entré en argument. Cela permet d'obtenir tous les objets d'une seule classe pour isoler et sectionner le traitement
    for enfant in gom5.iter():
        if enfant.get("nom") == name:
            for a in enfant.findall("fv"):
                elements_new3.append(a.get("val"))

    for enfant in gom6.iter():
        if enfant.get("nom") == name:
            for b in enfant.findall("fv"):
                elements_old3.append(b.get("val"))

    for g in range(max(len(elements_new3),len(elements_old3))):
        if len(elements_new3) - 1 <= g and len(elements_old3) > g:
            ecart_index_new3 -= 1
            print("Fin nouveau fichier")
            if elements_new3[-1] == elements_old3[g + ecart_index_old3]:
                print("Valeur : " + str(elements_old3[g + ecart_index_old3]) + " identique dans le nouveau et l'ancien fichier")
            else:
                diff = True
                print("Différence : " + str(elements_new3[-1]) + " dans nouveau fichier et " + str(elements_old3[g + ecart_index_old3]) + " dans ancien fichier")
        elif len(elements_new3) > g and len(elements_old3) - 1 <= g:
            ecart_index_old3 -= 1
            print("Fin ancien fichier")
            if elements_old3[-1] == elements_new3[g + ecart_index_new3]:
                print("Valeur : " + str(elements_old3[g + ecart_index_old3]) + " identique dans le nouveau et l'ancien fichier")
            else:
                diff = True
                print("Différence : " + str(elements_new3[g + ecart_index_new3]) + " dans nouveau fichier et " + str(elements_old3[-1]) + " dans ancien fichier")
        elif (len(elements_new3) <= g and len(elements_old3) <= g):
            print("Fin des deux fichiers")
            if elements_new3[-1] == elements_old3[-1]:
                print("Valeur : " + str(elements_old3[g + ecart_index_old3]) + " identique dans le nouveau et l'ancien fichier")
            else:
                diff = True
                print("Différence : " + str(elements_new3[-1]) + " dans nouveau fichier et " + str(elements_old3[-1]) + " dans ancien fichier")
        elif elements_new3[g + ecart_index_new3] == elements_old3[g + ecart_index_old3]:
            print("Valeur : " + str(elements_old3[g + ecart_index_old3]) + " identique dans le nouveau et l'ancien fichier")
        elif elements_old3[g + ecart_index_old3] != elements_new3[g + ecart_index_new3]:
            if elements_old3[g + ecart_index_old3] == elements_new3[g + 1 + ecart_index_new3]:
                diff = True
                print("Différence : " + str(elements_new3[g + ecart_index_new3]) + " dans nouveau fichier et " + str(elements_old3[g + ecart_index_old3]) + " dans ancien fichier")
                ecart_index_new3 -= 1
            elif elements_new3[g] == elements_old3[g + 1 + ecart_index_old3]:  # Idem
                diff = True
                print("Différence : " + str(elements_new3[g + ecart_index_new3]) + " dans nouveau fichier et " + str(elements_old3[g + ecart_index_old3]) + " dans ancien fichier")
                ecart_index_old3 -= 1


xmlParserClassName()
if diff == True :
    exit(1)
elif diff==False :
    exit(0)
