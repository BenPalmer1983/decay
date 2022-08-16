import sys
sys.path.append("../src")

from decay import decay


# Set path to isotopes dictionary
decay.set("../data/isotopes.pz")

# Create isotope chain dictionary
idata = {}

# Set parent isotope
parent = 86218

# Set time at which to calculate activity
time = 86400

# Fill in production rate and starting amount of isotopes
idata[86218] = {'w': 0.0, 'n0': 0.0}
idata[84214] = {'w': 0.0, 'n0': 0.0}
idata[82210] = {'w': 0.0, 'n0': 0.0}
idata[80206] = {'w': 0.0, 'n0': 0.0}
idata[83210] = {'w': 0.0, 'n0': 0.0}
idata[81206] = {'w': 0.0, 'n0': 0.0}
idata[84210] = {'w': 0.0, 'n0': 0.0}
idata[82206] = {'w': 0.0, 'n0': 0.0}

# Run calculation and save results in file
decay.calculate(parent, time, idata, "results/86rn218_01.txt")

# Fill in production rate and starting amount of isotopes
idata[86218] = {'w': 100.0, 'n0': 0.0}
idata[84214] = {'w': 0.0, 'n0': 0.0}
idata[82210] = {'w': 0.0, 'n0': 0.0}
idata[80206] = {'w': 0.0, 'n0': 0.0}
idata[83210] = {'w': 0.0, 'n0': 0.0}
idata[81206] = {'w': 0.0, 'n0': 0.0}
idata[84210] = {'w': 0.0, 'n0': 0.0}
idata[82206] = {'w': 0.0, 'n0': 0.0}

# Run calculation and save results in file
decay.calculate(parent, time, idata, "results/86rn218_02.txt")


# Fill in production rate and starting amount of isotopes
idata[86218] = {'w': 0.0, 'n0': 100.0}
idata[84214] = {'w': 0.0, 'n0': 0.0}
idata[82210] = {'w': 0.0, 'n0': 0.0}
idata[80206] = {'w': 0.0, 'n0': 0.0}
idata[83210] = {'w': 0.0, 'n0': 0.0}
idata[81206] = {'w': 0.0, 'n0': 0.0}
idata[84210] = {'w': 0.0, 'n0': 0.0}
idata[82206] = {'w': 0.0, 'n0': 0.0}

# Run calculation and save results in file
decay.calculate(parent, time, idata, "results/86rn218_03.txt")


# Fill in production rate and starting amount of isotopes
idata[86218] = {'w': 3.5e2, 'n0': 5.0e4}
idata[84214] = {'w': 0.0, 'n0': 0.0}
idata[82210] = {'w': 0.0, 'n0': 0.0}
idata[80206] = {'w': 0.0, 'n0': 0.0}
idata[83210] = {'w': 0.0, 'n0': 0.0}
idata[81206] = {'w': 0.0, 'n0': 0.0}
idata[84210] = {'w': 0.0, 'n0': 0.0}
idata[82206] = {'w': 0.0, 'n0': 0.0}

# Run calculation and save results in file
decay.calculate(parent, time, idata, "results/86rn218_04.txt")


# Fill in production rate and starting amount of isotopes
idata[86218] = {'w': 3.5e2, 'n0': 5.0e4}
idata[84214] = {'w': 7.0e1, 'n0': 1.0e3}
idata[82210] = {'w': 1.0e3, 'n0': 1.2e2}
idata[80206] = {'w': 1.7e1, 'n0': 7.0e2}
idata[83210] = {'w': 2.3e1, 'n0': 4.1e1}
idata[81206] = {'w': 8.1e1, 'n0': 5.0e2}
idata[84210] = {'w': 5.2e2, 'n0': 1.5e3}
idata[82206] = {'w': 1.0e3, 'n0': 1.0e4}

# Run calculation and save results in file
decay.calculate(parent, time, idata, "results/86rn218_05.txt")






