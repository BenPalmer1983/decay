import sys
sys.path.append("../src")

from decay import decay


# Set path to isotopes dictionary
decay.set("../data/isotopes.pz")

# Create isotope chain dictionary
idata = {}

# Set parent isotope
parent = 83213

# Set time at which to calculate activity
time = 86400

# Fill in production rate and starting amount of isotopes
idata[83213] = {'w': 0.0, 'n0': 0.0}
idata[84213] = {'w': 0.0, 'n0': 0.0}
idata[81209] = {'w': 0.0, 'n0': 0.0}
idata[82209] = {'w': 0.0, 'n0': 0.0}
idata[83209] = {'w': 0.0, 'n0': 0.0}
idata[81205] = {'w': 0.0, 'n0': 0.0}

# Run calculation and save results in file
decay.calculate(parent, time, idata, "results/83bi213_01.txt")


# Fill in production rate and starting amount of isotopes
idata[83213] = {'w': 100.0, 'n0': 0.0}
idata[84213] = {'w': 0.0, 'n0': 0.0}
idata[81209] = {'w': 0.0, 'n0': 0.0}
idata[82209] = {'w': 0.0, 'n0': 0.0}
idata[83209] = {'w': 0.0, 'n0': 0.0}
idata[81205] = {'w': 0.0, 'n0': 0.0}

# Run calculation and save results in file
decay.calculate(parent, time, idata, "results/83bi213_02.txt")


# Fill in production rate and starting amount of isotopes
idata[83213] = {'w': 0.0, 'n0': 100.0}
idata[84213] = {'w': 0.0, 'n0': 0.0}
idata[81209] = {'w': 0.0, 'n0': 0.0}
idata[82209] = {'w': 0.0, 'n0': 0.0}
idata[83209] = {'w': 0.0, 'n0': 0.0}
idata[81205] = {'w': 0.0, 'n0': 0.0}

# Run calculation and save results in file
decay.calculate(parent, time, idata, "results/83bi213_03.txt")


# Fill in production rate and starting amount of isotopes
idata[83213] = {'w': 300000, 'n0': 10000000000}
idata[84213] = {'w': 0.0, 'n0': 0.0}
idata[81209] = {'w': 0.0, 'n0': 0.0}
idata[82209] = {'w': 0.0, 'n0': 0.0}
idata[83209] = {'w': 0.0, 'n0': 0.0}
idata[81205] = {'w': 0.0, 'n0': 0.0}

# Run calculation and save results in file
decay.calculate(parent, time, idata, "results/83bi213_04.txt")


# Fill in production rate and starting amount of isotopes
idata[83213] = {'w': 3.0e5, 'n0': 1.0e10}
idata[84213] = {'w': 7.0e3, 'n0': 2.0e7}
idata[81209] = {'w': 2.0e4, 'n0': 2.0e6}
idata[82209] = {'w': 1.0e0, 'n0': 1.0e7}
idata[83209] = {'w': 3.5e8, 'n0': 1.0e6}
idata[81205] = {'w': 1.0e-10, 'n0': 1.0e-10}

# Run calculation and save results in file
decay.calculate(parent, time, idata, "results/83bi213_05.txt")









