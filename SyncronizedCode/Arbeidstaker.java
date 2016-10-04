package Arbeidstaker;

import lombok.Data;

import java.util.List;

/**
 * Alle arbeidstakere i HR-systemet.
 * 
 * Inneholder "ordinære" ansatte i fast og vikariat, i tillegg til oppdragstakere
 * (politikere, ressurser med timelønn, sensorer, etc).
 * 
 * Inneholder ikke leverandørrepresentant (eksterne konsulenter etc).
 * @author Tor Kjetil
 * @version 1.0
 * @updated 04-okt-2016 12:51:00
 */
@Data
public class Arbeidstaker extends Person {

	/**
	 * Inneholder en liste over alle stillinger til en arbeidstaker.
	 */
    private List<Stilling> stillinger;
	/**
	 * Dato for når den ansatte startet, og evtuelt sluttdato.
	 */
	public Periode ansettelsesperiode;
	/**
	 * Kontaktinformasjon for arbeidstaker, knyttet til sitt arbeidsforhold.
	 */
	public Kontaktinformasjon kontaktinformasjonArbeidssted;
	/**
	 * Kontaktinformasjon for arbeidstaker, knyttet til sitt arbeidsforhold.
	 */
	public Kontaktinformasjon kontaktinformasjonArbeid;

}