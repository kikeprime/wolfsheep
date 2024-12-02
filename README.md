<h1>English <br>Rabbits, Grass and Weeds population model <img src="rabbitgrassweed/pics/frabbit.png"></h1>

<h2>Introduction</h2>

The "Rabbits, Grass and Weed" is a self-programmed mesa implementation and further development of an agent-based model created in NetLogo.
This model models the cohabitation of a predator species and one of its prey in three ways.
The default model type contains my extensions while the rest two are meant to implement the original model's two types as faithfully as possible.

<h2>The model types' operational characteristics</h2>

<h3>Mutual characteristics</h3>

In all three models, there are two animal species, one predator and one of its prey, which are represented by wolves and sheep.
These animals live in a grassy area where the sheep graze the grass, the wolves eat the sheep.
Furthermore, all entities have some energy (energy point from now on) which is decreased by one in every step (the model's change of state) but is increased by the given parameter by eating. If there energy is fully consumed (not 0 but less than 0 energy point) they die. They can also reproduce randomly, however doing so halves their energy.

In the original model, the grass were put in the cells as patches while in this implementation as agents. In the case of all three models, the number of grass agents is the same as the number of cells. The grass has two states, grown and grazed.

New parameters which work for all three models:

<ul>
<li>Whether the wolves should hunt actively.</li>
<li>Hunting limiter exponent. See below.</li>
<li>Whether the sheep try to flock.</li>
<li>The seed that controls the random functions. The seed makes the runs reproducable, but can be turned off.</li>
</ul>

The hunt limiter exponent means that the probability of a wolf hunts actively is $(\text{energy point})^{-|\text{exponent}|}$.
So, if the exponent is 0 there's no limitation. It's imortant to note the reason behind the exponent being nonpositive is that the probability would be 100% just like in case of 0 due to how the code works. Overhunt is typical in case of free hunt this was the motivation behind the exponent.

<h3>Wolves and sheep</h3>

<ul>
<li>The simplest model type, which was directly implemented from the original model.</li>
<li>All the grasses are always grown.</li>
<li>The sheep have infinite energy (it doesn't change).</li>
<li>The wolves eat one sheep from the cell they're residing with given probability.</li>
<li>The entities give birth to one descendant with given probability which descendant is put into one of the neighboring cells.</li>
</ul>

<h3>Wolves, sheep and grass</h3>

<ul>
<li>Also implemented from the original model.</li>
<li>The rules above are still intact alongside the ones below.</li>
<li>The sheep's energy changes just like the wolves'.</li>
<li>The grazed grass agents become grown again after given number of steps.</li>
</ul>

<h3>Extended model</h3>

<ul>
<li>The model type extended by me.</li>
<li>The animal agents have gender.</li>
<li>For reproduction, two entities with different genders must be present in the same cell and both parents must "want" it.</li>
<li>Because of the new reproduction conditions, one parent's reproduction probability is the square root of the parameter, so the parents give the parameter together.</li>
</ul>

<h2>The visualization application</h2>

<h3>Running</h3>

The model's visualization is done by the mesa_viz_tornado python package (so Python is a dependency) which is automatically installed during mesa version 2.4.0's installation but the newer versions (3.0.0+) don't use it anymore so for the sake of compatibility the neccessary elements are imported directly. 

The visualization application can be run in multiple ways. One way is to run run.py which is can be found alongside this file, or we type "mesa runserver" without quotation marks into a terminal opened in this folder.

Unfortunatley, running is only recommended under Linux, because for some reason under Windows the interactive elements don't appear correctly on the webpage generated by mesa_viz_tornado, but despite this everything works fine. However, via WSL or virtual machine it can be perfectly run on Windows as well. Both methods were tested under Debian Linux. I recommend the WSL method, because the shown IP-address URL works (http://127.0.0.1:8521, which is equivalent with <a href=http://localhost:8521>localhost:8521</a>) unlike with a virtual machine, where the IP-address depends on the program and its settings, or we use the application inside the virtual machine.

<h3>Handling</h3>

<img src="rabbitgrassweed/pics/viz_showcase_eng.png" width=700>

<br>

The figure above is a screenshot of the app in initial state with deafult parameters.

The default language of the webpage is English but by clicking on the flag in the top right corner it can be changed to Hungarian and back. The model's name can be seen in the top left corner, next to it by clicking on the About button README.md's shortened and current language version can be read. The Start, Step and Reset buttons are left to the flag which do what's on the tin but the Start button becomes the Stop button if the simulation is running.

The model's parameters can be set on the left side, the grid that visualizes the model is in the middle, above it the simulation's speed can be set whose default value is 3 steps/second, however the number of agents can effect it (for example in case of overgrowth it's slower). Under the grid the graphs can be seen, among them the 1st one is the number of entities by species and gender depending on the number of steps. The bottom graph is the percentage of the grown grass agents also depending on the number of steps.

The female wolves are orange, the male ones are gray, the female sheep are white, the male ones are black. The consequence of this choice is that in the inherited models all wolves are male and all sheep are female.

<h1>Magyar <br>Farkasok és bárányok populációmodell <img src="rabbitgrassweed/pics/frabbit.png"></h1>

<h2>Előszó</h2>

A "Nyulak, fű és gyomok" egy NetLogoban készült ágens alapú modell saját programozású mesa implementációja, illetve továbbfejlesztése.
Ez a modell egy növényevőfaj és annak kétféle táplálékának populációinak együttélését modellezi.
Az alapértelmezett modelltípus az eredeti modellt hivatott a lehető leghűbben implementálni, míg a "Bővített modell" típusban az egyedenek neme is van.

Egy ilyen modellt főként a mezőgazdaság és a természetvédelem területén lehet hasznosítani. A mezőgazdaságon belül az állattartás megtervezésénél lehet hasznos, míg a természetvédelemben a veszélyeztetett fajok érdekében történő beavatkozások hatásai szimulálhatók. Természetesen pontosan ez a modell egyikre sem alkalmas, mert primitív, azonban egy kiindulási alapként szolgálhat. A modell jelenlegi állapotában főként szemléltetésre használható.

<h2>A modelltípusok működési jellemzői</h2>

<h3>Közös jellemzők</h3>

Mindkét modelltípusban van egy növényevőfaj, amelyet nyulakkal reprezentálunk.
Ezek a nyulak egy olyan területen élnek, ahol fű vagy gyomok nőhetnek valószínűségi alapon, amelyeknek van egy adott tápértéke.
Továbbá minden egyednek van valamennyi energiája (továbbiakban energiapont, röviden EP), amely minden lépésben (a modell állapotváltozása) eggyel csökken, de evés által a megevett táplálék típusától függő paraméternyivel megnő. Ha elfogy az energiájuk, akkor meghalnak. Ezek mellett képesek is szaporodni, amennyiben egy megadott szint feletti energiapontjuk van, azonban ekkor az energiájuk megfeleződik. A modell egy lépésében az állat ágensek egy szomszédos cellába lépnek át, ahol a szomszédos cellák a Moore-féle szomszédokat jelentik az ágens aktuális cellájának kivételével, tehát az állat ágensek nem maradhatnak egy helyben.

Az energiapontról annyit érdemes tudni, hogy a program eggyel kevesebb energiaponttal dolgozik, mint ami egy állaton látható a vizualizációs alkalmazásban, ha rájuk tesszük a kurzort. Ez azt hivatott korrigálni, hogy a szaporodási küszöb és a kezdeti maximális EP paraméterek szigorú egyenlőtlenséget használnak. Ezen paraméterek csúszkái a kijelzett értékek szerint állíthatók. Tehát a felhasználónak az alkalmazás legalább 1 EP-t jelez. Az állatokra rátéve a kurzort látható egy "Layer: 1" érték is, ami réteget jelent és nem elhagyható. A fű ágenseknél ez a réteg 0 és ennek köszönhető, hogy csak az állatokon jelenik meg ez a jelzés.

Az eredeti modellben a fű és a gyomok mint "patchek" voltak a cellákba helyezve, míg ebben az implementációban ágensként.
A füvet és a gyomokat egy közös fű ágens kezeli, amennyiből annyi van, ahány cella. A fű ágenseknek két állapota van, kinőtt és lelegelt.
Fontos tulajdonság, hogy a cellákban nagyobb valószínűséggel nő ki fű, mint gyomok. Ennek az az oka, hogy először az dől el, hogy gyomok nőhetnek-e ki és utána, hogy fű, azonban ez felülírja gyomokat, amennyiben bekövetkezik. Tehát, ha fű kinőhet a megadott valószínűség szerint, akkor fű nő ki függetlenül attól, hogy gyomok kinőhetnek-e vagy sem. Ez a viselkedés az eredeti modellből származik.

A modell továbbfejlesztése céljából lehetőség van egy ragadozófaj hozzáadásához, amelyet rókákkal reprezentálunk. A rókák alapvetően ugyanúgy viselkednek, mint a nyulak, de természetesen a rókák a nyulakat eszik meg. Emellett képesek aktívan is vadászni, vagyis csak olyan szomszédos cellába lépni, amelyben van nyúl.

A paraméterek sorrendben és alapértelmezett értékük:

<ul>
<li>A rács szélessége és magassága, ami csak a kód módosításával állítható a vizualizációs alkalmazás korlátai miatt.
<br><i>30 x 30</i></li>
<li>Tórusz: Ha egy állat ágens a rács szélén van, akkor átléphetnek-e a szemben lévő szélre vagy sem.
<br><i>Igaz</i></li>
<li>Modelltípus, amely lehet az eredeti modell, a "Nyulak, fű és gyomok modell", vagy a "Bővített modell", amiben az állatoknak van neme.
<br><i>Nyulak, fű és gyomok modell</i></li>
<li>A nyulak kezdeti száma.
<br><i>150</i></li>
<li>A rókák kezdeti száma.
<br><i>0</i></li>
<li>A nyulak fűből és gyomokból nyert energiapont mennyisége.
<br><i>5 és 0</i></li>
<li>A rókák nyulakból nyert energiapont mennyisége.
<br><i>5</i></li>
<li>A nyulak és rókák maximális kezdeti energiapont mennyisége, eredetileg ez az érték nem volt változtatható.
<br><i>10 és 10</i></li>
<li>A nyulak és rókák szaporodási küszöbe. Legalább ennyi energiapontra van szüksége egy egyednek a szaporodáshoz.
<br><i>15 és 15</i></li>
<li>A fű és a gyomok kinövési valószínűsége százalékban. Az eredeti modellben ezrelékben, de a csúszkák ilyen sűrű beosztású intervallumon pontatlanok.
<br><i>6%, eredetileg 15 ezrelék, vagyis 1,5%</i></li>
<li>A nyulak csordába igyekezzenek-e szerveződni.
<br><i>Hamis</i></li>
<li>A rókák aktívan vadásszanak-e.
<br><i>Igaz</i></li>
<li>A vadászatot korlátozó kitevő. Lásd lejjebb!
<br><i><math xmlns="http://www.w3.org/1998/Math/MathML"><mo>-</mo><mn>0,5</mn></math></i></li>
<li>A random függvényeket szabályzó seed. A seed segítségével reprodukálhatóvá válnak a futtatások, de kikapcsolható.
<br><i>Igaz és 474</i></li>
</ul>

A vadászatot korlátozó kitevő azt jelenti, hogy annak a valószínűsége, hogy egy róka aktívan vadászik, vagyis csak olyan szomszédos cellába lép, ahol van nyúl, $\text{energiapont}^{-|\text{kitevő}|}$. Tehát, ha a kitevő 0, akkor nincs korlátozás. Fontos megjegyezni, hogy a kitevő azért nem pozitív, mert különben a kód működéséből kifolyólag a valószínűség 100% lenne, mint 0 esetében. Szabad vadászat esetén jellemző a túlvadászat, ez volt a kitevő bevezetésének motivációja.

<h3>Bővített modell</h3>

<ul>
<li>Az általam bővített modelltípus.</li>
<li>Az állat ágenseknek van neme.</li>
<li>A szaporodáshoz a szükséges energiapont mellett két különböző nemű egyednek kell lennie egy közös cellában.</li>
</ul>

<h2>Megfigyelések</h2>

A modell elemzés céljából legérdekesebb tulajdonsága a stabilitás, vagyis, hogy a modellben szereplő fajok kihalnak-e vagy sem.<br>
A fent leírt alapértelmezett paraméterek esetén, amelyek a fű kinövési valószínűsége és az újak kivételével az eredeti modellből származnak, jellemző a stabilitás. A rókák paraméterei úgy lettek beállítva, hogy 50 kezdeti róka esetén is stabil legyen a modell. Ez utóbbi eset futtatható lejjebb és 10 000 lépés után is stabil.

Érdekes jelenség, hogy teljesen különböző paraméterek mellett is az indítás után az állatok száma lezuhan, de előfordulhat, hogy a zuhanást egy kis növekedés előzi meg, azonban ez a seedtől függ.

A modell akkor is stabil marad, ha a modelltípust átállítjuk, azonban rókákkal már ez nem teljesül, mert a rókák kihalnak. Mindkét modelltípusban megmarad a stabilitás, ha a gyomok szaporodási valószínűségét 12% állítjuk, de a gyomok tápértéke továbbra is 0.

Ha a kezdeti rókák száma 50 és az aktív vadászat ki van kapcsolva, akkor a rókák csak úgy élhetnek túl, ha valamilyen paramétert átállítunk. Több teszt futtatása után a nyulak tápértékének növelése bizonyult kifizetődőnek. A minimális tápérték amellett stabil a modell az 12.

A bővített modell rókákkal együtt jellemzően nem stabil, ami a rókák kihalását jelenti, de a nyúl populáció ezután stabilizálódik. Csak szélsőséges paraméterek mellett jellemző a nyulak kihalása. A rókák kihalása jellemzően úgy zajlik, hogy az említett kezdeti csökkenés után a nyulak száma megugrik, amelyet követ a rókák gyarapodása, de már kis mértékű gyarapodás után a nyulak száma olyan szintre zuhan, ami nem képes eltartani a rókákat, így a rókák kihalnak, amely kihalást a rókák aktív vadászata csak felgyorsít. Az egyik legjobb eredmény az, hogy a rókák száma 30 körül marad tartósan, de ugyanezen paraméterek mellett 474-es seeddel ez a szám csak 10. A paraméterek ehhez a kísérlethez a rókák kezdeti száma 75, a nyulak tápértéke 10 EP, a rókák szaporodási küszöbe 30 EP, fű 15% eséllyel nő újra, a rókák nem vadásznak aktívan, seed nem engedélyezve vagy a seed 474.

<h2>A vizualizációs program</h2>

<h3>Futattás</h3>

A modell vizualizációjáért a mesa_viz_tornado python csomag felelős (a Python tehát előfeltétele a futtatásnak), ami a mesa 2.4.0 verziójának telepítésekor automatikusan települ, azonban az ennél újabb verziók (3.0.0+) már nem használják, ezért a kompatibilitás érdekében közvetlenül importáltam a belőle szükséges elemeket.

A vizualizációs programot többféleképpen is el lehet indítani. Egyik lehetőség az ezen notebookkal egy mappában lévő run.py fálj futtatása, vagy a mappában megnyitott parancsorba azt írjuk be, hogy "mesa runserver" idézjelek nélkül.

Sajnálatos módon, csak Linux alatt ajánlott a futtatás, mert valamilyen ok folytán Windows alatt a mesa_viz_tornado által generált weboldalon nem jelennek meg rendesen az interaktív elemek, de ettől függetlenül minden működik. Azonban WSL-lel vagy virtuális géppel Windowson is hibátlanul futattható. Mindkét módszert Debian Linuxszal teszteltem. Én a WSL megoldást javaslom, mert a kiírt IP-címes URL működik (<a href=http://127.0.0.1:8521>http://127.0.0.1:8521</a>, amivel egyenértékű a <a href=http://localhost:8521>localhost:8521</a>) a virtuális gép esetével ellentétben, ahol a programtól és annak beállításaitól függ az IP-cím, vagy a virtuális gépen belül használjuk a programot.

<h3>Kezelés</h3>

<img src="rabbitgrassweed/pics/viz_showcase_hun.png" width=700>

<br>

A fenti ábrán egy az alapértelmezett paraméterekkel, kezdeti állapotban készült képernyőkép látható.

A weboldal alapértelmezett nyelve az angol, de a jobb felső sarokban lévő zászlóra kattintva a grafikonok jelmagyarázatának kivételével átállítható magyarra és akár vissza is. A bal felső sarokban a model neve látható, mellette a Leírás gombra kattintva a README.md egy rövidített, csak az oldal aktuális nyelvén lévő változata olvasható. A zászlótól balra látható az Indítás, a Léptetés és a Visszaállítás gombok, amelyek nevükhöz hűen működnek, de az Indítás gomb a Megállítás gombbá változik, ha fut a szimuláció.

A bal oldalon a modell paraméterei állíthatók be, középen a modellt vizualizáló négyzetrács látható, amely felett a rendes, Indítás gombbal való indított szimuláció sebessége allítható, amely alapértelmezett értéke 3 képkocka/másodperc, azonban ez az ágensek számától függően változhat (például túlszaporodás esetén lassabb). A rács alatt két grafikon látható, amely közül a felső az egyedek számát ábrázolja fajonként, illetve nemenként a lépésszám függvényében. Az alsó grafikon a kinőtt fűágensek százalékos arányát ábrázolja szintén a lépésszám függvényében. A lejjebb lévő "Vizualizáció nélküli futtattás" szakaszban ugyanezen grafikonok láthatóak.

A nőstény nyulak fehérek, a hímek barnák, a nőstény rókák narancssárgák, a hímek pirosak. Ennek a választásnak a következménye az, hogy az alapértelmezett modelltípusban minden nyúl nőstény és minden róka hím.

<h1>References / Hivatkozások</h1>

<ul>
<li>Wilensky, U. (2001). NetLogo Rabbits Grass Weeds model. <a href=http://ccl.northwestern.edu/netlogo/models/RabbitsGrassWeeds>http://ccl.northwestern.edu/netlogo/models/RabbitsGrassWeeds</a>. Center for Connected Learning and Computer-Based Modeling, Northwestern University, Evanston, IL.</li>
<li>Wilensky, U. (1997). NetLogo Wolf Sheep Predation model. <a href=http://ccl.northwestern.edu/netlogo/models/WolfSheepPredation>http://ccl.northwestern.edu/netlogo/models/WolfSheepPredation</a>. Center for Connected Learning and Computer-Based Modeling, Northwestern University, Evanston, IL.</li>
<li><a href=https://upload.wikimedia.org/wikipedia/commons/c/c1/Flag_of_Hungary.svg>https://upload.wikimedia.org/wikipedia/commons/c/c1/Flag_of_Hungary.svg</a></li>
<li><a href=https://upload.wikimedia.org/wikipedia/commons/a/a5/Flag_of_the_United_Kingdom_(1-2).svg>https://upload.wikimedia.org/wikipedia/commons/c/c1/Flag_of_Hungary.svg</a></li>
<li><a href=https://mesa.readthedocs.io/stable/tutorials/visualization_tutorial.html>https://mesa.readthedocs.io/stable/tutorials/visualization_tutorial.html</a> (dead/halott link)</li>
<li><a href=https://stackoverflow.com/questions/66624802/javascript-start-function-when-innertext-changes>https://stackoverflow.com/questions/66624802/javascript-start-function-when-innertext-changes</a></li>
</ul>
