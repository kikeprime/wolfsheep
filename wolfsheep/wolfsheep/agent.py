from mesa.agent import Agent

from wolfsheep.wolfsheep import WolfSheepModel


class _WolfSheepAgent(Agent):
    def __init__(self, unique_id: int, model: WolfSheepModel, energy: int, gender: bool = False):
        super().__init__(unique_id, model)

        # True: female
        # False: male
        self.gender = gender
        self.energy = energy

    def step(self):
        self.move()

    def move(self):
        pass


class WolfAgent(_WolfSheepAgent):
    def __init__(self, unique_id: int, model: WolfSheepModel, energy: int, gender: bool = False):
        super().__init__(unique_id, model, energy, gender)


class SheepAgent(_WolfSheepAgent):
    def __init__(self, unique_id: int, model: WolfSheepModel, energy: int, gender: bool = False):
        super().__init__(unique_id, model, energy, gender)
