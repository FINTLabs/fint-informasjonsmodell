package Arbeidstaker;

import Identifikasjon.Periode;

/**
 * @author ole.anders
 * @version 1.0
 * @created 28-sep-2016 17.40.30
 */
public class Stilling {

	/**
	 * Tilhørighet til avdeling, feks "Avdeling for Helse og mijlø" (dette er ikke med
	 * i Visma sitt API)
	 */
	public string avdeling;
	/**
	 * Eksempel (fra VFS-api): "Studiespesialisering" eller "PEDAGOGISK LEDELSE OG
	 * PEDAGOGISKE FELLESUTGIFTER<b>"</b>
	 */
	public string funksjon;
	public long grunnlønn;
	/**
	 * For eksempel: "Bjerke videregående skole". Tilsvarer Arbeidssted i HR-system,
	 * mens VFS kaller dette for Ansvar og beskriver det med: "Type 2 = Ansvar,
	 * benyttes til å plassere den ansatte på riktig skole".
	 */
	public string organisasjon;
	public string status;
	/**
	 * Hvilket tidsrom stillingen gjelder.
	 */
	public Tidsperiode stillingsdatoer;
	/**
	 * Se liste fra KS. Flere fylkeskommuner har utvidet denne med 2 siffer ekstra.
	 */
	public string stillingskode;
	/**
	 * En unik id for en ansatt sine stillinger.
	 */
	public int stillingsnummer;
	/**
	 * Stillingsprossent
	 */
	public double stillingsprosent;
	public string stillingstittel;
	public Periode m_Periode;

	public Stilling(){

	}

	public void finalize() throws Throwable {

	}

	/**
	 * Tilhørighet til avdeling, feks "Avdeling for Helse og mijlø" (dette er ikke med
	 * i Visma sitt API)
	 */
	public string getavdeling(){
		return avdeling;
	}

	/**
	 * Tilhørighet til avdeling, feks "Avdeling for Helse og mijlø" (dette er ikke med
	 * i Visma sitt API)
	 * 
	 * @param newVal
	 */
	public void setavdeling(string newVal){
		avdeling = newVal;
	}

}