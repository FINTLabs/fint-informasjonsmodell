<!-- MarkdownTOC autolink="true" -->

- [v4.0.0](#v400)
  - [Breaking changes](#breaking-changes)
    - [Utdanning: Removed deprecated elements](#utdanning-removed-deprecated-elements)
    - [Felles: Removed deprecated elements](#felles-removed-deprecated-elements)
    - [Arkiv: Removed deprecated elements](#arkiv-removed-deprecated-elements)
    - [Administrasjon: Removed deprecated elements](#administrasjon-removed-deprecated-elements)
    - [Utdanning: Changed name on Basisgruppe and Basisgruppemedlemskap](#utdanning-changed-name-on-basisgruppe-and-basisgruppemedlemskap)
      - [Klasse](#klasse)
      - [Klassemedlemskap](#klassemedlemskap)
    - [Utdanning: Moved Grepreferanse and Vigoreferanse](#utdanning-moved-grepreferanse-and-vigoreferanse)
      - [Basisklasser](#basisklasser)
      - [Timeplan](#timeplan)
      - [Utdanningsprogram](#utdanningsprogram)
    - [Arkiv: Removed relation to and use of abstract classes](#arkiv-removed-relation-to-and-use-of-abstract-classes)
    - [Økonomi: Changed multiplicity](#økonomi-changed-multiplicity)
- [v3.21.10](#v32110)
  - [Features](#features)
    - [Ressurs.Datautstyr](#ressursdatautstyr)
- [v3.21.0](#v3210)
  - [Features](#features-1)
    - [Ressurs.Datautstyr](#ressursdatautstyr-1)
    - [Ressurs.Kodeverk](#ressurskodeverk)
- [v3.20.0](#v3200)
  - [Features](#features-2)
    - [Utdanning: Oppmøtetid til Eksamen](#utdanning-oppmøtetid-til-eksamen)
    - [Administrasjon: Organisasjonstype](#administrasjon-organisasjonstype)
- [v3.19.0](#v3190)
  - [Features](#features-3)
    - [Arkiv: Innføring av fødselsnummer og organisasjonsnummer på Part](#arkiv-innføring-av-fødselsnummer-og-organisasjonsnummer-på-part)
    - [Arkiv: Innføring av Tilgangsgruppe](#arkiv-innføring-av-tilgangsgruppe)
    - [Utdanning: Eksamensvurdering](#utdanning-eksamensvurdering)
      - [Utgår](#utgår)
- [v3.18.0](#v3180)
  - [Features](#features-4)
    - [Eiendeler](#eiendeler)
- [v3.17.0](#v3170)
  - [Features](#features-5)
    - [Skille ut Elevvurdering fra Elevforhold](#skille-ut-elevvurdering-fra-elevforhold)
      - [Utgår](#utgår-1)
    - [Vitnemålsmerknad](#vitnemålsmerknad)
    - [Tilrettelegging på eksamen](#tilrettelegging-på-eksamen)
    - [Varselbrev](#varselbrev)
    - [Betalingsstatus for privatisteksamen](#betalingsstatus-for-privatisteksamen)
    - [Dokumentasjon av faglærte](#dokumentasjon-av-faglærte)
- [v3.16.0](#v3160)
  - [Features](#features-6)
- [v3.15.0](#v3150)
  - [Features](#features-7)
  - [Bugfixes](#bugfixes)
- [v3.14.0](#v3140)
  - [Features](#features-8)
  - [Bugfixes](#bugfixes-1)
- [v3.13.0](#v3130)
  - [Features](#features-9)
- [v3.12.0](#v3120)
  - [Features](#features-10)
- [v3.11.10](#v31110)
  - [Bugfix](#bugfix)
- [v3.11.0](#v3110)
  - [Features](#features-11)
  - [Deprecated](#deprecated)
  - [Bugfixes](#bugfixes-2)
- [v3.10.0](#v3100)
  - [Features](#features-12)
  - [Deprecated](#deprecated-1)
  - [Bugfixes](#bugfixes-3)
- [v3.9.0](#v390)
  - [Features](#features-13)
  - [Deprecated](#deprecated-2)
  - [Bugfixes](#bugfixes-4)
- [v3.8.10](#v3810)
  - [Bugfixes](#bugfixes-5)
- [v3.8.0](#v380)
  - [Deprecated](#deprecated-3)
  - [Bugfixes](#bugfixes-6)
  - [Features](#features-14)
- [v3.7.0](#v370)
  - [Features](#features-15)
- [v3.6.10](#v3610)
  - [Bugfixes](#bugfixes-7)
- [v3.6.0](#v360)
  - [Deprecated](#deprecated-4)
  - [Features](#features-16)
- [v3.5.0](#v350)
  - [Features](#features-17)
  - [Bugfixes](#bugfixes-8)
- [v3.4.0](#v340)
  - [Features](#features-18)
  - [Bugfixes](#bugfixes-9)
- [v3.3.0](#v330)
  - [Features](#features-19)
  - [Bugfixes](#bugfixes-10)
- [v3.2.0](#v320)
  - [Deprecated](#deprecated-5)
  - [Features](#features-20)
- [v3.1.0](#v310)
  - [Deprecated](#deprecated-6)
  - [Features](#features-21)
  - [Bugfixes](#bugfixes-11)
- [v3.0.0](#v300)
  - [Breaking changes](#breaking-changes-1)
  - [Features](#features-22)
  - [Bugfixes](#bugfixes-12)
- [v2.8.0](#v280)
  - [Features](#features-23)
  - [Bugfixes](#bugfixes-13)
- [v2.7.0](#v270)
  - [Features](#features-24)
- [v2.6.0](#v260)
  - [Features](#features-25)
  - [Bugfixes](#bugfixes-14)
- [v2.4.0](#v240)
  - [Features](#features-26)
- [v2.2.20](#v2220)
  - [Bugfixes](#bugfixes-15)
- [v2.2.10](#v2210)
  - [Bugfixes](#bugfixes-16)
- [v2.2.0](#v220)
  - [Features](#features-27)
- [v2.0.10](#v2010)
  - [Bugfixes](#bugfixes-17)
- [v2.0.0](#v200)
  - [Breaking changes](#breaking-changes-2)
  - [Features](#features-28)
  - [Bugfixes](#bugfixes-18)
- [v1.0.1](#v101)
  - [Features](#features-29)
  - [Bugfixes](#bugfixes-19)
  - [Known issues](#known-issues)
- [v1.0.0](#v100)
  - [Features](#features-30)

<!-- /MarkdownTOC -->

# v4.0.0

|      |                 |
| ---- |-----------------|
| Date | `19.01.2026`    |
| Tag  | `v4.0.0` |


## Breaking changes

### Utdanning: Removed deprecated elements
* Removed attribute `periode` on `Basisgruppe`.
* Removed attribute `periode` on `Eksamensgruppe`.
* Removed attribute `periode` on `Fag`.
* Removed attribute `periode` on `Faggruppe`.
* Removed attribute `periode` on `Gruppe`.
* Removed attribute `periode` on `Kontaktlærergruppe`.
* Removed attribute `periode` on `Persongruppe`.
* Removed attribute `periode` on `Programområde`.
* Removed attribute `periode` on `Undervisningsgruppe`.
* Removed attribute `periode` on `Utdanningsprogram`.
* Removed attribute `periode` on `Årstrinn`.
* Removed class `Fravær`.
* Removed class `Medlemskap`.
* Removed class `Vurdering`.
* Removed relation `basisgruppe` on `Elevforhold`.
* Removed relation `eksamensgruppe` on `Elevforhold`.
* Removed relation `fravær` on `Elevforhold`.
* Removed relation `halvårsfagvurdering` on `Elevforhold`.
* Removed relation `halvårsordensvurdering` on `Elevforhold`.
* Removed relation `kontaktlærergruppe` on `Elevforhold`.
* Removed relation `kroppsøving` on `Elevforhold`.
* Removed relation `programområde` on `Elevforhold`.
* Removed relation `sidemål` on `Elevforhold`.
* Removed relation `sluttfagvurdering` on `Elevforhold`.
* Removed relation `sluttordensvurdering` on `Elevforhold`.
* Removed relation `underveisfagvurdering` on `Elevforhold`.
* Removed relation `underveisordensvurdering` on `Elevforhold`.
* Removed relation `vurdering` on `Elevforhold`.
* Removed relation `elevforhold` on `Basisgruppe`.
* Removed relation `elevforhold` on `Eksamensgruppe`.
* Removed relation `elevforhold` on `Halvårsfagvurdering`.
* Removed relation `elevforhold` on `Halvårsordensvurdering`.
* Removed relation `elevforhold` on `Kontaktlærergruppe`.
* Removed relation `elevforhold` on `Programområde`.
* Removed relation `elevforhold` on `Sluttfagvurdering`.
* Removed relation `elevforhold` on `Sluttordensvurdering`.
* Removed relation `elevforhold` on `Underveisfagvurdering`.
* Removed relation `elevforhold` on `Underveisordensvurdering`.
* Removed relation `elevforhold` on `Undervisningsgruppe`.
* Removed relation `medlemskap` on `Basisgruppe`.
* Removed relation `medlemskap` on `Eksamensgruppe`.
* Removed relation `medlemskap` on `Elevforhold`.
* Removed relation `medlemskap` on `Fag`.
* Removed relation `medlemskap` on `Faggruppe`.
* Removed relation `medlemskap` on `Gruppe`.
* Removed relation `medlemskap` on `Kontaktlærergruppe`.
* Removed relation `medlemskap` on `Persongruppe`.
* Removed relation `medlemskap` on `Programområde`.
* Removed relation `medlemskap` on `Undervisningsforhold`.
* Removed relation `medlemskap` on `Undervisningsgruppe`.
* Removed relation `medlemskap` on `Utdanningsforhold`.
* Removed relation `medlemskap` on `Utdanningsprogram`.
* Removed relation `medlemskap` on `Årstrinn`.
* Removed relation `undervisningsgruppe` on `Eksamensvurdering`.
* Removed relation `undervisningsgruppe` on `Elevforhold`.
* Removed relation `undervisningsgruppe` on `Fagvurdering`.
* Removed relation `undervisningsgruppe` on `Halvårsfagvurdering`.
* Removed relation `undervisningsgruppe` on `Sluttfagvurdering`.
* Removed relation `undervisningsgruppe` on `Underveisfagvurdering`.

### Felles: Removed deprecated elements
* Removed attribute `foreldreansvar` on `Kontaktperson`.
* Removed relation `person` on `Kontaktperson`.

### Arkiv: Removed deprecated elements
* Removed attribute `format` on `Dokumentobject`.

### Administrasjon: Removed deprecated elements
* Removed relation `lønn` on `Arbeidsforhold`.
* Removed relation `myndighet` on `Fullmakt`.
* Removed relation `fullmakt` on `Aktivitet`.
* Removed relation `fullmakt` on `Anlegg`.
* Removed relation `fullmakt` on `Ansvar`.
* Removed relation `fullmakt` on `Art`.
* Removed relation `fullmakt` on `Diverse`.
* Removed relation `fullmakt` on `Formål`.
* Removed relation `fullmakt` on `Funksjon`.
* Removed relation `fullmakt` on `Kontodimensjon`.
* Removed relation `fullmakt` on `Kontrakt`.
* Removed relation `fullmakt` on `Løpenummer`.
* Removed relation `fullmakt` on `Objekt`.
* Removed relation `fullmakt` on `Prosjekt`.
* Removed relation `fullmakt` on `Prosjektart`.
* Removed relation `fullmakt` on `Ramme`.

### Utdanning: Changed name on Basisgruppe and Basisgruppemedlemskap
* Changed name of class `Basisgruppe` to `Klasse`.
* Changed name of class `Basisgruppemedlemskap` to `Klassemedlemskap`.

#### Klasse
* Changed relation `basisgruppe` on `Kontaktlærergruppe` to `klasse`.
* Changed relation `basisgruppe` on `Skole` to `klasse`.
* Changed relation `basisgruppe` on `Undervisningsforhold` to `klasse`.
* Changed relation `basisgruppe` on `Årstrinn` to `klasse`.

#### Klassemedlemskap
* Changed relation `basisgruppemedlemskap` on `Elevforhold` to `klassemedlemskap`.

### Utdanning: Moved Grepreferanse and Vigoreferanse

#### Basisklasser
* Removed relation `grepreferanse` on `Gruppe`.
* Removed relation `vigoreferanse` on `Gruppe`.

#### Timeplan
* Added relation `grepreferanse` on `Fag`.
* Added relation `vigoreferanse` on `Fag`.

#### Utdanningsprogram
* Added relation `grepreferanse` on `Årstrinn`.
* Added relation `vigoreferanse` on `Årstrinn`.
* Added relation `grepreferanse` on `Programområde`.
* Added relation `vigoreferanse` on `Programområde`.
* Added relation `grepreferanse` on `Utdanningsprogram`.
* Added relation `vigoreferanse` on `Utdanningsprogram`.

### Arkiv: Removed relation to and use of abstract classes
* Removed attribute `arkivnotat` on `DispensasjonAutomatiskFredaKulturminne`.
* Removed attribute `arkivnotat` on `Personalmappe`.
* Removed attribute `arkivnotat` on `Sak`.
* Removed attribute `arkivnotat` on `Saksmappe`.
* Removed attribute `arkivnotat` on `TilskuddFartøy`.
* Removed attribute `arkivnotat` on `TilskuddFredaBygningPrivatEie`.
* Removed relation `mappe` on `Arkivdel`.
* Removed relation `registrering` on `Arkivdel`.

### Økonomi: Changed multiplicity 
* Changed multiplicity for attribute `transaksjonsId` on `Transaksjon`, from 0..1 to 1.



# v3.21.10

|      |                 |
| ---- |-----------------|
| Date | `04.11.2025`    |
| Tag  | `v3.21.10` |

## Features

### Ressurs.Datautstyr

* Added relation `plattform` on `Enhetsgruppe`.
* Added relation `enhetstype` on `Enhetsgruppe`.
* Added relation `organisasjonsenhet` on `Enhetsgruppe`.

# v3.21.0

|      |                 |
| ---- |-----------------|
| Date | `04.11.2025`    |
| Tag  | `v3.21.0` |

## Features 

### Ressurs.Datautstyr

* Added class `DigitalEnhet`
* Added class `Enhetsgruppe`
* Added class `Enhetsgruppemedlemskap`

### Ressurs.Kodeverk

* Added class `Enhetstype`
* Added class `Status`
* Added class `Produsent`


# v3.20.0

|      |                 |
| ---- |-----------------|
| Date | `24.06.2025`    |
| Tag  | `v3.20.0` |

## Features

### Utdanning: Oppmøtetid til Eksamen

* Added attribute `oppmøtetidspunkt` on `Eksamen`.

### Administrasjon: Organisasjonstype

* Added class `Organisasjonstype`.
* Added relation `organisasjonstype` on `Organisasjonselement`.


# v3.19.0

|      |              |
| ---- |--------------|
| Date | `21.01.2025` |
| Tag  | `v3.19.0`    |

## Features

### Arkiv: Innføring av fødselsnummer og organisasjonsnummer på Part

* Added attribute `fødselsnummer` on `Part`.
* Added attribute `organisasjonsnummer` on `Part`.

### Arkiv: Innføring av Tilgangsgruppe

* Added class `Tilgangsgruppe`.
* Added relation `tilgangsgruppe` on `Saksmappe`.
* Added relation `tilgangsgruppe` on `Registrering`.

### Utdanning: Eksamensvurdering

* Added class `Eksamensvurdering`.
* Added relation `eksamensvurdering` on `Elevvurdering`.

#### Utgår

* Deprecated relation `eksamensgruppe` on `Sluttfagvurdering`.



# v3.18.0
 
|      |              |
| ---- | ------------ |
| Date | `12.06.2024` |
| Tag  | `v3.18.0`    |
 
## Features
 
### Eiendeler
 
* Added class `Applikasjon`.
* Added class `Applikasjonsressurs`.
* Added class `Applikasjonsressurstilgjengelighet`.
* Added class `Lisensmodell`.
* Added class `Brukertype`.
* Added class `Håndhevingstype`.
* Added class `Applikasjonskategori`.
* Added class `Plattform`.


# v3.17.0

|      |              |
| ---- | ------------ |
| Date | `07.05.2024` |
| Tag  | `v3.17.0`    |

## Features

### Skille ut Elevvurdering fra Elevforhold

* Added class `Elevvurdering`.
* Added relation `elevvurdering` on `Elevforhold`.
* Added relation `elevvurdering` on `Underveisordensvurdering`.
* Added relation `elevvurdering` on `Halvårsordensvurdering`.
* Added relation `elevvurdering` on `Sluttordensvurdering`.
* Added relation `elevvurdering` on `Underveisfagvurdering`.
* Added relation `elevvurdering` on `Halvårsfagvurdering`.
* Added relation `elevvurdering` on `Sluttfagvurdering`.

#### Utgår

* Deprecated relation `underveisordensvurdering` on `Elevforhold`.
* Deprecated relation `halvårsordensvurdering` on `Elevforhold`.
* Deprecated relation `sluttordensvurdering` on `Elevforhold`.
* Deprecated relation `underveisfagvurdering` on `Elevforhold`.
* Deprecated relation `halvårsfagvurdering` on `Elevforhold`.
* Deprecated relation `sluttfagvurdering` on `Elevforhold`.
* Deprecated relation `elevforhold` on `Underveisordensvurdering`.
* Deprecated relation `elevforhold` on `Halvårsordensvurdering`.
* Deprecated relation `elevforhold` on `Sluttordensvurdering`.
* Deprecated relation `elevforhold` on `Underveisfagvurdering`.
* Deprecated relation `elevforhold` on `Halvårsfagvurdering`.
* Deprecated relation `elevforhold` on `Sluttfagvurdering`.

### Vitnemålsmerknad

* Added class `Vitnemålsmerknad`.
* Added relation `vitnemålsmerknad` on `Elevvurdering`.

### Tilrettelegging på eksamen
* Added relation `eksamensform` on `Elevtilrettelegging`.

### Varselbrev
* Added class `Varsel`.
* Added class `Varseltype`.
* Added relation `varsel` on `Faggruppemedlemskap`.

### Betalingsstatus for privatisteksamen
* Added class `Betalingsstatus`.
* Added relation `betalingsstatus` on `Eksamensgruppemedlemskap`.
	
### Dokumentasjon av faglærte
* Added class `AvlagtPrøve`.
* Added class `Prøvestatus`.
* Added class `Fullførtkode`.
* Added class `Bevistype`.
* Added class `Brevtype`.
* Added relation `avlagtprøvei` on `Lærling`.

Improved and clarified a few descriptions in documentation.


# v3.16.0

|      |              |
| ---- | ------------ |
| Date | `15.12.2023` |
| Tag  | `v3.16.0`    |

## Features

* Utdanning
	* Added class `Fagstatus`.
	* Added class `Eksamen`.
	
	* Changed class `Fraværsregistrering` from `Kompleks datatype` to `Hovedklasse`.
	
	* Added attribute `delegert` on `Eksamensgruppemedlemskap`.
	* Added attribute `kandidatnummer` on `Eksamensgruppemedlemskap`.
	* Added attribute `systemId` on `Elevfravær`.
	* Changed attribute `kommentar` on `Elevfravær`.
	* Removed attribute `fravær` from `Elevfravær`.
	
	* Added relation `fagmerknad` on `Faggruppemedlemskap`.
	* Added relation `fagstatus` on `Faggruppemedlemskap`.
	* Added relation `eksamen` on `Rom`.
	* Added relation `eksamen` on `Eksamensgruppe`.
	* Added relation `foretrukketSkole` on `Eksamensgruppemedlemskap`.
	* Added relation `delegertTil` on `Eksamensgruppemedlemskap`.
	* Added relation `foretrukketSensor` on `Eksamensgruppemedlemskap`.
	* Added relation `skole` on `Faggruppe`.
	* Added relation `skoleår` on `Faggruppe`.
	* Added relation `faggruppe` on `Skole`.
	* Added relation `fraværsregistrering` on `Elevfravær`.
	* Added relation `elevfravær` on `Fraværsregistrering`.

Improved, bugfixed and clarified a few descriptions in documentation.


# v3.15.0

|      |              |
| ---- | ------------ |
| Date | `29.08.2023` |
| Tag  | `v3.15.0`    |

## Features

* Administrasjon
  * Added class `Prosjektart`.
  * Added relation `prosjektart` on `Prosjekt`.
  * Added relation `prosjektart` on `Kontostreng`.

* Personvern
  * Added attribute `slettet` on `Tjeneste`.
  * Added attribute `slettet` on `Behandling`.

## Bugfixes

* Utdanning
  * Removed relation `undervisningsgruppe` on `Fagvurdering`.
  * Changed name on class `OTUngdom` to `OtUngdom`.
  * Changed name on class `OTStatus` to `OtStatus`.
  * Changed name on class `OTEnhet` to `OtEnhet`.

Improved and clarified the descriptions and provided guidelines for using date and datetime fields.


# v3.14.0

|      |              |
| ---- | ------------ |
| Date | `25.04.2023` |
| Tag  | `v3.14.0`    |

## Features

* Utdanning
    * Added class `Lærling`.
    * Added class `OTUngdom`.
    * Added class `OTStatus`.
    * Added class `OTEnhet`.
    * Added relation `otungdom` on `Programområdemedlemskap`.
    * Added relation `lærling` on `Programområdemedlemskap`.
    * Changed multiplicity for relation `elevforhold` on `Programområdemedlemskap`, from 1 to 0..1.

* Felles
    * Added relation `otungdom` on `Person`.
    * Added relation `lærling` on `Person`.
    * Added relation `lærling` on `Virksomhet`.

## Bugfixes

* Removed duplicate class `Karakterstatus`.


# v3.13.0

|      |              |
| ---- | ------------ |
| Date | `14.02.2023` |
| Tag  | `v3.13.0`    |

## Features

* Økonomi
    * Added class `Postering`.
    * Added class `Transaksjon`.
    * Added class `Leverandør`.
    * Added class `Leverandørgruppe`.
    * Added class `Valuta`
    * Added complex datatype `Bilag`.

* Felles
    * Added class `Virksomhet`.


# v3.12.0

|      |              |
| ---- | ------------ |
| Date | `17.11.2022` |
| Tag  | `v3.12.0` |


## Features

* Arkiv
  * Added attribute `tiltak` on `DispensasjonAutomatiskFredaKulturminne`.

* Utdanning
  * Added relation `faggruppe` on `Fraværsregistrering`.

* Administrasjon
  * Added class `Arbeidslokasjon`.
  * Added relation `arbeidslokasjon` on `Arbeidsforhold`.


# v3.11.10

|      |              |
| ---- | ------------ |
| Date | `11.10.2022` |
| Tag  | `v3.11.10` |


## Bugfix

* Utdanning
  * Faggruppe now inherit Gruppe


# v3.11.0

|      |              |
| ---- | ------------ |
| Date | `07.09.2022` |
| Tag  | `v3.11.0` |


## Features

* Utdanning
  * Added class `Eksamensform`.
  * Added class `Karakterhistorie`.
  * Added class `Karakterstatus`.
  * Added class `Elevfravær`.
  * Added class `Faggruppemedlemskap`.
  * Added class `Faggruppe`.
  * Added class `Sensor`.
  
  * Added complex datatype `Fraværsregistrering`.
  
  * Added attribute `tospråkligFagopplæring` on `Elevforhold`.
  * Changed attribute `karakter ` on `Fagvurdering`.

  * Added relation `fraværsregistreringer` on `Elevforhold`.
  * Added relation `faggruppemedlemskap` on `Elevforhold`.
  * Added relation `skoleår` on `Elevforhold`.
  * Added relation `faggruppe` on `Fag`.
  * Added relation `nus` on `Eksamensgruppemedlemskap`.
  * Added relation `sensor` on `Eksamensgruppe`.
  * Added relation `eksamensform` on `Eksamensgruppe`.
  * Added relation `sensor` on `Skoleressurs`.
  * Added relation `karakterhistorie` on `Sluttfagvurdering`.

  
* Administrasjon
  * Added class `Formål`.

  * Added relation `formål` on `Kontostreng`.
  * Added relation `formål` on `Arbeidsforhold`.
  * Added relation `formål` on `Fullmakt`.

* Arkiv
  * Added class `Saksmappetype`

  * Added attribute `skjerming` on `Korrespondansepart`.

  * Added relation `saksmappetype` on `Saksmappe`.

## Deprecated

Note: Deprecated classes, attributes and relations might be removed in the next major release.

* Utdanning
  * The relation `fravær` on `Elevforhold` is deprecated.

## Bugfixes

* Administrasjon
  * The deprecated relation `myndighet` in `Fullmakt` changed multiplisity from 1..* to 0..*


# v3.10.0

|      |              |
| ---- | ------------ |
| Date | `09.12.2021` |
| Tag  | `v3.10.0` |

Utdanning has been the main focus of this release. Only smaller changes have been done on other domains.

## Features

* Utdanning
  * Added abstract class `Fagvurdering`.
  * Added abstract class `Ordensvurdering`.
  * Added class `Underveisfagvurdering`.
  * Added class `Halvårsfagvurdering`.
  * Added class `Sluttfagvurdering`.
  * Added class `Underveisordensvurdering`.
  * Added class `Halvårsordensvurdering`.
  * Added class `Sluttordensvurdering`.
  * Added relation `sluttordensvurdering` on `Elevforhold`.
  * Added relation `underveisfagvurdering` on `Elevforhold`.
  * Added relation `halvårsfagvurdering` on `Elevforhold`.
  * Added relation `sluttfagvurdering` on `Elevforhold`.
  * Added relation `halvårsordensvurdering` on `Elevforhold`.
  * Added relation `underveisordensvurdering` on `Elevforhold`.

  The changes above replace `Vurdering`

  * Added class `Anmerkninger`.
  * Added class `Elevtilrettelegging`.
  * Added class `Fraværsoversikt`.
  * Added complex datatype `Fagvurdering`.
  * Added complex datatype `Fraværsprosent`.
  * Added complex datatype `Ordensvurdering`.
  * Added attribute `gjest` on `Elev`.
  * Added attribute `hybeladresse` on `Elev`.
  * Added relation `tilrettelegging` on `Fag`.
  * Added relation `elevfravær` on `Fag`.
  * Added relation `kommune` on `Person`.
  * Added relation `registrertav` on `Fravær`.

  * Added attribute `anmerkninger` on `Elevforhold`.
  * Added attribute `avbruddsdato` on `Elevforhold`.
  * Added relation `sidemål` on `Elevforhold`.
  * Added relation `kroppsøving` on `Elevforhold`.
  * Added relation `avbruddsårsak` on `Elevforhold`.
  * Added relation `elevfravær` on `Elevforhold`.
  * Added relation `tilrettelegging` on `Elevforhold`.

  * Added class `Avbruddsårsak` (kodeverk).
  * Added class `Fagmerknad` (kodeverk).
  * Added class `Tilrettelegging` (kodeverk).

* Felles
  * Added relation `kommune` on `Person`.

## Deprecated

*Note:* Deprecated classes, attributes and relations might be removed in the next major release.

* Utdanning
  * The class `Vurdering` is deprecated.
  * The attribute `dokumentert` on `Fravær` is deprecated.
  * The relation `vurdering` on `Elevforhold` is deprecated.
  * The relation `eksamensgruppe` on `Fravær` is deprecated.

## Bugfixes

* Utdanning
  * Added description for attribute `persongruppemedlemskap` on `Elevforhold`.
  * Clarified description for reference `Grepreferanse`.

* Felles
  * Clarified description for attribute `foreldreansvar` on `Person`.
  * Clarified description for attribute `foreldre` on `Person`.

# v3.9.0


|      |              |
| ---- | ------------ |
| Date | `10.06.2021` |
| Tag  | `v3.9.0`     |

## Features

* Utdanning
  * Added class `Persongruppe`.
  * Added class `Persongruppemedlemskap`.
  * Added attribute `eksamensdato` on `Eksamensgruppe`.

* Arkiv
  * Added `Avskrivning` as complex datatype.

## Deprecated

*Note:* Deprecated classes, attributes and relations might be removed in the next major release.

* Utdanning
  * The relation `basisgruppe` on `Elevforhold` is deprecated.
  * The relation `undervisningsgruppe` on `Elevforhold` is deprecated.
  * The relation `kontaktlærergruppe` on `Elevforhold` is deprecated.
  * The relation `eksamensgruppe` on `Elevforhold` is deprecated.
  * The relation `programområde` on `Elevforhold` is deprecated.

## Bugfixes

* Arkiv
  * Changed name of field `fartoyNavn` on `TilskuddFartøy` from `fartoyNavn` to `fartøyNavn`.

# v3.8.10


|      |              |
| ---- | ------------ |
| Date | `14.04.2021` |
| Tag  | `v3.8.10`     |

## Bugfixes

* Arkiv
  * Changed name of relation `format` on `Dokumentobjekt` from `format` to `filformat`.
  
# v3.8.0


|      |              |
| ---- | ------------ |
| Date | `24.03.2021` |
| Tag  | `v3.8.0`     |

## Deprecated

*Note:* Deprecated classes, attributes and relations might be removed in the next major release.

* Administrasjon
  * The relation `myndighet` on `Fullmakt` is deprecated.
  * The relation `fullmakt` on `Kontodimensjon` is deprecated.

* Arkiv
  * The attribute `format` on `Dokumentobjekt` is deprecated.

## Bugfixes

* Arkiv
  * Changed multiplicity for attribute `klasse` on `Registrering`, from 1 to 0..1.

* Utdanning
  * Changed multiplicity for relation `utdanningsprogram` on `Programområde`, from 1 to 1..*.
  
## Features 

* Administrasjon
  * Added relation `aktivitet`, `anlegg`, `ansvar`, `art`, `diverse`, `funksjon`, `kontrakt`, `løpenummer`, `objekt`, `prosjekt`, `ramme` and `organisasjonselement` to `Fullmakt`.
  * Added relation `aktivitet`, `anlegg`, `diverse`, `kontrakt`, `løpenummer`, `objekt`, `prosjekt`, `ramme` to `Arbeidsforhold`.

* Arkiv
  * Added class `Format` as `Kodeverk`.
  * Added relation `format` to `Dokumentobjekt`. 

# v3.7.0


|      |              |
| ---- | ------------ |
| Date | `01.02.2021` |
| Tag  | `v3.7.0`     |

## Features 

* Administrasjon
  * Added attribute `kildesystemId` to `Fravær`.
  * Added attribute `godkjent` and relation `godkjenner` to `Fravær`.

* Arkiv
  * Added domain `Samferdsel` and class `SøknadDrosjeløyve`.
  
* Personvern
  * Added relation `samtykke` to `Behandling`.

* Felles
  * Added attribute `adresse` to `Matrikkelnummer`.

# v3.6.10


|      |              |
| ---- | ------------ |
| Date | `19.10.2020` |
| Tag  | `v3.6.10`     |

For more details, see https://github.com/FINTLabs/fint-informasjonsmodell/issues/197

## Bugfixes

* Arkiv
  * Fixed mulitiplicity for `klasse` on `Mappe`, from 0..1 to 0..*.

# v3.6.0

|      |              |
| ---- | ------------ |
| Date | `08.10.2020` |
| Tag  | `v3.6.0`     |

For more details, see https://github.com/FINTLabs/fint-informasjonsmodell/milestone/13

## Deprecated

*Note:* Deprecated classes, attributes and relations might be removed in the next major release.

* Utdanning
  * The attribute `periode` on `Gruppe` is deprecated. Timeframes for relevant group types should be represented using relations to `Termin` and/or `Skoleår`.

## Features

* Arkiv
  * Archive represents a new domain in the information model. The domain includes  `Noark`, `Kulturminnevern`, `Personal` and `Kodeverk`. Needs that are covered are joint integration with archive systems in accordance with the Noark 5 version 5.0 standard, and specific case types of personnel files and grants for cultural heritage.

* Økonomi
  * Economy represents a new domain in the information model. The domain includes `Faktura` and `Kodeverk`. Needs that are covered are joint integration with economy systems, limited to invoices and product registers, and especially invoicing of pupils in upper secondary education.

* Personvern
  * Privacy represents a new domain in the information model. The domain includes `Samtykke` and `Kodeverk`. Needs that are covered are collection and exchange of consents, at the individual level, which expresses which personal data can be processed by which services and for what purpose.

* Utdanning
  * Added relation from `Skoleressurs` to `Person`. The relation should be a link to a person object in the administrative domain, as the authoritative source for information on employees. The relation must be hardcoded in the adapter, if not it will automatically create a link to a person object in the education domain.

* Felles
  * Added `Matrikkelnummer` as complex datatype.
  
* Administrasjon
  * Added `jobbtittel` to `Personalressurs`.

# v3.5.0

|      |              |
| ---- | ------------ |
| Date | `04.05.2020` |
| Tag  | `v3.5.0`     |

For more details, see https://github.com/FINTLabs/fint-informasjonsmodell/milestone/12

## Features

* Administrasjon
  * Added `arbeidsforholdsperiode` to `Arbeidsforhold`
* Utdanning
  * Added abstract class `Gruppemedlemskap` as well as specific classes for `Undervisningsgruppemedlemskap`, 
    `Basisgruppemedlemskap`, `Kontaktlærergruppemedlemskap`, `Eksamensgruppemedlemskap`, and `Programområdemedlemskap`.
    These classes represent memberships for `Elevforhold` with added information on `gyldighetsperiode`. 
  * Added `Skoleår` and `Termin`.  These are code lists for school years and school terms.  Added relations to these
    from all relevant group types.
  * Added `gyldighetsperiode` and `hovedskole` to `Elevforhold`.

## Bugfixes

* Felles
  * Fixed documentation for `Kjønn` and `Periode`
* Administrasjon
  * Fixed multiplicity on `overordnet` reference for `Organisasjonselement`.
* Utdanning
  * Fixed documentation for `Gruppe`, `Grepreferanse` and `Vigoreferanse`

# v3.4.0

|      |              |
| ---- | ------------ |
| Date | `09.01.2020` |
| Tag  | `v3.4.0`     |

For more details, see https://github.com/FINTLabs/fint-informasjonsmodell/milestone/11

## Features

* Administrasjon
  * Added `Aktivitet`, `Anlegg`, `Diverse`, `Kontrakt`, `Løpenummer`, `Objekt` and `Ramme` as `Kontodimensjon`

## Bugfixes

* Administrasjon
  * Updated documentation on `Arbeidsforhold`

* Felles
  * Updated documentation on `Kontaktinformasjon`

# v3.3.0

|      |              |
| ---- | ------------ |
| Date | `06.09.2019` |
| Tag  | `v3.3.0`     |

For more details, see https://github.com/FINTLabs/fint-informasjonsmodell/milestone/10

## Features

* Administrasjon
  * Added `kildesystemId` to `Lønn`

## Bugfixes

* Felles
  * Updated documentation on `Kontaktinformasjon`

# v3.2.0

|      |              |
| ---- | ------------ |
| Date | `03.05.2019` |
| Tag  | `v3.2.0`     |

For more details, see https://github.com/FINTLabs/fint-informasjonsmodell/milestone/9

## Deprecated

*Note:* Deprecated classes, attributes and relations might be removed in the next major release.

* Felles
  * The relation `person` on `Kontaktperson` has been deprecated.  `Kontaktperson` now contains
    `navn` and `kontaktinformasjon` that should be used instead.
  * The attribute `foreldreansvar` on `Kontaktperson` has been deprecated.  Parents and children
    should be represented using the new relation `foreldre` and `foreldreansvar` from `Person` to
    `Person`.

## Features

* Felles
  * Added relation `foreldreansvar`..`foreldre` from `Person` to `Person`.  

* Administrasjon
  * Added relation from `Fraværstype` to `Lønnsart`
  * Added relation from `Lønnsart` to `Art`
  * Added relation from `Personalressurs` to `Art`

* Utdanning
  * Relation from `Skoleressurs` to `Skole` is now `0..*` for teachers associated with several
    schools.
  * Added relation from `Elevforhold` to `Programområde`.
  * Vigo Kodeverk has been moved to a separate repository.  No changes in naming or packaging otherwise.
  * On `Elev`, `kontaktinformasjon` is now marked as `writable` to account for updates via the API.

# v3.1.0

|      |              |
| ---- | ------------ |
| Date | `24.09.2018` |
| Tag  | `v3.1.0`     |

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
    * A new attribute `endelig` on `Vurdering` indicates final assessments.
  * Relations from `Vurdering` and `Fravær` to `Undervisningsgruppe` and `Eksamensgruppe` are used to indicate
    absence and assessments in context of these groups.

## Bugfixes

* Utdanning
  * Fixed multiplicity on relation to `Elevkategori` from `Elevforhold`.
  * Documentation updates.

# v3.0.0

|      |              |
| ---- | ------------ |
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
| ---- | ------------ |
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
| ---- | ------------ |
| Date | `05.04.2018` |
| Tag  | `v2.7.0`     |

## Features

* Utdanning
  * Added support for `feidenavn` for both students (`Elev`) and faculty/staff (`Skoleressurs`)
* Administrasjon
  * Added `kategori` to `Lønnsart`

# v2.6.0

|      |              |
| ---- | ------------ |
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
| ---- | ------------ |
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
| ---- | ------------ |
| Date | `07.12.2017` |
| Tag  | `v2.2.20`    |

## Bugfixes

* Made the attribute `brukernavn` optional on `Personalressurs` and `Elev`.

# v2.2.10

|      |              |
| ---- | ------------ |
| Date | `27.11.2017` |
| Tag  | `v2.2.10`    |

## Bugfixes

* Added new optional attribute `passiv` to `Begrep`.  Fixes #44.

# v2.2.0

|      |              |
| ---- | ------------ |
| Date | `27.10.2017` |
| Tag  | `v2.2.0`     |

## Features

* Added support for code lists from Vigo.  This is a pure addition to the model, with no impact to the existing model.
* References from the `Utdanning` model to Vigo code lists is represented as external references.


# v2.0.10

|      |              |
| ---- | ------------ |
| Date | `05.10.2017` |
| Tag  | `v2.0.10`    |

## Bugfixes

* Made association between `Organisasjonselement` and `Arbeidsforhold` bidirectional (fixes #38)
* Fixed multiplicity from `Elevforhold` to `Elevkategori` (fixes #36)
* Fixed documentation for `Art` and `Funksjon` (fixes #37)


# v2.0.0

|      |              |
| ---- | ------------ |
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
| ---- | ------------ |
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
| ---- | ------------ |
| Date | `07.04.2017` |
| Tag  | `v1.0.0`     |

* Initial release

## Features

* Common classes (`Fellesmodell`)
* Classes for Administration domain (`Administrasjon`):
  * `Personal`
  * `Organisasjon`
  * `Kodeverk`

