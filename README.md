# Usage :
```bash
clone https://github.com/Caotox/Stage_CS-Soprasteria
```
Then in the python file you want to use the functions type :
```py
from /final/final.py import *
```

## Functions :
1. xml_compare : smart comparaison of two xml files
example : xml_compare(xml-file1, xml-file2)
returns : a proggressive print of all differences, enabling a step by step modification of the xml-file

2. modele : xml file visualisation, can be served as a way to get a specific node of the xml file
example : modele(file, attribute, value)
  -> attribute : element of comparaison in the xml file (class-name, value...)
  -> value : value of the said attribute we want to get
returns : the node the program recovered, and an adapted print of that node

3. graphique : an adapted display of an xml file depending on certain parameters
example : graphique(node, argument, attribute, parameter)
  -> argument : value of the wanted attribute
  -> attribute : attribute to compare (example : class-name, value...)
  -> parameter : will define the pathing and display
*-e: Strict Equality (Equal) - Searches for elements whose specified attribute is exactly equal to the given argument.
-c: Contains (Contain) - Searches for elements whose specified attribute contains, starts with, ends with, or is equal to the given argument.
-r: Recursive Descendants (Recursive) - Searches recursively for descendant elements whose specified attribute is equal to the given argument.
-p: Direct Parent (Parent) - Searches for the direct parent of elements whose specified attribute is equal to the given argument.
-s: Siblings (Siblings) - Searches for sibling elements of those whose specified attribute is equal to the given argument.
-a: Ancestors (Ancestors) - Searches for all ancestor elements whose specified attribute is equal to the given argument.
-nX: X-Level Descendants (N-level Descendants) - Searches for descendants at level X of elements whose specified attribute is equal to the given argument.*
returns : an adapted display, depending on the parameter given








Work Report During My Engineering Internship as a Developer in Air Traffic Control
## Management and Maintenance of CMoIP Platform Objects:
Supervision and correction of various objects on the CMoIP platform, ensuring quality and compliance with established configuration standards.

## Development of Tools for Automating and Handling XML and YAML Files:
Utilized Python to create custom tools designed to simplify the management and manipulation of XML and YAML files, effectively addressing the specific needs and requirements of teams working on different projects.

## Development of Automated Scripts for Correcting Client Configurations:
Used Bash to develop and implement automated scripts for correcting configurations, allowing clients to efficiently manage errors detected during the testing phases on the platform. These scripts help identify anomalies, reduce resolution time, and improve the quality of deliverables.

## Execution of Tests and Proposals for Solutions and Fixes:
Conducted thorough tests on configurations, identified malfunctions, and implemented appropriate solutions. Proposed targeted fixes to optimize the quality of XML configuration files and ensure better project reliability.

---------------------------------------------------------------------------------

Dépot des travaux réalisés durant mon stage d'ingénieur d'études développeur dans le domaine du Contrôle aérien, où j'ai pu travailler sur différents projets :
## Gestion et maintenance des objets de la plateforme CMoIP :
Supervision et correction des différents objets de la plateforme CMoIP, garantissant la qualité et la conformité des configurations selon les standards établis.

## Développement d'outils pour l'automatisation et la manipulation de fichiers XML et YAML :
Utilisation de Python pour la création d'outils sur mesure permettant de simplifier la gestion et la manipulation des fichiers XML et YAML, afin de répondre efficacement aux demandes et aux besoins spécifiques des équipes de différents projets.

## Développement de scripts automatisés pour la correction des configurations clients :
Utilisation de Bash pour la création et implémentation de scripts automatisés afin de corriger les configurations, permettant ainsi aux clients de gérer efficacement les erreurs détectées lors des phases de test sur la plateforme. Ces scripts facilitent l’identification des anomalies, réduisent le temps de résolution, et améliorent la qualité des livrables.

## Réalisation de tests et propositions de solutions et corrections :
Exécution de tests approfondis sur les configurations, identification des dysfonctionnements, et mise en œuvre de solutions adaptées. Proposition de correctifs ciblés pour optimiser la qualité des fichiers XML de configuration et garantir une meilleure fiabilité des projets.
