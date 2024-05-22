![PyPI - Version](https://img.shields.io/pypi/v/pycutroh)
![PyPI - License](https://img.shields.io/pypi/l/pycutroh)
![PyPI - Downloads](https://img.shields.io/pypi/dm/pycutroh)
[![Publish PyPi](https://github.com/IT-Administrators/pycutroh/actions/workflows/release.yml/badge.svg?branch=main)](https://github.com/IT-Administrators/pycutroh/actions/workflows/release.yml)
[![CI](https://github.com/IT-Administrators/pycutroh/actions/workflows/ci.yaml/badge.svg)](https://github.com/IT-Administrators/pycutroh/actions/workflows/ci.yaml)

# pycutroh

_The pycutroh module is a simple string cutting module._

## Table of contents

1. [Introduction](#introduction)
2. [Getting started](#getting-started)
    1. [Prerequisites](#prerequisites)
    2. [Installation](#installation)
3. [How to use](#how-to-use)
    1. [How to import](#how-to-import)
    2. [Using the module](#using-the-module)
    3. [Using the cli](#using-the-cli)
4. [Releasing](#releasing)
5. [License](/LICENSE)

## Introduction

I've written this module to learn python and some python basics like using unittests, imports and how python modules/packets work. 

This module is inspired by the linux bash command.

At the moment this module provides four functions, which can be used to manipulate strings. For further information see here: [How to use](#how-to-use)

The cli interface for this module is now available. 

## Getting started

### Prerequisites

- Python installed
- Operatingsystem: Linux or Windows, not tested on mac
- IDE like VS Code, if you want to contribute or change the code

### Installation

There are two ways to install this module depending on the way you work and the preinstalled modules:

1. ```pip install pycutroh```
2. ```python -m pip install pycutroh```

## How to use

### How to Import

You can import the module in two ways:

```python
import pycutroh
```

- This will import all functions. Even the ones that are not supposed to be used (helper functions).

```python
from pycutroh import *
```

- This will import only the significant functions, meant for using. 

### Using the module

Depending on the way you imported the module, the following examples look a bit different.

Example 1:

```python
from pycutroh import *

print(get_letter_on_pos("This is a demonstration string.",0))
```
Result:
```
T
```

Example 2:

```python
from pycutroh import *

print(get_letters_from_pos_to_pos("This is a demonstration string.",(0,4)))

```
Result:
```
This
```

Example 3:

```python
from pycutroh import *

print(get_fields("This is a demonstration string.",(0,3)," "))

```
Result:
```
This demonstration
```

Example 4:

```python
import pycutroh

print(pycutroh.get_fields_new_separator("This is a demonstration string.",(0,3)," ","|"))
```
Result:
```
This|demonstration
```

### Using the cli

You can now use the cli of the pycutroh module. This cli is my first using the argparse module, so there might be adjustments in the future.

To show the help run the following command:

```python
python -m pycutroh -h
```
Result:
```
usage: __main__.py [-h] [-s STRING] [-glop GETLETTERONPOS | -glbp GETLETTERSFROMPOSTOPOS GETLETTERSFROMPOSTOPOS | -glbfs GETLETTERSBEFORESIGN | -glas GETLETTERSAFTERSIGN | -glbs GETLETTERSBETWEENSIGNS GETLETTERSBETWEENSIGNS] {f} ...

positional arguments:
  {f}                   Get fields separated by specified delimiter.
    f                   Get fields by delimiter and join using same delimiter.

options:
  -h, --help            show this help message and exit
  -s STRING, --string STRING
  -glop GETLETTERONPOS, --getLetterOnPos GETLETTERONPOS
                        Letter on position to return.
  -glbp GETLETTERSFROMPOSTOPOS GETLETTERSFROMPOSTOPOS, --getLettersFromPosToPos GETLETTERSFROMPOSTOPOS GETLETTERSFROMPOSTOPOS
                        Get letter between positions.
  -glbfs GETLETTERSBEFORESIGN, --getLettersBeforeSign GETLETTERSBEFORESIGN
                        Get letters Before specified sign.
  -glas GETLETTERSAFTERSIGN, --getLettersAfterSign GETLETTERSAFTERSIGN
                        Get letters after specified sign.
  -glbs GETLETTERSBETWEENSIGNS GETLETTERSBETWEENSIGNS, --getLettersBetweenSigns GETLETTERSBETWEENSIGNS GETLETTERSBETWEENSIGNS
                        Get letters between specified signs.
```

Using a function:

```python
python -m pycutroh f --getFields (0,1,2,3) --delimiter " " --newDelimiter ","
```

Result:
```
This,is,a,demonstration
```

## Releasing

Releases are published automatically when a tag is pushed to GitHub.

```Powershell
# Create release variable.
$Release = "x.x.x"
# Create commit.
git commit --allow-empty -m "Release $Release"
# Create tag.
git tag -a $Release -m "Version $Release"
# Push from original.
git push origin --tags
# Push from fork.
git push upstream --tags
```

## License

[MIT](/LICENSE)