package Arbeidstaker;

import lombok.Data;

import java.util.List;

/**
 * Alle ressurser i HR
 * @author Tor Kjetil
 * @version 1.0
 * @updated 29-sep-2016 10.40.01
 */
@Data
public class Arbeidstaker extends Person {

    private List<Stilling> stillinger;
	/**
	 * Ansettelsesperiode
	 */
	public Periode ansettelsesperiode;
	public Kontaktinformasjon kontaktinformasjonArbeidssted;

}