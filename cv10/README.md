Cvičenie 10
==========

**Riešenie odovzdávajte podľa
[pokynov na konci tohoto zadania](#technické-detaily-riešenia)
do utorka 17.5. 23:59:59.**

Súbory potrebné pre toto cvičenie si môžete stiahnuť ako jeden zip
[`cv10.zip`](https://github.com/FMFI-UK-1-AIN-412/lpi/archive/cv10.zip).

Plánovanie (3b)
----------

Vyriešte úlohu o gazdovi, koze, kapuste a vlku pomocu SAT solvera.
Implementujte metódu `vyries` triedy `VlkKozaKapusta`, ktorá dostane
ako argumenty počiatočný stav a počet krokov, koľko má mať nájdené riešenie – _plán_.

Počiatočný stav je reprezentovaný ako slovník tvaru

```python
{ "vlk": "vlavo", "koza": "vlavo", "kapusta": "vpravo", "gazda": "vlavo" }
```
Môžete predpokladať, že počiatočný stav je korektný vzhľadom na podmienky úlohy.

Vaša metóda vráti zoznam akcií (reťazcov), ktoré hovoria, koho má gazda previezť.
`"vlk"` znamená že prevezie vlka atď., `"gazda"` znamená, že sa prevezie sám.
Ak sa úloha nedá vyriešiť na daný počet krokov, metóda vráti prázdny zoznam.

Niekoľko poznámok, ktoré by mohli pomôcť:

Potrebujeme nejak reprezentovať stavy v jednotlivých krokoch, možné akcie a to, v ktorom
kroku sa ktorá akcia vykonala.

**Stavy** môžeme reprezentovať 4 stavovými premennými (`vlavo_vlk`, `vlavo_koza`,
`vlavo_kapusta` a `vlavo_gazda`). Keďže sa tieto menia z kroku na krok,
výrokové premenné, ktoré použijeme, budú ešte parametrizované číslom kroku:

- `vlavo_X_K` bude pravdivá, ak `X` je na ľavom brehu v kroku `K`.

Podobne budeme reprezentovať **akcie**: máme 8 akcií (
`prevez_dolava_vlk`, `prevez_dolava_koza`, `prevez_dolava_kapusta`, `prevez_dolava_gazda`
`prevez_doprava_vlk`, `prevez_doprava_koza`, `prevez_doprava_kapusta`, `prevez_doprava_gazda`
), ale keďže potrebujeme reprezentovať, v ktorom kroku
ktorú z nich vykonáme, premenné budú znovu mať číslo kroku ako parameter:

- `prevez_dolava_X_K` bude pravdivá, ak v `K`-tom kroku prevezie gazda objekt `X` doľava
  (`prevez_dolava_gazda_K` znamená, že sa preváža sám),
- `prevez_doprava_X_K` bude pravdivá, ak v `K`-tom kroku prevezie gazda objekt `X` doprava.

Poznámka: stačili by nám aj 4 premenné tvaru `prevez_X_K`, akurát by sa trochu
komplikovanejšie písali formuly pre ich podmienky a efekty.

Všimnite si, že pre plán dlhý `N` krokov máme `N` akcií (`0` až `N-1`)
a `N+1` stavov (`0` až `N`):
```
stav_0  akcia_0  stav_1  akcia_1  ...  stav_N-1  akcia_N-1  stav_N
```

Vo vstupe pre SAT solver sú premenné reprezentované číslami, takže pomôžu
správne pomocné funkcie a konštanty, ktoré uľahčia preklad z mien fluentov a
akcií do čísel a naopak. Ak hľadáme plán dĺžky `N`, potrebujeme `4*(N+1)`
premenných pre stavové premenné tvaru `vlavo_CO_I` pre 0 <= `I` <= `N`
a `2*4*N` premenných pre akcie tvaru `prevez_KAM_CO_I`
pre 0 <= `I` < `N-1`.

Zadanie pre SAT solver bude zložené z formúl popisujúcich:
- počiatočný stav,
- koncový stav,
- vykonanie práve jednej akcie v každom kroku,
- podmienky a efekty akcií,
- zotrvačnosť stavových premenných (frame problem) nezmenených akciou,
- obmedzenia úlohy.

**Počiatočný stav** popíšeme ako konjunkciu hodnôt stavových premenných v 0-tom kroku.
Napríklad počiatočný stav z vyššie uvedeného pythonovského slovníka (všetci vľavo) popisuje formula:
```
vlavo_vlk_0 ∧ vlavo_koza_0 ∧ vlavo_kapusta_0 ∧ vlavo_gazda_0
```
Podobne popíšeme želaný **koncový stav** ako konjunkciu hodnôt stavových
premenných v `N`-tom kroku:
```
vlavo_vlk_N ∧ vlavo_koza_N ∧ vlavo_kapusta_N ∧ vlavo_gazda_N
```

Vykonanie **práve jednej akcie** v každom kroku zabezpečíme formulami:
- aspoň jedna akcia v `I`-tom kroku:

    ```
    prevez_dolava_vlk_I ∨ prevez_dolava_koza_I ∨ ... ∨ prevez_doprava_gazda_I
    ```

- najviac jedna akcia v `I`-tom kroku:
  klauzuly `¬prevez_KAM1_CO1_I ∨ ¬prevez_KAM2_CO2_I` pre všetky kombinácie
  smerov `KAM1`, `KAM2` ∈ {`dolava`, `doprava`}
  a prevážaných objektov `CO1`, `CO2` ∈ {`vlk`, …, `gazda`}.

**Podmienky**, za ktorých možno akciu vykonať,
sú jej **nutnými** podmienkami —
teda ak sa akcia vykoná, museli pred jej vykonaním platiť.
Vyjadríme to implikáciami `akcia_I → (podmienka_1_I ∧ ... ∧ podmienka_k_I)`.
(Čo by znamenala opačná implikácia, teda ak by sme podmienky zapísali
ako postačujúce?)
Napríklad podmienkou prevezenia kapusty doprava v `I`-tom kroku je,
že sa kapusta v `I`-tom kroku nachádza vľavo a nachádza sa tam aj gazda
(kapusta sa sama neprevezie).
Zapíšeme ju teda
```
prevez_doprava_kapusta_I → (vlavo_kapusta_I ∧ vlavo_gazda_I)
```
Podmienky musíme pre SAT solver zapísať pre vykonanie akcie
v každom kroku `I` od 0 po `N-1`.

Akcia je **postačujúcou** podmienkou svojich **efektov**,
teda zmien stavových premenných
(nový stav určite nastane po vykonaní akcie,
ale môže nastať aj z iných príčin).
Zapíšeme ich teda implikáciami
`akcia_I → (efekt_1_I+1 ∧ ... ∧ efekt_k_I+1)`.
Napríklad efektom prevezenia kapusty doprava v `I`-tom kroku je,
že kapusta a gazda sa v `I+1`-om kroku nachádzajú vpravo:
```
prevez_doprava_kapusta_I → (¬vlavo_kapusta_I+1 ∧ ¬vlavo_gazda_I+1)
```
Efekty (rovnako ako podmienky) akcií
musíme pre SAT solver zapísať pre vykonanie akcie
v každom kroku `I` od 0 po `N-1`.

Pri popise efektov akcie je pohodlné zapisovať
iba zmeny stavových premenných.
SAT solveru však treba vysvetliť aj **zotrvačnosť stavových premenných**
(frame problem),
teda to, že stavové premenné neovplyvnené akciou
sa medzi `I`-tym a `I+1`-ým krokom nezmenia.
Môžeme to spraviť napríklad tak, že pre každú akciu a každý
krok priamo popíšeme, že hodnoty akciou neovplyvnených premenných
sa prenášajú do ďalšieho kroku.
Zvyčajne je ale oveľa stručnejšie zapísať,
že nutnou podmienkou zmeny stavovej premennej medzi
`I`-tym a `I+1`-ým krokom je vykonanie niektorej z akcií,
ktorá má túto zmenu ako efekt (explanatory frame axioms).
Napríklad kapusta sa premiestni zľava doprava
iba vykonaním akcie jej prevozu doprava:
```
(vlavo_kapusta_I ∧ ¬vlavo_kapusta_I+1) → prevez_doprava_kapusta_I
```
Nezabudnite, že treba opísať aj opačné prevozy:
```
(¬vlavo_kapusta_I ∧ vlavo_kapusta_I+1) → prevez_dolava_kapusta_I
```
Ak by niektorú zmenu spôsobovalo viacero akcií,
spojíme ich v konzekvente (na pravej strane) implikácie
disjunkciou (niektorá z nich sa musí vykonať, ale nie všetky).

**Obmedzenia úlohy** (čo nemôže ostať bez gazdu na tom istom brehu)
sa dajú buď zahrnúť do predpokladov akcií,
ale tiež ľahko napísať pre každý stav `I`.
Napríklad formula
```
¬(vlavo_vlk_I ∧ vlavo_kapusta_I ∧ ¬vlavo_gazda_I)
```
hovorí, že sa nesmie stať, aby vlk a kapusta boli v `I`-tom kroku
vľavo bez gazdu
(také ohodnotenie výrokových premenných nesplní našu teóriu).

## Technické detaily riešenia

Riešenie odovzdajte do vetvy `cv10` v adresári `cv10`.
Odovzdávajte (modifikujte) súbor `vlkKozaKapusta.py`.
Program [`vlkKozaKapustaTest.py`](vlkKozaKapustaTest.py)
musí s vašou knižnicou korektne zbehnúť.

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
