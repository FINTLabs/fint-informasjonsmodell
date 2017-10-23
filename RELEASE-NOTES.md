<!-- TOC -->

- [v2.2.0-beta-2](#v220-beta-2)
    - [Features](#features)
- [v2.0.10](#v2010)
    - [Bugfixes](#bugfixes)
- [v2.0.0](#v200)
    - [Breaking changes](#breaking-changes)
    - [Features](#features-1)
    - [Bugfixes](#bugfixes-1)
- [v1.0.1](#v101)
    - [Features](#features-2)
    - [Bugfixes](#bugfixes-2)
    - [Known issues](#known-issues)
- [v1.0.0](#v100)
    - [Features](#features-3)

<!-- /TOC -->

# v2.2.0-beta-2

|      |                  |
|------|------------------|
| Date | `23.10.2017`     |
| Tag  | `v2.2.0-beta-2`  |

## Features

* Added support for code lists from Vigo.  This is a pure addition to the model, with no impact to the existing model.
  References from the `Utdanning` model to Vigo code lists is represented as external references.


# v2.0.10

|      |              |
|------|--------------|
| Date | `05.10.2017` |
| Tag  | `v2.0.10`    |

## Bugfixes

* Made association between `Organisasjonselement` and `Arbeidsforhold` bidirectional (fixes #38)
* Fixed multiplicity from `Elevforhold` to `Elevkategori` (fixes #36)
* Fixed documentation for `Art` and `Funksjon` (fixes #37)


# v2.0.0

|      |              |
|------|--------------|
| Date | `27.09.2017` |
| Tag  | `v2.0.0`     |

## Breaking changes

Since this version of the Information Model is the first to go live, we opted to do a number of breaking changes, as we had the window of opportunity. 

* Changed name from `Fellesmodel` to `Felles` for common package
* Moved `ISO` from `Basisklasser` to `Kodeverk` in `Felles`
* In `Arbeidsforhold` changed `årslønn` to be an integer number expressing øre (1/100 Kroner)
* In `Arbeidsforhold` changed `stillingsprosent` and `lønnsprosent`, and the new `tilstedeprosent` to an integer
  expressing 1/100 %
* Renamed `TimerPerUkeKode` to `Uketimetall`
* Replaced `adresse` in `Adresse` with `adresselinje [0..*]`
* Replaced fields related to complex types with associations
* Relation `Person - Personalressurs` changed from Aggregation to Association
* Fixed class name from `Arbeidforholdstype` to `Arbeidsforholdstype`

## Features

* Added initial release of `Utdanning` (Education) model
* Expanded definition of `Person`
* Added `Fylke` and `Kommmune` as common classes
* Added `beskrivelse` (description) to `Periode`

## Bugfixes

* Rearranged and expanded diagrams (visible only in EAP file)
* Multiple fixes of markup in documentation
* Error correction and grammar revision


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
