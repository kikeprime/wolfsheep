from mesa.datacollection import DataCollector
from mesa.model import Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid

import wolfsheep.wolfsheep as ws


class WolfSheepModel(Model):
    def __init__(self, width, height, torus, n_wolf, n_sheep, wolf_energy: int, sheep_energy: int):
        super().__init__()
        self.schedule = RandomActivation(self)
        self.grid = MultiGrid(width, height, torus)

        # Adding wolves
        for wolf_id in range(n_wolf):
            gender = self.random.choice([True, False])
            wolf = ws.WolfAgent(wolf_id, self, wolf_energy, gender)
            self.schedule.add(wolf)
            x = self.random.randrange(0, width)
            y = self.random.randrange(0, height)
            self.grid.place_agent(wolf, (x, y))
        # Adding sheep
        for sheep_id in range(n_sheep):
            gender = self.random.choice([True, False])
            sheep = ws.SheepAgent(sheep_id, self, sheep_energy, gender)
            self.schedule.add(sheep)
            x = self.random.randrange(0, width)
            y = self.random.randrange(0, height)
            self.grid.place_agent(sheep, (x, y))

        self.datacollector = DataCollector()

    def step(self):
        self.schedule.step()
        self.datacollector.collect(self)
