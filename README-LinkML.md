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

TODO: Eksempler på:

* hovedklasse
* abstrakt
* kompleks datatype

## Utvikling

### Generer LinkML-modell fra XMI

```bash
python scripts/generate_linkml_from_xmi.py --xmi FINT-informasjonsmodell.xml --out src --overwrite
```

### Valider og _lint_ LinkML-modell

```bash
linkml-lint --validate src
```

Åpnes dette i Visual Studio Code eller Windsurf er det satt opp tasks.json som gjør at denne kommandoen kan kjøres med `Command + Shift + B` (MacOS) eller `Control + Shift + B` (Windows).

