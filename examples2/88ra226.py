import sys
sys.path.append("../src")

from decay import decay


# Set path to isotopes dictionary
decay.set("../data/isotopes.p")

# Create isotope chain dictionary
idata = {}

# Set parent isotope
parent = 88226

# Set time at which to calculate activity
time = 86400

chain_isotopes = decay.chain_isotopes(parent)
#decay.print_unique_isotopes(chain_isotopes)

results = decay.calculate(88226, 10000, time_steps=20, time_units='yr', parent_activity=1.0, activity_units='Bq', log='results/88ra226.txt', plot_name='results/88ra226.eps')


print(results)






