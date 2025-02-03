# Usage :
```bash
clone https://github.com/Caotox/Stage_CS-Soprasteria
```
Then in the python file you want to use the functions type :
```py
from /final/final.py import *
```

## Functions
### 1. xml_compare
Smart comparison of two XML files.
*Usage:*
```python
xml_compare(xml_file1, xml_file2)
```
*Returns:* A progressive print of all differences, allowing a step-by-step modification of the XML file.

### 2. modele
XML file visualization. Helps retrieve a specific node in the XML file.
*Usage:*

```python
modele(file, attribute, value)
```
*attribute:* The element used for comparison in the XML file (e.g., class-name, value, etc.).

*value:* The value of the specified attribute to search for.

*Returns:* The retrieved node and a formatted print of that node.

### 3. graphique
Displays an XML file in an adapted format based on specific parameters.

*Usage:*
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
  
  -nX: X-Level Descendants (N-level Descendants) - Searches for descendants at level X of elements where the specified attribute is equal to the given argument.*

*Returns:* A formatted display of the XML file, customized based on the given parameter.

**License**

This project is open-source. Feel free to use and modify it as needed.

**Author**

Developed by Caotox.

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
