from mesa.datacollection import DataCollector
from mesa.model import Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid

import rabbitgrassweed as ws


class RabbitGrassWeedModel(Model):
    """
    Class for the RabbitGrassWeed model.

    Parameters:
        width (int): Width of the grid
        height (int): Height of the grid
        torus (bool): Torus for grid
        model_type (str): Model type
        n_rabbit (int): Initial number of rabbits
        n_fox (int): Initial number of foxes
        rabbit_ep_gain_grass (int): Energy point gain for rabbits from grass
        rabbit_ep_gain_weed (int): Energy point gain for rabbits from weed
        fox_ep_gain (int): Energy point gain for foxes
        rabbit_max_init_ep (int): maximum initial energy point for rabbits
        fox_max_init_ep (int): maximum initial energy point for foxes
        rabbit_reproduction_threshold (int): Reproduction threshold for rabbits
        fox_reproduction_threshold (int): Reproduction threshold for foxes
        grass_regrow_rate (int): Probability of grass growth (%)
        weed_regrow_rate (int): Probability of weed growth (%)
        allow_flocking (bool): Allow flocking
        allow_hunt (bool): Allow hunt
        hunt_exponent (float): Limiter exponent for hunt
        allow_seed (bool): Allow seed usage
        random_seed (int): Random seed
    """
    def __init__(self, width: int, height: int, torus: bool,
                 model_type: str, n_rabbit: int, n_fox: int,
                 rabbit_ep_gain_grass: int, rabbit_ep_gain_weed: int, fox_ep_gain: int,
                 rabbit_max_init_ep: int, fox_max_init_ep: int,
                 rabbit_reproduction_threshold: int, fox_reproduction_threshold: int,
                 grass_regrow_rate: int, weed_regrow_rate: int,
                 allow_flocking: bool, allow_hunt: bool, hunt_exponent: float,
                 allow_seed: bool, random_seed: int):
        super().__init__()
        self.schedule = RandomActivation(model=self)
        self.grid = MultiGrid(width=width, height=height, torus=torus)

        # model-version in the NetLogo code
        model_types = {
            "Extended model": 0,
            "Rabbits, Grass and Weeds model": 1,
        }
        self.model_type = model_types[model_type]

        self.n_rabbit = n_rabbit
        self.n_fox = n_fox

        self.allow_hunt = allow_hunt
        self.allow_flocking = allow_flocking
        self.hunt_exponent = -abs(hunt_exponent)

        if allow_seed:
            self.random.seed(random_seed)

        # Adding rabbits
        for i in range(self.n_rabbit):
            rabbit = ws.RabbitAgent(unique_id=self.next_id(),
                                    model=self,
                                    ep_gain_grass=rabbit_ep_gain_grass,
                                    ep_gain_weed=rabbit_ep_gain_weed,
                                    max_init_ep=rabbit_max_init_ep,
                                    reproduction_threshold=rabbit_reproduction_threshold)
            if self.model_type == 0:
                rabbit.gender = self.random.choice([True, False])
            else:
                rabbit.gender = True
            self.schedule.add(rabbit)
            x = self.random.randrange(width)
            y = self.random.randrange(height)
            self.grid.place_agent(rabbit, (x, y))

        # Adding foxes
        for i in range(self.n_fox):
            fox = ws.FoxAgent(unique_id=self.next_id(),
                              model=self,
                              ep_gain=fox_ep_gain,
                              max_init_ep=fox_max_init_ep,
                              reproduction_threshold=fox_reproduction_threshold)
            if self.model_type == 0:
                fox.gender = self.random.choice([True, False])
            else:
                fox.gender = False
            self.schedule.add(agent=fox)
            x = self.random.randrange(width)
            y = self.random.randrange(height)
            self.grid.place_agent(agent=fox, pos=(x, y))

        # Adding grass and weeds
        for grass_id in range(width * height):
            grass = ws.GrassAgent(unique_id=self.next_id(), model=self,
                                  grass_regrow_rate=grass_regrow_rate / 100.0,
                                  weed_regrow_rate=weed_regrow_rate / 100.0)
            self.schedule.add(agent=grass)
            self.grid.place_agent(agent=grass, pos=(grass_id % width, grass_id // width))

        self.datacollector = DataCollector(
            model_reporters={
                "Number of rabbits": self.rabbit_counter,
                "Number of foxes": self.fox_counter,
                "Number of female rabbits": self.female_rabbit_counter,
                "Number of male rabbits": self.male_rabbit_counter,
                "Number of female foxes": self.female_fox_counter,
                "Number of male foxes": self.male_fox_counter,
                "Ratio of grass patches (%)": self.grass_counter,
                "Ratio of weed patches (%)": self.weed_counter
            }
        )
        self.datacollector.collect(self)

    def step(self):
        self.schedule.step()
        self.datacollector.collect(self)

    def place_child(self, child, pos):
        self.schedule.add(agent=child)
        neighborhood = self.grid.get_neighborhood(pos=pos, moore=True, include_center=False, radius=1)
        self.grid.place_agent(agent=child, pos=self.random.choice(neighborhood))

    # Agent counters
    @staticmethod
    def agent_counter(model, race: int, by_gender=False, gender=False) -> int:
        """
        Count number of rabbits and foxes.

        Parameters:
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
    def fox_counter(model) -> int:
        return model.agent_counter(model=model, race=0)

    @staticmethod
    def rabbit_counter(model) -> int:
        return model.agent_counter(model=model, race=1)

    @staticmethod
    def female_fox_counter(model) -> int:
        return model.agent_counter(model=model, race=0, by_gender=True, gender=True)

    @staticmethod
    def male_fox_counter(model) -> int:
        return model.agent_counter(model=model, race=0, by_gender=True, gender=False)

    @staticmethod
    def female_rabbit_counter(model) -> int:
        return model.agent_counter(model=model, race=1, by_gender=True, gender=True)

    @staticmethod
    def male_rabbit_counter(model) -> int:
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

    @staticmethod
    def weed_counter(model) -> float:
        """Return percentage of grown weed."""
        result = 0
        for agent in model.schedule.agents:
            agent: ws.GrassAgent
            if agent.race == 3 and agent.grown:
                result += 1
        return 100 * result / float(model.grid.width * model.grid.height)
