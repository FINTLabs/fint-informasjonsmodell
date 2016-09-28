package Aktør;

import Identifikasjon.Identifikator;

/**
 * person eller enhet vi samhandler med
 * @author Tor Kjetil
 * @version 1.0
 * @created 28-sep-2016 17.39.21
 */
public abstract class Aktør {

	/**
	 * det som identifiserer en aktør
	 */
	public Identifikator identifikator;
	/**
	 * informasjon for å kontakte aktør
	 */
	public Kontaktinformasjon kontaktinformasjon;

	public Aktør(){

	}

	public void finalize() throws Throwable {

	}

}