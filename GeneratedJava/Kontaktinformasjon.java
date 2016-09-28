package Aktør;


/**
 * Informasjon som kan brukes for uformell kontakt med en aktør
 * @author Tor Kjetil
 * @version 1.0
 * @created 28-sep-2016 17.39.23
 */
public class Kontaktinformasjon {

	/**
	 * navngitt elektronisk adresse for mottak av e-post
	 */
	public string epostadresse;
	/**
	 * person sitt mobiltelefonnummer ihht norsk nummerplan for telefoni (E.164).
	 * 
	 * Merknad:
	 * 8 siffer, evt. flere siffer dersom første to siffer er utenlandsprefix 00 eller
	 * “+”.
	 */
	public string mobiltelefonummer;
	/**
	 * tallkode som telenettet bruker for å få fram teletrafikk til riktig adressat
	 */
	public string telefonnummer;
	public string websted;

	public Kontaktinformasjon(){

	}

	public void finalize() throws Throwable {

	}

}