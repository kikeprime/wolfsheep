from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.UserParam import *

import wolfsheep as ws


def ws_model_portrayal(agent):
    if agent is None:
        return

    portrayal = {}
    if isinstance(agent, ws.WolfAgent):
        if agent.gender:
            portrayal["Shape"] = "pics/fwolf.png"
        else:
            portrayal["Shape"] = "pics/wolf.png"
        portrayal["scale"] = 1
        portrayal["Layer"] = 1
    if isinstance(agent, ws.SheepAgent):
        if agent.gender:
            portrayal["Shape"] = "pics/fsheep.png"
        else:
            portrayal["Shape"] = "pics/sheep.png"
        portrayal["scale"] = 1
        portrayal["Layer"] = 2
    if isinstance(agent, ws.GrassAgent):
        if agent.grown:
            portrayal["Color"] = ["green"]
        else:
            portrayal["Color"] = ["brown"]
        portrayal["Shape"] = "rect"
        portrayal["Filled"] = "true"
        portrayal["Layer"] = 0
        portrayal["w"] = 1
        portrayal["h"] = 1

    return portrayal


canvas_element = CanvasGrid(ws_model_portrayal, 30, 30, 500, 500)

model_params = {
    "width": 30,
    "height": 30,
    "torus": Checkbox("Torus", True),
    "model_type": Choice("Model type", 0, [0, 1, 2]),
    "n_wolf": Slider("Initial number of wolves", 50, 0, 100, 1),
    "n_sheep": Slider("Initial number of sheep", 100, 0, 100, 1),
    "wolf_energy_from_food": Slider("Energy gain from eating (wolves)", 20, 0, 100, 1),
    "sheep_energy_from_food": Slider("Energy gain from eating (sheep)", 4, 0, 100, 1),
    "wolf_reproduction_rate": Slider("Reproduction rate of the wolves (%)", 5, 0, 100),
    "sheep_reproduction_rate": Slider("Reproduction rate of the sheep (%)", 4, 0, 100),
    "regrow_time": Slider("Grass regrow time", 30, 0, 100)
}

server = ModularServer(ws.WolfSheepModel, [canvas_element], "Wolves and Sheep", model_params)
