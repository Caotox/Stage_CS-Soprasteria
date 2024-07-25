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

Dans le fichier template, le format est :
nom_de_la_classe : chemin depuis le répertoire où le programme s'exécute vers le fichier template correspondant
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

