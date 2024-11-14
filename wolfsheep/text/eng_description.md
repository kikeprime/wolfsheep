<h1>Wolves and Sheep population model<br>
<img src="/local/custom/wolfsheep/pics/wolf.png"> <img src="/local/custom/wolfsheep/pics/fsheep.png"></h1>

<h2>Introduction</h2>
The "Wolves and Sheep" is a self-programmed mesa implementation and further development of an agent-based model created in NetLogo.
This model models the cohabitation of a predator species and one of its prey in three ways.
The default model type contains my extensions while the rest two are meant to implement the original model's two types as faithfully as possible.

<h2>The model types' operational characteristics</h2>
<h3>Mutual characteristics</h3>
In all three models, there are two animal species, one predator and one of its prey, which are represented by wolves and sheep.
These animals live in a grassy area and the sheep graze the grass, the wolves eat the sheep.
Furthermore, all entities have some energy (energy point from now on) which is decreased by one in every step (the model's change of state) but is increased by the given parameter by eating. If there energy is fully consumed (not 0 but less than 0 energy point) they die. The can also reproduce randomly, however doing so halves their energy.

In the original model, the grass were put in the cells as patches while in this implementation as agents. In the case of all three models, the number of grass agents equals to the number of cells. The grass has two states, grown and grazed.

New parameters which work for all three models:

<ul>
<li>Whether the wolves should hunt actively.</li>
<li>Hunting limiter exponent. See below.</li>
<li>Whether the sheep try to flock.</li>
<li>The seed that controls the random functions. The seed makes the runs reproducable, but can be turned off.</li>
</ul>

The hunt limiter exponent means that the probability of a wolf hunts actively is $\text{(energy point)}^{-|\text{exponent}|}$.
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

<h2>The visualization program</h2>
<h3>Running</h3>
The model's visualization is done by the mesa_viz_tornado python package (so Python is a dependency) which is automatically installed during mesa version 2.4.0's installation but the newer versions (3.0.0+) don't use it anymore so for the sake of compatibility the neccessary elements are imported directly. 

A vizualizációs programot többféleképpen is el lehet indítani. Egyik lehetőség az ezen notebookkal egy mappában lévő run.py fálj futtatása, vagy a mappában megnyitott parancsorba azt írjuk be, hogy "mesa runserver" idézjelek nélkül.

Sajnálatos módon, csak Linux alatt ajánlott a futtatás, mert valamilyen ok folytán Windows alatt a mesa_viz_tornado által generált weboldalon nem jelennek meg rendesen az interaktív elemek, de ettől függetlenül minden működik. Azonban WSL-lel vagy virtuális géppel Windowson is hibátlanul futattható, de a Microsoft Edge böngésző így sem tudja megjeleníteni az érintett elemeket, de a Firefox és a Google Chrome igen. Mindkét módszert Debian Linuxszal teszteltem. Én a WSL megoldást javaslom, mert a kiírt IP-címes URL működik (http://127.0.0.1:8521, amivel egyenértékű a <a href=http://localhost:8521>localhost:8521</a>) a virtuális gép esetével ellentétben, ahol a programtól és annak beállításaitól függ az IP-cím, vagy a virtuális gépen belül használjuk a programot.

<h1>References</h1>
<ul>
<li>Wilensky, U. (1997). NetLogo Wolf Sheep Predation model. http://ccl.northwestern.edu/netlogo/models/WolfSheepPredation. Center for Connected Learning and Computer-Based Modeling, Northwestern University, Evanston, IL.</li>
</ul>
