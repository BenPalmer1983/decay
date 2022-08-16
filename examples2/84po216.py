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
time = 86400

# Fill in production rate and starting amount of isotopes
idata[84216] = {'w': 0.0, 'n0': 0.0}
idata[82212] = {'w': 0.0, 'n0': 0.0}
idata[83212] = {'w': 0.0, 'n0': 0.0}
idata[81208] = {'w': 0.0, 'n0': 0.0}
idata[84212] = {'w': 0.0, 'n0': 0.0}
idata[82208] = {'w': 0.0, 'n0': 0.0}

# Run calculation and save results in file
decay.calculate(parent, time, idata, "results/84po216_01.txt")

# Fill in production rate and starting amount of isotopes
idata[84216] = {'w': 100.0, 'n0': 0.0}
idata[82212] = {'w': 0.0, 'n0': 0.0}
idata[83212] = {'w': 0.0, 'n0': 0.0}
idata[81208] = {'w': 0.0, 'n0': 0.0}
idata[84212] = {'w': 0.0, 'n0': 0.0}
idata[82208] = {'w': 0.0, 'n0': 0.0}

# Run calculation and save results in file
decay.calculate(parent, time, idata, "results/84po216_02.txt")

# Fill in production rate and starting amount of isotopes
idata[84216] = {'w': 0.0, 'n0': 100.0}
idata[82212] = {'w': 0.0, 'n0': 0.0}
idata[83212] = {'w': 0.0, 'n0': 0.0}
idata[81208] = {'w': 0.0, 'n0': 0.0}
idata[84212] = {'w': 0.0, 'n0': 0.0}
idata[82208] = {'w': 0.0, 'n0': 0.0}

# Run calculation and save results in file
decay.calculate(parent, time, idata, "results/84po216_03.txt")

# Fill in production rate and starting amount of isotopes
idata[84216] = {'w': 350.0, 'n0': 50000.0}
idata[82212] = {'w': 0.0, 'n0': 0.0}
idata[83212] = {'w': 0.0, 'n0': 0.0}
idata[81208] = {'w': 0.0, 'n0': 0.0}
idata[84212] = {'w': 0.0, 'n0': 0.0}
idata[82208] = {'w': 0.0, 'n0': 0.0}

# Run calculation and save results in file
decay.calculate(parent, time, idata, "results/84po216_04.txt")

# Fill in production rate and starting amount of isotopes
idata[84216] = {'w': 0.20, 'n0': 100.0}
idata[82212] = {'w': 0.1, 'n0': 5.0}
idata[83212] = {'w': 0.07, 'n0': 15.0}
idata[81208] = {'w': 0.005, 'n0': 10.0}
idata[84212] = {'w': 0.02, 'n0': 17.0}
idata[82208] = {'w': 0.01, 'n0': 300.0}

# Run calculation and save results in file
decay.calculate(parent, time, idata, "results/84po216_05.txt")
