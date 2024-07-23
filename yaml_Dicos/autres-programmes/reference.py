from pprint import pprint
import sys, os, json, yaml
from pathlib import Path
import logging
from read_excel import convertExeclToDict

def isGlobalSpecificConf(d):
    if len(d) == 1 and ('__Global__' in d or '__Specifique__' in d) or (len(d) == 2 and ('__Global__' in d and '__Specifique__' in d)):
        return True
    else:
        return False

def mergeDict(d1, d2):
    if isGlobalSpecificConf(d1) and isGlobalSpecificConf(d2):
        globalDict = d1.get('__Global__', {})
        globalDict.update(d2.get('__Global__', {}))
        specificDict = d1.get('__Specifique__', {})
        specificDict.update(d2.get('__Specifique__', {}))
        return {
            '__Global__' : globalDict,
            '__Specifique__': specificDict
        }
    elif not isGlobalSpecificConf(d1) and not isGlobalSpecificConf(d2):
        return d1.update(d2)
    else:
        logging.error(f"mergeDict() les dictionnaires sont incohérents")
        return None

def gestionGlobalSpecifique(d):
    listeItems = d.get('__Specifique__')
    confGlobal = d.get('__Global__')
    if confGlobal == None:
        confGlobal = {}
    if not listeItems:
        logging.error(f"gestionGlobalSpecifique() : la clé '__Specifique__' ne contient rien")
        return None
    #print("==============   GLOBAL   ===============")
    #pprint(confGlobal)
    #print("============== SPECIFIQUE ===============")
    #pprint(listeItems)
    #print("=========================================")
    dict_result = {}
    for nomItem, item in listeItems.items():
        item_result = {}
        #print("==============   1   ===============")
        #pprint(item_result)
        #pprint(confGlobal)
        item_result.update(confGlobal)
        #print("==============   2   ===============")
        #pprint(item_result)
        item_result.update(item)
        #print("==============   3   ===============")
        #pprint(item_result)
        dict_result[nomItem] = item_result
    #pprint(dict_result)
    #print("==============   dict_result   ===============")
    #pprint(dict_result)
    return dict_result

def lireFichierYamlJson(nomFichier: str) -> dict:
    """lecture d'un fichier yaml ou json
    
    La lecture est brute, il n'y a aucune interprétation du fichier

    Args:
        nomFichier (str): nom du fichier

    Returns:
        dict: contenu du fichier sous la forme d'un dictionnaire
    """
    logging.debug(f"lireFichierYamlJson() : file={nomFichier}")
    configData = {}
    fileDescr = Path(nomFichier)
    #print(f"lireFichierYamlJson() : nomFichier={nomFichier} exists={fileDescr.exists()}")
    if fileDescr.exists():
        if fileDescr.is_file():
            suffix = fileDescr.suffix
            logging.debug(f"lireFichierYamlJson() : file={nomFichier} suffix={suffix}")
            with open(nomFichier, encoding="utf-8") as yamlJson_file:
                try:
                    if suffix in ['.yaml', '.yml']:
                        configData = yaml.safe_load(yamlJson_file)
                        #print(f"lireFichierYamlJson() : nomFichier={nomFichier} configData={configData}")
                        #configData = yaml.load(yamlJson_file)
                    elif suffix in ['.json', '.jsn']:
                        configData = json.load(yamlJson_file)
                    else:
                        logging.error(f"lireFichierYamlJson() nomFichier={nomFichier} suffix=[{suffix}] inconnu")
                except ValueError as e:
                    configData = None
                    logging.error(f"lireFichierYamlJson() : YAML/JSON object issue: error=[{e}]")
        else:
            logging.error(f"lireFichierYamlJson() : {nomFichier} fichier non lisible")
    else:
        logging.warning(f"lireFichierYamlJson() : {nomFichier} fichier absent")
    return configData

def lireTabFichiers(tabFichier, configFileDir=None, libelle='-'):
    """lecture d'un fichier ou d'un ensemble de fichiers yaml ou json,
    ou d'un fichier excel

    Args:
        tabFichier (str | list): fichier d'entrée
        
        soit un nom de fichier,
        soit un tableau de noms de fichiers,
        soit un tableau décrivant une feuille d'un fichier excel :
        - 'XLSX' pour indiquer que c'est un fichier excel qu'il faut lire
        - nom du fichier excel
        - nom ou numéro de la feuille
        - transpose (booléen) true pour un fichier organisé en ligne
        - nb colonnes de gauche (avant transpose) à ignorer
        - nb de lignes du haut (avant transpose) à ignorer
        
        configFileDir (_type_, optional): emplacement du ou des fichiers,
        si None répertoire courant. Defaults to None.
        
        libelle (str, optional): texte pour les logs. Defaults to '-'.

    Returns:
        _type_: _description_
    """
    if not isinstance(tabFichier, list):
        fichier = tabFichier
        tabFichier = [fichier]
    listeItems = None
    logging.info("lireTabFichiers() tabFichier={} configFileDir={}".format(tabFichier, configFileDir))
    if configFileDir:
        pathConfigFileDir = Path(configFileDir)
    else:
        pathConfigFileDir = Path.cwd()
    #print("pathConfigFileDir={} type={}".format(pathConfigFileDir, type(pathConfigFileDir)))
    logging.info(f"lireTabFichiers(tabFichier=[{tabFichier}], libelle=[{libelle}])")
    if tabFichier[0] == "XLSX":
        if len(tabFichier) == 6:
            fichier = pathConfigFileDir / tabFichier[1]
            feuilles = tabFichier[2]
            transpose = tabFichier[3]
            nbColonnesAIgnorer = tabFichier[4]
            nbLignesAIgnorer = tabFichier[5]
            logging.info("fichier={} feuilles={} transpose={} nbColonnesAIgnorer={} nbLignesAIgnorer={} ".format(fichier, feuilles, transpose, nbColonnesAIgnorer, nbLignesAIgnorer))
            if not isinstance(feuilles, list):
                feuille = feuilles
                feuilles = [feuille]
            listeItems = {}
            for feuille in feuilles:
                newListeItems = convertExeclToDict(fileName=fichier, sheetName=feuille, transpose=transpose, nbColonnesAIgnorer=nbColonnesAIgnorer, nbLignesAIgnorer=nbLignesAIgnorer)
                listeItems.update(newListeItems)
        else:
            logging.error("lireTabFichiers() {} contient {} éléments : il en faut 6".format(tabFichier, len(tabFichier)))
    else:
        for fichier in tabFichier:
            logging.debug(f"lireTabFichiers() fichier=[{fichier}]")
            # for file in tabFichier:
                
            #     logging.info(f"lireTabFichiers() : p={p} file={file}")
            #     fileName = p / file
            #     logging.info(f"lireTabFichiers() : file={file}")
            #     if len(file) > 0:
            #         if not Path(fileName).is_file:
            #             logging.error(f"lireTabFichiers() {libelle} {fileName} fichier non lisible")
            #             return None
            #         else:
            #             tabPathFilenames.append(Path(fileName))
            #     else:
            #         logging.info(f"lireTabFichiers() {libelle} clé vide")
            #         return None
            if fichier != None:
                if type(fichier is not Path):
                    #print("pathConfigFileDir={} type={} isinstance={}".format(pathConfigFileDir, type(pathConfigFileDir), isinstance(pathConfigFileDir, Path)))
                    #print("fichier={} type={} isinstance={}".format(fichier, type(fichier), isinstance(fichier, Path)))
                    fichier = pathConfigFileDir / fichier
                if fichier.suffix in [".json", ".jsn", '.yaml', '.yml']:

                    newItems = lireFichierYamlJson(fichier)
                    # if (libelle == '1301_mg2s.IFarCexSnmp'):
                    #     pprint(f"{fichier}--->listeItems={listeItems}")
                    #     pprint(f"{fichier}--->newItems={newItems}")
                    #     print('------------------------------------------------------------------------')
                    if not newItems:
                            # le fichier est vide
                            logging.error(f"lireTabFichiers() : libelle=[{libelle}] fichier={fichier} non trouvé")
                    elif listeItems:
                        if isinstance(newItems, list):
                            listeItems = listeItems + newItems
                        elif isinstance(newItems, dict):
                            #listeItems.update(newItems)
                            #print(f"lireTabFichiers() libelle={libelle}")
                            mergeDict(listeItems, newItems)
                        else:
                            logging.error(f"lireTabFichiers() : libelle=[{libelle}] fichier={fichier} type inconnu={type(newItems)}")
                    else:
                        # 1er tour de boucle
                        listeItems = newItems
                else:
                    logging.error(f"lireTabFichiers() : fichier={fichier} -> libelle=[{libelle}] extension inconnue=[{fichier.suffix}]")
    return listeItems

def chercherImport(listeItems):
    if isinstance(listeItems, dict):
        pass

def priseEnCompteImport(listeItems):
    pass

def dataToInclude(contenuCleInclure: str | list | dict, configFileDir:str = None) -> dict:
    # 3 possibilités en fonction du type de 'donneesAInclure' :
    #   str     => c'est le nom d'un fichier et on inclut le contenu
    #   dict    => clés 'fichier' et 'cle"
    #   list    => doit contenir 2 éléments le nom du fichier et la clé
    data = {}
    fichierAInclure = None
    cleAInclure = None
    if isinstance(contenuCleInclure, str):
        fichierAInclure = contenuCleInclure
        cleAInclure = ''        # chaine vide pour indiquer qu'il faut prendre tout le fichier
    elif isinstance(contenuCleInclure, dict):
        fichierAInclure = contenuCleInclure.get('fichier')
        cleAInclure = contenuCleInclure.get('cle')
    elif isinstance(contenuCleInclure, list):
        if len(contenuCleInclure) == 2:
            fichierAInclure = contenuCleInclure[0]
            cleAInclure = contenuCleInclure[1]
    else:
        logging.error("dataToInclude() le contenu de la clé {} n'est pas exploitable type={} contenu={}".format('__Inclure__', type(contenuCleInclure), contenuCleInclure))
    #print("dataToInclude() : contenuCleInclure={}".format(contenuCleInclure))
    if fichierAInclure != None and cleAInclure != None:
        if fichierAInclure != '':
            dataFichier = configItemsGenerique(fichier=fichierAInclure, configFileDir=configFileDir)
            if cleAInclure:
                data = dataFichier.get(cleAInclure)
            else:
                data = dataFichier
        else:
            logging.error("dataToInclude() fichier à inclure vide contenuCleInclure={} ".format(contenuCleInclure))
    else:
        logging.error("dataToInclude() pb avec la clé contenuCleInclure={} fichierAInclure={} cleAInclure={}".format(contenuCleInclure, fichierAInclure, cleAInclure))
    return data

def gestionInclude(data, configFileDir=None):
    logging.debug("gestionInclude() data={}".format(data))
    #p = Path.cwd()
    #print ("répertoire courant={}".format(p))
    if type(data) is dict:
        
        #print("==== dict ====")
        if '__Inclure__' in data:
            cle = '__Inclure__'
        elif '__Include__' in data:
            cle = '__Include__'
        elif '__inclure__' in data:
            cle = '__inclure__'
        elif '__include__' in data:
            cle = '__include__'
        else:
            cle = None
        if cle:
            #print("==== __Inclure__ ====")
            donneesAInclure = data.pop(cle)
            logging.debug("gestionInclude() donneesAInclure={}".format(donneesAInclure))
            originalData = data
            data = dataToInclude(contenuCleInclure=donneesAInclure, configFileDir=configFileDir)
            
            data.update(originalData)
        
        for nomElement, element in data.items():
            #print("appel récursif dans élément du dictionnaire={}".format(nomElement))
            data[nomElement] = gestionInclude(data=element, configFileDir=configFileDir)
    elif type(data) is list:
        # on ne prend pas en compte les "inclure" dans les tableaux
        for element in data:
            #print("appel récursif dans élément du tableau")
            element = gestionInclude(data=element, configFileDir=configFileDir)
    return data

def configItemsGenerique(fichier, configFileDir=None, libelle="-") -> dict[str, dict]:
    """ convertit les fichiers xlsx, yaml ou json passés en paramètre
    
        prend en charge :
        - une liste de fichiers, auquel cas les dictionnaires correspondants sont mergés
        - les clés particulières __Global__ / __Specifique__
        - la clé __Inclure__

    Args:
        fichier (str ou list): nom du fichier yaml ou json à charger, ou liste de noms
        libelle (str, optional): texte utilisé dans les logs ;
            par exemple mettre la clé ayant servi à récupérer la liste de noms de fichiers.
            Defaults to "-".

    Returns:
        dict[str, dict]: dictionnaire constitué du contenu des fichiers passés en entrée
    """
    logging.debug("configItemsGenerique() : fichier={}, libelle={}".format(fichier, libelle))
    if type(fichier) is list:
        tabFichier = fichier
    else:
        tabFichier = []
        if type(fichier) is str:
            tabFichier.append(fichier)
    if len(tabFichier) == 0:
        logging.error("configItemsGenerique() : Impossible lire fichier={}".format(fichier))
        return {}
    # if not listeItems:
    #     listeItems = {}
    listeItems = lireTabFichiers(tabFichier=tabFichier, configFileDir=configFileDir, libelle=libelle)
    if not listeItems:
        return {}
    if len(listeItems) == 1 and '__parSites__' in listeItems:
        logging.warning("pour la clé={cle} structure __parSites__ activée".format(cle=libelle))
    if listeItems:
        logging.debug("lireTabFichiers() listeItems={}".format(listeItems))
        logging.debug("lireTabFichiers() len(listeItems)={}".format(len(listeItems)))
        #print(listeItems)
        listeItems = gestionInclude(data=listeItems, configFileDir=configFileDir)
        if isGlobalSpecificConf(listeItems):
            # if 'AIRBUS' in listeItems['__Specifique__']:
            #     print("&&&&&&&&&&&&&&&&&")
            #     pprint(listeItems['__Specifique__']['AIRBUS'])
            #     print("&&&&&&&&&&&&&&&&&")
            listeItems = gestionGlobalSpecifique(listeItems)
            # print("???????????")
            # pprint(listeItems)
            # print("???????????")
    else:
        logging.error(f"lireTabFichiers() : libelle=[{libelle}] rien à lire")
    #pprint(f"listeItems={listeItems}")
    #listeItems = priseEnCompteImport(listeItems)
    # if '__Import__' in 
    return listeItems

if __name__ == "__main__":

    logginLevel = logging.DEBUG
    p = Path.cwd()
    print ("répertoire courant={}".format(p))
    logging.basicConfig(level=logginLevel, format="%(asctime)s - %(levelname)s - %(message)s")
    confMngr = configItemsGenerique(fichier='fichiersTest/testInclure.yaml')
    if confMngr:
        #print("getFilenameFromKey(key='roles') -> {}".format(confMngr.getFilenameFromKey(key="roles")))
        #pprint("configGlobale={}".format(confMngr.getConfigGlobale()))
        pprint(confMngr)
        print ("fin")
    else:
        print ("erreur")