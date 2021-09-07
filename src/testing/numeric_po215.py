import numpy

# Values altered
# Po215, Pb211, At215, Bi211, Tl207, Po211, Pb207
w = [1.0,0.4,0.0,0.0,0.0,0.0,2.0]
l = [8.351171e-03, 1.474781e-02, 7.534208e-03, 3.465736e-01, 1.368666e-03, 1.181958e-03, None]
n0 = [10000,0.0,0.0,40.0,20.0,0.0,10.0]


t_end = 10.0
steps = 1000000
t_step = t_end / steps


n = numpy.copy(n0)
for i in range(steps):
  source = [0.0,0.0,0.0,0.0,0.0,0.0,0.0]
  loss = [0.0,0.0,0.0,0.0,0.0,0.0,0.0]
  
  # Po215
  k = 0
  source[k] = t_step * w[k] 
  loss[k] = n[k] * (1.0 - numpy.exp(- l[k] * t_step))
  
  # Pb211  0.8
  k = 1
  source[k] = t_step * w[k] + 0.8 * loss[0]
  loss[k] = n[k] * (1.0 - numpy.exp(- l[k] * t_step))
  
  # At215  0.2
  k = 2
  source[k] = t_step * w[k] + 0.2 * loss[0]
  loss[k] = n[k] * (1.0 - numpy.exp(- l[k] * t_step))
 
  # Bi211 
  k = 3
  source[k] = t_step * w[k] + loss[1] + loss[2]
  loss[k] = n[k] * (1.0 - numpy.exp(- l[k] * t_step))
  
  # Tl207 0.6
  k = 4
  source[k] = t_step * w[k] + 0.6 * loss[3]
  loss[k] = n[k] * (1.0 - numpy.exp(- l[k] * t_step))
  
  # Po211 0.4
  k = 5
  source[k] = t_step * w[k] + 0.4 * loss[3]
  loss[k] = n[k] * (1.0 - numpy.exp(- l[k] * t_step))
  
  # Pb207
  k = 6
  source[k] = t_step * w[k] + loss[4] + loss[5]
 
 
 
 
  
  n = n + source - loss


print("Po215  ", n[0])
print("Pb211  ", n[1])
print("At215  ", n[2])
print("Bi211  ", n[3])
print("Tl207  ", n[4])
print("Po211  ", n[5])
print("Pb207  ", n[6])
