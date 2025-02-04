# Déscription du projet

Projet d'utilitaires pour fichiers XML et YAML. Contient un module final.py, qui peut être importé dans n'importe quel programme python pour utiliser les fonctions du module. Utilitaires pour fichiers YAML et XML incluant : des affichages personnalisés, des modifications intelligentes et adaptées aux besoins utilisateurs, une comparaison de deux fichiers progressive et interractive permettant la correction d'un des deux fichiers.

# Installation

## Cloner le repository:

```bash
git clone https://github.com/Caotox/Stage_CS-Soprasteria
```

Then, in your Python file, import the necessary functions:

```python
from final/final import *
```

## Fonctions

### 1. xml_compare

Comparaison intelligente de 2 fichiers XML

**Utilisation:**

```python
xml_compare(xml_file1, xml_file2)
```

**Retourne:**

Un affichage progressif de toute les différences, permettant une modification étape par étape du fichier XML.

### 2. modele

Visualiation d'un noeud spécifique du fichier XML

**Utilisation:**

```python
modele(file, attribute, value)
```

*attribute:* L'élément utilisé pour la comparaison dans le fichier XML (par exemple class-name, value...) 

*value:* La value recherchée pour cet attribut.

**Returns:**

Le noeud récupéré et un affichage adapté

### 3. graphique

Affichage adapté et personnalisé de certains éléments du fichier XML selon le paramètre choisi

**Utilisation:**

```python
graphique(node, argument, attribute, parameter)
```

*argument:* La value recherchée pour l'attribut

*attribute:* L'attribut voulu pour la comparaison (par exemple class-name, value...)

*parameter:* Défini le type de parcours

Types de parcours :
    -e : Egalité stricte (Equal) - Cherche les éléments dont l'attribut spécifié est exactement égal à l'argument donné.
    
    -c : Contient (Contain) - Cherche les éléments dont l'attribut spécifié contient l'argument donné, commence par, se termine par ou est égal à l'argument donné.
    
    -r : Descendants récursifs (Recursive) - Cherche les éléments descendants de manière récursive dont l'attribut spécifié est égal à l'argument donné.
    
    -p : Parent direct (Parent) - Cherche le parent direct des éléments dont l'attribut spécifié est égal à l'argument donné.
    
    -s : Frères (Siblings) - Cherche les éléments frères des éléments dont l'attribut spécifié est égal à l'argument donné.
    
    -a : Ancêtres (Ancestors) - Cherche tous les ancêtres des éléments dont l'attribut spécifié est égal à l'argument donné.
    
    -nX : Descendants au niveau X (N-level Descendants) - Cherche les descendants au niveau X des éléments dont l'attribut spécifié est égal à l'argument donné.

***Le tiret doit être inclus***

**Retourne:**

Un affichage adapté au paramètre choisi par l'utilisateur du fichier XML choisi en paramètre

### License

Projet open source, n'hésitez pas à y ajouter des modifications !

### Auteur

Développe par Caotox.

-----------------------------------------------------------------------------------------------

# Dépot des travaux réalisés durant mon stage d'ingénieur d'études développeur dans le domaine du Contrôle aérien, où j'ai pu travailler sur différents projets :

## Gestion et maintenance des objets de la plateforme CMoIP :

Supervision et correction des différents objets de la plateforme CMoIP, garantissant la qualité et la conformité des configurations selon les standards établis.

## Développement d'outils pour l'automatisation et la manipulation de fichiers XML et YAML :

Utilisation de Python pour la création d'outils sur mesure permettant de simplifier la gestion et la manipulation des fichiers XML et YAML, afin de répondre efficacement aux demandes et aux besoins spécifiques des équipes de différents projets.

## Développement de scripts automatisés pour la correction des configurations clients :

Utilisation de Bash pour la création et implémentation de scripts automatisés afin de corriger les configurations, permettant ainsi aux clients de gérer efficacement les erreurs détectées lors des phases de test sur la plateforme. Ces scripts facilitent l’identification des anomalies, réduisent le temps de résolution, et améliorent la qualité des livrables.

## Réalisation de tests et propositions de solutions et corrections :

Exécution de tests approfondis sur les configurations, identification des dysfonctionnements, et mise en œuvre de solutions adaptées. Proposition de correctifs ciblés pour optimiser la qualité des fichiers XML de configuration et garantir une meilleure fiabilité des projets.

-------------------------

# Installation

## Clone the repository:

```bash
git clone https://github.com/Caotox/Stage_CS-Soprasteria
```

Then, in your Python file, import the necessary functions:

```python
from final/final import *
```

## Functions

### 1. xml_compare

Smart comparison of two XML files.

**Usage:**

```python
xml_compare(xml_file1, xml_file2)
```

**Returns:**

A progressive print of all differences, allowing a step-by-step modification of the XML file.

### 2. modele

XML file visualization. Helps retrieve a specific node in the XML file.

**Usage:**

```python
modele(file, attribute, value)
```

*attribute:* The element used for comparison in the XML file (e.g., class-name, value, etc.).

*value:* The value of the specified attribute to search for.

**Returns:**

The retrieved node and a formatted print of that node.

### 3. graphique

Displays an XML file in an adapted format based on specific parameters.

**Usage:**

```python
graphique(node, argument, attribute, parameter)
```

*argument:* The value of the desired attribute.

*attribute:* The attribute used for comparison (e.g., class-name, value, etc.).

*parameter:* Defines the pathing and display behavior.

-e: Strict Equality (Equal) - Searches for elements where the specified attribute is exactly equal to the given argument.

-c: Contains (Contain) - Searches for elements where the specified attribute contains, starts with, ends with, or is equal to the given argument.

-r: Recursive Descendants (Recursive) - Searches recursively for descendant elements where the specified attribute is equal to the given argument.

-p: Direct Parent (Parent) - Searches for the direct parent of elements where the specified attribute is equal to the given argument.

-s: Siblings (Siblings) - Searches for sibling elements of those where the specified attribute is equal to the given argument.

-a: Ancestors (Ancestors) - Searches for all ancestor elements where the specified attribute is equal to the given argument.

-nX: X-Level Descendants (N-level Descendants) - Searches for descendants at level X of elements where the specified attribute is equal to the given argument.

**Returns:**

A formatted display of the XML file, customized based on the given parameter.

### License

This project is open-source. Feel free to use and modify it as needed.

### Author

Developed by Caotox.

-----------------------------------------------------------------------------------------------

## Internship Report: Developer in Air Traffic Control

### Management and Maintenance of CMoIP Platform Objects

Supervision and correction of various objects on the CMoIP platform, ensuring quality and compliance with established configuration standards.

### Development of Tools for Automating and Handling XML and YAML Files

Utilized Python to create custom tools designed to simplify the management and manipulation of XML and YAML files, addressing the specific needs of project teams.

### Development of Automated Scripts for Correcting Client Configurations

Used Bash to develop and implement automated scripts for correcting configurations, allowing clients to efficiently manage errors detected during testing phases. These scripts help identify anomalies, reduce resolution time, and improve deliverable quality.

### Execution of Tests and Proposal of Solutions and Fixes

Conducted thorough tests on configurations, identified malfunctions, and implemented appropriate solutions. Proposed targeted fixes to optimize XML configuration files and improve project reliability.



