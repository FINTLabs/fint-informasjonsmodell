# FINT-informasjonsmodell

Innhold i informasjonsmodellen som benyttes i felleskomponentene som lages i FINT-prosjektet. Se [fintprosjektet.no](https://www.fintprosjektet.no) 

Release notater finner her: [RELEASE-NOTES.md](RELEASE-NOTES.md)

## Dokumentasjon

Dokumentasjon av informasjonsmodellen blir automatisk publisert på [informasjonsmodell.felleskomponent.no](https://informasjonsmodell.felleskomponent.no/)

## Versjonsnummerering

Prosjektet bruker [semantisk versjonering](http://semver.org/) for å spesifisere bakoverkompatibilitet.

De tre posisjonene i versjonsnummeret brukes slik:

1. _Major_: Denne økes med 1 når det introduseres endringer som bryter bakoverkompatibilitet. Modeller med forskjellig major versjon kan ikke utveksle data uten tap av informasjon.
1. _Minor_: Denne økes med 1 når ny funksjonalitet legges til modellen.  Klienter som brukere en lavere minor versjon kan bruke informasjonen, men ikke nyttiggjøre seg de elementene som er lagt til.
1. _Patch_: Denne økes med 10 når kompatible forbedringer eller forbedret dokumentasjon legges til modellen.  Klienter kan forvente å representere informasjonen likt, selv med forskjellige patch versjoner.  Patch økes med 10 for å gi rom for oppdateringer i kode basert på samme versjon av informasjonsmodellen.

Klienter og generert Java og C#-kode skal i utgangspunktet versjoneres likt som informasjonsmodellen, men kan øke patch med 1 for endringer som kun gjelder internt.

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
1. Oppdater RELEASE_NOTES.md - husk at Table of Contents må oppdateres med en plugin som håndterer MarkdownTOC.
1. Åpne Pull Request i GitHub for å få endringene tilbake til master.
1. Kommenter alle issues som er berørt av endringen.
1. Se over Pull Request, be om tilbakemeldinger.
1. Aksepter Pull Request og merge til `master`.
1. Lukk alle issues som er berørt av endringen.
1. Lag en ny prerelease med navn på formen `v0.0.0-rc-0`
1. Kontroller den genererte modellen og modellkoden
1. Lag en ny release med navn på formen `v0.0.0`

### Merging og konflikter

Vi benytter [LemonTree](https://www.lieberlieber.com/lemontree/en/) for merging.  Denne settes opp i Git på følgende måte:

```
merge.lemontree.name=lemontree merge driver
merge.lemontree.driver='C:\Program Files\LieberLieber\LemonTree\LemonTree.exe' --merge=auto --base=%O --mine=%A --theirs=%B --out=%A
merge.lemontree.recursive=binary
merge.tool=lemontree
mergetool.lemontree.cmd='C:/Program Files/LieberLieber/LemonTree/LemonTree.exe' --merge=auto --base="$BASE" --mine="$LOCAL" --theirs="$REMOTE" --out="$MERGED"
diff.tool=lemontree
difftool.lemontree.cmd='C:\Program Files\LieberLieber\LemonTree\LemonTree.exe' --diff --base=$LOCAL --mine=$LOCAL --theirs=$REMOTE
```

For "enkle" konflikter vil LemonTree kunne håndtere flettingen automatisk.  Merk at LemonTree vil 
forsøke å håndtere `FINT-informasjonsmodell.xml`, men dette feiler.  Etter at 
`FINT-informasjonsmodell.eap` er OK, åpne denne i Enterprise Architect og eksportert XMI på nytt
i merge-commit.

Dersom konflikten er vanskeligere vil LemonTree åpne et brukergrensesnitt for å håndtere konfliktene.

### Sjekkliste for endringer i modellen

  1. Alt skal skje innenfor pakken `FINT`.
  1. Pakker under `FINT` kun i to nivåer.
  1. Hovedklasse?  Legg til stereotypen `hovedklasse`.
  1. Dokumentasjon på felter og relasjoner.
  1. Multiplisitet: Nye obligatoriske felter og relasjoner er ikke bakoverkompatible.
  1. Relasjoner kan kun gå til hovedklasser, og ikke til abstrakte klasser.
  1. Relasjoner bør gå fra hovedklasser eller komplekse datatyper, og ikke fra abstrakte klasser.
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
- Pakkene skal representere en semantisk gruppering innenfor domenet.
- I pakken `Kodeverk` skal alle klasser arve `Begrep` og være `hovedklasse`. 
- Alle klasser, attributter og relasjoner skal ha dokumentasjon som beskriver bruken og forståelsen.

## Enterprise Architect

Modellen er utviklet og vedlikeholdt med Enterprise Architect versjon 13.5.  Det er tilstrekkelig med
lisens for Professional Edition.

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

Modellkode blir produsert automatisk for alle releaser (tags) på modellen.  Versjonsnummeret til den
produserte modellkoden vil være det samme som versjonsnummeret for modellen.
