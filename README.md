# kirja-arvostelusovellus

Sovelluksessa:
* Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen.
* Käyttäjä pystyy lisäämään, muokkaamaan ja poistamaan antamiaan julkisia kirja-arvosteluja.
* Käyttäjä näkee kaikki sovellukseen lisätyt kirja-arvostelut.
* Käyttäjä pystyy etsimään arvosteluita eri kirjoista hakusanalla tai kirjan kuvauksen tai lajityypin perusteella.

(* Sovelluksessa on käyttäjäsivut, jotka näyttävät käyttäjien tilastoja ja käyttäjän lisäämät arvostelut.
* Käyttäjä pystyy valitsemaan arvostelulleen yhden tai useamman luokittelun, kuten teoksen lajityyppi, arvostelun kieli.
* Sovelluksessa käyttäjä voi arvosteluiden lisäksi kommentoida sekä toisten käyttäjien tekemiä, että omia arvosteluja ja kommentteja.)

Ohjeet sovelluksen testaamiseen:
  1. Asenna flask-kirjasto: $ pip install flask
  2. Kloonaa repositorio: $ git clone https://github.com/haikoj/kirja-arvostelut.git
  3. Luo tietokannan taulut: $ sqlite3 database.db < schema.sql
  4. Käynnistä komennolla: $ flask run
