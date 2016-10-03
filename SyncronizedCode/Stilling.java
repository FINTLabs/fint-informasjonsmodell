package Arbeidstaker;

import lombok.Data;

@Data
public class Stilling {

	/**
	 * Tilhørighet til avdeling, feks "Avdeling for Helse og mijlø" (dette er ikke med
	 * i Visma sitt API)
	 */
    private String avdeling;
	/**
	 * Eksempel (fra VFS-api): "Studiespesialisering" eller "PEDAGOGISK LEDELSE OG
	 * PEDAGOGISKE FELLESUTGIFTER<b>"</b>
	 */
    private String funksjon;
    private long grunnlonn;
	/**
	 * For eksempel: "Bjerke videregående skole". Tilsvarer Arbeidssted i HR-system,
	 * mens VFS kaller dette for Ansvar og beskriver det med: "Type 2 = Ansvar,
	 * benyttes til å plassere den ansatte på riktig skole".
	 */
    private String organisasjon;
    private String status;
	/**
	 * Se liste fra KS. Flere fylkeskommuner har utvidet denne med 2 siffer ekstra.
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
    private String stillingstittel;
	/**
	 * stillingsperiode
	 */
	private Periode stillingsperiode;
}