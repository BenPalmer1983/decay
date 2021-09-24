import sys
sys.path.append("../src")

from decay import decay


# Set path to isotopes dictionary
decay.set("../data/isotopes.pz")

# Create isotope chain dictionary
idata = {}

# Set parent isotope
parent = 84216

# Set time at which to calculate activity
time = 10

# Fill in production rate and starting amount of isotopes
idata[84216] = {'w': 0.20, 'n0': 100.0}
idata[82212] = {'w': 0.0, 'n0': 5.0}
idata[83212] = {'w': 0.07, 'n0': 15.0}
idata[81208] = {'w': 0.005, 'n0': 0.0}
# 84Po212 0 0 (default values of 0 and 0)
idata[82208] = {'w': 0.01, 'n0': 300.0}

# Run calculation and save results in file
decay.calculate(parent, time, idata, "polonium/log_84216_new.txt")
