// set default language here
let lang = "en"

navbar = document.getElementById("navbar")
config = { attributes: true, childList: true, subtree: true }

switch(lang) {
    default:
    case "hu":
    navbar.innerHTML += `
<div id="lang-flag">
<img src="/local/custom/wolfsheep/pics/hu_flag.png">
</div>
`
    break;
    case "en":
    navbar.innerHTML += `
<div id="lang-flag">
<img src="/local/custom/wolfsheep/pics/en_flag.png">
</div>
`
    break;
}

startButton = document.getElementById("play-pause")
stepButton = document.getElementById("step")
resetButton = document.getElementById("reset")
currentStep = document.getElementById("currentStep").parentElement

currentStep.outerHTML = `<span id="currentStepText">Current Step: </span><span id="currentStep">0</span>`
console.log(currentStep.innerHTML)
currentStep = document.getElementById("currentStepText")

fpsText = document.getElementById("elements-topbar").firstElementChild.firstElementChild

StartButtonCallback = (mutationList, observer) => {
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

StartButtonObserver = new MutationObserver(StartButtonCallback);
StartButtonObserver.observe(startButton.firstElementChild, config);

function SwitchToHun() {
    document.getElementsByClassName("navbar-brand")[0].innerText = "Farkasok és bárányok"
    if (!controller.running)
        startButton.firstElementChild.innerText = "Indítás"
    else
        startButton.firstElementChild.innerText = "Megállítás"

    stepButton.firstElementChild.innerText = "Léptetés"
    resetButton.firstElementChild.innerText = "Visszaállítás"
    currentStep.innerText = "Jelenlegi lépés: "
    navbar.firstElementChild.firstElementChild.firstElementChild.innerText = "Leírás"
    fpsText.innerText = "Képkocka per másodperc"
    lang_flag.firstElementChild.src = "/local/custom/wolfsheep/pics/eng_flag.png"
    lang = "hu"
}

function SwitchToEng() {
    document.getElementsByClassName("navbar-brand")[0].innerText = "Wolves and Sheep"
    if (!controller.running)
        startButton.firstElementChild.innerText = "Start"
    else
        startButton.firstElementChild.innerText = "Stop"
    navbar.firstElementChild.firstElementChild.firstElementChild.innerText = "About"
    stepButton.firstElementChild.innerText = "Step"
    resetButton.firstElementChild.innerText = "Reset"
    currentStep.innerText = "Current Step: "
    fpsText.innerText = "Frames Per Second"
    lang_flag.firstElementChild.src = "/local/custom/wolfsheep/pics/hun_flag.png"
    lang = "en"
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
