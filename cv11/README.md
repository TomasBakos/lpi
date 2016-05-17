Cvičenie 11
==========

**Riešenie odovzdávajte podľa [pokynov na konci tohoto
zadania](#technické-detaily-riešenia) najneskôr do utorka 24.5. 23:59:59, ale
musí byť odovzdané aspoň deň pred zapísaním známky.**

Toto cvičenie je bonusové v zmysle, že si ním môžete nahradiť niektoré iné
cvičenie, t.j. zaráta sa vám namiesto cvičenia,
za ktoré ste dostali najmenej bodov (alebo ste ho neodovzdali).

Navyše má toto cvičenie [bonusovú časť](#bonus),
za ktorú môžete získať ďalšie 2 body.


## Rezolver (3b)

Naprogramujte dokazovač založený na rezolvencii. Napíšte program,
ktorý načíta teóriu v CNF a pokúsi sa nájsť rezolvenčný dôkaz (t.j.
odvodenie prázdnej klauzuly).

Odskúšajte váš program (minimálne) na príkladoch uvedených nižšie.

### Vstup a výstup

Vstupný formát je rovnaký ako pre SAT solver (môžete predpokladať,
že nebude obsahovať komentáre a že na začiatku má korektnú hlavičku
s počtom klauzúl a premenných). Načítavať treba zo štandardného vstupu.

Výstupom je len informácia o tom, či sa podarilo odvodiť prázdnu klauzulu.
Výsledok treba vypísať na štandardný výstup, pričom prvý riadok musí obsahovať
buď `SAT`, ak je teória splniteľná (t.j. nepodarilo sa odvodiť prázdnu
klauzulu), alebo `UNSAT`, ak je nesplniteľná (t.j. podarilo sa odvodiť prázdnu
klauzulu).


### Hodnotenie

Hodnotí sa hlavne korektnosť a čiastočne efektívnosť; riešenia s horšou
zložitosťou ako nižšie popísané „priamočiare“ riešenie môžu dostať menej
bodov.

„Priamočiare“ riešenie skúša všetky dvojice klauzúl a pre každú dvojicu skúsi
každú premennú, či sa cez ňu dajú rezolvnúť. Aby naozaj prešlo všetky dvojice
(aj s novopridanými klauzulami), tak prechádza dvojice tak, že najskôr začne
s C1 a C2 a potom vždy skúša postupne rezolvovať klauzuly C1, C2, … C(<var>N</var>−1)
s klauzulou C<var>N</var> a následne zvýši <var>N</var>. Ak si klauzuly
pamätáme utriedené (podľa absolútnej hodnoty premenných), tak rezolvnúť
klauzuly cez konkrétnu premennú sa dá lineárne od ich veľkosti. (Takisto sa dá
lineárne od veľkosti oboch klauzúl zistiť, podľa ktorých premenných sa dajú
rezolvnúť.)

Základná kostra programu môže vyzerať napríklad nasledovne:

```c++
class Resolver {
public:

	typedef vector<int> Clause;
	typedef vector<Clause> Clauses;
	typedef pair<int, pair<int,int> > Resolution;  // premenna a dvojica klauzul na rezolvnutie

	Clauses clauses;


	/**
	 * Metoda, ktora vrati dalsiu premennu a dvojicu klauzul,
	 * ktore mozno rezolvnut  (potrebuje samozrejme
	 * nejaky globalny stav, ze kde sa prave nachadza...)
	 *
	 * vrati ako premennu (res.first) 0 ak uz presla vsetky moznosti
	 */
	Resolution chooseRes();

	/**
	 * Funkcia, ktora prida ich rezolventu na
	 * koniec zoznamu klauzul
	 */
	void resolve(Resolution res);


	bool resolve()
	{
		// nacitanie...

		// osetrenie specialnych vynimiek (ziadne / 1 klauzula, ...)

		Resolution res;
		while (
				clauses.back().size()			// posledná klauzula nie je prázdna
				&& (res = chooseRes()).first	// vybrata premenna a klauzuly
		) {
			resolve(res);
		}

		if (!clauses.back().size()) {
			cout << "UNSAT" << endl;
			cerr << "resolved empty clause (after "
				<< clauses.size() - Nclauses << ")" << endl;
			return true;
		}
		else {
			cout << "SAT" << endl;
			cerr << "unable to resolve ("
				<< clauses.size() - Nclauses << ")" << endl;
			return false;
		}
	}
};

int main()
{
	Resolver().resolve();
	return 0;
}
```

### Príklad 1

Bez oblakov niet dažďa (ak nie sú oblaky, nemôže pršať). 
Ak je cesta mokrá, tak prší alebo práve prešlo umývacie auto.
Umývacie autá nechodia v sobotu (ak je sobota, tak umývacie autá
nechodia).
Dokážte, že ak je sobota a je mokrá cesta, tak je oblačno.


```
-o -> -p

m -> ( p || u )

s -> -u

-( (s && m) -> o )
  => -( -s || -m || o)
  => s && m && -o
```

```
p cnf 5 6
1 -2 0

-3 2 4 0

-5 -4 0

5 0
3 0
-1 0
```

### Príklad 2: Agáta
Premenné sú v poradí (trochu iné ako bolo na cvikách):

1 : `Agatha_killed_Agatha`
2 : `butler_killed_Agatha`
3 : `Charles_killed_Agatha`
4 : `Agatha_hates_Agatha`
5 : `Agatha_richer_than_Agatha`
6 : `Agatha_killed_butler`
7 : `Agatha_hates_butler`
8 : `Agatha_richer_than_butler`
9 : `Agatha_killed_Charles`
10 : `Agatha_hates_Charles`
11 : `Agatha_richer_than_Charles`
12 : `butler_hates_Agatha`
13 : `butler_richer_than_Agatha`
14 : `butler_killed_butler`
15 : `butler_hates_butler`
16 : `butler_richer_than_butler`
17 : `butler_killed_Charles`
18 : `butler_hates_Charles`
19 : `butler_richer_than_Charles`
20 : `Charles_hates_Agatha`
21 : `Charles_richer_than_Agatha`
22 : `Charles_killed_butler`
23 : `Charles_hates_butler`
24 : `Charles_richer_than_butler`
25 : `Charles_killed_Charles`
26 : `Charles_hates_Charles`
27 : `Charles_richer_than_Charles`

```
p cnf 27 34
1 2 3 0
-1 4 0
-1 -5 0
-6 7 0
-6 -8 0
-9 10 0
-9 -11 0
-2 12 0
-2 -13 0
-14 15 0
-14 -16 0
-17 18 0
-17 -19 0
-3 20 0
-3 -21 0
-22 23 0
-22 -24 0
-25 26 0
-25 -27 0
-4 -20 0
-7 -23 0
-10 -26 0
4 0
10 0
5 12 0
13 15 0
21 18 0
-4 12 0
-7 15 0
-10 18 0
-4 -7 -10 0
-12 -15 -18 0
-20 -23 -26 0
-1 0
```

### Výstup „priamočiareho“ riešenia

```
yoyo@tableta 11 $ time ./resolve.cpp.bin  <agatha.cnf
UNSAT
resolved empty clause (after 1120120)

real    0m2.333s
user    0m2.293s
sys     0m0.032s

yoyo@tableta 11 $ time ./resolve.cpp.bin <prsi.cnf
UNSAT
resolved empty clause (after 50)

real    0m0.003s
user    0m0.002s
sys     0m0.001s

yoyo@tableta 11 $ time ( echo "1 2 0 -1 0 -2 0" | ./resolve.cpp.bin )
UNSAT
resolved empty clause (after 3)

real    0m0.003s
user    0m0.001s
sys     0m0.002s

yoyo@tableta 11 $ wc -l resolve.cpp
151 resolve.cpp
```

### Literatúra

Krátky popis
[rezolvencie](http://en.wikipedia.org/wiki/Resolution_(logic))
na wikipédii alebo v prvej kapitole
[Handbook of Knowledge Representation](http://ii.fmph.uniba.sk/~sefranek/kri/handbook/)
(časť 1.3.1.).

## Technické detaily riešenia

Riešenie odovzdajte do vetvy `cv11` v adresári `cv11`.
Odovzdajte súbor `resolve.py`/`resolve.cpp`/`Resolve.java`.


## Bonus

Uvedené „priamočiare“ riešenie nevyhľadáva rezolvovateľné dvojice klauzúl
veľmi efektívnym spôsobom, ani sa obzvlášť nezaujíma o poradie rezolvovania.

Ak implementujete nejakú efektívnejšiu (vzhľadom na čas behu) metódu výberu
alebo usporiadania rezolvovaných dvojíc klauzúl, uveďte to v pull requeste
s krátkym popisom vášho algoritmu (odkaz na nejaký internetový zdroj je OK,
implementácia ale musí byť vaša vlastná) a môžete získať **až 2 bonusové
body**.
