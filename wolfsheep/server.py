from mesa_viz_tornado.ModularVisualization import ModularServer
from mesa_viz_tornado.modules import CanvasGrid, ChartModule
from mesa_viz_tornado.UserParam import *
import tornado.web

import wolfsheep as ws


# Accessing the files from root instead of from /local/custom
class WolfSheepServer(ModularServer):
    """
    Attach the module's folder to the web server's root then reinitialize the server.
    """

    def __init__(self,
                 model_cls,
                 visualization_elements,
                 name="Mesa Model",
                 model_params=None,
                 port=None):
        """Override ModularServer.__init__"""
        # call ModularServer.__init__
        super().__init__(
            model_cls=model_cls,
            visualization_elements=visualization_elements,
            name=name,
            model_params=model_params,
            port=port,
        )

        # Attach the module's folder to the web server's root
        self.handlers.append((r"/(.*)", tornado.web.StaticFileHandler, {"path": ""}))

        # Reinitialize server by calling tornado.web.Application.__init__
        # Taken from the end of ModularServer.__init__
        super(ModularServer, self).__init__(self.handlers, **self.settings)


def ws_model_portrayal(agent):
    """
    Handle agent portrayals, including icons by gender.
    Return the agent portrayal dictionary.
    """

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


canvas_element = CanvasGrid(portrayal_method=ws_model_portrayal,
                            grid_width=30, grid_height=30,
                            canvas_width=600, canvas_height=600)

chart_list = [
    {"Label": "Number of wolves", "Color": "red"},
    {"Label": "Number of sheep", "Color": "blue"},
    {"Label": "Number of female wolves", "Color": "orange"},
    {"Label": "Number of male wolves", "Color": "grey"},
    {"Label": "Number of female sheep", "Color": "white"},
    {"Label": "Number of male sheep", "Color": "black"},
    {"Label": "Ratio of grass patches (%)", "Color": "green"}
]
chart_element = ChartModule(series=chart_list[:-1], data_collector_name="datacollector")
chart_element_grass = ChartModule(series=[chart_list[-1]], data_collector_name="datacollector")

viz_elements = [canvas_element, chart_element, chart_element_grass]

model_types = ["Extended model", "Wolves, sheep and grass model", "Wolves and sheep model"]
params = {
    "width": 30,
    "height": 30,
    "torus": Checkbox(name="Torus", value=True, description="Whether the edges are connected or not."),
    "model_type": Choice(name="Model type", value=model_types[0], choices=model_types),
    "n_wolf": Slider(name="Initial number of wolves", value=50, min_value=0, max_value=100, step=1),
    "n_sheep": Slider(name="Initial number of sheep", value=100, min_value=0, max_value=100, step=1),
    "wolf_ep_gain": Slider(name="Energy gain from eating (wolves)",
                           value=20, min_value=0, max_value=100, step=1),
    "sheep_ep_gain": Slider(name="Energy gain from eating (sheep)",
                            value=4, min_value=0, max_value=100, step=1),
    "wolf_reproduction_rate": Slider(name="Reproduction rate of the wolves (%)",
                                     value=5, min_value=0, max_value=100, step=1),
    "sheep_reproduction_rate": Slider(name="Reproduction rate of the sheep (%)",
                                      value=4, min_value=0, max_value=100, step=1),
    "regrow_time": Slider(name="Grass regrow time", value=30, min_value=0, max_value=100, step=1),
    "allow_hunt": Checkbox(name="Allow hunting", value=True, description="The wolves actively hunt."),
    "allow_flocking": Checkbox(name="Allow flocking", value=True, description="The sheep will flock."),
    "hunt_exponent": NumberInput(name="Hunt limiter exponent", value=-0.5, description="Limiting the hunting"),
    "allow_seed": Checkbox(name="Allow Seed", value=True),
    "seed": NumberInput(name="Random Seed", value=474, description="Seed for random number generators")
}

server = WolfSheepServer(model_cls=ws.WolfSheepModel,
                         visualization_elements=viz_elements,
                         name="Wolves and Sheep",
                         model_params=params)
server.local_js_includes.add("custom/wolfsheep/js/LangSwitch.js")
