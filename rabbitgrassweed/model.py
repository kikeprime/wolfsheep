from mesa.datacollection import DataCollector
from mesa.model import Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid

import rabbitgrassweed as ws


class RabbitGrassWeedModel(Model):
    """
    Class for the WolfSheep model.

    Parameters:
        width (int): Width of the grid
        height (int): Height of the grid
        torus (bool): Torus for grid
        model_type: Type of the model (see below)
        n_fox (int): Initial number of wolves
        n_rabbit (int): Initial number of sheep
        rabbit_ep_gain_grass (int): Energy point gain for rabbits from grass
        rabbit_ep_gain_weed (int): Energy point gain for rabbits from weed
        fox_ep_gain (int): Energy point gain for foxes
        rabbit_reproduction_threshold (float): Reproduction threshold for rabbits
        fox_reproduction_threshold (float): Reproduction threshold for foxes
        regrow_time (int): Regrow step count for grass agents
        allow_hunt (bool): Allow hunting
        allow_flocking (bool): Allow flocking
        hunt_exponent (float): Limiter exponent for hunt
        allow_seed (bool): Allow seed usage
        seed (int): Random seed

    """
    def __init__(self, width: int, height: int, torus: bool,
                 model_type: int, n_rabbit: int, n_fox: int,
                 fox_ep_gain: int, rabbit_ep_gain_grass: int, rabbit_ep_gain_weed: int,
                 rabbit_reproduction_threshold: float, fox_reproduction_threshold: float, regrow_time: int,
                 allow_hunt: bool, allow_flocking: bool, hunt_exponent: float,
                 allow_seed: bool, seed: int):
        super().__init__()
        self.schedule = RandomActivation(model=self)
        self.grid = MultiGrid(width=width, height=height, torus=torus)

        # model-version in the NetLogo code
        model_types = {
            "Extended model": 0,
            "Wolves, sheep and grass model": 1,
            "Wolves and sheep model": 2
        }
        self.model_type = model_types[model_type]

        self.n_rabbit = n_rabbit
        self.n_fox = n_fox

        self.allow_hunt = allow_hunt
        self.allow_flocking = allow_flocking
        self.hunt_exponent = -abs(hunt_exponent)

        if allow_seed:
            self.random.seed(seed)

        # Adding wolves
        for wolf_id in range(self.n_fox):
            wolf = ws.FoxAgent(unique_id=self.next_id(),
                               model=self,
                               ep_gain=fox_ep_gain,
                               reproduction_rate=fox_reproduction_threshold)
            if self.model_type == 0:
                wolf.gender = self.random.choice([True, False])
            else:
                wolf.gender = False
            self.schedule.add(agent=wolf)
            x = self.random.randrange(width)
            y = self.random.randrange(height)
            self.grid.place_agent(agent=wolf, pos=(x, y))

        # Adding sheep
        for sheep_id in range(self.n_rabbit):
            sheep = ws.RabbitAgent(unique_id=self.next_id(),
                                   model=self,
                                   ep_gain=rabbit_ep_gain_grass,
                                   reproduction_rate=rabbit_reproduction_threshold)
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
                grass = ws.GrassAgent(unique_id=self.next_id(), model=self, grown=grown, regrow_time=regrow_time)
                if not grass.grown:
                    grass.countdown = self.random.randrange(regrow_time)
            self.schedule.add(agent=grass)
            self.grid.place_agent(agent=grass, pos=(grass_id % width, grass_id // width))

        self.datacollector = DataCollector(
            model_reporters={
                "Number of wolves": self.wolf_counter,
                "Number of sheep": self.sheep_counter,
                "Number of female wolves": self.female_wolf_counter,
                "Number of male wolves": self.male_wolf_counter,
                "Number of female sheep": self.female_sheep_counter,
                "Number of male sheep": self.male_sheep_counter,
                "Ratio of grass patches (%)": self.grass_counter
            }
        )
        self.datacollector.collect(self)

    def step(self):
        self.schedule.step()
        self.datacollector.collect(self)

    def place_child(self, child, pos):
        self.schedule.add(agent=child)
        neighborhood = self.grid.get_neighborhood(pos=pos, moore=True, include_center=False, radius=1)
        self.grid.place_agent(child=child, pos=self.random.choice(neighborhood))

    # Agent counters
    @staticmethod
    def agent_counter(model, race: int, by_gender=False, gender=False) -> int:
        """
        Count number of wolves and sheep.

        Attributes:
            model (RabbitGrassWeedModel): model instance
            race (int): agent race
            by_gender (bool): whether to count specific gender (optional)
            gender (bool): specify gender (optional)
        """
        result = 0
        for agent in model.schedule.agents:
            agent: ws.FoxAgent | ws.RabbitAgent
            if agent.race == race:
                if by_gender and agent.gender == gender or not by_gender:
                    result += 1
        return result

    @staticmethod
    def wolf_counter(model) -> int:
        return model.agent_counter(model=model, race=0)

    @staticmethod
    def sheep_counter(model) -> int:
        return model.agent_counter(model=model, race=1)

    @staticmethod
    def female_wolf_counter(model) -> int:
        return model.agent_counter(model=model, race=0, by_gender=True, gender=True)

    @staticmethod
    def male_wolf_counter(model) -> int:
        return model.agent_counter(model=model, race=0, by_gender=True, gender=False)

    @staticmethod
    def female_sheep_counter(model) -> int:
        return model.agent_counter(model=model, race=1, by_gender=True, gender=True)

    @staticmethod
    def male_sheep_counter(model) -> int:
        return model.agent_counter(model=model, race=1, by_gender=True, gender=False)

    @staticmethod
    def grass_counter(model) -> float:
        """Return percentage of grown grass."""
        result = 0
        for agent in model.schedule.agents:
            agent: ws.GrassAgent
            if agent.race == 2 and agent.grown:
                result += 1
        return 100 * result / float(model.grid.width * model.grid.height)
