import sys
sys.path.append("../src")

from decay import decay


# Set path to isotopes dictionary
decay.set("../data/isotopes.pz")

# Create isotope chain dictionary
idata = {}

# Set parent isotope
parent = 28066

# Set time at which to calculate activity
time = 86400

# Fill in production rate and starting amount of isotopes
idata[28066] = {'w': 0.0, 'n0': 0.0}
idata[29066] = {'w': 0.0, 'n0': 0.0}
idata[30066] = {'w': 0.0, 'n0': 0.0}

# Run calculation and save results in file
decay.calculate(parent, time, idata, "results/28ni66_01.txt")


# Fill in production rate and starting amount of isotopes
idata[28066] = {'w': 100.0, 'n0': 0.0}
idata[29066] = {'w': 0.0, 'n0': 0.0}
idata[30066] = {'w': 0.0, 'n0': 0.0}

# Run calculation and save results in file
decay.calculate(parent, time, idata, "results/28ni66_02.txt")


# Fill in production rate and starting amount of isotopes
idata[28066] = {'w': 0.0, 'n0': 100.0}
idata[29066] = {'w': 0.0, 'n0': 0.0}
idata[30066] = {'w': 0.0, 'n0': 0.0}

# Run calculation and save results in file
decay.calculate(parent, time, idata, "results/28ni66_03.txt")


# Fill in production rate and starting amount of isotopes
idata[28066] = {'w': 2.5, 'n0': 30000.0}
idata[29066] = {'w': 0.0, 'n0': 0.0}
idata[30066] = {'w': 0.0, 'n0': 0.0}

# Run calculation and save results in file
decay.calculate(parent, time, idata, "results/28ni66_04.txt")


# Fill in production rate and starting amount of isotopes
idata[28066] = {'w': 2.5, 'n0': 30000.0}
idata[29066] = {'w': 1.07, 'n0': 1000.0}
idata[30066] = {'w': 3.2, 'n0': 20000.0}

# Run calculation and save results in file
decay.calculate(parent, time, idata, "results/28ni66_05.txt")







