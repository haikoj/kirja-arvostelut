# Kirja-arvostelusovellus
Sovellus on englanninkielinen kirja-arvostelusovellus (book review app), jossa jokainen rekisteröitynyt käyttäjä saa käyttäjäsivut ja luoda julkisia kirja-arvosteluja lukemistaan kirjoista.

### Sovelluksessa:
* Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen.
* Käyttäjä pystyy lisäämään kirja-arvosteluja
* Käyttäjä voi muokata ja poistaa antamiaan kirja-arvosteluja.
* Käyttäjä näkee kaikki sovellukseen lisätyt kirja-arvostelut uusimmasta vanhimpaan.
* Käyttäjä pystyy etsimään arvosteluita eri kirjoista hakusanalla kirjan ja/tai kirjailijan nimen perusteella.
* Jos hakusanalle löytyy useampi tulos, arvostelut joissa on eniten kommentteja näkyvät ylimpänä.
* Sovelluksessa on käyttäjäsivut, jotka näyttävät käyttäjän lisäämät arvostelut.
* Käyttäjä pystyy valitsemaan arvostelulleen kaksi luokittelua: kirjan kategorian (fiction tai nonfiction) ja tarkemman lajityypin.
* Sovelluksessa käyttäjä voi arvosteluiden lisäksi kommentoida sekä toisten käyttäjien tekemiä, että omia arvosteluja.

### Ohjeet sovelluksen testaamiseen:
  1. Asenna flask-kirjasto:
```bash
$ pip install flask
```
  2. Luo tietokannan taulut:
```bash
$ sqlite3 database.db \< schema.sql
$ sqlite3 database.db \< init.sql
```
  3. Käynnistä komennolla:
```bash
$ flask run
```

### Sovelluksen testaus suurella tietomäärällä:
Ajamalla tiedoston seed.py sovellusta voi testata suurella määrällä dataa.
```
$ python seed.py
```
Testauksessa käytin ensin arvoja:
```
review_count = 10**5
comment_count = 10**6
```
Ennen indeksien lisäämistä etusivun lataamiseen meni aikaa n. 0,8s ja indeksoinnin jälkeen <0,01s

Testatessa suuremmilla arvoilla
```
review_count = 10**6
comment_count = 10**7
```
indeksien lisäämisen jälkeen aikaa kului 0,01-0,03s.
Indeksit on lisätty schema.sql-tiedoston loppuun.
