from mesa.agent import Agent

from wolfsheep import WolfSheepModel


class WolfSheepAgent(Agent):
    def __init__(self, unique_id: int, model: WolfSheepModel, energy_from_food: int, gender: bool = False):
        super().__init__(unique_id, model)

        self.energy_from_food = energy_from_food
        self.energy = self.model.random.randrange(2 * self.energy_from_food)
        # True: female
        # False: male
        self.gender = gender
        # The child classes set this
        # 0: Wolf
        # 1: Sheep
        # 2: Grass
        self.race = None

    def step(self):
        self.model: WolfSheepModel
        self.move()
        # Sheep don't eat and lose energy in the Wolves Sheep model
        if not (self.model.model_type == 2 and self.race == 1):
            self.energy -= 1
            self.eat()
            self.die()

    def move(self):
        self.model: WolfSheepModel
        cells_to_move = self.model.grid.get_neighborhood(
            pos=self.pos,
            moore=True,
            include_center=False,
            radius=4
        )
        dest_cell = self.model.random.choice(cells_to_move)
        self.model.grid.move_agent(self, dest_cell)

    def eat(self):
        pass  # self.energy += self.energy_from_food

    def reproduce(self):
        pass

    # death by having no energy
    def die(self):
        if self.energy < 0:
            self.destroy()

    def destroy(self):
        self.model: WolfSheepModel
        self.model.schedule.remove(self)
        self.model.grid.remove_agent(self)


class WolfAgent(WolfSheepAgent):
    def __init__(self, unique_id: int, model: WolfSheepModel, energy_from_food: int, gender: bool = False):
        super().__init__(unique_id, model, energy_from_food, gender)
        self.race = 0


class SheepAgent(WolfSheepAgent):
    def __init__(self, unique_id: int, model: WolfSheepModel, energy_from_food: int, gender: bool = False):
        super().__init__(unique_id, model, energy_from_food, gender)
        self.race = 1


class GrassAgent(Agent):
    def __init__(self, unique_id: int, model: WolfSheepModel, grown: bool, regrow_time: int):
        super().__init__(unique_id, model)
        self.race = 2
        self.grown = grown
        self.regrow_time = regrow_time
        self.countdown = regrow_time

    def step(self):
        if not self.grown:
            self.grow()

    def grow(self):
        self.countdown -= 1
        if self.countdown == 0:
            self.countdown = self.regrow_time
            self.grown = True
