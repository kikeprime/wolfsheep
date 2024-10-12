from mesa.datacollection import DataCollector
from mesa.model import Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid

import wolfsheep as ws


class WolfSheepModel(Model):
    def __init__(self, width, height, torus, model_type, n_wolf, n_sheep, wolf_energy, sheep_energy):
        super().__init__()
        self.schedule = RandomActivation(self)
        self.grid = MultiGrid(width, height, torus)

        # 0: My extended model
        # 1: Wolves, Sheep, Grass model
        # 2: Wolves, Sheep model
        self.model_type = model_type
        # Adding wolves
        for wolf_id in range(n_wolf):
            if model_type == 0:
                gender = self.random.choice([True, False])
            else:
                gender = False
            wolf = ws.WolfAgent(wolf_id, self, wolf_energy, gender)
            self.schedule.add(wolf)
            x = self.random.randrange(0, width)
            y = self.random.randrange(0, height)
            self.grid.place_agent(wolf, (x, y))
        # Adding sheep
        for sheep_id in range(n_sheep):
            if model_type == 0:
                gender = self.random.choice([True, False])
            else:
                gender = True
            sheep = ws.SheepAgent(sheep_id, self, sheep_energy, gender)
            self.schedule.add(sheep)
            x = self.random.randrange(0, width)
            y = self.random.randrange(0, height)
            self.grid.place_agent(sheep, (x, y))

        self.datacollector = DataCollector()

    def step(self):
        self.schedule.step()
        self.datacollector.collect(self)
