package no.fint.arbeidstaker;

import lombok.Data;

@Data
public abstract class Aktor {

    private Identifikator identifikator;
    private Kontaktinformasjon kontaktinformasjon;

}