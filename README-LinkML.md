# FINT Informasjonsmodell med LinkML

<!-- TOC depthfrom:2 insertanchor:false detectandautosetsection:true -->

- [Definisjon av informasjonsmodellen](#definisjon-av-informasjonsmodellen)
    - [Kardinalitet/multiplisitet](#kardinalitetmultiplisitet)
        - [Felter og relasjoner](#felter-og-relasjoner)
        - [Forskjell på felter og relasjoner](#forskjell-p%C3%A5-felter-og-relasjoner)
    - [Utgått/deprecated](#utg%C3%A5ttdeprecated)
        - [Felt som er utgått](#felt-som-er-utg%C3%A5tt)
        - [Klasse som er utgått](#klasse-som-er-utg%C3%A5tt)
        - [Relasjon som er utgått](#relasjon-som-er-utg%C3%A5tt)
    - [Stereotyper på klasser](#stereotyper-p%C3%A5-klasser)
        - [hovedklasse](#hovedklasse)
        - [referanse](#referanse)
        - [abstrakt](#abstrakt)
        - [kompleks datatype](#kompleks-datatype)
- [Pågående avklaringer og beslutninger](#p%C3%A5g%C3%A5ende-avklaringer-og-beslutninger)
    - [Komplekse datatyper med inlined og inlined_as_list brukes ikkeikke](#komplekse-datatyper-med-inlined-og-inlined_as_list-brukes-ikkeikke)
    - [Hva gjør vi med isSource/primaryRelation?](#hva-gj%C3%B8r-vi-med-issourceprimaryrelation)
- [Utvikling](#utvikling)
    - [Kom i gang](#kom-i-gang)
    - [Generer LinkML-modell fra Enterprise Architect sin XMI](#generer-linkml-modell-fra-enterprise-architect-sin-xmi)
    - [Generer XMI som likner på Enterprise Architect sin XMI fra LinkML](#generer-xmi-som-likner-p%C3%A5-enterprise-architect-sin-xmi-fra-linkml)
    - [Valider og lint LinkML-modellll](#valider-og-lint-linkml-modellll)
    - [Teste genering av Java](#teste-genering-av-java)
    - [Verktøy som blir tilgjengelig med LinkML](#verkt%C3%B8y-som-blir-tilgjengelig-med-linkml)
    - [Andre verktøy](#andre-verkt%C3%B8y)

<!-- /TOC -->

## Definisjon av informasjonsmodellen

LinkML brukes til å definere informasjonsmodellen for FINT. Denne filen beskriver hvordan vi bruker LinkML til å definere modellen.

### Kardinalitet/multiplisitet

LinkML bruker `required` og `multivalued` for å definere kardinalitet. Dette er en standard måte å gjøre det på i LinkML.

#### Felter og relasjoner

Både felter og relasjoner defineres med `range` i LinkML, men de kan ende opp med å behandles ulikt i generert XMI/Java.

```yaml
  gyldighetsperiode:
    range: Periode          # 0..1

  navn:
    range: Personnavn
    required: true          # 1..1

  adresser:
    range: Adresse
    multivalued: true       # 0..*

  foreldre:
    range: Person
    multivalued: true
    required: true          # 1..*  
```

#### Forskjell på felter og relasjoner

I LinkML ser begge deler like ut (`attributes` med `range`), men i generert XMI/Java/etc behandles de ulikt:

- **Felt (attributt)**: `range` er en primitiv type (`string`, `boolean`, `integer`, osv.) eller en **kompleks datatype** (klasse uten `Identifikator` og uten `abstract: true`).
  - Genereres som felt i Java (`private ...`).
- **Relasjon**: `range` peker til en **hovedklasse** (klasse med `Identifikator`).
  - Genereres som relasjon i Java (`Relasjonsnavn` / links i resource-klasser), ikke som vanlig felt.

Praktisk tommelfingerregel:

- `Identifikator` i målklassen => relasjon
- Ingen `Identifikator` i målklassen => felt (kompleks datatype)



### Utgått/deprecated

#### Felt som er utgått

```yaml
  eksamensgruppe:
    range: Eksamensgruppe
    description: |
Eksamensgruppe vurderingen er foretatt i.
    deprecated: >  
      Bruk Eksamensvurdering
```

#### Klasse som er utgått

```yaml
Medlemskap:
  deprecated: >
    Gruppemedlemskap representeres i stedet som relasjoner mellom
    Elevforhold eller Undervisningsforhold og de aktuelle gruppene.
```

#### Relasjon som er utgått

```yaml
  attributes:
    person:
      deprecated: >
        Kontaktperson inneholder nå navn og kontaktinformasjon,
        som skal brukes i stedet.
```

### Stereotyper på klasser

Det er behov for å bevare EA-stereotype på klassenivå i LinkML. `hovedklasse` og `abstrakt` utledes fortsatt av generatorlogikken (`Identifikator`/arv/`abstract`) og trenger derfor ikke å settes eksplisitt i LinkML.

#### hovedklasse

Alle klasser som ikke har abstract = true og ikke har noen stereotype er hovedklasser. Disse må ha minst en Identifikator.

```yaml
Person:
  is_a: Aktør
  attributes:
    fødselsnummer:
      range: Identifikator
      required: true
    navn:
      range: Personnavn
      required: true
    ...
```

#### referanse

Klasser med `annotations.stereotype: referanse` behandles som relasjonsmål i XMI/Java-generering, på samme måte som hovedklasser. Slotter som peker på disse blir derfor relasjoner (links), ikke felter.

```yaml
Vigoreferanse:
  annotations:
    stereotype: referanse
```

Kunne det i stedet vært som følger: 

```yaml
Referanse:
  abstract: true

Vigoreferanse:
  is_a: Referanse
```
Blir rart å gjøre det samme for `kompleks datatype`?


#### abstrakt

Klasser som er merket med abstract: true` er abstrakte klasser.

```yaml
Aktør:
  abstract: true
  attributes:
    kontaktinformasjon:
      range: Kontaktinformasjon
    ...
```

#### kompleks datatype

Klasser som ikke er merket som abstrakt og ikke har noen identifikator er komplekse datatyper. Se [Se avklaringen om komplekse datatyper](#komplekse-datatyper-med-inlined-og-inlined_as_list-brukes-ikke)

```yaml
Adresse:
  annotations:
    stereotype: kompleks-datatype
  attributes:
    adresselinje:
      range: Adresselinje
      multivalued: true
      inlined_as_list: true
    ...
```


## Pågående avklaringer og beslutninger

### Komplekse datatyper med inlined og inlined_as_list brukes ikkeikke

Disse er brukt for å angi hvordan komplekse datatyper skal serialiseres i JSON, Java, etc. Ved brukt av standard verktøy i LinkML for export vil ikke "komplekse datatyper" bli generert/serialisert riktig.

```yaml
  postadresse: 
    range: Adresse
    inlined: true           # 0..1

  bostedsadresse: 
    range: Adresse
    inlined: true           
    required: true          # 1..1

  adresselinje: 
    range: Adresselinje
    multivalued: true
    inlined_as_list: true   # 0..*

  adresselinje2:
    range: Adresselinje
    multivalued: true
    inlined_as_list: true   
    required: true          # 1..*
```

### Hva gjør vi med isSource/primaryRelation?

Bedre navn enn primaryRelation?

```yaml
...
  kontaktperson:
    range: Person
    inverse: pårørende
    annotations:
      primaryRelation: true # isSource, 
```


## Utvikling

### Kom i gang

```bash
brew install uv
```

### Generer LinkML-modell fra Enterprise Architect sin XMI

Dette en en engangsjobb. Trenger kun å gjøres den gangen man ønsker overgang til LinkML. Scriptet beholdes for å gjøre det mulig å generere på nytt om det viser seg at ikke man har fått med alt som trengs i LinkML.

```bash
python scripts/generate_linkml_from_xmi.py --xmi FINT-informasjonsmodell.xml --out src --overwrite
```

### Generer XMI (som likner på Enterprise Architect sin XMI) fra LinkML

Dette gjøres for å beholde bakoverkompabilitet med XMI, og alle tjenester som bruker XMI-filen. På sikt kan vi gå bort fra denne, og generere alt ut fra LinkML.

```bash
python scripts/generate_xmi_from_linkml.py --src src --out FINT-informasjonsmodell.xml
```

### Valider og lint LinkML-modellll

```bash
linkml-lint --validate src
```

Åpnes dette i Visual Studio Code eller Windsurf er det satt opp tasks.json som gjør at denne kommandoen kan kjøres med `Command + Shift + B` (MacOS) eller `Control + Shift + B` (Windows).


### Teste genering av Java

Original java-kode:

```
docker run --rm -v $(pwd):/src ghcr.io/fintlabs/fint-model:3.0.8 --tag v4.0.30 generate --lang JAVA --resource 
```

Javakode fra XMI som er generert fra LinkML:

```
~/go/bin/fint-model --tag linkml --filename "FINT-informasjonsmodell.generated.xml"  generate --lang JAVA --resource
docker run --rm -v $(pwd):/src ghcr.io/fintlabs/fint-model:3.0.8 --tag linkml --filename \"FINT-informasjonsmodell.generated.xml\"  generate --lang JAVA --resource

Det ser ut som dette er trikset:
~/go/bin/fint-model -f --tag linklm  generate --lang JAVA --resource
cp FINT-informasjonsmodell.generated.xml ~/.fint-model/.cache/linklm.xml
~/go/bin/fint-model --tag linklm  generate --lang JAVA --resource
````

### Verktøy som blir tilgjengelig med LinkML

- gen-csv
- gen-dbml
- gen-doc
- gen-erdiagram
- gen-excel
- gen-golang
- gen-golr-views
- gen-graphql
- gen-graphviz
- gen-java
- gen-json-schema
- gen-jsonld
- gen-jsonld-context
- gen-linkml
- gen-markdown
- gen-mermaid-class-diagram
- gen-namespaces
- gen-owl
- gen-pandera
- gen-plantuml
- gen-prefix-map
- gen-project
- gen-proto
- gen-py-classes
- gen-pydantic
- gen-python
- gen-rdf
- gen-rust
- gen-shacl
- gen-shex
- gen-sparql
- gen-sqla
- gen-sqlddl
- gen-sqltables
- gen-sssom
- gen-summary
- gen-terminusdb
- gen-typescript
- gen-yaml
- gen-yuml
- linkml
- linkml-convert
- linkml-jsonschema-validate
- linkml-lint
- linkml-run-examples
- linkml-schema-fixer
- linkml-sparql-validate
- linkml-sqldb
- linkml-validate
- run-tutorial


### Andre verktøy

Kan dette brukes til noe? https://github.com/cimug-org/CIMTool?tab=readme-ov-file

og https://docs.astral.sh/uv/ til python
