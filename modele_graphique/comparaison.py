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
