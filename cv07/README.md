Cvičenie 7
==========

**Riešenie odovzdávajte podľa
[pokynov na konci tohoto zadania](#technické-detaily-riešenia)
do utorka 19.4. 23:59:59.**


Súbory potrebné pre toto cvičenie si môžete stiahnuť ako jeden zip
[`cv07.zip`](https://github.com/FMFI-UK-1-AIN-412/lpi/archive/cv07.zip).

Tablo (3b)
------------------

Implementujte tablový algoritmus.

Vaše riešenie sa má skladať z dvoch častí:

1. Do tried na reprezentáciu formúl z cvičenia 3 doimplementujte
   metódy `signedSubf` a `getType`, ktoré reprezentujú informácie
   o tablových pravidlách pre jednotlivé typy formúl.
2. Implementujte triedu `TableauBuilder` obsahujúcu metódu `build`,
   ktorá dostane zoznam označených formúl a vytvorí pre ne úplné (alebo
   uzavreté) tablo.

### Označené formuly a tablové pravidlá

Označené formuly reprezentujeme triedou `SignedFormula` z modulu
[`tableau.py`](tableau.py). Pri ich vyrábaní môžete použiť buď konštruktor,
ktorý očakáva znamienko (`True` alebo `False`) a formulu, alebo pomocné statické
metódy `T` a `F`, ktoré očakávajú iba formulu. Na vytvorenie opačnej formuly
voči danej označenej formule môžete použiť metódu `neg`:

```python
from tableau import SignedFormula, T, F

f = Conjunction([Variable('a'), Variable('b')])

tf = SignedFormula(True, f)  # T (a∧b)
tf = T(f)                    # to isté

ff = SignedFormula(False, f) # F (a∧b)
ff = F(f)                    # to isté
ff = tf.neg()                # to isté
ff = -tf                     # to isté
```

Metóda `getType(sign)` vráti akého typu (&alpha; alebo &beta;) by dotyčná
formula bola, ak by bola označená značkou `sign` (negácia a premenná sú vždy
typu &alpha;).

Metóda `signedSubf` vráti „podformuly“ označenej formuly,
t.j. &alpha;<sub>1</sub> a &alpha;<sub>2</sub>, ak by bola typu &alpha;,
a &beta;<sub>1</sub> a &beta;<sub>2</sub>, ak by bola typu &beta;.

Pamätajte, že konjukcia a disjunkcia môžu mať viacero podformúl, takže
tablové pravidlá v skutočnosti vyzerajú nasledovne:

```
 T A1 ∧ A2 ∧ A3 ∧ ... ∧ An           F A1 ∧ A2 ∧ A3 ∧ ... ∧ An
 ───────────────────────────      ──────┬──────┬──────┬─────┬──────
           T A1                    F A1 │ F A2 │ F A3 │ ... │ F An
           T A2
           T A3
           ...
           T An
```
Ekvivalencia je konjunkcia dvoch implikácií ((A⇔B) je skratka za
((A⇒B)∧(B⇒A)), takže pravidlá pre ňu vyzerajú podobne ako pre konjunkciu, len
podformuly majú trošku zložitejší tvar:

```
 T A⇔B             F A⇔B
───────       ───────┬───────
 T A⇒B         F A⇒B │ F B⇒A
 T B⇒A
```

### Tablo

Tablo, ktoré vytvorí metóda `TableauBuilder::build`, bude reprezentované ako
strom vytvorený z objektov `tableau.Node` definovaných v knižnici
[`tableau.py`](tableau.py). Ukážková implementácia v [`builder.py`](builder.py)
iba vytvorí prázdne tablo a následne doň popridáva „vstupné“ formuly.

Pri vytváraní ďalších uzlov tabla potom treba vždy ako druhý parameter  (`source`) konštruktora
`Node` uviesť referenciu na uzol s formulou, z ktorej vznikla formula nového uzla.

Keď pridáme uzol s formulou, ktorá uzatvára vetvu, treba ho navyše „označiť“ volaním metódy
`close`, ktorá má ako parameter referenciu na uzol, ktorého formula má
opačné znamienko ako formula nového uzla.

Jednoduchý príklad na vygenerovanie uzavretého tabla a výsledné tablo:

```python
tab = tableau.Tableau()
root = tableau.Node( tableau.F( Implication( Variable('a'), Variable('a') ) ) )
tab.append(None, root) # Pridávame prvý vrchol - koreň

node1 = tableau.Node( tableau.T( Variable('a') ), source = root)
tab.append(root, node1) # Pridávame node1 pod root

node2 = tableau.Node( tableau.F( Variable('a') ), source = root)
tab.append(node1, node2) # Pridávame node2 pod node1
node2.close(node1)  # node2 je opačný k node1, takže sme zavreli tablo

print(tab)
```

```
(1) F (a=>a)
============
(2) T a (1) 
(3) F a (1) 
  * [3,2]   
```

## Technické detaily riešenia

Riešenie odovzdajte do vetvy `cv07` v adresári `cv07`.  Odovzdávajte
(modifikujte) súbory `formula.py` a `builder.py`.  Program
[`tableauTest.py`](tableauTest.py) musí korektne zbehnúť s vašou knižnicou.

Odovzdávanie riešení v iných jazykoch konzultujte s cvičiacimi.
