from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid

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
        portrayal["Layer"] = 0
    if isinstance(agent, ws.SheepAgent):
        if agent.gender:
            portrayal["Shape"] = "pics/fsheep.png"
        else:
            portrayal["Shape"] = "pics/sheep.png"
        portrayal["scale"] = 1
        portrayal["Layer"] = 1
    return portrayal


canvas_element = CanvasGrid(ws_model_portrayal, 30, 30, 500, 500)

model_params = {
    "width": 30,
    "height": 30,
    "torus": True,
    "n_wolf": 50,
    "n_sheep": 100,
    "wolf_energy": 20,
    "sheep_energy": 20
}

server = ModularServer(ws.WolfSheepModel, [canvas_element], "Wolves and Sheep", model_params)
