package Arbeidstaker;

import Person.Person;

/**
 * Alle ressurser i HR
 * @author Tor Kjetil
 * @version 1.0
 * @created 19-sep-2016 10.01.40
 */
public class Arbeidstaker extends Person {

	private Tidsperiode ansettelsesdato;
	private Kontaktinformasjon2 kontaktinformasjon;
	private Stilling stillinger;

	public Arbeidstaker(){

	}

	public void finalize() throws Throwable {
		super.finalize();
	}

}