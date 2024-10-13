from mesa.agent import Agent

from wolfsheep import WolfSheepModel


class WolfSheepAgent(Agent):
    def __init__(self, unique_id: int, model: WolfSheepModel, energy_from_food: int, reproduction_rate: float):
        super().__init__(unique_id, model)

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
        if self.model.random.random() < self.reproduction_rate:
            self.can_reproduce = True
            agent: WolfSheepAgent
            mates = [agent for agent in self.model.grid.get_cell_list_contents([self.pos])
                     if agent.race == self.race and agent.gender != self.gender and agent.can_reproduce]
            if self.model.model_type == 0:
                if len(mates) == 0 or self.gender is False:
                    return
            self.energy = self.energy // 2
            if self.race == 0:
                child = WolfAgent(self.model.n_wolf, self.model, self.energy_from_food, self.reproduction_rate)
                child.gender = False
            else:
                child = SheepAgent(self.model.n_sheep, self.model, self.energy_from_food, self.reproduction_rate)
                child.gender = True
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
        if self.countdown <= 0:
            self.grown = True
            self.countdown = self.regrow_time
        else:
            self.countdown -= 1
