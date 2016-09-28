package Person;

import felles.ISO.ISO 3166 - Landkoder.Landkode;
import Adresse.GeografiskAdresse;
import Aktør.Aktør;

/**
 * private, fysiske personer
 * @author Tor Kjetil
 * @version 1.0
 * @created 28-sep-2016 17.31.25
 */
public abstract class Person extends Aktør {

	/**
	 * dato for dødsfall
	 */
	public dateTime dødsdato;
	/**
	 * land hvor dødsfall fant sted
	 */
	public Landkode dødsland;
	/**
	 * sted hvor dødsfall fant sted
	 */
	public string dødssted;
	/**
	 * fullt utskrevet navn
	 */
	public string fulltNavn;
	/**
	 * land for fødsel
	 */
	public Landkode fødeland;
	/**
	 * sted for fødsel
	 */
	public string fødested;
	/**
	 * dato for fødsel
	 */
	public dateTime fødselsdato;
	/**
	 * kjønn for person
	 * 
	 * Merknad: Sosialt kjønn? Se ISO 5218 - Representation of Human Sexes. 
	 */
	public Kjønn kjønn;
	/**
	 * navn på person
	 */
	public Personnavn navn;
	/**
	 * navn før navneendring av ulike årsaker, for eksempel pikenavn
	 */
	public Personnavn opprinneligNavn;
	/**
	 * persons stilling i forhold til ekteskap eller partnerskap
	 */
	public Sivilstand sivilstand;
	/**
	 * rettslig bånd mellom en person og en stat og består av både plikter og
	 * rettigheter [wikipedia]
	 */
	public Landkode statsborgerskap;
	public GeografiskAdresse adresse;

	public Person(){

	}

	public void finalize() throws Throwable {
		super.finalize();
	}

}