from mesa.visualization.ModularVisualization import ModularServer
import wolfsheep.wolfsheep as ws


model_params = {}
server = ModularServer(ws.WolfSheepModel, None, "Wolves and Sheep", model_params)
