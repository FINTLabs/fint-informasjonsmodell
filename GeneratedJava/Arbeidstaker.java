package Arbeidstaker;

import Person.Person;

/**
 * Alle ressurser i HR
 * @author Tor Kjetil
 * @version 1.0
 * @updated 28-sep-2016 17.40.30
 */
public class Arbeidstaker extends Person {

	private Tidsperiode ansettelsesdato;
	private Kontaktinformasjon2 kontaktinformasjon;
	public Stilling stillinger;
	public Periode m_Periode;
	public Kontaktinformasjon m_Kontaktinformasjon;

	public Arbeidstaker(){

	}

	public void finalize() throws Throwable {
		super.finalize();
	}

}