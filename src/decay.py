import numpy
from pz import pz
from isotopes import isotopes
import matplotlib.pyplot as plt
import copy

class decay:

  isotopes = None
  path_isotopes = "../data/isotopes.pz"
  loaded = False

  @staticmethod
  def set(path_isotopes):
    decay.path_isotopes = path_isotopes
    isotopes.set(path_isotopes)
    decay.load()

  @staticmethod
  def load():
    if(decay.loaded == False):
      decay.isotopes = pz.load(decay.path_isotopes)
      decay.loaded = True


  @staticmethod
  def chain_isotopes(key, out=[]):
    if(not isotopes.is_valid(key)):
      return out
    if(key not in out):
      out.append(key)
    else:
      return out
    if(isotopes.is_stable(key)):
      return out
    else:
      dm = isotopes.get_decay_modes(key)
      for k in dm.keys():        
        decay.chain_isotopes(k, out)
      return out


  @staticmethod
  def make_chain(key, l=0, out=[], bf=0.0, q=0.0):
    if(not isotopes.is_valid(key)):
      return out
    if(l == 0):   
      decay.chains_store = []
    out.append([l, key, bf, q])
    if(isotopes.is_stable(key)):
      if(len(out) > 1):
        for i in range(len(out)-1,1,-1):
          if(out[i-1][0]>=out[i][0]):
            out.pop(out[i-1][0])
      return decay.chains_store.append(copy.deepcopy(out))
    else:
      l = l + 1 
      dms = isotopes.get_decay_modes(key)
      for k in dms.keys():
        bf = dms[k]['branching_factor']
        q = dms[k]['qvalue']
        decay.make_chain(k, l, out, bf, q)
      return out      

  @staticmethod
  def calculate(parent, time, i_data_in, log=None):
    decay.results = {
                    'tally': {},
                    'unique': None,
                    'chains': None, 
                    } 
    decay.chains_store = None

    decay.results['unique'] = decay.chain_isotopes(parent, [])   


    for k in decay.results['unique']:
      i_data = isotopes.get(k)
      decay.results['tally'][k] = {
        'element': i_data['element'],
        'protons': i_data['protons'],
        'nucleons': i_data['nucleons'],
        'metastable': i_data['metastable'],
        'stable': i_data['stable'],
        'half_life': None,
        'decay_constant': 0.0,
        'n0': 0.0,
        'nend': 0.0,
        'w': 0.0,
      }
      if(not i_data['stable']):
        decay.results['tally'][k]['half_life'] = i_data['half_life']
        decay.results['tally'][k]['decay_constant'] = i_data['decay_constant']
             
      if(k in i_data_in.keys()):
        decay.results['tally'][k]['n0'] = i_data_in[k]['n0']
        decay.results['tally'][k]['w'] = i_data_in[k]['w']

    decay.chains_store = []
    decay.make_chain(parent, 0, [])
    decay.results['chains'] = copy.deepcopy(decay.chains_store)

    set = []      
    for cn in range(len(decay.results['chains'])):
      chain = decay.results['chains'][cn]
      n0 = numpy.zeros((len(chain),),)
      w = numpy.zeros((len(chain),),)
      l = numpy.zeros((len(chain),),)
      b = numpy.zeros((len(chain)-1,),)

      for n in range(len(chain)):
        k = chain[n][1]
        n0[n] = decay.results['tally'][k]['n0']
        w[n] = decay.results['tally'][k]['w']
        l[n] = decay.results['tally'][k]['decay_constant']
        if(n > 0):
          b[n-1] = chain[n][2]

      nt = decay.calculate_activity(time, l, b, w, n0)  
      for n in range(len(chain)):
        k = chain[n][1]
        sk = '0'
        for m in range(n+1):
          sk = sk + str(chain[m][1]) 
          if(sk not in set):        
            set.append(sk)
            decay.results['tally'][k]['nend'] = decay.results['tally'][k]['nend'] + nt[n]

    
    # Log
    if(log != None):
      width = 120
      fh = open(log, 'w')
      fh.write("Unique Isotopes\n")
      fh.write(decay.hr(width) + "\n")
      for k in decay.results['unique']: 
        line = decay.pad(isotopes.get_printable_name(k), 12)
        fh.write(line + "\n")
      fh.write("\n")
      fh.write("\n")
      fh.write("Decay Chains\n")
      fh.write(decay.hr(width) + "\n")
      for cn in range(len(decay.results['chains'])):
        chain = decay.results['chains'][cn]
        fh.write(decay.pad(cn+1,3))
        for n in range(len(chain)):
          k = chain[n][1]
          fh.write(isotopes.get_printable_name(k))
          if(n<(len(chain)-1)):
            b = "{0:3f}".format(chain[n+1][2])
            fh.write(" --[" + str(b) + "]--> ")
        fh.write("\n")
      fh.write("\n")
      fh.write("\n")


      fh.write("Amounts\n")
      fh.write(decay.hr(width) + "\n")
      fh.write("\n")
      fh.write(decay.hr(width) + "\n")
      line = decay.pad("Isotope", 12)
      line = line + decay.pad("T(1/2)", 18)
      line = line + decay.pad("W", 18)
      line = line + decay.pad("N(t=0)", 18)
      line = line + decay.pad("N(t=" + str(time) + ")", 18)
      fh.write(line + "\n")
      fh.write(decay.hr(width) + "\n")


      for k in decay.results['tally'].keys():
        line = decay.pad(isotopes.get_printable_name(k), 12)
        if(decay.results['tally'][k]['half_life'] is None):
          line = line + decay.pad("Stable", 18)
        else:
          line = line + decay.pad(str("{0:16e}".format(decay.results['tally'][k]['half_life'])).strip(), 18)
        line = line + decay.pad(str("{0:16e}".format(decay.results['tally'][k]['w'])).strip(), 18)
        line = line + decay.pad(str("{0:16e}".format(decay.results['tally'][k]['n0'])).strip(), 18)
        line = line + decay.pad(str("{0:16e}".format(decay.results['tally'][k]['nend'])).strip(), 18)
        fh.write(line + "\n")
      fh.write(decay.hr(width) + "\n")
      fh.write("\n")
      fh.write("\n")

      fh.close()


  ##########################################
  # DECAY EQUATIONS
  ##########################################

  @staticmethod
  def calculate_activity(t, l, b, w, n0):
    nt = numpy.zeros((len(n0),),)
    for m in range(0,len(n0)):
      if(l[m] > 0.0):
        nt[m] = decay.activity_unstable(t, l, b, w, n0, m)
      elif(l[m] == 0.0):
        nt[m] = decay.activity_stable(t, l, b, w, n0, m)
    return nt

  @staticmethod
  def activity_unstable(t, l, b, w, n0, m):
    s = 0.0
    for k in range(0, m+1):
      s = s + decay.r(k, m, b, l) * (decay.f_unstable(t,k,m,l) * n0[k] + decay.g_unstable(t,k,m,l) * w[k])
    return s

  @staticmethod
  def f_unstable(t,k,m,l):
    s = 0.0
    for i in range(k, m+1):
      p = 1.0
      for j in range(k, m+1):
        if(i != j):
          p = p * (1 / (l[i] - l[j]))
      s = s + numpy.exp(-1 * l[i] * t) * p
    s = (-1)**(m-k) * s
    return s

  @staticmethod
  def g_unstable(t,k,m,l):
    pa = 1.0
    for i in range(k,m+1):
      pa = pa * l[i]
    pa = 1.0 / pa
    s = 0.0
    for i in range(k, m+1):
      pb = 1.0
      for j in range(k, m+1):
        if(i != j):
          pb = pb * (1 / (l[i]-l[j]))
      s = s + (1/l[i]) * numpy.exp(-l[i]*t) * pb
    return pa + s * (-1)**(m-k+1) 

  @staticmethod
  def activity_stable(t, l, b, w, n0, m):
    s = n0[m] + w[m] * t
    for k in range(0, m):
      s = s + decay.r(k, m, b, l) * decay.f_stable(t,k,m-1,l) * n0[k]
      s = s + decay.r(k, m, b, l) * decay.g_stable(t,k,m-1,l) * w[k]
    return s

  @staticmethod
  def f_stable(t,k,m,l):    
    p = 1.0
    for i in range(k, m+1):
      p = p * l[i]
    s = 0.0
    for i in range(k, m+1):
      r = l[i]
      for j in range(k, m+1):
        if(i != j):
          r = r * (l[i] - l[j])
      s = s + (1/r)*numpy.exp(-1*l[i]*t)   
    return (1.0/p) + s * (-1.0)**(m-k+1)


  @staticmethod
  def g_stable(t,k,m,l):
    nd = 0.0
    mp = (-1.0)**(m - k)

    r = 1.0
    for i in range(k, m+1):
      r = r * l[i]
    nd = nd + (1.0/r) * t

    p = 0.0
    for i in range(k, m+1):
      tm = 1.0
      for j in range(k, m+1):
        if(i != j):
          tm = tm * l[j]
      p = p + tm

    q = 1.0
    for i in range(k, m+1):
      q = q * l[i]*l[i]
    
    r = (-1.0) * (p / q)
    nd = nd + r  

    C = 0.0
    for i in range(k, m+1):
      r = 1.0 * l[i] * l[i]
      for j in range(k, m+1):
        if(i != j):
          r = r * (l[i] - l[j])
      C = C + (1/r) * numpy.exp(-1.0 * l[i] * t)
    nd = nd + C * mp

    return nd 


  @staticmethod
  def r(k, m, b, l):
    if(k == m):
      return 1.0
    else:
      p = 1.0
      for i in range(k, m):
        p = p * (b[i] * l[i])
      return p

  
  @staticmethod
  def pad(inp, l=16):
    inp = str(inp)
    while(len(inp)<l):
      inp = inp + " "
    return inp

  @staticmethod
  def hr(l=16):
    inp = ""
    while(len(inp)<l):
      inp = inp + "="
    return inp

  @staticmethod
  def test():
    print("Decay")

    decay.set("../data/isotopes.pz")

    #parent = 83214
    #time = 1000
    #idata = {}
    #idata[83214] = {'w': 5.0, 'n0': 100.0}
    #decay.calculate(parent, time, idata, "log.txt")

    #idata = {}
    #parent = 27055
    #time = 3000
    #idata[27055] = {'w': 0.02, 'n0': 100.0}
    #idata[26055] = {'w': 0.04, 'n0': 20.0}
    #idata[25055] = {'w': 0.023, 'n0': 30.0}
    #decay.calculate(parent, time, idata, "log.txt")

    idata = {}
    parent = 83213
    time = 1000
    idata[83213] = {'w': 0.02, 'n0': 100.0}
    decay.calculate(parent, time, idata, "testing/log_83213.txt")

#decay.test()









