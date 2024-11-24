"""
Simulation of RabbitGrassWeed without the server app.
"""

import matplotlib.pyplot as plt

from rabbitgrassweed import RabbitGrassWeedModel


def main():
    width = 30
    height = 30
    torus = True
    model_type = "Rabbits, grass and weeds model"
    n_fox = 50
    n_rabbit = 100
    rabbit_ep_gain_grass = 5
    rabbit_ep_gain_weed = 0
    fox_ep_gain = 5
    rabbit_max_init_ep = 10
    fox_max_init_ep = 10
    rabbit_reproduction_threshold = 15
    fox_reproduction_threshold = 15
    grass_regrow_rate = 30
    weed_regrow_rate = 0
    allow_hunt = True
    allow_flocking = True
    hunt_exponent = -0.5
    allow_seed = True
    seed = 474
    model = RabbitGrassWeedModel(width=width, height=height, torus=torus,
                                 model_type=model_type,
                                 n_rabbit=n_rabbit, n_fox=n_fox,
                                 rabbit_ep_gain_grass=rabbit_ep_gain_grass,
                                 rabbit_ep_gain_weed=rabbit_ep_gain_weed,
                                 fox_ep_gain=fox_ep_gain,
                                 rabbit_max_init_ep=rabbit_max_init_ep,
                                 fox_max_init_ep=fox_max_init_ep,
                                 rabbit_reproduction_threshold=rabbit_reproduction_threshold,
                                 fox_reproduction_threshold=fox_reproduction_threshold,
                                 grass_regrow_rate=grass_regrow_rate,
                                 weed_regrow_rate=weed_regrow_rate,
                                 allow_hunt=allow_hunt,
                                 allow_flocking=allow_flocking,
                                 hunt_exponent=hunt_exponent,
                                 allow_seed=allow_seed,
                                 random_seed=seed)
    t = 100
    for sim_t in range(t):
        model.step()

    model_data = model.datacollector.get_model_vars_dataframe()
    df = model.datacollector.get_model_vars_dataframe()
    df.index.name = "Step"
    df[df.columns[:2]].plot()
    plt.show()
    df[df.columns[-2:]].plot()
    plt.show()
    print(df)


main()
