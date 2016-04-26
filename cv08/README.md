Cvičenie 8
==========

**Riešenie odovzdávajte podľa
[pokynov na konci tohoto zadania](#technické-detaily-riešenia)
do utorka 3.5. 23:59:59.**

Súbory potrebné pre toto cvičenie si môžete stiahnúť ako jeden zip
[`cv08.zip`](https://github.com/FMFI-UK-1-AIN-412/lpi/archive/cv08.zip).

## Hamiltonovská kružnica (3b)

Pomocou SAT solveru nájdite hamiltonovskú kružnicu v orientovanom grafe.

Implementujte triedu `HamiltonianCycle` s metódou `find` s jediným argumentom
`edges`, maticou susednosti: dvojrozmerné pole n x n bool-ov popisujúce hrany v
grafe: ak je v i-tom riadku na j-tom mieste `True` (`edges[i][j] == True`), tak
z i do j vedie hrana (vrcholy sú číslované od 0). Metóda vráti ako výsledok
pole n čísel, postupnosť vrcholov na kružnici, ak kružnica existuje, alebo
prázdne pole, ak kružnica neexistuje.

Potrebujeme zistiť, či sa dajú vrcholy grafu usporiadať do takej postupnosti, že
vždy ide hrana z i-teho do (i+1)-teho vrcholu v tejto postupnosti (a
z posledného do prvého). Potrebujeme teda uhhádnuť, ktorý vrchol bude na ktorej
pozícii v tejto postupnosti (zabezpečiť, že pre kažú pozíciu vyberieme práve
jeden vrchol) a zabezpečiť že za sebou idúce vrcholy sú sppojené hranou
správnym smerom (ak nie je v grafe hrana z a do b, nesmú byť a a b na nejakých
pozíciách i a i+1).

Jedna z možností je mať premenné `v_pos_i`, ktoré budú
pravdivé práve vtedy ak vrchol `i` je na pozicii `pos`. Potom stačí:

- zabezpečiť, že je to postuponosť neopakujúcich sa vrcholov (dlžky N):
  - pre každé `pos` aspoň jedno z `v_pos_i` je pravdivé
    (na každej pozícii je aspoň jeden vrchol)
  - pre každé `pos` nie sú dve rôzne `v_pos_i` a `v_pos_j` pravdivé naraz
    (nie sú dva vrholy na tej istej pozícii)
  - pre každé `i` nie sú dve rôzne `v_pos1_i` `v_pos2_i` pravdivé naraz
    (nie je jeden vrchol na dvoch rôznych pozíciách)
- zabezpečiť, že za sebou idúce vrholy sú spojené hranou, teda, ak sú v
  postupnosti za sebou, tak musia byť spojené hranou, resp (obmena) ak nie je
  hrana z i do j, tak nemôžu byť za sebou:
  - ak nie je v grafe hrana z `i` do `j`, tak pre každé `pos` nesmú platiť
    `v_pos_i` a `v_(pos+1)_j` (naraz), plus samozrejme aj pre poslendý a prvý,
    aby to bola kružnica.

Trošku nepekná vec na tomto zakódovaní / riešení je, že potrebujeme generovať
klauzy (alebo pomocné premenné) pre každú dvojicu vrcholov, medzi ktorými nie
je hrana. Plus netreba zabúdať, že pracujeme s orientovaným grafom.


## Technické detaily riešenia

Riešenie odovzdajte do vetvy `cv08` v adresári `cv08`.

Odovzdajte súbor `ham.py` v ktorom je implementovaná trieda `HamiltonianCycle`
s metódou `find`. Program `hamTest.py` musí s vašou knižnicou korektne zbehnúť.

Ak chcete v pythone použiť knižnicu z [examples/sat](../examples/sat), nemusíte
si ju kopírovať do aktuálne adresára, stačí ak na začiatok svojej knižnice
pridáte:
```python
import os
import sys
sys.path[0:0] = [os.path.join(sys.path[0], '../examples/sat')]
import sat
```

Odovzdávanie riešení v iných jazykoch konzultujte s cvičiacimi.
