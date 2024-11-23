from importlib.metadata import version
from mesa.agent import Agent

from rabbitgrassweed import RabbitGrassWeedModel

mesa_version = version("mesa")


class RabbitFoxAgent(Agent):
    """
    Agent class for the animal agents.

    Define shared methods, implement default movement and reproduction, handle steps.

    Parameters:
        unique_id (int): Unique identifier for instance agent (legacy support)
        model (RabbitGrassWeedModel): the RabbitGrassWeed model
        ep_gain (int): energy point gained from eating
        reproduction_rate (float): probability of reproduction
    """
    def __init__(self, unique_id: int, model: RabbitGrassWeedModel, ep_gain: int, reproduction_rate: float):
        if mesa_version == "2.4.0":
            super().__init__(unique_id=unique_id, model=model)
        elif mesa_version > "2.4.0":
            super().__init__(model=model)
        else:
            try:
                super().__init__(unique_id=unique_id, model=model)
            # Bare except because error type is unknown
            except:
                print("Incompatible mesa version.")

        self.ep_gain = ep_gain
        self.energy = self.model.random.randrange(2 * self.ep_gain)
        self.reproduction_rate = reproduction_rate / 100.0

        # True: female
        # False: male
        self.gender = None

        # The subclasses set this
        # 0: Wolf
        # 1: Sheep
        # 2: Grass
        self.race = None

        self.can_reproduce = False
        self.dead = False

    def step(self):
        self.model: RabbitGrassWeedModel
        self.move()
        # Sheep don't eat and lose energy in the Wolves and Sheep model
        if not (self.model.model_type == 2 and self.race == 1):
            self.energy -= 1
            self.eat()
            self.die()
        if not self.dead:
            self.reproduce()

    def move(self):
        """Default move method, no hunting and no flocking."""

        self.model: RabbitGrassWeedModel
        cells_to_move = self.model.grid.get_neighborhood(
            pos=self.pos,
            moore=True,
            include_center=False,
            radius=1
        )
        dest_cell = self.model.random.choice(cells_to_move)
        self.model.grid.move_agent(agent=self, pos=dest_cell)

    # The subclasses will define this
    def eat(self):
        pass

    def reproduce(self):
        """Reproduction.

        In my model there should be at least one of each gender who can reproduce and the females will give birth.
        """
        self.model: RabbitGrassWeedModel
        if self.model.model_type == 0:
            reproduction_rate = self.reproduction_rate ** 0.5
        else:
            reproduction_rate = self.reproduction_rate
        if self.model.random.random() < reproduction_rate:
            self.can_reproduce = True
            if self.model.model_type == 0:
                agent: RabbitFoxAgent
                mates = [agent for agent in self.model.grid.get_cell_list_contents([self.pos])
                         if agent.race == self.race and agent.gender != self.gender and agent.can_reproduce]
                if len(mates) == 0:
                    return
            self.energy = self.energy // 2
            if self.gender is False:
                return
            if self.race == 0:
                child = FoxAgent(unique_id=self.model.next_id(),
                                 model=self.model,
                                 ep_gain=self.ep_gain,
                                 reproduction_rate=self.reproduction_rate)
                child.gender = False
            else:
                child = RabbitAgent(unique_id=self.model.next_id(),
                                    model=self.model,
                                    ep_gain=self.ep_gain,
                                    reproduction_rate=self.reproduction_rate)
                child.gender = True
            child.reproduction_rate *= 100
            if self.model.model_type == 0:
                child.gender = self.random.choice([True, False])
            self.model.place_child(child=child, pos=self.pos)

    def die(self):
        """Death by starvation"""
        if self.energy < 0:
            self.destroy()

    def destroy(self):
        """Remove agents"""
        self.model: RabbitGrassWeedModel
        self.model.grid.remove_agent(agent=self)
        self.model.schedule.remove(agent=self)
        self.dead = True


class FoxAgent(RabbitFoxAgent):
    """
    Agent class for wolves.

    Implement eating sheep and active hunt.

    Parameters:
        unique_id (int): Unique identifier for this agent (legacy support)
        model (RabbitGrassWeedModel): the WolfSheep model
        ep_gain (int): energy point gained from eating
        reproduction_rate (float): probability of reproduction
    """
    def __init__(self, unique_id: int, model: RabbitGrassWeedModel, ep_gain: int, reproduction_rate: float):
        super().__init__(unique_id=unique_id, model=model, ep_gain=ep_gain, reproduction_rate=reproduction_rate)
        self.race = 0

    def eat(self):
        self.model: RabbitGrassWeedModel
        agent: RabbitAgent
        sheep = [agent for agent in self.model.grid.get_cell_list_contents([self.pos]) if agent.race == 1]
        if len(sheep) > 0:
            self.model.random.choice(sheep).energy = -1  # the safest method to kill them
            self.energy += self.ep_gain

    def move(self):
        """
        Implement active hunt.

        Hunting if the parameter is true.
        Choose a neighboring cell with sheep.
        """
        self.model: RabbitGrassWeedModel
        if self.allow_hunt():
            cells = self.model.grid.get_neighborhood(
                pos=self.pos,
                moore=True,
                include_center=False,
                radius=1
            )
            cells_to_move = []
            cell_contents = {cell: self.model.grid.get_cell_list_contents([cell]) for cell in cells}
            for cell in cell_contents.keys():
                if cell_contents[cell] is not None:
                    cell_contents[cell] = {type(agent) for agent in cell_contents[cell]}
                    if RabbitAgent in cell_contents[cell]:
                        cells_to_move.append(cell)
            if len(cells_to_move) > 0:
                dest_cell = self.model.random.choice(cells_to_move)
            else:
                dest_cell = self.model.random.choice(cells)
            self.model.grid.move_agent(self, dest_cell)
        else:
            super().move()

    def allow_hunt(self) -> bool:
        self.model: RabbitGrassWeedModel
        return (self.model.allow_hunt and self.energy > 0 and
                self.model.random.random() < (self.energy ** self.model.hunt_exponent))


class RabbitAgent(RabbitFoxAgent):
    """Agent class for sheep.

    Implement grazing and flocking.

    Parameters:
        unique_id (int): Unique identifier for this agent (legacy support)
        model (RabbitGrassWeedModel): the WolfSheep model
        ep_gain (int): energy point gained from eating
        reproduction_rate (float): probability of reproduction
    """
    def __init__(self, unique_id: int, model: RabbitGrassWeedModel, ep_gain: int, reproduction_rate: float):
        super().__init__(unique_id=unique_id, model=model, ep_gain=ep_gain, reproduction_rate=reproduction_rate)
        self.race = 1

    def eat(self):
        self.model: RabbitGrassWeedModel
        agent: GrassAgent
        for agent in self.model.grid.get_cell_list_contents([self.pos]):
            if agent.race == 2 and agent.grown:
                self.energy += self.ep_gain
                agent.grown = False
                
    def move(self):
        """Implement flocking."""
        self.model: RabbitGrassWeedModel
        if self.model.allow_flocking and self.energy > 0:  # if energy is too low focus on survival
            cells = self.model.grid.get_neighborhood(
                pos=self.pos,
                moore=True,
                include_center=False,
                radius=1
            )
            cells_to_move = []
            cell_contents = {cell: self.model.grid.get_cell_list_contents([cell]) for cell in cells}
            for cell in cell_contents.keys():
                if cell_contents[cell] is not None:
                    cell_contents[cell] = {type(agent) for agent in cell_contents[cell]}
                    if RabbitAgent in cell_contents[cell]:
                        # Include center to not make reproduction impossible
                        for neighbor in self.model.grid.get_neighborhood(pos=cell,
                                                                         moore=True,
                                                                         include_center=True,
                                                                         radius=5):
                            if neighbor in cells:
                                cells_to_move.append(cell)
            if len(cells_to_move) > 0:
                dest_cell = self.model.random.choice(cells_to_move)
            else:
                dest_cell = self.model.random.choice(cells)
            self.model.grid.move_agent(agent=self, pos=dest_cell)
        else:
            super().move()


class GrassAgent(Agent):
    """
    Agent class for grass.

    Parameters:
        unique_id (int): Unique identifier for this agent (legacy support)
        model (RabbitGrassWeedModel): the WolfSheep model
        grown (bool): grass state, True for grown grass, False for grazed cell
        regrow_time (int): Number of steps after grazed cell becomes grown grass again
    """
    def __init__(self, unique_id: int, model: RabbitGrassWeedModel, grown: bool, regrow_time: int):
        if mesa_version == "2.4.0":
            super().__init__(unique_id=unique_id, model=model)
        elif mesa_version > "2.4.0":
            super().__init__(model=model)
        else:
            try:
                super().__init__(unique_id=unique_id, model=model)
            # Same reason as for animals.
            except:
                print("Incompatible mesa version.")

        self.race = 2
        self.grown = grown
        self.regrow_time = regrow_time
        self.countdown = regrow_time

    def step(self):
        if not self.grown:
            self.grow()

    def grow(self):
        """Handle countdown and regrowing."""
        if self.countdown <= 0:
            self.grown = True
            self.countdown = self.regrow_time
        else:
            self.countdown -= 1
