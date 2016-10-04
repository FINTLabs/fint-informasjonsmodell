package Arbeidstaker;

import lombok.Data;

/**
 * Definisjon av stilling til en arbeidstaker.
 * @author ole.anders
 * @version 1.0
 * @updated 04-okt-2016 09:54:50
 */
@Data
public class Stilling {

	/**
	 * Tilhørighet til avdeling, feks "Avdeling for Helse og mijlø"
	 */
    private String avdeling;
	/**
	 * Eksempel (fra VFS-api): "Studiespesialisering" eller "PEDAGOGISK LEDELSE OG
	 * PEDAGOGISKE FELLESUTGIFTER<b>"</b>
	 */
    private String funksjon;
	/**
	 * Grunnlønn i gjeldende stilling
	 */
    private long grunnlonn;
	/**
	 * Tilknyttning i organisasjonen.  Tilsvarer Arbeidssted i HR-system, mens VFS
	 * kaller dette for Ansvar og beskriver det med: "Type 2 = Ansvar, benyttes til å
	 * plassere den ansatte på riktig skole".
	 * 
	 * For eksempel: "Bjerke videregående skole".
	 */
    private String organisasjon;
	/**
	 * Definerer om stillingen er aktiv, utløpt eller slettet.
	 * 
	 * Gyldige verdier er: AKTIV, ...
	 */
    private String status;
	/**
	 * En fire- eller sekssifret stillingskode. Se liste fra KS for firesiffret kode.
	 */
    private String stillingskode;
	/**
	 * En unik id for en ansatt sine stillinger.
	 */
    private int stillingsnummer;
	/**
	 * Stillingsprossent
	 */
    private double stillingsprosent;
	/**
	 * Arbeidstakers stillingstittel i gjeldende stilling.
	 */
    private String stillingstittel;
	/**
	 * Tidsperiode hvor stillingen er aktiv.
	 */
	private Periode stillingsperiode;
}