from mesa.datacollection import DataCollector
from mesa.model import Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid

import wolfsheep as ws


class WolfSheepModel(Model):
    def __init__(self, width, height, torus, model_type, n_wolf, n_sheep,
                 wolf_energy_from_food, sheep_energy_from_food, regrow_time):
        super().__init__()
        self.schedule = RandomActivation(self)
        self.grid = MultiGrid(width, height, torus)

        # model-version in the NetLogo code
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
            wolf = ws.WolfAgent(wolf_id, self, wolf_energy_from_food, gender)
            self.schedule.add(wolf)
            x = self.random.randrange(width)
            y = self.random.randrange(height)
            self.grid.place_agent(wolf, (x, y))

        # Adding sheep
        for sheep_id in range(n_sheep):
            if model_type == 0:
                gender = self.random.choice([True, False])
            else:
                gender = True
            sheep = ws.SheepAgent(sheep_id, self, sheep_energy_from_food, gender)
            self.schedule.add(sheep)
            x = self.random.randrange(width)
            y = self.random.randrange(height)
            self.grid.place_agent(sheep, (x, y))

        # Adding grass
        for grass_id in range(width * height):
            if model_type == 2:
                grass = ws.GrassAgent(grass_id, self, True, regrow_time)
                self.schedule.add(grass)
                if grass_id != 0:
                    self.grid.place_agent(grass, (grass_id % width, grass_id // width))
                else:
                    self.grid.place_agent(grass, (0, 0))
            else:
                grown = self.random.choice([True, False])
                grass = ws.GrassAgent(grass_id, self, grown, regrow_time)
                self.schedule.add(grass)
                if grass_id != 0:
                    self.grid.place_agent(grass, (grass_id % width, grass_id // width))
                else:
                    self.grid.place_agent(grass, (0, 0))

        self.datacollector = DataCollector(
            model_reporters={
                "Number of wolves": wolf_counter,
                "Number of sheep": sheep_counter,
                "Number of female wolves": fwolf_counter,
                "Number of male wolves": mwolf_counter,
                "Number of female sheep": fsheep_counter,
                "Number of male sheep": msheep_counter
            }
        )
        self.datacollector.collect(self)

    def step(self):
        self.schedule.step()
        self.datacollector.collect(self)


# Agent counters
def agent_counter(model, race, by_gender, gender=False):
    result = 0
    for agent in model.schedule.agents:
        agent: ws.WolfSheepAgent
        if agent.race == race:
            if by_gender and agent.gender == gender or not by_gender:
                result += 1
    return result


def wolf_counter(model):
    return agent_counter(model,0, False)


def sheep_counter(model):
    return agent_counter(model, 1, False)


def fwolf_counter(model):
    return agent_counter(model, 0, True, True)


def mwolf_counter(model):
    return agent_counter(model, 0, True, False)


def fsheep_counter(model):
    return agent_counter(model, 1, True, True)


def msheep_counter(model):
    return agent_counter(model, 1, True, False)
