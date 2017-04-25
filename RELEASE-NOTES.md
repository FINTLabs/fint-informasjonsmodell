<!-- MarkdownTOC -->

- [v1.0.1](#v101)
	- [Features](#features)
	- [Bugfixes](#bugfixes)
	- [Known issues](#known-issues)
- [v1.0.0](#v100)

<!-- /MarkdownTOC -->


# v1.0.1

|      |              |
|------|--------------|
| Date | `25.04.2017` |
| Tag  | `v1.0.1`     |

## Features

* Added release notes as a separate file in repo

## Bugfixes

* Clean up files: xsd + old documentation
* Field `gender` on the class `Person` should be a relation
* `Personalressurskategori` on the object `Person` is defined as both field and relation
* Several `Kodeverk` classes har `parent` (`forelder`) as field and not as relation. This applies to following classes: `ansvar`, `arbeidsforholdstype`, `funksjon` og `stillingskode`)
* `ksKode` field is removed from `Stillingskategori`

## Known issues

* Class `Språk` (`Language`) is not referred from any other classes


# v1.0.0

|      |              |
|------|--------------|
| Date | `07.04.2017` |
| Tag  | `v1.0.0`     |

* Initial release