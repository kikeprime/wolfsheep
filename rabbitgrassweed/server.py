"""
This file is responsible for creating the server and its components.
"""

from mesa_viz_tornado.ModularVisualization import ModularServer
from mesa_viz_tornado.modules import CanvasGrid, ChartModule
from mesa_viz_tornado.UserParam import *
import tornado.web

import rabbitgrassweed as ws


# Accessing the files from root instead of from /local/custom
class RabbitGrassWeedServer(ModularServer):
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
        super().__init__(model_cls=model_cls,
                         visualization_elements=visualization_elements,
                         name=name,
                         model_params=model_params,
                         port=port)

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
    if isinstance(agent, ws.FoxAgent):
        if agent.gender:
            portrayal["Shape"] = "rabbitgrassweed/pics/ffox.png"
        else:
            portrayal["Shape"] = "rabbitgrassweed/pics/fox.png"
        portrayal["Layer"] = 1
        portrayal["Energy"] = agent.energy
    if isinstance(agent, ws.RabbitAgent):
        if agent.gender:
            portrayal["Shape"] = "rabbitgrassweed/pics/frabbit.png"
        else:
            portrayal["Shape"] = "rabbitgrassweed/pics/rabbit.png"
        portrayal["Layer"] = 1
        portrayal["Energy"] = agent.energy
    if isinstance(agent, ws.GrassAgent):
        if agent.grown:
            if agent.race == 2:
                portrayal["Color"] = ["green"]
            else:
                portrayal["Color"] = ["purple"]
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
    {"Label": "Number of rabbits", "Color": "blue"},
    {"Label": "Number of foxes", "Color": "black"},
    {"Label": "Number of female rabbits", "Color": "gray"},
    {"Label": "Number of male rabbits", "Color": "brown"},
    {"Label": "Number of female foxes", "Color": "orange"},
    {"Label": "Number of male foxes", "Color": "red"},
    {"Label": "Ratio of grass patches (%)", "Color": "green"},
    {"Label": "Ratio of weed patches (%)", "Color": "purple"}
]
chart_element = ChartModule(series=chart_list[:-2], data_collector_name="datacollector")
chart_element_grass = ChartModule(series=chart_list[-2:], data_collector_name="datacollector")

viz_elements = [canvas_element, chart_element, chart_element_grass]

model_types = ["Extended model", "Rabbits, grass and weeds model"]
params = {
    "width": 30,
    "height": 30,
    "torus": Checkbox(name="Torus", value=True, description="Whether the edges are connected or not."),
    "model_type": Choice(name="Model type", value=model_types[1], choices=model_types),
    "n_rabbit": Slider(name="Initial number of rabbits", value=150, min_value=0, max_value=200, step=1),
    "n_fox": Slider(name="Initial number of foxes", value=0, min_value=0, max_value=200, step=1),
    "rabbit_ep_gain_grass": Slider(name="EP gain from eating grass (rabbits)",
                                   value=5, min_value=0, max_value=100, step=1),
    "rabbit_ep_gain_weed": Slider(name="EP gain from eating weeds (rabbits)",
                                  value=0, min_value=0, max_value=100, step=1),
    "fox_ep_gain": Slider(name="EP gain from eating rabbits (foxes)",
                          value=5, min_value=0, max_value=100, step=1),
    "rabbit_max_init_ep": Slider(name="Rabbits' maximal initial EP",
                                 value=10, min_value=0, max_value=100, step=1),
    "fox_max_init_ep": Slider(name="Foxes' maximal initial EP",
                              value=10, min_value=0, max_value=100, step=1),
    "rabbit_reproduction_threshold": Slider("Rabbits' reproduction threshold (EP)",
                                            value=15, min_value=0, max_value=100, step=1),
    "fox_reproduction_threshold": Slider(name="Foxes' reproduction threshold (EP)",
                                         value=15, min_value=0, max_value=100, step=1),
    "grass_regrow_rate": Slider(name="Grass' regrow rate (%)", value=6, min_value=0, max_value=100, step=1),
    "weed_regrow_rate": Slider(name="Weeds' regrow rate (%)", value=0, min_value=0, max_value=100, step=1),
    "allow_hunt": Checkbox(name="Allow hunt", value=True, description="The foxes actively hunt."),
    "allow_flocking": Checkbox(name="Allow flocking", value=False, description="The rabbits will flock."),
    "hunt_exponent": NumberInput(name="Hunt limiter exponent", value=-0.5, description="Limiting the hunting"),
    "allow_seed": Checkbox(name="Allow Seed", value=True),
    # Cannot be named "seed" otherwise it cannot be turned off
    "random_seed": NumberInput(name="Random Seed", value=474, description="Seed for random number generator functions")
}

server = RabbitGrassWeedServer(model_cls=ws.RabbitGrassWeedModel,
                               visualization_elements=viz_elements,
                               name="Rabbits, Grass and Weeds",
                               model_params=params)
server.local_js_includes.add("custom/rabbitgrassweed/js/LangSwitch.js")
