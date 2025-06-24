﻿# FINT-informasjonsmodell

Innhold i Informasjonsmodellen som benyttes i felleskomponentene utarbeides og vedlikeholdes av [Novari IKS](https://novari.no). Se også [fintlabs.no](https://fintlabs.no/) for ytterlige informasjon.

Releasenotater finner her: [RELEASE-NOTES.md](RELEASE-NOTES.md)

## Dokumentasjon

Dokumentasjon av Informasjonsmodellen blir automatisk publisert på [informasjonsmodell.felleskomponent.no](https://informasjonsmodell.felleskomponent.no/)

## Versjonsnummerering

Det brukes [semantisk versjonering](http://semver.org/) for å spesifisere bakoverkompatibilitet.

De tre posisjonene i versjonsnummeret brukes slik:

1. _Major_: Denne økes med 1 når det introduseres endringer som bryter bakoverkompatibilitet. Modeller med forskjellig major versjon kan ikke utveksle data uten tap av informasjon.
1. _Minor_: Denne økes med 1 når ny funksjonalitet legges til modellen.  Klienter som brukere en lavere minor versjon kan bruke informasjonen, men ikke nyttiggjøre seg de elementene som er lagt til.
1. _Patch_: Denne økes med 10 når kompatible forbedringer eller forbedret dokumentasjon legges til modellen.  Klienter kan forvente å representere informasjonen likt, selv med forskjellige patch versjoner.  Patch økes med 10 for å gi rom for oppdateringer i kode basert på samme versjon av informasjonsmodellen.

Klienter og generert Java og C#-kode skal i utgangspunktet versjoneres likt som Informasjonsmodellen, men kan øke patch med 1 for endringer som kun gjelder internt.

## Arbeidsflyt

### Hvordan åpne og gjøre endringer

1. Sjekk ut prosjektet fra GitHub
1. Lag en ny branch
1. Åpne `FINT-informasjonsmodell.eap` i Sparx Enterprise Architect
1. Gjør ønskede endringer
1. Pass på at Enterprise Architect er satt opp med `windows-1252` som tegnsett for eksport til XMI.
1. Eksporter prosjekt til `FINT-informasjonsmodell.xml` ved å gå til følgende meny: _Model_ -> _Import/Export_ -> _Export Package for XMI_ (**`Ctrl + Alt + E`**). Velg _Export Type_ `XMI 2.1`.
1. Commit og push prosjektet tilbake til GitHub.
1. Sjekk branch på https://informasjonsmodell.felleskomponent.no
1. Generer modellkode og se etter problemer: `docker run -itv $PWD:/src fint/fint-model --tag <mybranch> generate`
1. Oppdater RELEASE_NOTES.md - husk at Table of Contents må oppdateres med en plugin som håndterer Markdown TOC (For Visual Studio Code: [Markdown All In One](https://marketplace.visualstudio.com/items?itemName=yzhang.markdown-all-in-one)).
1. Åpne Pull Request i GitHub for å få endringene tilbake til master.
1. Kommenter alle issues som er berørt av endringen.
1. Se over Pull Request, be om tilbakemeldinger.
1. Aksepter Pull Request og merge til `master`.
1. Lukk alle issues som er berørt av endringen.
3. Lag en ny prerelease med navn på formen `v0.0.0-rc-0`
4. Kontroller den genererte modellen og modellkoden
5. Lag en ny release med navn på formen `v0.0.0`. 
5. Pull request for Java- og C#-modeller blir publisert automatisk. 

### Dersom du skal oppdatere jsonschema og GraphQL:

Oppdater versjonsnummer og trigg GitHub Action i 
  * [fint-jsonschema](https://github.com/FINTLabs/fint-jsonschema/)
  * [fint-graphql](https://github.com/FINTLabs/fint-graphql/)

### Dersom du skal generer nye konsumere:    
  
Generer consumere fra modellen: [fint-release-utils](https://github.com/FINTLabs/fint-release-utils)
  * ([fint-consumer-skeleton](https://github.com/FINTLabs/fint-consumer-skeleton) inneholder mal for consumere)

### Sjekkliste for endringer i modellen

  1. Alt skal skje innenfor pakken `FINT`.
  1. Pakker under `FINT` kun i to nivåer.
  1. Hovedklasse?  Legg til stereotypen `hovedklasse`.
  1. Dokumentasjon på felter og relasjoner.
  1. Multiplisitet: Nye obligatoriske felter og relasjoner er ikke bakoverkompatible.
  1. Relasjoner kan kun gå til hovedklasser, og ikke til abstrakte klasser.
  1. Alle hovedklasser må ha minst én `Identifikator`.
  1. Retning og multiplisitet på relasjoner.  Enveis eller toveis? 
  1. Typer på attributter.  Enten en kompleks datatype fra modellen, eller en av disse: `long`, `int`, `date`, `dateTime`, `float`, `double`, `string`, `boolean`.
  1. Er attributten skrivbar?  Legg i så fall på stereotypen `writable`.

## Navnekonvensjoner

- Klasser og attributter er i entall.
- Uttrykk bestående av flere ord slås sammen med stor forbokstav i mellom ordene: _endelig karakter_ -> `endeligKarakter`. 
- Klasser skal være meningsbærende begreper.
- Dokumentasjon benyttes til å definere forståelsen av begrepet, og referere til dokumentasjon og kilde for definisjonen.
- Begreper på assosiasjoner skal forståes i kontekst av navnet på de klassene de går i mellom.
- Innenfor hvert domene er det tre faste underpakker:
   - `Basisklasser`
   - `Kodeverk`
   - `Komplekse datatyper`
- De andre pakkene skal representere en semantisk gruppering innenfor domenet.
- Alle klasser, attributter og relasjoner skal ha dokumentasjon som beskriver bruken og forståelsen.

## Enterprise Architect

Modellen er utviklet og vedlikeholdt med Enterprise Architect versjon 15.2.  Det er tilstrekkelig med lisens for Professional Edition.

Vi benytter et svært begrenset sett av funksjonaliteten som finnes.  Følgende elementer benyttes:

 - Class Diagram
 - Class:
   - Package
   - Class
 - Class Relationships:
   - Generalize
   - Associate
 - Stereotype:
   - `ApplicationSchema` på pakker
   - `hovedklasse` på klasser
   - `writable` på attributter
 - Tags
   - `DEPRECATED` på Class, Attribute eller Association

## Generering av modellkode

Modellkode blir produsert automatisk for alle releaser (tags) på modellen.  Versjonsnummeret til den produserte modellkoden vil være det samme som versjonsnummeret for modellen.
