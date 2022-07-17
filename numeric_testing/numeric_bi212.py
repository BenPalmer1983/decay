import numpy


w = [0.02,0.0,0.0,0.0]
#w = [0.0, 0.0, 0.0]
thalf = [3.632400e+03, 3.000000e-01, 1.834800e+02, None]
l = [numpy.log(2) / thalf[0], numpy.log(2) / thalf[1], numpy.log(2) / thalf[2], None]
n0 = [100,0.0,0.0,0.0]


t_end = 0.1
steps = 1000000000
t_step = t_end / steps


n = numpy.copy(n0)
for i in range(steps):
  source = [0.0,0.0,0.0,0.0]
  loss = [0.0,0.0,0.0,0.0]
  
  # Bi 212
  k = 0
  source[k] = t_step * w[k] 
  loss[k] = n[k] * (1.0 - numpy.exp(- l[k] * t_step))
 
  # Po 212
  k = 1
  source[k] = t_step * w[k] + 0.6407 * loss[0]
  loss[k] = n[k] * (1.0 - numpy.exp(- l[k] * t_step))
 
  # Tl 208
  k = 2
  source[k] = t_step * w[k] + 0.3593 * loss[0]
  loss[k] = n[k] * (1.0 - numpy.exp(- l[k] * t_step))
 
  # Pb 208
  k = 3
  source[k] = t_step * w[k] + loss[1] + loss[2]
  
  n = n + source - loss



print(n)


