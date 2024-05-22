# imxInsights
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/imxInsights)
[![PyPI version](https://badge.fury.io/py/imxInsights.svg)](https://pypi.org/project/imxInsights)
[![PyPI - Status](https://img.shields.io/pypi/status/imxInsights)](https://pypi.org/project/imxInsights/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/imxInsights)](https://pypi.org/project/imxInsights)

[![GitHub](https://badgen.net/badge/icon/github?icon=github&label)](https://github.com)
[![Documentation Status](https://readthedocs.org/projects/ansicolortags/badge/?version=latest)](http://ansicolortags.readthedocs.io/?badge=latest)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](http://makeapullrequest.com)
![PyPI - License](https://img.shields.io/pypi/l/imxInsights)

Documentation: https://xxxxxx

Source Code: [https://github.com/Hazedd/imxInsightsCore](https://github.com/Hazedd/imxInsightsCore)

!!! danger "Warning!" 
    
    The goal of `imxInsights` is to extract information from imx files. **Please note that modifying, adding, deleting, or altering data is beyond the scope of this module**. `imxInsights` supports imx versions 1.2.4 and 5.0.0 exclusively. 
    Our aim is to stay compatible with the latest production versions of the imx model.

!!! abstract
    
    `imxInsights` is designed to parse imx files, which may contain Situations or Projects with an InitialSituation 
    and optionally a NewSituation. Each situation includes a repository that houses value objects. A value object represents an item of interest and is equipped with properties and methods to retrieve information. 
    The module facilitates the creation of tabular views or spatial GeoJSON, and enables network queries using a networkx graph.


!!! info "Audience"
    
    The intended audience for `imxInsights` consists of end users with basic Python knowledge. Therefore, the module offers a minimalistic API that is thoroughly documented. 
    We leverage the remarkable `makedocs` plugins to effortlessly generate a polished website from documentations and markdown files.


## Features
- **Value Objects Repository**: Every object of interest is stored in a repository, utilizing puic as the default key. If no puic attribute is present, a configurable custom key is employed.
- **RailConnection Geometry**: Generated from junctions referenced in the microLink From- and ToNode attributes, ensuring accurate spatial representation.
- **Track Fragments and Demarcation Marker Objects**: Equipped with projected geometry for precise visualization and analysis.
- **Area Classifier**: Classifies every value object within an imx project area (if has geometry), streamlining organization and analysis.
- **View as DataFrame**: Easily convert value objects into a Pandas dataframe, providing a convenient data structure for analysis.
- **View as GeoJSON**: Export data in GeoJSON format, preserving spatial information for interoperability and visualization.
- **Referenced Objects Links**: Seamlessly access referenced objects as value objects, enhancing data accessibility and integrity.
- **Difference Generator**: Enables comparison and discrepancy generation, with options for exporting in Excel and GeoJSON formats, facilitating efficient data validation and analysis.
- **Network Graph**: Utilized for retrieving route information and creating geometry, facilitating comprehensive network analysis.

## Supported Python Versions
This library is compatible with ***Python 3.10*** and above. 

!!! warning
    ***3.9 and below will NOT be supported***.


## Quick Start

### Distribution and installation
imxInsights is distributed on https://pypi.org and can be installed by the following pip command:

``pip install imxInsights``

***import, load file, get repo got insights!***

## Code samples and snippets
```
from imxInsight import Imx

imx = Imx(file_path)

init_repo = imx.project.initial_situation
object_of_intrest = init_repo.get_by_puic(puic)

pandas_df = imx.project.new_situation.get_pandas_df("Signal")
```

For more code samples and snippets in the example section / folder and use the api reference for exploration.


# Contributing
Contributions welcome! For more information on the design of the library, see [contribution guidelines for this project](CONTRIBUTING.md).


#  Projects used in this project
[make](https://www.gnu.org/software/make/manual/make.html)
, [flake8](https://flake8.pycqa.org/en/latest/)
, [black](https://github.com/psf/black)
, [mypy](https://mypy.readthedocs.io/en/stable/)
, [iSort](https://github.com/PyCQA/isort)
, [bumpversion](https://github.com/peritus/bumpversion)
, [flit](https://flit.pypa.io/en/latest/)
, [mkdocs](https://www.mkdocs.org/)
, [mkdocs-material](https://squidfunk.github.io/mkdocs-material/)
, [lxml](https://lxml.de/)
, [pyproj](https://pypi.org/project/pyproj/)
, [shapely](https://pypi.org/project/shapely/)
, [loguru](https://pypi.org/project/loguru/)
, [pandas](https://pandas.pydata.org/)
, [xlsxwriter](https://pypi.org/project/XlsxWriter/)
, [ruamel.yaml](https://pypi.org/project/ruamel.yaml/)
, [networkx](https://pypi.org/project/networkx/)
, [dateparser](https://pypi.org/project/dateparser/)


