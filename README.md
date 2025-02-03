# Installation

## Clone the repository:

```bash
git clone https://github.com/Caotox/Stage_CS-Soprasteria
```

Then, in your Python file, import the necessary functions:

```python
from final.final import *
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

