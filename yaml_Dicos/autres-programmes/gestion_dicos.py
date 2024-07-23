dico = {"1": "2", "3": "4","val":{"t1":"v2976","t2":"v2"},"temp":{"t6":"v2673","t7":"v7"}}
dico2 = {"1":"2","3":"4","val":{"t1":"v3","t2":"v4","t3":"v0"},"temp":{"t6":"v6","t7":"v7","t8":"v8"}}

ecart = 0

temp=[]
# Doit pouvoir update les dicos de manière à ce que dico soit prioritaire mais si dico 2 présente
# certains éléments (clés) non présents dans dico ils doivent être inclus.
# Mais les valeurs qui priment pour toute autre clé présente dans les deux dicos il faut que dico
# soit prioritaire et donc que dico2 soit écrasé
if dico==dico2:
    pass
elif dico!=dico2:
    for n, v in dico2.items():
        if type(n) == dict or type(v) == dict:
            for i in dico2[n] :
                if i not in dico[n] :
                    temp.append(n)
                    temp.append(v)
for j in range (len(temp)//2):
    if len(temp) == 0:
        pass
    elif ecart + 2 > len(temp):
        pass
    elif str(dico2[temp[0]]) not in dico:
        for p in temp[1+ecart].keys():
            if p in dico[temp[0+ecart]].keys() :
                dico[temp[0 + ecart]][p]=dico[temp[0 + ecart]][p]
            elif p not in dico[temp[0+ecart]].keys():
                dico[temp[0 + ecart]][p] = dico2[temp[0 + ecart]][p]
        ecart += 2

print(temp)

dico3 = {"__Include__" : 1, "var1":1,"var2":2,"__Inclure__":3,"var3":4,"__include__":{"var7":7,"__inclure__":12}}

def parcours(attribs, dico3, a=0):
    for n, v in dico3.items():
        if n in attribs:
            a += 1
        if isinstance(v, dict):  # Vérifier si la valeur est un dictionnaire
            a = parcours(attribs, v, a)  # Appeler récursivement la fonction sur le sous-dictionnaire
    return a

# Liste des clés à détecter
attribs = ["__Include__", "__Inclure__", "__include__", "__inclure__"]

print(parcours(attribs, dico3))


def gestionInclude(data, configFileDir=None):
    logging.debug("gestionInclude() data={}".format(data))
    # p = Path.cwd()
    # print ("répertoire courant={}".format(p))
    ecart = 0
    temp = []
    if type(data) is dict:

        # print("==== dict ====")
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
            # print("==== __Inclure__ ====")
            donneesAInclure = data.pop(cle)
            logging.debug("gestionInclude() donneesAInclure={}".format(donneesAInclure))
            originalData = data
            data = dataToInclude(contenuCleInclure=donneesAInclure, configFileDir=configFileDir)
            if originalData == data:
                pass
            elif originalData != data:
                for n, v in data.items():
                    if type(n) == dict or type(v) == dict:
                        for i in data[n]:
                            if i not in originalData[n]:
                                temp.append(n)
                                temp.append(v)
            for j in range(len(temp) // 2):
                if len(temp) == 0:
                    pass
                elif ecart + 2 > len(temp):
                    pass
                elif str(data[temp[0]]) not in originalData:
                    for p in temp[1 + ecart].keys():
                        if p in originalData[temp[0 + ecart]].keys():
                            originalData[temp[0 + ecart]][p] = originalData[temp[0 + ecart]][p]
                        elif p not in originalData[temp[0 + ecart]].keys():
                            originalData[temp[0 + ecart]][p] = data[temp[0 + ecart]][p]
                    ecart += 2

            data.update(originalData)

        for nomElement, element in data.items():
            # print("appel récursif dans élément du dictionnaire={}".format(nomElement))
            data[nomElement] = gestionInclude(data=element, configFileDir=configFileDir)
    elif type(data) is list:
        # on ne prend pas en compte les "inclure" dans les tableaux
        for element in data:
            # print("appel récursif dans élément du tableau")
            element = gestionInclude(data=element, configFileDir=configFileDir)
    return data



print(dico2)
print(dico)