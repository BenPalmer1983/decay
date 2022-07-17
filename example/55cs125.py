import sys
sys.path.append("../src")

from decay import decay


# Set path to isotopes dictionary
decay.set("../data/isotopes.pz")

# Create isotope chain dictionary
idata = {}

# Set parent isotope
parent = 55125

# Set time at which to calculate activity
time = 86400

# Fill in production rate and starting amount of isotopes
idata[55125] = {'w': 0.0, 'n0': 0.0}
idata[54125] = {'w': 0.0, 'n0': 0.0}
idata[53125] = {'w': 0.0, 'n0': 0.0}
idata[52125] = {'w': 0.0, 'n0': 0.0}

# Run calculation and save results in file
decay.calculate(parent, time, idata, "results/55cs125_01.txt")



# Fill in production rate and starting amount of isotopes
idata[55125] = {'w': 100.0, 'n0': 0.0}
idata[54125] = {'w': 0.0, 'n0': 0.0}
idata[53125] = {'w': 0.0, 'n0': 0.0}
idata[52125] = {'w': 0.0, 'n0': 0.0}

# Run calculation and save results in file
decay.calculate(parent, time, idata, "results/55cs125_02.txt")



# Fill in production rate and starting amount of isotopes
idata[55125] = {'w': 0.0, 'n0': 100.0}
idata[54125] = {'w': 0.0, 'n0': 0.0}
idata[53125] = {'w': 0.0, 'n0': 0.0}
idata[52125] = {'w': 0.0, 'n0': 0.0}

# Run calculation and save results in file
decay.calculate(parent, time, idata, "results/55cs125_03.txt")



# Fill in production rate and starting amount of isotopes
idata[55125] = {'w': 50.0, 'n0': 200000.0}
idata[54125] = {'w': 0.0, 'n0': 0.0}
idata[53125] = {'w': 0.0, 'n0': 0.0}
idata[52125] = {'w': 0.0, 'n0': 0.0}

# Run calculation and save results in file
decay.calculate(parent, time, idata, "results/55cs125_04.txt")



# Fill in production rate and starting amount of isotopes
idata[55125] = {'w': 23.0, 'n0': 3.0e5}
idata[54125] = {'w': 54.0, 'n0': 2.0e2}
idata[53125] = {'w': 21.0, 'n0': 1.7e6}
idata[52125] = {'w': 4.0, 'n0': 5.0e4}

# Run calculation and save results in file
decay.calculate(parent, time, idata, "results/55cs125_05.txt")






