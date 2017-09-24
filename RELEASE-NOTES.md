<!-- MarkdownTOC -->

- [master](#master)
- [v1.1.0](#v110)
	- [Features](#features)
	- [Bugfixes](#bugfixes)
- [v1.0.1](#v101)
	- [Features](#features-1)
	- [Bugfixes](#bugfixes-1)
	- [Known issues](#known-issues)
- [v1.0.0](#v100)
	- [Features](#features-2)

<!-- /MarkdownTOC -->

# master

# v1.1.0

|      |              |
|------|--------------|
| Date | `27.09.2017` (tentative) |
| Tag  | `v1.1.0` |

## Features

* Added initial release of `Utdanning` (Education) model
* Changed name from `Fellesmodel` to `Felles` for common package
* Expanded definition of `Person`
* Added `Fylke` and `Kommmune` as common classes
* Moved `ISO` from `Basisklasser` to `Kodeverk` in `Felles`
* Added `beskrivelse` (description) to `Periode`
* In `Arbeidsforhold` changed `årslønn` to be an integer number expressing øre (1/100 Kroner)
* In `Arbeidsforhold` changed `stillingsprosent` and `lønnsprosent`, and the new `tilstedeprosent` to an integer
  expressing 1/100 %

## Bugfixes

* Replaced fields related to complex types with associations
* Rearranged and expanded diagrams (visible only in EAP file)
* Multiple fixes of markup in documentation
* Error correction and grammar revision
* Relation `Person - Personalressurs` changed from Aggregation to Association
* Fixed class name from `Arbeidforholdstype` to `Arbeidsforholdstype`


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

* [ ] Class `Språk` (`Language`) is not referred from any other classes


# v1.0.0

|      |              |
|------|--------------|
| Date | `07.04.2017` |
| Tag  | `v1.0.0`     |

* Initial release

## Features

* Common classes (`Fellesmodell`)
* Classes for Administration domain (`Administrasjon`):
  * `Personal`
  * `Organisasjon`
  * `Kodeverk`
