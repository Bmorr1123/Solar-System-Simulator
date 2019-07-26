mass_scale = .5e-28
dist_scale = mass_scale**(1/3)
force_scale = 10**9

print("Mass_scale = " + str(mass_scale))
print("Dist_scale = " + str(dist_scale))

# Body Masses

sun_mass = 1.9891e30
earth_mass = 5.972e24

sun = "sun"
mercury = "mercury"
venus = "venus"
earth = "earth"
moon = "moon"
mars = "mars"
jupiter = "jupiter"
saturn = "saturn"
uranus = "uranus"
neptune = "neptune"
pluto = "pluto"

planets = [mercury, venus, earth, mars, jupiter, saturn, uranus, neptune, pluto]

mass = "mass"
distance = "dist"
diameter = "diameter"

key = {
    "mass": 0,
    "dist": 1,
    "diameter": 2
}

data = {
    "scale":   [10**24,  10**6,  1],
    "sun":     [1989100, 0,      1392530],
    "mercury": [0.330,   57.9,   4879],
    "venus":   [4.87,    108.2,  12104],
    "earth":   [5.97,    149.6,  12756],
    "moon":    [0.073,   0.384,  3475],
    "mars":    [0.642,   227.9,  6792],
    "jupiter": [1898,    778.6,  142984],
    "saturn":  [568,     1433.5, 120536],
    "uranus":  [86.8,    2872.5, 51118],
    "neptune": [102,     4495.1, 49528],
    "pluto":   [0.0146,  5906.4, 2370]
}

colors = {
    "sun": (255, 255, 0),
    "mercury": (100, 0, 180),
    "venus":   (175, 0, 0),
    "earth":   (0, 0, 255),
    "mars":    (255, 0, 0),
    "jupiter":    (255, 255 // 2, 0),
    "saturn": (186, 129, 80),
    "uranus":  (0, 255 // 2, 255),
    "neptune":  (0, 0, 255),
    "pluto": (255, 255, 225)
}


def get_info(body, type):
    return data[body][key[type]] * data["scale"][key[type]]


def get_mass_ratio(body):
    return data[body][0] / data["sun"][0]


def get_distance_ratio(body):
    return data[body][1] / data["earth"][1]


def get_radius_ratio(body):
    return data[body][2] / data["earth"][2]


# mass_scale = 10**24

# Body Distances from the Sun

sun_dist = 0
earth_dist = 5.972e24
