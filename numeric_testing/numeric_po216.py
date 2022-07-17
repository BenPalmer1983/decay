import numpy

# Values altered
# Po216 Pb212 Bi212 Tl208 Po212 Pb208
w = [0.02, 0.0, 0.0, 0.0, 0.0, 0.0]
l = [4.683427e+00, 1.809595e-05, 1.908235e-04, 3.777781e-03, 2.310491e+06, None]
n0 = [100,0.0,0.0,0.0,0.0,0.0]


t_end = 1000.0
steps = 10000000
t_step = t_end / steps


n = numpy.copy(n0)
for i in range(steps):
  source = [0.0,0.0,0.0,0.0,0.0,0.0]
  loss = [0.0,0.0,0.0,0.0,0.0,0.0]
  
  # Po216
  k = 0
  source[k] = t_step * w[k] 
  loss[k] = n[k] * (1.0 - numpy.exp(- l[k] * t_step))
  
  # Pb212
  k = 1
  source[k] = t_step * w[k] + loss[0]
  loss[k] = n[k] * (1.0 - numpy.exp(- l[k] * t_step))
  
  # Bi212
  k = 2
  source[k] = t_step * w[k] + loss[1]
  loss[k] = n[k] * (1.0 - numpy.exp(- l[k] * t_step))
 
  # Tl208 0.359300
  k = 3
  source[k] = t_step * w[k] + 0.359300 * loss[2]
  loss[k] = n[k] * (1.0 - numpy.exp(- l[k] * t_step))
  
  # Po212 0.640700
  k = 4
  source[k] = t_step * w[k] + 0.640700 * loss[2]
  loss[k] = n[k] * (1.0 - numpy.exp(- l[k] * t_step))
  
  # Pb208
  k = 5
  source[k] = t_step * w[k] + loss[3] + loss[4]

  
  n = n + source - loss


print("Po216  ", n[0])
print("Pb212  ", n[1])
print("Bi212  ", n[2])
print("Tl208  ", n[3])
print("Po212  ", n[4])
print("Pb208  ", n[5])
