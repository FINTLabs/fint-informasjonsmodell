package no.fint.arbeidstaker;


import lombok.Data;

import java.util.Date;

@Data
public abstract class Person extends Aktor {

	private Date dodsdato;
	private Landkode dodsland;
	private String dodssted;
	private String fulltNavn;
	private Landkode fodeland;
	private String fodested;
	private Date fodselsdato;
	private Kjonn kjonn;
	private Personnavn navn;
	private Personnavn opprinneligNavn;
	private Sivilstand sivilstand;
	private Landkode statsborgerskap;
	private GeografiskAdresse adresse;

}