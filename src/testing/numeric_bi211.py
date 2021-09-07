import numpy


w = [1.0,0.0,0.0,0.0]
l = [5.373234e-3, 2.419869e-3, 2.924672e-2 , None]
n0 = [100,0.0,0.0,1.0]


t_end = 10.0
steps = 1000000
t_step = t_end / steps


n = numpy.copy(n0)
for i in range(steps):
  source = [0.0,0.0,0.0,0.0]
  loss = [0.0,0.0,0.0,0.0]
  
  # Bi 212
  k = 0
  source[k] = t_step * w[k] 
  loss[k] = n[k] * (1.0 - numpy.exp(- l[k] * t_step))
 
  # Tl 207
  k = 1
  source[k] = t_step * w[k] + 0.6 * loss[0]
  loss[k] = n[k] * (1.0 - numpy.exp(- l[k] * t_step))
 
  # Po 211
  k = 2
  source[k] = t_step * w[k] + 0.4 * loss[0]
  loss[k] = n[k] * (1.0 - numpy.exp(- l[k] * t_step))
 
  # Pb 207
  k = 3
  source[k] = t_step * w[k] + loss[1] + loss[2]
  
  n = n + source - loss


print(n)



w = [1.0,0.0,0.0]
l = [5.373234e-3, 2.419869e-3, None]
n0 = [100,0.0,1.0]
bf1 = [1.0,0.6,0.6]


t_end = 10.0
steps = 1000000
t_step = t_end / steps


n1 = numpy.copy(n0)
n1 = bf1 * n1
for i in range(steps):
  source = [0.0,0.0,0.0]
  loss = [0.0,0.0,0.0]
  
  # Bi 212
  k = 0
  source[k] = t_step * w[k] 
  loss[k] = n1[k] * (1.0 - numpy.exp(- l[k] * t_step))
 
  # Tl 207
  k = 1
  source[k] = t_step * w[k] + 0.6 * loss[0]
  loss[k] = n1[k] * (1.0 - numpy.exp(- l[k] * t_step))
  
  # Pb 207
  k = 2
  source[k] = t_step * w[k] + loss[1]
  
  n1 = n1 + source - loss


print(n1)


w = [1.0,0.0,0.0]
l = [5.373234e-3, 2.924672e-2, None]
n0 = [100,0.0,1.0]
bf2 = [1.0,0.4,0.4]


t_end = 10.0
steps = 1000000
t_step = t_end / steps


n2 = numpy.copy(n0)
n2 = bf2 * n2
for i in range(steps):
  source = [0.0,0.0,0.0]
  loss = [0.0,0.0,0.0]
  
  # Bi 212
  k = 0
  source[k] = t_step * w[k] 
  loss[k] = n2[k] * (1.0 - numpy.exp(- l[k] * t_step))
 
  # Tl 207
  k = 1
  source[k] = t_step * w[k] + 0.4 * loss[0]
  loss[k] = n2[k] * (1.0 - numpy.exp(- l[k] * t_step))
  
  # Pb 207
  k = 2
  source[k] = t_step * w[k] + loss[1]
  
  n2 = n2 + source - loss


print(n2)


