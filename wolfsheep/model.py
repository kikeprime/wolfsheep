from mesa.datacollection import DataCollector
from mesa.model import Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid

import wolfsheep as ws


class WolfSheepModel(Model):
    def __init__(self, width, height, torus,
                 model_type, n_wolf, n_sheep,
                 wolf_energy_from_food, sheep_energy_from_food,
                 wolf_reproduction_rate, sheep_reproduction_rate, regrow_time):
        super().__init__()
        self.schedule = RandomActivation(self)
        self.grid = MultiGrid(width, height, torus)

        # model-version in the NetLogo code
        model_types = {
            "Extended model": 0,
            "Wolves, sheep and grass model": 1,
            "Wolves and sheep model": 2
        }
        self.model_type = model_types[model_type]

        self.n_wolf = n_wolf
        self.n_sheep = n_sheep

        # Adding wolves
        for wolf_id in range(self.n_wolf):
            wolf = ws.WolfAgent(self.next_id(), self, wolf_energy_from_food, wolf_reproduction_rate)
            if self.model_type == 0:
                wolf.gender = self.random.choice([True, False])
            else:
                wolf.gender = False
            self.schedule.add(wolf)
            x = self.random.randrange(width)
            y = self.random.randrange(height)
            self.grid.place_agent(wolf, (x, y))

        # Adding sheep
        for sheep_id in range(self.n_sheep):
            sheep = ws.SheepAgent(self.next_id(), self, sheep_energy_from_food, sheep_reproduction_rate)
            if self.model_type == 0:
                sheep.gender = self.random.choice([True, False])
            else:
                sheep.gender = True
            self.schedule.add(sheep)
            x = self.random.randrange(width)
            y = self.random.randrange(height)
            self.grid.place_agent(sheep, (x, y))

        # Adding grass
        for grass_id in range(width * height):
            if self.model_type == 2:
                grass = ws.GrassAgent(self.next_id(), self, True, 0)
            else:
                grown = self.random.choice([True, False])
                grass = ws.GrassAgent(self.next_id(), self, grown, regrow_time)
                if not grass.grown:
                    grass.countdown = self.random.randrange(regrow_time)
            self.schedule.add(grass)
            self.grid.place_agent(grass, (grass_id % width, grass_id // width))

        self.datacollector = DataCollector(
            model_reporters={
                "Number of wolves": wolf_counter,
                "Number of sheep": sheep_counter,
                "Number of female wolves": fwolf_counter,
                "Number of male wolves": mwolf_counter,
                "Number of female sheep": fsheep_counter,
                "Number of male sheep": msheep_counter,
                "Ratio of grass patches (%)": grass_counter
            }
        )
        self.datacollector.collect(self)

    def step(self):
        self.schedule.step()
        self.datacollector.collect(self)

    def place_child(self, child, pos):
        if child.race == 0:
            self.n_wolf += 1
        else:
            self.n_sheep += 1
        self.schedule.add(child)
        neighborhood = self.grid.get_neighborhood(pos, True, include_center=False, radius=1)
        self.grid.place_agent(child, self.random.choice(neighborhood))


# Agent counters
def agent_counter(model, race, by_gender, gender=False):
    result = 0
    for agent in model.schedule.agents:
        agent: ws.WolfAgent | ws.SheepAgent
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


def grass_counter(model):
    result = 0
    for agent in model.schedule.agents:
        agent: ws.GrassAgent
        if agent.race == 2 and agent.grown:
            result += 1
    return 100 * result / float(model.grid.width * model.grid.height)
