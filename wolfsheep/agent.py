from importlib.metadata import version
from mesa.agent import Agent

from wolfsheep import WolfSheepModel

mesa_version = version("mesa")


class WolfSheepAgent(Agent):
    def __init__(self, unique_id: int, model: WolfSheepModel, energy_from_food: int, reproduction_rate: float):
        if mesa_version == "2.4.0":
            super().__init__(unique_id, model)
        elif mesa_version > "2.4.0":
            super().__init__(model)
        else:
            try:
                super().__init__(unique_id, model)
            # I must use bare except because if there are any issues, then the entire model should stop
            except:
                print("Incompatible mesa version.")

        self.energy_from_food = energy_from_food
        self.energy = self.model.random.randrange(2 * self.energy_from_food)
        self.reproduction_rate = reproduction_rate / 100.0

        # True: female
        # False: male
        self.gender = None

        # the subclasses set this
        # 0: Wolf
        # 1: Sheep
        # 2: Grass
        self.race = None

        self.can_reproduce = False
        self.dead = False

    def step(self):
        self.model: WolfSheepModel
        self.move()
        # Sheep don't eat and lose energy in the Wolves Sheep model
        if not (self.model.model_type == 2 and self.race == 1):
            self.energy -= 1
            self.eat()
            self.die()
        if not self.dead:
            self.reproduce()

    # Default move method, no hunting and no flocking
    def move(self):
        self.model: WolfSheepModel
        cells_to_move = self.model.grid.get_neighborhood(
            pos=self.pos,
            moore=True,
            include_center=False,
            radius=1
        )
        dest_cell = self.model.random.choice(cells_to_move)
        self.model.grid.move_agent(self, dest_cell)

    # the subclasses will define this
    def eat(self):
        pass

    # In my model there should be at least one of each gender who can reproduce and the females will give birth
    def reproduce(self):
        self.model: WolfSheepModel
        if self.model.model_type == 0:
            reproduction_rate = self.reproduction_rate ** 0.5
        else:
            reproduction_rate = self.reproduction_rate
        if self.model.random.random() < reproduction_rate:
            self.can_reproduce = True
            if self.model.model_type == 0:
                agent: WolfSheepAgent
                mates = [agent for agent in self.model.grid.get_cell_list_contents([self.pos])
                         if agent.race == self.race and agent.gender != self.gender and agent.can_reproduce]
                if len(mates) == 0:
                    return
            self.energy = self.energy // 2
            if self.gender is False:
                return
            if self.race == 0:
                child = WolfAgent(self.model.next_id(), self.model, self.energy_from_food, self.reproduction_rate)
                child.gender = False
            else:
                child = SheepAgent(self.model.next_id(), self.model, self.energy_from_food, self.reproduction_rate)
                child.gender = True
            child.reproduction_rate *= 100
            if self.model.model_type == 0:
                child.gender = self.random.choice([True, False])
            self.model.place_child(child, self.pos)

    # death by starvation
    def die(self):
        if self.energy < 0:
            self.destroy()

    def destroy(self):
        self.model: WolfSheepModel
        self.model.grid.remove_agent(self)
        self.model.schedule.remove(self)
        self.dead = True


class WolfAgent(WolfSheepAgent):
    def __init__(self, unique_id, model, energy_from_food, reproduction_rate):
        super().__init__(unique_id, model, energy_from_food, reproduction_rate)
        self.race = 0

    def eat(self):
        self.model: WolfSheepModel
        agent: SheepAgent
        sheep = [agent for agent in self.model.grid.get_cell_list_contents([self.pos]) if agent.race == 1]
        if len(sheep) > 0:
            self.model.random.choice(sheep).energy = -1  # the safest method to kill them
            self.energy += self.energy_from_food

    # Hunting if the parameter is true
    # Choose a neighboring cell with sheep
    def move(self):
        self.model: WolfSheepModel
        if self.allow_hunting():
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
                    if SheepAgent in cell_contents[cell]:
                        cells_to_move.append(cell)
            if len(cells_to_move) > 0:
                dest_cell = self.model.random.choice(cells_to_move)
            else:
                dest_cell = self.model.random.choice(cells)
            self.model.grid.move_agent(self, dest_cell)
        else:
            super().move()

    def allow_hunting(self) -> bool:
        self.model: WolfSheepModel
        return (self.model.allow_hunting and self.energy > 0 and
                self.model.random.random() < (self.energy ** self.model.hunting_exponent))


class SheepAgent(WolfSheepAgent):
    def __init__(self, unique_id, model, energy_from_food, reproduction_rate):
        super().__init__(unique_id, model, energy_from_food, reproduction_rate)
        self.race = 1

    def eat(self):
        self.model: WolfSheepModel
        agent: GrassAgent
        for agent in self.model.grid.get_cell_list_contents([self.pos]):
            if agent.race == 2 and agent.grown:
                self.energy += self.energy_from_food
                agent.grown = False
                
    def move(self):
        self.model: WolfSheepModel
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
                    if SheepAgent in cell_contents[cell]:
                        # Include center to not make reproduction impossible
                        for neighbor in self.model.grid.get_neighborhood(cell, True, True, 5):
                            if neighbor in cells:
                                cells_to_move.append(cell)
            if len(cells_to_move) > 0:
                dest_cell = self.model.random.choice(cells_to_move)
            else:
                dest_cell = self.model.random.choice(cells)
            self.model.grid.move_agent(self, dest_cell)
        else:
            super().move()


class GrassAgent(Agent):
    def __init__(self, unique_id: int, model: WolfSheepModel, grown: bool, regrow_time: int):
        if mesa_version == "2.4.0":
            super().__init__(unique_id, model)
        elif mesa_version > "2.4.0":
            super().__init__(model)
        else:
            try:
                super().__init__(unique_id, model)
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
        if self.countdown <= 0:
            self.grown = True
            self.countdown = self.regrow_time
        else:
            self.countdown -= 1
