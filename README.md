# FINT-informasjonsmodell

Innehold i informasjonsmodellen som benyttes i felleskomponentene som lages i FINT-prosjektet. Se [fintprosjektet.no](http://fintprosjektet.no) 

Release notater finner her: [RELEASE-NOTES.md](RELEASE-NOTES.md)

## Dokumentasjon

Dokumentasjon av informasjonsmodellen blir automatisk publisert på [informasjonsmodell.felleskomponent.no](https://informasjonsmodell.felleskomponent.no/)

## Versjonsnummerering

Prosjektet bruker [semantisk versjonering](http://semver.org/) for å spesifisere bakoverkompatibilitet.

De tre posisjonene i versjonsnummeret brukes slik:

1. Major. Denne økes med 1 når det introduseres endringer som bryter bakoverkompatibilitet. Modeller med forskjellig major versjon kan ikke utveksle data uten tap av informasjon.
1. Minor. Denne økes med 1 når ny funksjonalitet legges til modellen.  Klienter som brukere en lavere minor versjon kan bruke informasjonen, men ikke nyttiggjøre seg de elementene som er lagt til.
1. Patch. Denne økes med 10 når kompatible forbedringer eller forbedret dokumentasjon legges til modellen.  Klienter kan forvente å representere informasjonen likt, selv med forskjellige patch versjoner.  Patch økes med 10 for å gi rom for oppdateringer i kode basert på samme versjon av informasjonsmodellen.

Klienter og generert Java og C#-kode skal i utgangspunktet versjoneres likt som informasjonsmodellen, men kan øke patch med 1 for endringer som kun gjelder internt.

## Arbeidsflyt

### Hvordan åpne og gjøre endringer

1. Åpne `FINT-informasjonsmodeller.eap` i Sparx Enterprise Architect
1. Gjør ønskede endringer
1. Pass på at Enterprise Architect er satt opp med `windows-1252` som tegnsett for eksport til XMI.
1. Eksporter prosjekt til FINT-informasjonsmodell.xml ved å gå til følgende meny: _Model_ -> _Import/Export_ -> _Export Package for XMI_ (**`Ctrl + Alt + E`**). Velg _Export Type_ `XMI 2.1`.

## Navnekonvensjoner

- Klasser og attributter er i entall.
- Uttrykk bestående av flere ord slås sammen med stor forbokstav i mellom ordene: _endelig karakter_ -> `endeligKarakter`. 
- Klasser skal være meningsbærende begreper.
- Dokumentasjon benyttes til å definere forståelsen av begrepet, og referere til dokumentasjon og kilde for definisjonen.
- Begreper på assosiasjoner skal forståes i kontekst av navnet på de klassene de går i mellom.
- Innenfor hvert domene er det tre faste underpakker:
  1. `Basisklasser`
  1. `Kodeverk`
  1. `Komplekse datatyper`
- De andre pakkene skal representere en semantisk gruppering innenfor domenet.
- Alle klasser, attributter og relasjoner skal ha dokumentasjon som beskriver bruken og forståelsen.
