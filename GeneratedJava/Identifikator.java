package Identifikasjon;


/**
 * En kombinasjon av tegn eller og/eller bokstaver som identifiserer en aktør
 * eller objekt innenfor et sett av aktører eller objekter
 * @author Tor Kjetil
 * @version 1.0
 * @created 28-sep-2016 17.39.53
 */
public class Identifikator {

	/**
	 * Perioden, gitt i form av fra-og-med-dato og til-dato, som en gitt identifikator
	 * er gyldig
	 */
	public Periode gyldighetsperiode;
	/**
	 * En kategori av identifikatorer, f.eks. fødselsnummer, organisasjosnummer, d-
	 * nummer
	 * 
	 * Identifikatortyper:
	 * - fødselsnummer (kan også inneholde d-nummer)
	 * - ansattnummer (ressursnummer i Agresso, lønnsnummer i Bluegarden, Ansattnr i
	 * Visma Enterprise)
	 */
	public string identifikatortype;
	/**
	 * En konkret kombinasjonen av tegn og/eller bokstaver som utgjør en bestemt
	 * identifikator
	 */
	public string identifikatorverdi;
	/**
	 * Myndigheten, i Norge eller utlandet, som har utstedt en gitt identifikator. For
	 * eksempel om det er snakk om ansattnummer, kan det være "Agresso i Vest-Agder
	 * fylkeskommune"
	 */
	public string utstedtAvAutoritet;
	/**
	 * Datoen en gitt identifikator ble utstedt
	 */
	public date utstedtdato;

	public Identifikator(){

	}

	public void finalize() throws Throwable {

	}

}