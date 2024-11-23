import matplotlib.pyplot as plt

from rabbitgrassweed import RabbitGrassWeedModel


def main():
    width = 30
    height = 30
    torus = True
    model_type = 0
    n_wolf = 50
    n_sheep = 100
    wolf_ep_gain = 20
    sheep_ep_gain = 4
    wolf_reproduction_rate = 0.05
    sheep_reproduction_rate = 0.04
    regrow_time = 30
    allow_hunt = True
    allow_flocking = True
    hunt_exponent = -0.5
    allow_seed = True
    seed = 474
    model = RabbitGrassWeedModel(width=width, height=height, torus=torus,
                                 model_type=model_type, n_fox=n_wolf, n_rabbit=n_sheep,
                                 fox_ep_gain=wolf_ep_gain, rabbit_ep_gain_grass=sheep_ep_gain,
                                 fox_reproduction_threshold=wolf_reproduction_rate,
                                 rabbit_reproduction_threshold=sheep_reproduction_rate,
                                 grass_regrow_rate=regrow_time,
                                 allow_hunt=allow_hunt,
                                 allow_flocking=allow_flocking,
                                 hunt_exponent=hunt_exponent,
                                 allow_seed=allow_seed,
                                 seed=seed)
    t = 200
    for sim_t in range(t):
        model.step()

    model_data = model.datacollector.get_model_vars_dataframe()
    model_data.plot()
    plt.show()
    print(model_data[["Number of wolves", "Number of sheep", "Number of female wolves", "Number of male sheep"]])
