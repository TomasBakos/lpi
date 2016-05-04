Cvičenie 9
==========

**Riešenie odovzdávajte podľa
[pokynov na konci tohoto zadania](#technické-detaily-riešenia)
do utorka 10.5. 23:59:59.**

Súbory potrebné pre toto cvičenie si môžete stiahnúť ako jeden zip
[`cv09.zip`](https://github.com/FMFI-UK-1-AIN-412/lpi/archive/cv09.zip).

SAT solver (3b)
----------

Naprogramujte SAT solver, ktorý zisťuje, či je vstupná formula (v konjunktívnej
normálnej forme) splniteľná.

Na prednáške bola základná kostra DPLL metódy, ktorej hlavnou ideou je
propagácia klauz s iba jednou premennou (unit clause).  Tá ale hovorí o veciach
ako *vymazávanie literálov* z klauz a *vymazávanie klauz*, čo sú veci, ktoré nie
je také ľahké efektívne (či už časovo alebo pamäťovo) implementovať, hlavne ak
počas backtrackovania treba zmazané literály resp.  klauzy správne naspäť
obnovovať.

Ukážeme si preto jednoduchú modifikáciu DPLL metódy, ktorá výrazne zjednodušuje
"menežment" literálov, klauz a dátových štruktúr.

## Watched literals

Základným problémom pri DPLL metóde je vedieť povedať, či už klauza obsahuje
nejaký literál ohodnotený `true` (a teda je už splnená), ak nie, tak či obsahuje
práve jeden neohodnotený literál (unit clause), alebo či už sú všetky literály
`false` (nesplnená klauza: treba backtrackovať).

Namiesto mazania / obnovovania literálov a klauz si pre každú klauzu si označíme
/ budeme pamätať dva literály z nej, pričom budem požadovať aby každý z nich
- buď ešte nemal priradenú hodnotu,
- alebo mal priradenú hodnotu `true`.

Ak nejaký literál počas prehľadávania nastavíme na `true`, tak očividne nemusíme
nič meniť. Ak ho nastavíme na `false` (lebo sme napríklad jeho negáciu nastavili
na `true`) tak pre každú klauzu, v ktorej je označený, musíme nájsť nový
literál, ktorý spĺňa horeuvedené podmienky. Môžu nastať nasledovné možností:
- našli sme iný literál, ktorý je buď nenastavený, alebo je `true`, odteraz
  bude označený ten,
- nenašli sme už literál, ktorý by spĺňal naše podmienky (všetky ostatné sú
 `false`):
    - ak druhý označený literál bol `true`, tak to nevadí (klauza je aj tak splnená),
    - ale ak bol druhý literál nenastavený, tak nám práve vznikla unit clause, a mali by sme ho
      nastaviť na `true`.
    - podľa toho, ako presne implementujeme propagáciu, sa nám môže stať, že sa
      dostaneme do momentu, že aj druhý označený literál sa práve stal `false`,
      v tom prípade sme práve našli nesplnenú klauzu a musíme backtracovať.

Bonus navyše: ak backtrackujeme (meníme nejaký true alebo false literál naspäť
na nenastavený), tak nemusíme vôbec nič robiť (s označenými literálmi v klauzách;
samotný literál/premennú samozrejme musíme korektne "odnastaviť").

Dosť podrobný pseudokód riešenia:

```
solve:
  readInput() # nacita clauses, vyrobi (nenastavene) vars
  if not initWatchedLiterals():
    return false
  if not unitPropagate():
    return false
  return dpll()

dpll:
  if all vars are assigned:
    return true
  branchLit = chooseBranchLiteral()

  for lit in branchLit and -branchLit: # backtracking
    setLiteral(lit)
    unitPropagate()
    dpll()
    unsetLiterals()

initWathcedLiterals:  # returns false if it finds a conflict / UNSAT
  for each clause c:
    if c is empty:
      return false
    if len(c) == 1:
      c.w1 = c.w2 = c[0] # watch the same lit
      append c[0] to unitLiterals
    else:
      c.w1 = c[0], c.w2 = another lit from c different then c[0]
  return true

unitPropagate:  # returns false if it finds a conflict / UNSAT
  while unitLiterals not empty:
    take lit from unitLiterals
    if not setLiteral(lit):
      return false
  return true

setLiteral(lit):  # returns false if it finds a conflict / UNSAT
  set lit to true (-lit to false)
  for each clause c in which -lit is watched:
    let c.w1 be -lit, c.w2 be the other watched literal
    if can't find new watched literal for c.w1 (insteda of -lit) in c:
      if c.w2 is set to to false:
        return false  # all are false in this clause
      if c.w2 is unset:
        # c.w2 is the last unset, no true literals -> unit propagate on c.w2
        add c.w2 to unitLiterals
      # else other is set to true, this is a satisfied clause, leave it be
  return true

unsetLiterals():
  for lit in literals that have beend set on this recursion level
    unsetLiteral(lit)

unsetLiteral(lit):
  set lit and -lit to unset
  nothing else to do...
```
V tomto pseudokóde samozrejme nie sú riešené implementačné "drobnosti" ako reprezentovať
literály a premenné, ako si pamatať, ktoré literály sú oznčené (watched) v klauze
a v ktorých klauzách je označený daný literál, ako vedieť, ktoré premenné / literály
odnastaviť atď...

## Technické detaily riešenia

Riešenie odovzdajte do vetvy `cv09` v adresári `cv09`.
Odovzdávajte (modifikujte) súbor `satsolver.py` resp `satsolver.cpp` / `SatSolver.java`.
Program [`satTest.py`](satTest.py) otestuje váš solver na rôznych vstupoch
(z adresara testData). Testovač by mal automaticky detekovať Python / C++ / Java
riešenia prítomné v adresári.

Vaším riešením má byť konzolový program (žiadne gui), ktorý dostane dva
argumenty: meno vstupného a výstupného súboru. Vstupný súbor bude v DIMACS
formáte s korektnou hlavičkou (môže obsahovať komentáre).

Do výstupného subóru váš program zapíše na prvý riadok buď `SAT` alebo `UNSAT`,
podľa toho, či je formula splniteľná. Ak je formula splniteľná, tak na druhý
riadok zapíše model (spĺňajúce ohodnotenie): medzerami oddelené čísla s
absolutnými hodnotami 1, 2, ... až najväčšia premenná. Kladné číslo znamená, že
premenná je nastavená na true a záporne, že je nastavená na false.
V predpripravenom `satsolver.py` už je implementované korektné načítavanie a zápis riešenia.

Za korektný beh programu sa považuje iba keď váš program skončí s návratovou hodnotou 0,
nenulová hodnota sa považuje za chybu (Runtime Error). Toto je dôležite hlavne v C++
(`return 0;` na konci `main`), ak Python korektne skončí, tak by mal vrátiť 0.

Môžete predpokladať, že počet premenných bude do 2048.

### Python
Python má limit na počet rekurzívných volaní funkcií (maximálna hĺbka stack-u).
Štandardne je to 1000 vo väčšine implementácii.  Keďže naša dpll metóda je
rekurzívna, možete ho ľahko dosiahnuť. Dá sa zväčšiť príkazom
[sys.setrecursionlimit](https://docs.python.org/3.3/library/sys.html#sys.setrecursionlimit).

### C++
Odovzdávajte program `satsolver.cpp`, ktorý musí byť skompilovateľný príkazom
`g++ -Wall --std=c++11 -o satsolver *.cpp`.

###Java:
Odovzdávajte program `SatSolver.java`, ktorý implementuje triedu `SatSolver` s
main metódou. Kód musí byť skompilovateľný príkazom
`javac SatSolver.java`.

Odovzdávanie riešení v iných jazykoch konzultujte s cvičiacimi.
