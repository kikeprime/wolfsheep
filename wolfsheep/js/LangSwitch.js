// set default language here
let lang = "en"

navbar = document.getElementById("navbar")
config = { attributes: true, childList: true, subtree: true }

navbar.innerHTML += `
<div><p>Tab</p></div>
<div id="lang-flag">
<img width="64" src="wolfsheep/pics/Flag_of_Hungary.svg">
</div>
`

// Initialize description
fetch("wolfsheep/text/eng_description.md")
    .then(response => response.text())
    .then(text => description.innerHTML = text)

startButton = document.getElementById("play-pause")
stepButton = document.getElementById("step")
resetButton = document.getElementById("reset")
currentStep = document.getElementById("currentStep").parentElement

currentStep.outerHTML = `<span id="currentStepText">Current Step: </span><span id="currentStep">0</span>`
currentStep = document.getElementById("currentStepText")

fpsText = document.getElementById("elements-topbar").firstElementChild.firstElementChild

StartButtonCallback = (mutationList) => {
    if (lang === "hu") {
        for (const mutation of mutationList) {
            if (startButton.firstElementChild.innerText === "Start") {
                startButton.firstElementChild.innerText = "Indítás"
            }
            else if (startButton.firstElementChild.innerText === "Stop") {
                startButton.firstElementChild.innerText = "Megállítás"
            }
        }
    }
};

const StartButtonObserver = new MutationObserver(StartButtonCallback);
StartButtonObserver.observe(startButton.firstElementChild, config);

const description = document.getElementsByClassName("modal-body")[0].firstElementChild

function SwitchToHun() {
    HeaderToHun()
    ButtonsToHun()
    ParamsToHun()
    lang_flag.firstElementChild.src = "wolfsheep/pics/Flag_of_the_United_Kingdom_(1-2).svg"
    lang = "hu"
}

function HeaderToHun() {
    document.title = "Farkasok és bárányok (Mesa vizualizáció)"
    document.getElementsByClassName("navbar-brand")[0].innerText = "Farkasok és bárányok"
    document.getElementsByClassName("modal-title")[0].innerText = "Farkasok és bárányok leírás"

    fetch("wolfsheep/text/hun_description.md")
        .then(response => response.text())
        .then(text => description.innerHTML = text)
}

function ButtonsToHun() {
    if (!controller.running)
        startButton.firstElementChild.innerText = "Indítás"
    else
        startButton.firstElementChild.innerText = "Megállítás"

    stepButton.firstElementChild.innerText = "Léptetés"
    resetButton.firstElementChild.innerText = "Visszaállítás"
    currentStep.innerText = "Jelenlegi lépés: "
    navbar.firstElementChild.firstElementChild.firstElementChild.innerText = "Leírás"
    fpsText.innerText = "Képkocka per másodperc"
}

function ParamsToHun() {
    // Torus
    let torus = document.getElementById("torus_id")
    torus.parentElement.firstElementChild.innerText = "Tórusz"
    // Model type
    let model_type = document.getElementById("model_type_id")
    model_type.parentElement.firstElementChild.firstElementChild.innerText = "Modelltípus"
    model_type.children[0].innerText = "Bővített modell"
    model_type.children[1].innerText = "Farkasok, bárányok és fű modell"
    model_type.children[2].innerText = "Farkasok és bárányok modell"
    // Initial number of wolves
    document.getElementById("n_wolf_id_tooltip").innerText = "A farkasok kezdeti száma"
    // Initial number of sheep
    document.getElementById("n_sheep_id_tooltip").innerText = "A bárányok kezdeti száma"
    // EP gain from eating (wolves)
    document.getElementById("wolf_ep_gain_id_tooltip").innerText = "Táplálékból nyert EP (farkasok)"
    // EP gain from eating (sheep)
    document.getElementById("sheep_ep_gain_id_tooltip").innerText = "Táplálékból nyert EP (bárányok)"
    // Reproduction rate of the wolves (%)
    document.getElementById("wolf_reproduction_rate_id_tooltip").innerText = "A farkasok szaporodási rátája (%)"
    // Reproduction rate of the sheep (%)
    document.getElementById("sheep_reproduction_rate_id_tooltip").innerText = "A bárányok szaporodási rátája (%)"
    // Grass regrow time
    document.getElementById("regrow_time_id_tooltip").innerText = "A fű visszanövési ideje"
    // Allow hunt
    let allow_hunt = document.getElementById("allow_hunt_id")
    allow_hunt.parentElement.firstElementChild.innerText = "Vadászat engedélyezése"
    // Allow flocking
    let allow_flocking = document.getElementById("allow_flocking_id")
    allow_flocking.parentElement.firstElementChild.innerText = "Nyájba szerveződés engedélyezése"
    // Hunt limiter exponent
    let hunt_exponent = document.getElementById("hunt_exponent_id")
    hunt_exponent.parentElement.firstElementChild.firstElementChild.innerText = "A vadászatot korlátozó kitevő"
    // Allow seed
    let allow_seed = document.getElementById("allow_seed_id")
    allow_seed.parentElement.firstElementChild.innerText = "Seed engedélyezése"
    // Random seed
    let seed = document.getElementById("random_seed_id")
    seed.parentElement.firstElementChild.firstElementChild.innerText = "Random seed"
}

function SwitchToEng() {
    HeaderToEng()
    ButtonsToEng()
    ParamsToEng()
    lang_flag.firstElementChild.src = "wolfsheep/pics/Flag_of_Hungary.svg"
    lang = "en"
}

function HeaderToEng() {
    document.title = "Wolves and Sheep (Mesa visualization)"
    document.getElementsByClassName("navbar-brand")[0].innerText = "Wolves and Sheep"
    document.getElementsByClassName("modal-title")[0].innerText = "About Wolves and Sheep"

    fetch("wolfsheep/text/eng_description.md")
        .then(response => response.text())
        .then(text => description.innerHTML = text)
}

function ButtonsToEng() {
    if (!controller.running)
        startButton.firstElementChild.innerText = "Start"
    else
        startButton.firstElementChild.innerText = "Stop"
    navbar.firstElementChild.firstElementChild.firstElementChild.innerText = "About"
    stepButton.firstElementChild.innerText = "Step"
    resetButton.firstElementChild.innerText = "Reset"
    currentStep.innerText = "Current Step: "
    fpsText.innerText = "Frames Per Second"
}

function ParamsToEng() {
    // Torus
    let torus = document.getElementById("torus_id")
    torus.parentElement.firstElementChild.innerText = "Torus"
    // Model type
    let model_type = document.getElementById("model_type_id")
    model_type.parentElement.firstElementChild.firstElementChild.innerText = "Model type"
    model_type.children[0].innerText = "Extended model"
    model_type.children[1].innerText = "Wolves, sheep and grass model"
    model_type.children[2].innerText = "Wolves and sheep model"
    // Initial number of wolves
    document.getElementById("n_wolf_id_tooltip").innerText = "Initial number of wolves"
    // Initial number of sheep
    document.getElementById("n_sheep_id_tooltip").innerText = "Initial number of sheep"
    // EP gain from eating (wolves)
    document.getElementById("wolf_ep_gain_id_tooltip").innerText = "EP gain from eating (wolves)"
    // EP gain from eating (sheep)
    document.getElementById("sheep_ep_gain_id_tooltip").innerText = "EP gain from eating (sheep)"
    // Reproduction rate of the wolves (%)
    document.getElementById("wolf_reproduction_rate_id_tooltip").innerText = "Reproduction rate of the wolves (%)"
    // Reproduction rate of the sheep (%)
    document.getElementById("sheep_reproduction_rate_id_tooltip").innerText = "Reproduction rate of the sheep (%)"
    // Grass regrow time
    document.getElementById("regrow_time_id_tooltip").innerText = "Grass regrow time"
    // Allow hunt
    let allow_hunt = document.getElementById("allow_hunt_id")
    allow_hunt.parentElement.firstElementChild.innerText = "Allow hunt"
    // Allow flocking
    let allow_flocking = document.getElementById("allow_flocking_id")
    allow_flocking.parentElement.firstElementChild.innerText = "Allow flocking"
    // Hunt limiter exponent
    let hunt_exponent = document.getElementById("hunt_exponent_id")
    hunt_exponent.parentElement.firstElementChild.firstElementChild.innerText = "Hunt limiter exponent"
    // Allow seed
    let allow_seed = document.getElementById("allow_seed_id")
    allow_seed.parentElement.firstElementChild.innerText = "Allow seed"
    // Random seed
    let seed = document.getElementById("random_seed_id")
    seed.parentElement.firstElementChild.firstElementChild.innerText = "Random seed"
}

const lang_flag = document.getElementById("lang-flag")
if (lang_flag !== null)
{
    lang_flag.onclick = () => {
        if (lang === "en") {
            SwitchToHun()
        }
        else if (lang === "hu") {
            SwitchToEng()
        }
    }
}
