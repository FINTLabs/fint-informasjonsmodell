package Enhet;

import Adresse.GeografiskAdresse;
import Aktør.Aktør;

/**
 * Alle hovedenheter, underenheter og organisasjonsledd som er identifisert med et
 * organisasjonsnummer
 * 
 * Merknad: Forslag til definisjon med utgangspunkt i Enhetsregisteret
 * @author Tor Kjetil
 * @version 1.0
 * @created 28-sep-2016 17.39.45
 */
public abstract class Enhet extends Aktør {

	/**
	 * Navn på enhet som er registrert i Enhetsregisteret
	 */
	public string navn;
	/**
	 * Femsifret kode som tildeles på bakgrunn av enhetens virksomhet/bransje. Bygger
	 * på EU sin næringsstandard (NACE) som består av fire siffer. Det femte sifferet
	 * er nasjonalt nivå
	 */
	public string næringskode;
	/**
	 * Inndeling av enheter ut fra hvordan disse er organisert (eierform,
	 * ansvarsforhold, regelverk og lignende)
	 */
	public string organisasjonsform;
	/**
	 * Nisifret nummer som entydig identifiserer enheter i Enhetsregisteret
	 */
	public string organisasjonsnummer;
	public GeografiskAdresse adresse;

	public Enhet(){

	}

	public void finalize() throws Throwable {
		super.finalize();
	}

}