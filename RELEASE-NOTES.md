<!-- TOC -->

- [v3.1.0](#v310)
    - [Deprecated](#deprecated)
    - [Features](#features)
    - [Bugfixes](#bugfixes)
- [v3.0.0](#v300)
    - [Breaking changes](#breaking-changes)
    - [Features](#features-1)
    - [Bugfixes](#bugfixes-1)
- [v2.8.0](#v280)
    - [Features](#features-2)
    - [Bugfixes](#bugfixes-2)
- [v2.7.0](#v270)
    - [Features](#features-3)
- [v2.6.0](#v260)
    - [Features](#features-4)
    - [Bugfixes](#bugfixes-3)
- [v2.4.0](#v240)
    - [Features](#features-5)
- [v2.2.20](#v2220)
    - [Bugfixes](#bugfixes-4)
- [v2.2.10](#v2210)
    - [Bugfixes](#bugfixes-5)
- [v2.2.0](#v220)
    - [Features](#features-6)
- [v2.0.10](#v2010)
    - [Bugfixes](#bugfixes-6)
- [v2.0.0](#v200)
    - [Breaking changes](#breaking-changes-1)
    - [Features](#features-7)
    - [Bugfixes](#bugfixes-7)
- [v1.0.1](#v101)
    - [Features](#features-8)
    - [Bugfixes](#bugfixes-8)
    - [Known issues](#known-issues)
- [v1.0.0](#v100)
    - [Features](#features-9)

<!-- /TOC -->

|      |              |
|------|--------------|
| Date | `18.09.2018` |
| Tag  | `v3.1.0`     |

# v3.1.0

## Deprecated

*Note:* Deprecated classes, attributes and relations will be removed in the next major release.

* Utdanning
  * The class `Medlemskap` has been deprecated.  
    Group membership is instead represented as relations between `Elevforhold` or `Undervisningsforhold` and the 
    various groups.

## Features

* Utdanning
  * Relations are expressed between concrete classes instead of abstract classes.  This makes relations more explicit,
    and simplifies the way these relations are consumed.
  * Added relation from `Skole` to groups.
  * Added relation between `Fag` and `Programområde`.
  * Added bidirectional relation between `Elevforhold` and `Vurdering` and `Fravær`.
    * A new attribute `endelig` on `Vurdering` indicates final assesments.
  * Relations from `Vurdering` and `Fravær` to `Undervisningsgruppe` and `Eksamensgruppe` are used to indicate
    absence and assessments in context of these groups.

## Bugfixes

* Utdanning
  * Fixed multiplicity on relation to `Elevkategori` from `Elevforhold`.
  * Documentation updates.

# v3.0.0

|      |              |
|------|--------------|
| Date | `07.06.2018` |
| Tag  | `v3.0.0`     |

## Breaking changes

* Administrasjon
  * `Fastlønn` and `Variabellønn` have been revised.  
    * Instead of collections containing multiple transactions they have been remodeled to represent individual transactions.
    * `Beskjeftigelse` is incorporated into `Fastlønn`
    * `Variabelttillegg` is incorporated into `Variabellønn`
    * The class `Fasttillegg` has been introduced to represent the `fasttillegg` attribute previously found on `Fastlønn`
* Utdanning
  * `Vurdering` has been moved to the package `Vurdering` and is now `hovedklasse` with `systemId`.
  * `Elev` now has an optional `elevnummer` and mandatory `systemId`.

## Features

* Administrasjon
  * `systemId` is now optional on `Fastlønn`, `Variabellønn` and `Fravær`, as these classes are used to create new information in the back end system.
* Ressurser
  * Added `Identitet` and `Rettighet` under `Tilgangsstyring` for identity and access management.

## Bugfixes

* Administrasjon
  * Fixed multiplicity for `ansiennitet`.  The field is now optional.
  * Fixed documentation for `Fravær`.

# v2.8.0

|      |              |
|------|--------------|
| Date | `23.05.2018` |
| Tag  | `v2.8.0`     |

## Features

* Felles
  * Added `Kontaktperson`
* Administrasjon
  * Added `ansiennitet` to `Personalressurs` 

## Bugfixes

* Felles
  * Updated documentation for `fødselsdato` on `Person`
* Administrasjon
  * Fixed multiplicity of `kategori` on `Lønnsart`

# v2.7.0

|      |              |
|------|--------------|
| Date | `05.04.2018` |
| Tag  | `v2.7.0`     |

## Features

* Utdanning
  * Added support for `feidenavn` for both students (`Elev`) and faculty/staff (`Skoleressurs`)
* Administrasjon
  * Added `kategori` to `Lønnsart`

# v2.6.0

|      |              |
|------|--------------|
| Date | `13.03.2018` |
| Tag  | `v2.6.0`     |

## Features

* Administrasjon
  * Added support for `Fravær` (Absence)
  * Added `Fasttillegg`
  * Added `periode` to `Beskjeftigelse`, `Fasttillegg`, and `Variabelttillegg`

## Bugfixes

* Administrasjon
  * Fixed relations and members for `Beskjeftigelse` and `Variabelttillegg`
* Utdanning
  * Fixed regressions on `Medlemskap`

# v2.4.0

|      |              |
|------|--------------|
| Date | `06.02.2018` |
| Tag  | `v2.4.0`     |

## Features

* Added support for `Lønn` (Salary) and `Fullmakt` (Authorizations).
* Added `personalleder` and `personalansvar` relations between `Personalressurs` and `Arbeidsforhold`.
* Made relations between `Skole` and `Fag`, and `Skole` and `Utdanningsprogram`, bidirectional.
* Added relation between `Skole` and `Utdanningsforhold`.
* Made relation `leder` from `Personalressurs` to `Organisasjonselement` `0..*`.

# v2.2.20

|      |              |
|------|--------------|
| Date | `07.12.2017` |
| Tag  | `v2.2.20`    |

## Bugfixes

* Made the attribute `brukernavn` optional on `Personalressurs` and `Elev`.

# v2.2.10

|      |              |
|------|--------------|
| Date | `27.11.2017` |
| Tag  | `v2.2.10`    |

## Bugfixes

* Added new optional attribute `passiv` to `Begrep`.  Fixes #44.

# v2.2.0

|      |              |
|------|--------------|
| Date | `27.10.2017` |
| Tag  | `v2.2.0`     |

## Features

* Added support for code lists from Vigo.  This is a pure addition to the model, with no impact to the existing model.
* References from the `Utdanning` model to Vigo code lists is represented as external references.


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
