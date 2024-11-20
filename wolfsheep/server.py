from mesa_viz_tornado.ModularVisualization import ModularServer
from mesa_viz_tornado.modules import CanvasGrid, ChartModule
from mesa_viz_tornado.UserParam import *
import tornado.web

import wolfsheep as ws


# Accessing the files from root instead of from /local/custom
class WolfSheepServer(ModularServer):
    def __init__(
        self,
        model_cls,
        visualization_elements,
        name="Mesa Model",
        model_params=None,
        port=None,
    ):
        super().__init__(
            model_cls,
            visualization_elements,
            name,
            model_params,
            port,
        )

        self.handlers.append((r"/(.*)", tornado.web.StaticFileHandler, {"path": ""}))

        super(ModularServer, self).__init__(self.handlers, **self.settings)


def ws_model_portrayal(agent):
    if agent is None:
        return

    portrayal = {}
    if isinstance(agent, ws.WolfAgent):
        if agent.gender:
            portrayal["Shape"] = "wolfsheep/pics/fwolf.png"
        else:
            portrayal["Shape"] = "wolfsheep/pics/wolf.png"
        portrayal["Layer"] = 1
        portrayal["Energy"] = agent.energy
    if isinstance(agent, ws.SheepAgent):
        if agent.gender:
            portrayal["Shape"] = "wolfsheep/pics/fsheep.png"
        else:
            portrayal["Shape"] = "wolfsheep/pics/sheep.png"
        portrayal["Layer"] = 1
        portrayal["Energy"] = agent.energy
    if isinstance(agent, ws.GrassAgent):
        if agent.grown:
            portrayal["Color"] = ["green"]
        else:
            portrayal["Color"] = ["#663300"]
        portrayal["Shape"] = "rect"
        portrayal["Filled"] = "true"
        portrayal["Layer"] = 0
        portrayal["w"] = 1
        portrayal["h"] = 1

    return portrayal


canvas_element = CanvasGrid(ws_model_portrayal, 30, 30, 600, 600)

chart_list = [
    {"Label": "Number of wolves", "Color": "red"},
    {"Label": "Number of sheep", "Color": "blue"},
    {"Label": "Number of female wolves", "Color": "orange"},
    {"Label": "Number of male wolves", "Color": "grey"},
    {"Label": "Number of female sheep", "Color": "white"},
    {"Label": "Number of male sheep", "Color": "black"},
    {"Label": "Ratio of grass patches (%)", "Color": "green"}
]
chart_element = ChartModule(chart_list[:-1], data_collector_name="datacollector")
chart_element_grass = ChartModule([chart_list[-1]], data_collector_name="datacollector")

viz_elements = [canvas_element, chart_element, chart_element_grass]

model_types = ["Extended model", "Wolves, sheep and grass model", "Wolves and sheep model"]
params = {
    "width": 30,
    "height": 30,
    "torus": Checkbox("Torus", True, "Whether the edges are connected or not."),
    "model_type": Choice("Model type", model_types[0], model_types, ""),
    "n_wolf": Slider("Initial number of wolves", 50, 0, 100, 1, ""),
    "n_sheep": Slider("Initial number of sheep", 100, 0, 100, 1, ""),
    "wolf_energy_from_food": Slider("Energy gain from eating (wolves)",
                                    20, 0, 100, 1, ""),
    "sheep_energy_from_food": Slider("Energy gain from eating (sheep)",
                                     4, 0, 100, 1, ""),
    "wolf_reproduction_rate": Slider("Reproduction rate of the wolves (%)",
                                     5, 0, 100, 1, ""),
    "sheep_reproduction_rate": Slider("Reproduction rate of the sheep (%)",
                                      4, 0, 100, 1, ""),
    "regrow_time": Slider("Grass regrow time", 30, 0, 100, 1, ""),
    "allow_hunting": Checkbox("Allow hunting", True, "The wolves actively hunt."),
    "allow_flocking": Checkbox("Allow flocking", True, "The sheep will flock."),
    "hunting_exponent": NumberInput("Hunt limiter exponent", -0.5, "Limiting the hunting"),
    "allow_seed": Checkbox("Allow Seed", True, ""),
    "seed": NumberInput("Random Seed", 474, "Seed for random number generators")
}

server = WolfSheepServer(ws.WolfSheepModel, viz_elements, "Wolves and Sheep", params)
server.local_js_includes.add("custom/wolfsheep/js/LangSwitch.js")
