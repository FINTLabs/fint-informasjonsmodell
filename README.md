# FINT-informasjonsmodell

Innehold i informasjonsmodellen som benyttes i felleskomponentene som lages i FINT-prosjektet. Se [fintprosjektet.no](http://fintprosjektet.no) 

Release notater finner her: [RELEASE-NOTES.md](RELEASE-NOTES.md)

## Dokumentasjon

Dokumentasjon av informasjonsmodellen blir automatisk publisert på [dokumentasjon.felleskomponent.no](https://dokumentasjon.felleskomponent.no/)

## Arbeidsflyt

### Hvordan åpne og gjøre endringer

1. Åpne `FINT-informasjonsmodeller.eap` i Sparx Enterprise Architect
1. Gjør ønskede endringer
1. Pass på at Enterprise Architect er satt opp med `windows-1252` som tegnsett for eksport til XMI.
1. Eksporter prosjekt til FINT-informasjonsmodell.xml ved å gå til følgende meny: _Model_ -> _Import/Export_ -> _Export Package for XMI_ (**`Ctrl + Alt + E`**)

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
