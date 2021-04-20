import random
import numpy as np
import bruges as bg
from PIL import Image


def contains_all_nums(strata, max_layers):
    """Checks if each layer is represented in the strata."""
    for i in range(0, max_layers):
        if i not in strata:
            return False
    return True


def calc_split_points(strata):
    """Calculate random points at which to split the data."""
    split_points = np.array([random.random() for _ in range(2)])
    split_points *= random.randint(8, len(strata) - 2)/np.amax(split_points)

    split_points = np.round(split_points)
    split_points = np.sort(split_points)
    return split_points


def make_random_wedges():
    """Create random data based on the bruges library."""
    depth = (random.randint(600,1200), random.randint(800, 2000), random.randint(400,1200))
    width = (random.randint(600,1200), random.randint(800, 2000), random.randint(400,1200))

    mode = random.choice(['linear', 'clinoform'])
    max_layers = random.randint(4, 10)

    strata = [random.randint(0, max_layers) for j in range(5, 20)]
    while not contains_all_nums(strata, max_layers):
        strata = [random.randint(0, max_layers) for j in range(5, 20)]

    threshold = random.randint(2, max(len(strata)//4,2))
    split_points = calc_split_points(strata).astype('int8')
    while split_points[1] - split_points[0] < threshold:
        split_points = calc_split_points(strata).astype('int8')

    upper_strata = tuple(strata[:split_points[0]])
    middle_strata = tuple(strata[split_points[0]:split_points[1]])
    lower_strata = tuple(strata[split_points[1]:])
    starting_thickness = random.uniform(0, 2)
    thickness=(starting_thickness, starting_thickness + random.uniform(0,2))
    wedges, _, _, _ = bg.models.wedge(depth=depth,
                                    width=width,
                                    strat=tuple([upper_strata, middle_strata, lower_strata]),
                                    mode=mode,
                                    thickness=thickness,
                                   )
    return wedges

# Number of samples to create
NUM_SAMPLES = 100
for j in range(NUM_SAMPLES):
    IS_DONE = False
    while not IS_DONE:
        try:
            w = make_random_wedges()
            rocks = np.array([j+1 for j in np.unique(w)])
            # Fancy indexing into the rocks with the model.
            impedance = rocks[w-1]
            # Make reflectivity.
            rc = (impedance[1:] - impedance[:-1]) / (impedance[1:] + impedance[:-1])
            rc -= np.amin(rc)
            rc *= 255/(np.amax(rc)-np.amin(rc))

            impedance -= np.amin(impedance)
            impedance = impedance.astype('float64')
            impedance *= 255/(np.amax(impedance) - np.amin(impedance))
            impedance = np.round(impedance).astype('int8')
            # Saving both impedance and reflectivity. Can switch between images
            # in the training data for different effects
            Image.fromarray(rc).convert("RGB").convert("L").save("images/reflectivity_{}.\
                png".format(j+1))
            Image.fromarray(impedance).convert("RGB").convert("L").save("images/impedance_{}.\
                png".format(j+1))

            with open('data/reflectivity_{}.npy'.format(j+1), 'wb') as gen_file:
                np.save(gen_file, rc)
            with open('data/impedance_{}.npy'.format(j+1), 'wb') as gen_file:
                np.save(gen_file, impedance)
            IS_DONE=True
        # Ignore random errors and generate a new one instead
        except:
            pass
