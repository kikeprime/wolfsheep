from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid

import wolfsheep as ws


def ws_model_portrayal(agent):
    if agent is None:
        return

    portrayal = {}
    if isinstance(agent, ws.WolfAgent):
        portrayal["Shape"] = None
        portrayal["scale"] = 1
        portrayal["Layer"] = 1
    if isinstance(agent, ws.SheepAgent):
        portrayal["Shape"] = None
        portrayal["scale"] = 1
        portrayal["Layer"] = 1


canvas_element = CanvasGrid(ws_model_portrayal, 15, 15, 500, 500)

model_params = {
    "width": 15,
    "height": 15,
    "torus": True,
    "n_wolf": 50,
    "n_sheep": 100,
    "wolf_energy": 20,
    "sheep_energy": 20
}

server = ModularServer(ws.WolfSheepModel, [canvas_element], "Wolves and Sheep", model_params)
