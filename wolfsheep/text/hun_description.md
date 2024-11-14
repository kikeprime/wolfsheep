<h1>Farkasok és bárányok populációmodell<br>
<img src="/local/custom/wolfsheep/pics/wolf.png"> <img src="/local/custom/wolfsheep/pics/fsheep.png"></h1>

<h2>Előszó</h2>
A "Farkasok és bárányok" egy NetLogoban készült ágens alapú modell saját programozású mesa implementációja, illetve továbbfejlesztése.
Ez a modell egy ragadozófaj és annak egy prédájának populációinak együttélését modellezi háromféleképpen.
Az alapértelmezett modelltípus a saját bővítéseimet tartalmazza, míg a másik kettő az eredeti modell két típusát hivatott a lehető leghűbben implementálni.

<h2>A modelltípusok működési jellemzői</h2>
<h3>Közös jellemzők</h3>
Mindhárom modellben van két állatfaj, egy ragadozó és annak egy prédája, amelyeket farkasokkal és bárányokkal reprezentálunk.
Ezek az állatok egy füves területen élnek és a bárányok legelik a füvet, a farkasok megeszik a bárányokat.
Továbbá minden egyednek van valamennyi energiája (továbbiakban energiapont), amely minden lépésben (a modell állapotváltozása) eggyel csökken, de evés által a megadott paraméternyivel megnő. Ha elfogy az energiájuk (nem 0, hanem kevesebb, mint 0 energiapont), akkor meghalnak. Ezek mellett képesek is szaporodni valószínűségi alapon, azonban ekkor az energiájuk megfeleződik.

Az eredeti modellben a fű mint "patchek" voltak a cellákba helyezve, míg ebben az implementációban ágensként. Mindhárom modell esetén annyi fű ágens van ahány cella. A fűnek két állapota van, a kinőtt és a lelegelt.

Új paraméterek, amely mindhárom modellnél működnek:

<ul>
<li>A farkasok aktívan vadásszanak-e.</li>
<li>A vadászatot korlátozó kitevő. Lásd lejjebb.</li>
<li>A bárányok nyájba igyekezzenek-e szerveződni.</li>
<li>A random függvényeket szabályzó seed. A seed segítségével reprodukálhatóvá válnak a futtattások, de kikapcsolható.</li>
</ul>

A vadászatot korlátozó kitevő azt jelenti, hogy annak a valószínűsége, hogy egy farkas aktívan vadászik $\text{energiapont}^{-|\text{kitevő}|}$. Tehát, ha a kitevő 0, akkor nincs korlátozás. Fontos megjegyezni, hogy a kitevő azért nempozitív, mert különben a kód működéséből kifolyólag a valószínűség 100% lenne, mint a 0 esetében. Szabad vadászat esetén jellemző a túlvadászat, ez volt a kitevő bevezetésének motivációja.

<h3>Farkasok és bárányok</h3>
<ul>
<li>A legegyszerűbb modelltípus, amely az eredeti modellből lett közvetlenül implementálva.</li>
<li>Minden fű mindig ki van nőve.</li>
<li>A bárányoknak végtelen energiájuk van (nem változik).</li>
<li>A farkasok megadott valószínűséggel esznek meg egy bárányt abból a cellából amelyen ők is vannak.</li>
<li>Az egyedek megadott valószínűséggel hoznak világra utódot, amely utód az egyik szomszédos cellába kerül.</li>
</ul>

<h3>Farkasok, bárányok és fű</h3>
<ul>
<li>Szintén az eredeti modellből implementálva.</li>
<li>A fentiek érvényesek az alábbiak mellett.</li>
<li>A bárányok energiája ugyanúgy változik, mint a farkasoké.</li>
<li>A lelegelt fű ágensek megadott számú lépés után nőnek ki újra.</li>
</ul>

<h3>Bővített modell</h3>
<ul>
<li>Az általam bővített modelltípus.</li>
<li>Az állat ágenseknek van neme.</li>
<li>A szaporodáshoz a valószínűség mellett két különböző nemű egyed kell legyen egy közös cellában és mindkét szűlőnek "akarnia" kell.</li>
<li>Az új szaporodási feltételek miatt egy szülő szaporodási valószínűsége a paraméter gyöke, így a két szülő együtt adja ki a paramétert.</li>
</ul>

<h2>Megfigyelések</h2>
A megfigyelések leírása előtt rögzíteném a kiindulási paramétereket, amelyeket nagyrészt az eredeti modellből választottam, de az energiapontszerzést és a farkasok szaporodási rátáját növeltem a stabbilitás érdekében.
Az életteret reprezentáló rács szélei össze vannak kötve egymással azaz, ha egy állat például egy felső szélen lévő cellából felfelé lép, akkor az alsó szélen lyukad ki.
A farkasok kezdeti száma 50, a bárányoké 100. A farkasok egy bárány megevésével 30 energiapontot szereznek (eredetileg 20-at), míg a bárányok egy cellányi fűből szintén 20 energiapontot nyernek (eredetileg 4-et).
A farkasok 10 (eredetileg 5), a bárányok 4% valószínűséggel szaporodnak. A lelegelt fű 30 lépésenként nő vissza. A farkasok aktívan vadásznak, a bárányok nyájba igyekeznek szerveződni.
A vadászatot korlátozó kitevő -0,5, a seed 474.

A modell elemzés szempontjából legérdekesebb tulajdonsága a stabilitása, vagyis milyen paraméterek mellett nem halnak ki az állatok, illetve nem szaporodnak túl.

Először egy az eredeti modell esetében is stabil beállításról beszélnék, arról, amikor a farkasok, bárányok és fű modellben a farkasok kezdeti számát nullára állítjuk. Ha a modellem minden paraméterét alapértelmezetten hagyunk kivéve a farkasok kezdeti számát, akkor is stabil modellt kapunk, szép nagy nyájakkal. Ha azonban a bárányok fűből nyert energiapontmennyiségét visszaállítjuk 4-re, akkor a bárányok párokba szerveződnek és könnyen előfordulhat, hogy a populáció egyneművé válik, tehát a modell így nem stabil. A párokba szerveződésnek az az eddig nem említett oka, hogy, ha egy báránynak 0 energiapontja van, akkor a mozgásuk nem korlátozott (bármely szomszédos cellába léphetnek, ez az alapértelmezett viselkedés is) a túlélés valószínűségének növelése érdekében.

<h2>A vizualizációs program</h2>
<h3>Futattás</h3>
A modell vizualizációjáért a mesa_viz_tornado python csomag felelős (a Python tehát előfeltétele a futtatásnak), ami a mesa 2.4.0 verziójának telepítésekor automatikusan települ, azonban az ennél újabb verziók (3.0.0+) már nem használják, ezért a kompatibilitás érdekében közvetlenül importáltam a belőle szükséges elemeket.

A vizualizációs programot többféleképpen is el lehet indítani. Egyik lehetőség az ezen notebookkal egy mappában lévő run.py fálj futtatása, vagy a mappában megnyitott parancsorba azt írjuk be, hogy "mesa runserver" idézjelek nélkül.

Sajnálatos módon, csak Linux alatt ajánlott a futtatás, mert valamilyen ok folytán Windows alatt a mesa_viz_tornado által generált weboldalon nem jelennek meg rendesen az interaktív elemek, de ettől függetlenül minden működik. Azonban WSL-lel vagy virtuális géppel Windowson is hibátlanul futattható, de a Microsoft Edge böngésző így sem tudja megjeleníteni az érintett elemeket, de a Firefox és a Google Chrome igen. Mindkét módszert Debian Linuxszal teszteltem. Én a WSL megoldást javaslom, mert a kiírt IP-címes URL működik (http://127.0.0.1:8521, amivel egyenértékű a <a href=http://localhost:8521>localhost:8521</a>) a virtuális gép esetével ellentétben, ahol a programtól és annak beállításaitól függ az IP-cím, vagy a virtuális gépen belül használjuk a programot.

<h3>Kezelés</h3>
<img src="/local/custom/wolfsheep/pics/viz_showcase.png" width=700>

A fenti ábrán egy az alapértelmezett paraméterekkel, kezdeti állapotban készült képernyőkép látható.

A felső sávban látható a modell neve, mellette az "About" gomb, amelyre rákattintva egy angol nyelvű leírás ugrik fel. A sáv jobb szélén a "Start", "Step" és "Stop" gombok vannak, amelyek közül a középső a modellt lépteti.

A bal oldalon a modell paraméterei állíthatók be, középen a modellt vizualizáló négyzetrács látható, amely felett a rendes, Start gombbal való indított szimuláció sebessége allítható, amely alapértelmezett értéke 3 lépés/másodperc, azonban ez az ágensek számától függően változhat (például túlszaporodás esetén lassabb). A rács alatt két grafikon látható (az alsó nem fért a képre), amely közül a felső az egyedek számát ábrázolja fajonként, illetve nemenként a lépésszám függvényében. Az alsó grafikon a kinőtt fűágensek százalékos arányát ábrázolja szintén a lépésszám függvényében. A lejjebb lévő "Vizualizáció nélküli futtattás" szakaszban ugyanezen grafikonok láthatóak.

A nőstény farkasok narancssárgák, a hímek szürkék, a nőstény bárányok fehérek, a hímek feketék. Ennek a választásnak a következménye az, hogy az öröklött modelltípusokban minden farkas hím és minden bárány nőstény.

<h1>References / Hivatkozások</h1>
<ul>
<li>Wilensky, U. (1997). NetLogo Wolf Sheep Predation model. http://ccl.northwestern.edu/netlogo/models/WolfSheepPredation. Center for Connected Learning and Computer-Based Modeling, Northwestern University, Evanston, IL.</li>
</ul>
