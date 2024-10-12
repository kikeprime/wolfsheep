import matplotlib.pyplot as plt

from wolfsheep import WolfSheepModel


def main():
    width = 30
    height = 30
    torus = True
    model_type = 0
    n_wolf = 50
    n_sheep = 100
    wolf_energy_from_food = 20
    sheep_energy_from_food = 4
    regrow_time = 30
    model = WolfSheepModel(width, height, torus, model_type, n_wolf, n_sheep,
                           wolf_energy_from_food, sheep_energy_from_food, regrow_time)
    t = 1000
    for sim_t in range(t):
        model.step()

    model_data = model.datacollector.get_model_vars_dataframe()
    model_data.plot()
    plt.show()


if __name__ == "__main__":
    main()
