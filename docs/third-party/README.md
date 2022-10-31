# Third Party Dependencies

<!--[[[fill sbom_sha256()]]]-->
The [SBOM in CycloneDX v1.4 JSON format](https://github.com/sthagen/pilli/blob/default/sbom.json) with SHA256 checksum ([c0b967f2 ...](https://raw.githubusercontent.com/sthagen/pilli/default/sbom.json.sha256 "sha256:c0b967f267482eb3675760c5a84cb4b6b6ed67fd6066dfc8587baa4f694458e4")).
<!--[[[end]]] (checksum: 6b1a7115478da7cb6583ce71d310a0ce)-->
## Licenses 

JSON files with complete license info of: [direct dependencies](direct-dependency-licenses.json) | [all dependencies](all-dependency-licenses.json)

### Direct Dependencies

<!--[[[fill direct_dependencies_table()]]]-->
| Name                                       | Version                                        | License     | Author            | Description (from packaging data)                                  |
|:-------------------------------------------|:-----------------------------------------------|:------------|:------------------|:-------------------------------------------------------------------|
| [PyYAML](https://pyyaml.org/)              | [6.0](https://pypi.org/project/PyYAML/6.0/)    | MIT License | Kirill Simonov    | YAML parser and emitter for Python                                 |
| [typer](https://github.com/tiangolo/typer) | [0.6.1](https://pypi.org/project/typer/0.6.1/) | MIT License | Sebastián Ramírez | Typer, build great CLIs. Easy to code. Based on Python type hints. |
<!--[[[end]]] (checksum: 2cbd9167abfa69505798af7ad0916e5c)-->

### Indirect Dependencies

<!--[[[fill indirect_dependencies_table()]]]-->
| Name                                                                                           | Version                                                    | License                            | Author         | Description (from packaging data)                      |
|:-----------------------------------------------------------------------------------------------|:-----------------------------------------------------------|:-----------------------------------|:---------------|:-------------------------------------------------------|
| [click](https://palletsprojects.com/p/click/)                                                  | [8.1.3](https://pypi.org/project/click/8.1.3/)             | BSD License                        | Armin Ronacher | Composable command line interface toolkit              |
| [typing-extensions](https://github.com/python/typing/blob/master/typing_extensions/README.rst) | [4.4.0](https://pypi.org/project/typing-extensions/4.4.0/) | Python Software Foundation License | UNKNOWN        | Backported and Experimental Type Hints for Python 3.7+ |
<!--[[[end]]] (checksum: a4fd9f338cb32c0c8dbd26ebdd435ba0)-->

## Dependency Tree(s)

JSON file with the complete package dependency tree info of: [the full dependency tree](package-dependency-tree.json)

### Rendered SVG

Base graphviz file in dot format: [Trees of the direct dependencies](package-dependency-tree.dot.txt)

<img src="./package-dependency-tree.svg" alt="Trees of the direct dependencies" title="Trees of the direct dependencies"/>

### Console Representation

<!--[[[fill dependency_tree_console_text()]]]-->
````console
PyYAML==6.0
typer==0.6.1
  - click [required: >=7.1.1,<9.0.0, installed: 8.1.3]
````
<!--[[[end]]] (checksum: 02796995333dbf7df09e445adae7be69)-->
