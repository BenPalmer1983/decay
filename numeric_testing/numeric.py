import numpy


w = [0.02, 0.04, 0.023]
#w = [0.0, 0.0, 0.0]
thalf = [63108,86700000,None]
l = [numpy.log(2) / thalf[0], numpy.log(2) / thalf[1], None]
n0 = [100,20,30]


t_end = 3000.0
steps = 30000000
t_step = t_end / steps

n = numpy.copy(n0)
for i in range(steps):
  d_source = [0.0,0.0,0.0]
  for k in range(len(n0)):
    d_source[k] = t_step * w[k]  
  d_loss = [0.0,0.0,0.0]
  for k in range(len(n0)):
    if(l[k] is not None):
      d_loss[k] = n[k] * (1.0 - numpy.exp(- l[k] * t_step))
      d_source[k+1] = d_source[k+1] + d_loss[k]
  n = n + d_source - d_loss


print(n)


