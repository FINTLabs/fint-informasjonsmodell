package no.fint.arbeidstaker;

import lombok.Data;

@Data
public abstract class Enhet extends Aktor {

    private String navn;
    private String naeringskode;
    private String organisasjonsform;
    private String organisasjonsnummer;
    private GeografiskAdresse adresse;

}