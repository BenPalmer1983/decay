# python3 example.py

from decay import decay

# Set the isotopes file
decay.set("../data/isotopes.pz")


# Pick the parent isotope
parent = 84216

# Set the time the activity is measured at
time = 10

# Create a dictionary to set production rates and starting amounts (at least for the parent isotope)
idata = {}
idata[84216] = {'w': 0.20, 'n0': 100.0}
idata[82212] = {'w': 0.0, 'n0': 5.0}
idata[83212] = {'w': 0.07, 'n0': 15.0}
idata[81208] = {'w': 0.005, 'n0': 0.0}
idata[82208] = {'w': 0.01, 'n0': 300.0}

# Calculate and store results in a file
decay.calculate(parent, time, idata, "example.txt")
