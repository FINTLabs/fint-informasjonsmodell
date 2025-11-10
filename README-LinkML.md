# Er LinkML et alternativ til Enterprise Architect?

## Definisjon av informasjonsmodell i LinkML

### Kardinalitet/multiplisitet

#### Relasjoner

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

#### Felter med komplekse datatyper

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

### Utgått/deprecated

```yaml
  kommunenavn:
    range: string
    deprecated: Ikke i bruk. Bruk i stedet feltet kommune.
```

### Klasser

#### hovedklasse

Alle klasser som har en Identifikator er hovedklasser.

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

Klasser som ikke er merket som abstrakt og ikke har noen identifikator er komplekse datatyper.

```yaml
Adresse:
  attributes:
    adresselinje:
      range: Adresselinje
      multivalued: true
      inlined_as_list: true
    ...
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

### Valider og _lint_ LinkML-modell

```bash
linkml-lint --validate src
```

Åpnes dette i Visual Studio Code eller Windsurf er det satt opp tasks.json som gjør at denne kommandoen kan kjøres med `Command + Shift + B` (MacOS) eller `Control + Shift + B` (Windows).



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