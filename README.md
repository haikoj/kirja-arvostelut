# Kirja-arvostelusovellus

### Sovelluksessa:
* Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen.
* Käyttäjä pystyy lisäämään kirja-arvosteluja
* Käyttäjä voi muokata ja poistaa antamiaan kirja-arvosteluja.
* Käyttäjä näkee kaikki sovellukseen lisätyt kirja-arvostelut.
* Käyttäjä pystyy etsimään arvosteluita eri kirjoista hakusanalla.
* Sovelluksessa on käyttäjäsivut, jotka näyttävät käyttäjän lisäämät arvostelut.
* Käyttäjä pystyy valitsemaan arvostelulleen kaksi luokittelua: kirjan kategorian ja tarkemman lajityypin.
* Sovelluksessa käyttäjä voi arvosteluiden lisäksi kommentoida sekä toisten käyttäjien tekemiä, että omia arvosteluja.

### Ohjeet sovelluksen testaamiseen:
  1. Asenna flask-kirjasto:
```bash
$ pip install flask
```
  2. Kloonaa repositorio:
```bash
$ git clone https://github.com/haikoj/kirja-arvostelut.git
```
  3. Luo tietokannan taulut:
```bash
$ sqlite3 database.db < schema.sql
$ sqlite3 database.db < init.sql
```
  4. Käynnistä komennolla:
```bash
$ flask run
```
