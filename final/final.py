"""
Doc :
Programmes contenus dans le module :
- Comparaison de fichiers XML
Fonction : xml_compare(fichier_new, fichier_old)
Argument 1 (fichier_new) : fichier XML récent
Argument 2 (fichier_old) : fichier XML ancien

- Affichage de fichiers XML
Fonction 1 : modele(fichier, attribut_modele, valeur_modele) --> Récupération d'un modèle graphique
Argument 1 (fichier) : fichier XML
Argument 2 (attribut_modele) : attribut à comparer (class-name, nom, id...)
Argument 3 (valeur_modele) : valeur de cet attribut (cmoIP.exemple, VGoIP.Equipement...)

Fonction 2 : graphique(noeud_racine, arguments, attribut, parametre) --> Affichage personnalisé
Argument 1 (noeud_racine) : élément sur lequel va porter le parcours (exemple : fichier_XML, ou modele graphique)
Argument 2 (arguments) : valeur de l'attribut recherché (comoIP.exemple, VGoIP.Equipement...)
Argument 3 (attribut) : attribut à comparer (class-name, nom, id...)
Argument 4 (parametre) : parametre qui va définir le type de parcours et d'affichage
Exemple d'utilisation :
modele_test=modele(exemple.xml, class-name, cmoIP.ISiteConfig)
graphique(modele_test, comoIP.ISiteConfigExterne, class-name, -c)

- Comparaison du fichier squelette et des fichiers templates associés
Fonction :
Argument 1 (squelette) : fichier squelette
Argument 2 (yamlfile) : fichier YAML

- Autres ? (- création d'un fichier XML à partir de certains éléments issus d'un fichier XML d'origine
            - fichier de gestion de fichiers YAML)
"""


#################################### COMPARE ##############################################

import xml.etree.ElementTree as ET
from lxml import etree
import sys
import time
import logging
from typing import Generator, Tuple
from enum import Enum
from infosClasses import numeros_de_classe, classes_a_exclure
from pprint import pprint

def xml_compare(fichier_new, fichier_old):
    listeClassesExclues = []
    listeClassesAjoutees = []
    listeClassesSupprimees = []
    modificationsClasse = []
    modificationsAjoutsClasse = []
    modificationsSuppressionsClasse = []
    listeModifications = {}
    verbose = False


    class CompareResult(Enum):
        EGAL = 0
        ADD = 1
        SUPPR = 2
        INC = 3


    def verbosePrint(texte: str):
        global verbose
        if verbose:
            print(texte)


    def getAttribFromTag(tag: str) -> str:
        if tag == 'obj':
            attrib = 'class-name'
        elif tag == 'fv':
            attrib = 'nom'
        elif tag == 'a':
            attrib = 'i'
        return attrib


    def compareElement(element_new: ET.Element, element_old: ET.Element, attrib: str) -> Tuple[str, str, str, bool, bool]:
        result = '?'
        texte = "--------"
        if element_new is not None and element_old is not None:
            # on a obtenu 1 element dans new et dans old
            tagValueNew = element_new.tag
            tagValueOld = element_old.tag
            if tagValueNew != tagValueOld or tagValueNew is None:
                return '?', None, None, None, None
            attrib = getAttribFromTag(tag=tagValueNew)
            attribValue_new = element_new.get(attrib)
            attribValue_old = element_old.get(attrib)
            # print(f"compareElement() attrib={attrib} {attribValue_new} <--> {attribValue_old}")
            if attribValue_new == attribValue_old:
                result = '='
                texte = f""
                # compareLevel(element_new, element_old, path=f"{path} / {attribValue_new}", attrib='nom')
                attribValue = attribValue_new
                get_new = True
                get_old = True
            elif attribValue_new > attribValue_old:
                result = 's'
                texte = "--> supprimé"
                attribValue = attribValue_old
                get_new = False
                get_old = True
            elif attribValue_new < attribValue_old:
                result = 'a'
                texte = "--> ajouté"
                attribValue = attribValue_new
                get_new = True
                get_old = False
        elif element_new is not None:
            result = 'a'
            tagValueNew = element_new.tag
            attrib = getAttribFromTag(tag=tagValueNew)
            attribValue_new = element_new.get(attrib)
            texte = "--> ajouté"
            attribValue = attribValue_new
            get_new = True
            get_old = False
        elif element_old is not None:
            result = 's'
            tagValueOld = element_old.tag
            attrib = getAttribFromTag(tag=tagValueOld)
            attribValue_old = element_old.get(attrib)
            texte = "--> supprimé"
            attribValue = attribValue_old
            get_new = False
            get_old = True
        else:
            result = '?'
            return '?', None, None, None, None
        logging.info(
            f"compareElement() : result={result}, texte={texte}, attribValue={attribValue}, get_new={get_new}, get_old={get_old}")
        return result, texte, attribValue, get_new, get_old


    def iterOneLevelXml(tree: ET.Element) -> Generator[ET.Element, None, None]:
        # doc = ET.parse(file)
        # root = doc.getroot()
        # objectmodel = root[0][0]

        for element in tree:
            # print(f"iterOneLevelXml() tag={element.tag} classname={element.get('class-name')} nom={element.get('nom')}")
            yield element


    def compareLevel(tree_new, tree_old, attrib, path, level, nomClasse):
        global listeClassesExclues, listeClassesAjoutees, listeClassesSupprimees, listeModifications
        global modificationsClasse, modificationsAjoutsClasse, modificationsSuppressionsClasse

        generator_new = iterOneLevelXml(tree_new)
        generator_old = iterOneLevelXml(tree_old)
        get_new = True
        get_old = True
        while True:
            if get_new:
                try:
                    element_new = next(generator_new)
                    # print(f"NEW --> tag={element_new.tag} class-name={element_new.get(attrib)}")
                except StopIteration:
                    # print("FIN_new")
                    element_new = None
            if get_old:
                try:
                    element_old = next(generator_old)
                    # print(f"OLD --> tag={element_old.tag} class-name={element_old.get(attrib)}")
                except StopIteration:
                    # print("FIN_old")
                    element_old = None
            if element_new is None and element_old is None:
                break

            result, texte, attribValue, get_new, get_old = compareElement(element_new, element_old, attrib)
            logging.info(f"result={result}, texte={texte}, attribValue={attribValue}, get_new={get_new}, get_old={get_old}")

            if level == 0:
                nomClasse = attribValue
                verbosePrint("")
                verbosePrint(f"===== {attrib} = {nomClasse} [{numeros_de_classe.get(nomClasse)}] =====")
                if nomClasse in classes_a_exclure:
                    verbosePrint("--------> IGNOREE")
                    listeClassesExclues.append(nomClasse)
                    continue

            if path == '':
                textePath = f'{attribValue}'
            else:
                textePath = f"{path} / {attribValue}"

            if result == 'a':
                ### AJOUT ###
                logging.info(f"AJOUT    {attrib} {attribValue} {element_new.get(attrib)}")
                if level == 0:
                    # on est au premier niveau  => ajout de classe
                    listeClassesAjoutees.append(nomClasse)
                    verbosePrint(f"CLASSE {texte}")
                else:
                    modificationsClasse.append(f"{textePath} {texte}")
                    modificationsAjoutsClasse.append(textePath)
                    verbosePrint(f"{textePath} {texte}")
            elif result == 's':
                ### SUPPRESSION ###
                logging.info(f"SUPPR    {attrib}  {attribValue} {element_old.get(attrib)}")
                if level == 0:
                    listeClassesSupprimees.append(nomClasse)
                    verbosePrint(f"CLASSE {texte}")
                else:
                    modificationsClasse.append(f"{textePath} {texte}")
                    modificationsSuppressionsClasse.append(textePath)
                    verbosePrint(f"{textePath} {texte}")
            elif result == '=':
                logging.info(f"EGAL    {attrib}  {attribValue}")
                # print(texte)
            elif result == '?':
                verbosePrint(f"???? result={result} attrib={attrib}  attribValue={attribValue} ")
                # print(texte)
            else:
                logging.warning(f"???? result={result}   attrib={attrib}  attribValue={attribValue} ")
            if element_new is None:
                lg = '--'
            else:
                lg = len(element_new)
            # print(f"compareLevel(attrib={attrib}, path={path}, level={level}) result={result}, texte={texte}, attribValue={attribValue}, get_new={get_new}, get_old={get_old} len(element_new)={lg}")
            if result == '=' and len(element_new) > 0:
                logging.info(f"EGAL => compareLevel()    {attrib}  {attribValue}")
                if level == 0:
                    pathForCompare = f""
                    modificationsClasse = []
                    modificationsAjoutsClasse = []
                    modificationsSuppressionsClasse = []
                elif level == 1:
                    pathForCompare = f"{attribValue}"
                else:
                    pathForCompare = f"{path} / {attribValue}"
                compareLevel(element_new, element_old, attrib='nom', path=pathForCompare, level=level + 1,
                             nomClasse=nomClasse)
                if level == 0:
                    if len(modificationsClasse) > 0:
                        listeModifications[nomClasse] = {}
                        listeModifications[nomClasse]['AJOUT'] = modificationsAjoutsClasse
                        listeModifications[nomClasse]['SUPPR'] = modificationsSuppressionsClasse

                    # on a terminé de parcourir toute la classe

        # print("TERMINE")


    def parcours(tree, texte):
        # print(f"DEB parcours() : texte={texte} len={len(tree)}_______________")
        generator = iterOneLevelXml(tree)
        pprint(tree)
        print(f"len(tree)={len(tree)}")
        cpt = 0
        while True:
            try:
                cpt += 1
                element = next(generator)
                # print(f"cpt={cpt} -> {element}")

            except StopIteration:
                # print("FIN_new")
                element = None
                break
            # print(f"cpt={cpt} / {len(tree)} -> {element.get('nom')}")
            if element != None:
                if element.tag == "obj":
                    print(f"CLASS --> {element.get('class-name')} nom={element.get('nom')} {len(element)} éléments")
                elif element.tag == "fv":
                    print(f"ELEMENT --> {element.get('nom')} {len(element)} éléments")
                elif element.tag == "a":
                    print(f"A --> {element.get('nom')} {len(element)} éléments")
                else:
                    print(f"??? [{element.tag}] --> nom={element.get('nom')} {len(element)} éléments")
                # print(f"cpt={cpt} / {len(tree)} -> {element.get('nom')}")
                if len(element) > 0:
                    for item in element:
                        # print(f"boucle for() -> tag={item.tag} nom={item.get('nom')}")
                        pass
                    # print(f"===> parcours")
                    parcours(element,
                             texte=f"parcours() --> tag={element.tag} class-name={element.get('class-name')} nbElements={len(element)}")
                    # print(f"_______________ fin parcours() _______________")
            else:
                print("element=None -> ???")
        # print(f"FIN parcours() : texte={texte} _______________")

    """
    nb_par = len(sys.argv)
    if nb_par not in [2, 3]:
        print("Veuillez inclure les arguments du programme en vous fiant à sa documentation")
        sys.exit()
    """
    nb_par=3

    start_time = time.time()

    #fichier_new = sys.argv[1]
    arbre_new = ET.parse(fichier_new)
    root_new = arbre_new.getroot()
    pprint(root_new)
    gom_new = root_new[0][0]

    if nb_par == 3:
        diff = True
        #fichier_old = sys.argv[2]
        arbre_old = ET.parse(fichier_old)
        root_old = arbre_old.getroot()
        gom_old = root_old[0][0]
        diff = compareLevel(tree_new=gom_new, tree_old=gom_old, attrib='class-name', path='', level=0, nomClasse=None)
    else:
        parcours(tree=gom_new, texte="gom_new")
        diff = True

    end_time = time.time()
    execution_time = end_time - start_time
    print(execution_time)

    print("============= listeClassesExclues =============")
    pprint(listeClassesExclues)
    print("")

    print("============= listeClassesAjoutees =============")
    pprint(listeClassesAjoutees)
    print("")

    print("============= listeClassesSupprimees =============")
    pprint(listeClassesSupprimees)
    print("")

    print("============= listeModifications =============")
    pprint(listeModifications)
    print("")

    if diff:
        exit(1)
    elif not diff:
        exit(0)

###############################################################################################

############################# PARCOURS ET AFFICHAGE ###########################################

import xml.etree.ElementTree as ET

def modele(fichier, attribut_modele, valeur_modele):
    """
    Recherche le modèle graphique avec l'attribut spécifié et renvoie cet élément.

    argument 1 (fichier) : nom du fichier où effectuer le parcours
    argument 2 (attribut_modele) : chaine de caractère correspondant au type d'attribut du modèle recherché ("class-name" par exemple)
    argument 3 (valeur_modele) : valeur de l'attribut du modèle recherché ("cmoIP.Exemple" par exemple)
    """
    racine = fichier.getroot()

    for noeud in racine.iter():
        if noeud.get(attribut_modele) == valeur_modele:
            return noeud

    return None

def graphique(noeud_racine, arguments, attribut, parametre):
    """
    Parcours et affichage d'un fichier de modèle graphique selon le paramètre spécifié

    argument 1 (noeud_racine) : noeud racine où effectuer le parcours
    argument 2 (arguments) : chaine de caractère correspondant à l'attribut recherché ("cmoIP.Exemple" par exemple)
    argument 3 (attribut) : chaine de caractère correspondant au type d'attribut recherché ("class-name" par exemple)
    argument 4 (parametre) : paramètre correspondant au type de parcours, ou à l'opération souhaitée

    Types de parcours :
    -e : Egalité stricte (Equal) - Cherche les éléments dont l'attribut spécifié est exactement égal à l'argument donné.
    -c : Contient (Contain) - Cherche les éléments dont l'attribut spécifié contient l'argument donné, commence par, se termine par ou est égal à l'argument donné.
    -r : Descendants récursifs (Recursive) - Cherche les éléments descendants de manière récursive dont l'attribut spécifié est égal à l'argument donné.
    -p : Parent direct (Parent) - Cherche le parent direct des éléments dont l'attribut spécifié est égal à l'argument donné.
    -s : Frères (Siblings) - Cherche les éléments frères des éléments dont l'attribut spécifié est égal à l'argument donné.
    -a : Ancêtres (Ancestors) - Cherche tous les ancêtres des éléments dont l'attribut spécifié est égal à l'argument donné.
    -nX : Descendants au niveau X (N-level Descendants) - Cherche les descendants au niveau X des éléments dont l'attribut spécifié est égal à l'argument donné.
    """

    liste = []

    def recherche_recursive(noeud):
        """Recherche récursive des éléments descendants avec l'attribut spécifié."""
        for enfant in noeud:
            if attribut == "any" or enfant.get(attribut) == str(arguments):
                liste.append(enfant.attrib)
            recherche_recursive(enfant)

    def descendants_au_niveau(noeud, niveau):
        """Recherche des descendants au niveau X avec l'attribut spécifié."""
        if niveau == 0:
            for enfant in noeud:
                if attribut == "any" or enfant.get(attribut) == str(arguments):
                    liste.append(enfant.attrib)
        else:
            for enfant in noeud:
                descendants_au_niveau(enfant, niveau - 1)

    for noeud in noeud_racine:
        if parametre == "-e":
            if attribut == "any" or noeud.get(str(attribut)) == str(arguments):  # EGALITE STRICTE (EQUAL)
                liste.append(noeud.attrib)
        elif parametre == "-c":
            if attribut == "any" or str(arguments) in str(noeud.get(attribut)) or str(noeud.get(attribut)).startswith(str(arguments)) or str(
                    noeud.get(attribut)).endswith(str(arguments)) or noeud.get(str(attribut)) == str(arguments):
                liste.append(noeud.attrib)
        elif parametre == "-r":
            if attribut == "any" or noeud.get(str(attribut)) == str(arguments):
                recherche_recursive(noeud)
        elif parametre == "-p":
            parent = noeud_racine.find(".//" + noeud.tag + "/..")
            if parent is not None and (attribut == "any" or parent.get(attribut) == str(arguments)):
                liste.append(parent.attrib)
        elif parametre == "-s":
            parent = noeud_racine.find(".//" + noeud.tag + "/..")
            if parent is not None:
                for frere in parent:
                    if frere != noeud and (attribut == "any" or frere.get(attribut) == str(arguments)):
                        liste.append(frere.attrib)
        elif parametre == "-a":
            parent = noeud.find("..")
            while parent is not None:
                if attribut == "any" or parent.get(attribut) == str(arguments):
                    liste.append(parent.attrib)
                parent = parent.find("..")
        elif parametre.startswith("-n"):
            niveau = int(parametre[2:])
            descendants_au_niveau(noeud, niveau)

    print(liste)  # AFFICHAGE

    return

######################################################################################

######################" COMPARAISON CONFORMITE SQUELETTE TEMPLATE #######################

import xml.etree.ElementTree as ET
import sys
import glob
import yaml

"""
Doc :

Compare la conformité des fichiers templates associés à un fichier squelette

Argument 1 : nom du fichier squelette. Exemple : squelette.xml
Argument 2 : nom du fichier yaml. Exemple : srsa.yaml

Exemple d'utilisation : 
python affiche.py squelette.xml srsa.yaml

"""
#squelette = "squelette.xml" # --> A mettre en commentaire si programme en dynamique
#template = "genTempl_propDynPartition.xml"

print("\n") # Meilleur affichage
squelette = sys.argv[1] # --> Enlever le commentaire afin d'utiliser la version "dynamique" du programme. Il faudra aussi mettre l'appel en dur en commentaire
yamlfile = sys.argv[2]

if len(sys.argv) != 3:
    print("Vous devez donner en premier argument le nom du fichier squelette et en deuxième argument le path qui mène aux fichiers templates.")
    sys.exit()

diff=False
def read_yaml_to_dict(yamlfile):  # Fonction de transformation d'un fichier YAML en dictionnaire
    with open(yamlfile, 'r', encoding='utf-8') as file:  # ouverture du fichier YAML
        try:
            yaml_dict = yaml.safe_load(file)  # Transformation en dictionnaire
            return yaml_dict
        except yaml.YAMLError as e:  # Gestion d'erreurs
            print(f"Erreur lors de la lecture du fichier YAML: {e}")
            return None


yaml_dict = read_yaml_to_dict(yamlfile) # Création du dictionnaire

for p in yaml_dict.keys():
    if p == "Exclure" :
        for v in yaml_dict[p].keys():
            print("Classes à exclure : " + v )

print("\n")

arbre1 = ET.parse(squelette) # Ouverture du fichier
# = ET.parse(template)

root1 = arbre1.getroot() # Récupération de la racine (pour le rendre lisible)

root1 = root1[0][0] # On se place au premier niveau
#root2 = arbre2.getroot()

# Différentes listes qui vont ensuites contenir les attributs class-name (L1) et nom (L2 et LT)
L1 = []
L2 = []
LT = []

#nbr_fichiers=0

trouve=False

#for n in root1.iter(): # Parcours de la racine du fichier squelette
for n in root1 :
    #if n.get("class-name") :
    if n.get("class-name") is not None :    # On ne récupère que les éléments ayant un class-name
                                            # sinon cela posera problème lors de l'ouverture des fichiers
                                            # templates à partir des class-name obtenus
        L1.append(n.get("class-name"))      # On ajoute les class-name à une liste

for n in L1 : # n prendra les valeurs de L1 à chaque itération, donc de chaque class-name l'un après l'autre
    for m in root1.iter(): # on parcours encore le fichier cette fois ci pour récupérer
        # les noms propres à une class-name en particulier
        if m.get("class-name") == n :   # Si le class-name de l'élément parcouru est le même que la valeur de n dans L1
                                        # alors on va récupérer les noms car on se trouve dans le class-name
                                        # qui nous intéresse

            for a in m.findall("fv"): # Permet de parcourir les éléments ayant des attributs nom
                L2.append(a.get("nom")) # Récupération et ajout à une autre liste

                for l in a.findall("obj") : # Parcours des objets présents dans l'objet parcouru
                    for k in l.iter():
                        for b in k.findall("fv"):
                            L2.append(b.get("nom")) # Instruction permettant de récupérer l'attribut nom d'un objet
                                                    # étant un enfant de l'élément comparé à l'origine (élément fv)
            for p in m.findall("obj") : # Instruction cette fois ci permettant de récupérer l'attribut nom d'un objet
                                        # se trouvant dans l'objet comparé, au même niveau que ce dernier
                for c in p.iter() :
                    for f in c.findall("fv"):               # Dans les deux cas les instructions de parcours restent les mêmes
                        L2.append(f.get("nom"))
    # permet d'ouvrir le fichier qui contient n dans son nom, n étant la valeur de class-name contenue dans L1
    try : # Si le fichier n'est pas trouvé, cela permet de sortir de la boucle pour passer au prochain class-name
        #fichier =  ET.parse(next(glob.iglob(f".{path}*{n}*.xml")))
        #fichier = ET.parse(next(glob.iglob(f".{var}*{n}*.xml")))

        """ --> Ancienne ouverture des fichiers templates associés
        fichier = ET.parse(next(glob.iglob(f".{path}{n}.xml"))) # On cherche d'abord si le fichier est identique au class-name
        if not fichier : # On continue à chercher tant qu'aucun fichier template n'a été trouvé
            fichier = ET.parse(next(glob.iglob(f".{path}{n}*.xml"))) # Puis si il y a eu un ajout après
            if not fichier :
                fichier =  ET.parse(next(glob.iglob(f".{path}*{n}*.xml"))) # Et enfin si il y a eu un ajout avant et après
                if not fichier :
                    notthere = True
        """
        """ --> Ancienne récupération des attributs "nom" se trouvant dans les fichiers templates respectifs
        for a, w in yaml_dict.items(): # Parcours du dictionnaire (couple clé / valeur)
            if a == n and w != "exclure": # Si la clé correspond à n, donc l'itération du class-name faisant référence à un nom de template
                fichier = ET.parse(a+".xml") # On récupère puis ouvre ce template

        froot = fichier.getroot()# On récupère la racine du fichier ainsi ouvert
        for i in froot.iter():  # On le parcours
            for j in i.findall("fv"):  # Et identiquement au fichier squelette, on récupère les noms du fichiers templates
                #temp = j.get("nom")
                LT.append(j.get("nom"))  # Qu'on ajoute à une liste LT
                # continue
        # --> comparaison parallèle
        #nbr_fichiers=nbr_fichiers+1
        """
        for a,w in yaml_dict["Inclure"].items() : # On parcours les fichiers avec la clé Inclure, pour ne pas traiter les fichiers à exclure
            if a == n : # Si la clé est égale à n donc à l'instance de L1 qui correspond à une classe, donc si a est la classe actuellement traitée
                trouve=True
                fichier=ET.parse(w) # Alors on ouvre le fichier
        rootfile = fichier.getroot() # Et on récupère la racine
        for i in rootfile.iter() : # On parcours ensuite cette racine
            for j in i.findall("fv") : # Parcours des éléments ayant un attribut "nom" qui nous intéresse
                LT.append(j.get("nom")) # On ajoute la valeur de l'attribut dans LT
                for l in j.findall("obj") : # On cherche les objets pour également parcourir leurs éléments
                    for k in l.iter() : # On parcours l'objet
                        for b in k.findall("fv") : # Puis les éléments ayant un attribut nom
                            L2.append(b.get("nom")) # Qu'on ajoute également
            for p in i.findall("obj"): # On répète l'opération pour les objets se trouvant au niveau de la racine, et non pas dans un élément fv
                for c in p.iter() :
                    for f in c.findall("fv") :
                        L2.append(f.get("nom"))
        if trouve == False :
            print("Pour la classe " + n + ", pas de fichiers template associés")
    except :
        # message personnalisé
        # On stop la boucle
        continue

    #print(LT) # Instruction d'affichage des éléments récupérés pour débugage
    #print("\n")
    #print(L2)
    #print("\n")

    for v in L2 : # On compare de chaque côté pour savoir quels éléments sont manquants et de quels côtés
        if v not in LT :
            #print(v+" pas dans le fichier template "+str(n)+".xml .") # Affichage
            print(v+" manquant dans le fichier template "+str(n)+".xml")
            diff=True
    for v in LT :
        if v not in L2 :
            #print(v+" pas dans le fichier squelette " +squelette+".")
            print(v+" en trop dans le fichier template "+str(n)+".xml")
            diff=True
    if diff == False :
        print("template "+str(n)+" identique aux informations du squelette " +squelette+".")
        print("\n")
    # Réinitialisation des listes pour les autres instances, sans ça, les comparaisons se feraient sur tous les
    # éléments initiaux plus ceux qui se sont ajoutés au fur et à mesure et ce jusqu'à la fin du programme. Cela
    # déclencherait aussi une comparaison sur des éléments n'ayant pas de différences
    L2 = []
    LT = []
    trouve=False
    if diff ==True :
        print("\n")

###################################################################################################################
