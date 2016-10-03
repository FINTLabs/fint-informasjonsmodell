package no.fint.arbeidstaker;


import lombok.Data;

import java.util.Date;

@Data
public class Identifikator {

    private Periode gyldighetsperiode;
    private String identifikatortype;
    private String identifikatorverdi;
    private String utstedtAvAutoritet;
    private Date utstedtdato;

}