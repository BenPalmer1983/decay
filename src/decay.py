import os
import numpy
import sys
from pz import pz
from isotopes import isotopes
import matplotlib.pyplot as plt
import copy
import hashlib
import time

class decay:

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
  def make_chain(key, l=0, out=[], bf=0.0):
    if(not isotopes.is_valid(key)):
      return out
    if(l == 0):   
      decay.chains_store = []
    out.append([l, key, bf])
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
        decay.make_chain(k, l, out, bf)
      return out      


  @staticmethod
  def calculate(parent, mtime, i_data_in=None, log=None, parent_activity=None, parent_amount=None, parent_production_rate=0.0, custom_chain=None, time_units=None, activity_units=None, time_steps=1, plot_name=None):

    # At a single time
    if(time_steps == 1):
      return decay.calculate_at_time(parent, mtime, i_data_in=i_data_in, log=log, parent_activity=parent_activity, parent_amount=parent_amount, parent_production_rate=parent_production_rate, custom_chain=custom_chain, time_units=time_units)

    # Multiple time steps
    else:
      t = numpy.logspace(start=0.0, stop=numpy.log10(mtime), num=time_steps)
      activity = []

      for tn in t:
        r = decay.calculate_at_time(parent, tn, i_data_in=i_data_in, parent_activity=parent_activity, parent_amount=parent_amount, parent_production_rate=parent_production_rate, custom_chain=custom_chain, time_units=time_units)
        activity.append(r)

      if(time_units is None):
        time_units = 's'
      if(activity_units is None):
        activity_units = 'Bq'
      
      result = {}
      result['time'] = t
      result['activity'] = {}

      # Add isotope activity arrays
      for n in range(len(activity)):
        for key in activity[n]['unique']:
          if(key not in result['activity'].keys()):
            result['activity'][key] = numpy.zeros((time_steps,), dtype=numpy.float64)
      for n in range(len(activity)):
        for key in activity[n]['tally']:
          result['activity'][key][n] = activity[n]['tally'][key]['activityend']
      
      if(plot_name is not None):
        plt.figure(figsize=[12, 8], dpi=144)
        styles = ['solid', 'dashed', 'dashdot', 'dotted']
        n = 0
        for key in activity[n]['tally']:
          if(isotopes.is_unstable(key)):          
            plt.plot(result['time'], result['activity'][key], label=isotopes.get_hr(key), ls=styles[n%len(styles)])
            n = n + 1
        plt.xscale('log')
        plt.yscale('log')
        plt.title('Activity over time: ' + isotopes.get_hr(parent))
        plt.xlabel('Time (' + time_units + ')')
        plt.ylabel('Activity (' + activity_units + ')')
        plt.legend()
        plt.savefig(plot_name)

      return result



  @staticmethod
  def calculate_at_time(parent, mtime, i_data_in=None, log=None, parent_activity=None, parent_amount=None, parent_production_rate=0.0, custom_chain=None, time_units=None):
    tstart = time.time()

    # Create an empty dictionary 
    # Starting isotope amounts will be zero
    # Production rates will be zero
    if(i_data_in is None):
      i_data_in = {}

    if(parent_activity is not None):
      parent_data = isotopes.get(parent)
      if(not parent_data['stable']):
        n0 = parent_activity / parent_data['decay_constant']
        if(parent not in i_data_in.keys()):
          i_data_in[parent] = {'w': parent_production_rate, 'n0': 0.0}
        i_data_in[parent]['n0'] = n0

    if(time_units is not None):
      if(time_units.lower() == 'min' or 'time_units'.lower() == 'mins'):
        mtime = 60.0 * mtime
      elif(time_units.lower() == 'hr' or 'time_units'.lower() == 'hrs'):
        mtime = 3600.0 * mtime
      elif(time_units.lower() == 'day' or 'time_units'.lower() == 'days'):
        mtime = 86400.0 * mtime
      elif(time_units.lower() == 'yr' or time_units.lower() == 'year' or 'time_units'.lower() == 'years'):
        mtime = 31557600.0 * mtime
    



    if(log != None):
      log_dir = decay.get_file_dir(log)
      decay.make_dir(log_dir)

    decay.results = {
                    'tally': {},
                    'unique': None,
                    'chains': None, 
                    } 
    decay.chains_store = None

    if(custom_chain == None):
      decay.chains_store = []
      decay.make_chain(parent, 0, [])
      decay.results['chains'] = []
      cn = 0
      for chain in decay.chains_store:
        decay.results['chains'].append([])
        for iso in chain:
          k = iso[1]
          bf = iso[2]
          i_data = isotopes.get(k)
          half_life = None
          decay_constant = None
          n0 = 0.0
          w = 0.0
          if(not i_data['stable']):
            half_life = i_data['half_life'] 
            decay_constant = i_data['decay_constant']           
          if(k in i_data_in.keys()):
            n0 = i_data_in[k]['n0']
            w = i_data_in[k]['w']
          d = {
              'isotope_key': k, 
              'bf': bf,
              'w': w,
              'n0': n0,
              'nend': 0,
              'half_life': half_life,
              'decay_constant': decay_constant,
              } 
          decay.results['chains'][cn].append(d)
        cn = cn + 1
    else:
      decay.results['chains'] = custom_chain


    # Find unique and make tally
    decay.results['unique'] = []
    for chain in decay.results['chains']:
      for iso in chain:
        k = iso['isotope_key']
        if(k not in decay.results['tally'].keys()):
          decay.results['unique'].append(k)
          # Use provided data
          if(iso['half_life'] == None):
            stable = True
            half_life = None
            decay_constant = 0.0
          else:
            stable = False
            half_life = iso['half_life']
            decay_constant = numpy.log(2) / iso['half_life']
          w = iso['w']
          n0 = iso['n0'] 
          # Get proton/neutron etc from isotopes database
          i_data = isotopes.get(k)
          if(i_data is None):     
            decay.results['tally'][k] = {
                                        'printable': 'Custom',
                                        'element': 'ZZ',
                                        'protons': 999,
                                        'nucleons': 999,
                                        'metastable': 9,
                                        'stable': stable,
                                        'half_life': half_life,
                                        'decay_constant': decay_constant,
                                        'w': w,
                                        'n0': n0,
                                        'nend': 0.0,
                                        'activity0': 0.0,
                                        'activityend': 0.0,
                                        }
          else:
            decay.results['tally'][k] = {
                                        'printable': decay.pad(isotopes.get_printable_name(k), 12),
                                        'element': i_data['element'],
                                        'protons': i_data['protons'],
                                        'nucleons': i_data['nucleons'],
                                        'metastable': i_data['metastable'],
                                        'stable': stable,
                                        'half_life': half_life,
                                        'decay_constant': decay_constant,
                                        'w': w,
                                        'n0': n0,
                                        'nend': 0.0,
                                        'activity0': 0.0,
                                        'activityend': 0.0,
                                        }


    decay.results['chains_individual'] = []
    for cn in range(len(decay.results['chains'])):
      for n in range(len(decay.results['chains'][cn])):
        nc = []
        if(decay.results['chains'][cn][n]['n0']>0.0 or decay.results['chains'][cn][n]['w']>0.0):
          for j in range(n, len(decay.results['chains'][cn])):
            iso = copy.deepcopy(decay.results['chains'][cn][j])
            if(j>n):
              iso['n0'] = 0.0
              iso['w'] = 0.0
            nc.append(iso)
        if(len(nc)>0):
          decay.results['chains_individual'].append(nc)

    for cn in range(len(decay.results['chains_individual'])):
      chain = decay.results['chains_individual'][cn]
      n0 = numpy.zeros((len(chain),),)
      w = numpy.zeros((len(chain),),)
      l = numpy.zeros((len(chain),),)
      b = numpy.zeros((len(chain)-1,),)
      for n in range(len(decay.results['chains_individual'][cn])):
        k = decay.results['chains_individual'][cn][n]['isotope_key']
        n0[n] = decay.results['chains_individual'][cn][n]['n0']
        w[n] = decay.results['chains_individual'][cn][n]['w']
        l[n] = decay.results['tally'][k]['decay_constant']
        if(n>0):
          b[n-1] = decay.results['chains_individual'][cn][n]['bf']
        # Some observationally stable will still have a decay constant, so set to -1.0
        if(isotopes.is_stable(k)):
          l[n] = -1.0
      nt = decay.calculate_activity(mtime, l, b, w, n0) 
      for n in range(len(decay.results['chains_individual'][cn])):
        decay.results['chains_individual'][cn][n]['nend'] = nt[n]

    set = []
    for cn in range(len(decay.results['chains_individual'])):
      ckey = ''
      for n in range(len(decay.results['chains_individual'][cn])):
        k = decay.results['chains_individual'][cn][n]['isotope_key']
        ckey = ckey + str(decay.results['chains_individual'][cn][n]['isotope_key']) + "N0:" + str(decay.results['chains_individual'][cn][n]['n0']) + "W:" + str(decay.results['chains_individual'][cn][n]['w'])
        ckeyh = hashlib.md5(ckey.encode())
        ckeyh = ckeyh.hexdigest()
        if(ckeyh not in set):
          decay.results['tally'][k]['nend'] = decay.results['tally'][k]['nend'] + decay.results['chains_individual'][cn][n]['nend']
          set.append(ckeyh)

    # Calculate activity
    for key in decay.results['tally']:
      if(decay.results['tally'][key]['stable']):
        decay.results['tally'][key]['activity0'] = 0.0
        decay.results['tally'][key]['activityend'] = 0.0
      else:
        lam = decay.results['tally'][key]['decay_constant']
        decay.results['tally'][key]['activity0'] = decay.results['tally'][key]['n0'] * lam
        decay.results['tally'][key]['activityend'] = decay.results['tally'][key]['nend'] * lam
        
    # Log
    if(log != None):
      width = 140
      fh = open(log, 'w')
      fh.write("Unique Isotopes\n")
      fh.write(decay.hr(width) + "\n")
      for k in decay.results['unique']: 
        line = decay.results['tally'][k]['printable']
        fh.write(line + "\n")
      fh.write("\n")
      fh.write("\n")
      fh.write("Decay Chains\n")
      fh.write(decay.hr(width) + "\n")
      fh.write("\n")
      fh.write("\n")
      for cn in range(len(decay.results['chains'])):
        chain = decay.results['chains'][cn]

        fh.write(decay.pad(cn+1,6)) 
        for n in range(len(chain)):
          iso = chain[n]
          k = iso['isotope_key']
          if(n>0):
            bf = "{0:3e}".format(iso['bf'])
            fh.write(" --[" + str(bf) + "]--> ")
          fh.write(decay.pad(decay.results['tally'][k]['printable'], 12))
        fh.write("\n")
        fh.write(decay.pad("T1/2",6)) 
        for n in range(len(chain)):
          if(n>0):
            fh.write(decay.pad("",17)) 
          if(decay.results['chains'][cn][n]['half_life'] == None):
            fh.write(decay.pad("[Stable]",12))
          else:
            fh.write(decay.pad("[" + str("{0:8e}".format(decay.results['chains'][cn][n]['half_life'])) + "]",12))
        fh.write("\n")
        fh.write(decay.pad("L",6)) 
        for n in range(len(chain)):
          if(n>0):
            fh.write(decay.pad("",17)) 
          if(decay.results['chains'][cn][n]['decay_constant'] == None):
            fh.write(decay.pad("[Stable]",12))
          else:
            fh.write(decay.pad("[" + str("{0:8e}".format(decay.results['chains'][cn][n]['decay_constant'])) + "]",12))
        fh.write("\n")
        fh.write("\n")        
        fh.write("\n")


     
      fh.write("Amounts\n")
      fh.write(decay.hr(width) + "\n")
      fh.write("\n")
      fh.write(decay.hr(width) + "\n")
      line = decay.pad("Isotope", 12)
      line = line + decay.pad("T(1/2)", 18)
      line = line + decay.pad("Decay Constant", 18)
      line = line + decay.pad("W", 18)
      line = line + decay.pad("N(t=0)", 18)
      line = line + decay.pad("N(t=" + str(mtime) + ")", 18)
      line = line + decay.pad("A(t=0)", 18)
      line = line + decay.pad("A(t=" + str(mtime) + ")", 18)
      fh.write(line + "\n")
      fh.write(decay.hr(width) + "\n")


      for k in decay.results['tally'].keys():
        line = decay.pad(decay.results['tally'][k]['printable'], 12)
        if(decay.results['tally'][k]['half_life'] is None):
          line = line + decay.pad("Stable", 18)
          line = line + decay.pad("Stable", 18)
        else:
          line = line + decay.pad(str("{0:16e}".format(decay.results['tally'][k]['half_life'])).strip(), 18)
          line = line + decay.pad(str("{0:16e}".format(decay.results['tally'][k]['decay_constant'])).strip(), 18)
        line = line + decay.pad(str("{0:16e}".format(decay.results['tally'][k]['w'])).strip(), 18)
        line = line + decay.pad(str("{0:16e}".format(decay.results['tally'][k]['n0'])).strip(), 18)
        line = line + decay.pad(str("{0:16e}".format(decay.results['tally'][k]['nend'])).strip(), 18)
        if(decay.results['tally'][k]['half_life'] is not None):
          line = line + decay.pad(str("{0:16e}".format(decay.results['tally'][k]['decay_constant'] * decay.results['tally'][k]['n0'])).strip(), 18)
          line = line + decay.pad(str("{0:16e}".format(decay.results['tally'][k]['decay_constant'] * decay.results['tally'][k]['nend'])).strip(), 18)
        fh.write(line + "\n")
      fh.write(decay.hr(width) + "\n")
      fh.write("\n")
      fh.write("\n")
      fh.write("Time: " + str(time.time() - tstart) + "\n")
      fh.write("\n")
      
      fh.close()
  
    return decay.results



  @staticmethod
  def print_unique_isotopes(chain):
    for isotope in chain:
      print(isotopes.get_hr(isotope))



  ##########################################
  # DECAY EQUATIONS
  ##########################################
    
  @staticmethod
  def calculate_activity(t, lam, b, w, n0):
    nt = numpy.zeros((len(n0),),)
    for m in range(0,len(n0)):
      if(lam[m] <= 0):
        nt[m] = decay.calc_stable(t, m, lam, b, w, n0)
      else:
        nt[m] = decay.calc_unstable(t, m, lam, b, w, n0)
    return nt

  @staticmethod
  def calc_unstable(t, m, lam, b, w, n0):
    y = 0.0 
    k = 0
    while(k<=m):    
      y = y + decay.r(k, m, lam, b) * (decay.f_unstable(t, k, m, lam) * n0[k] + decay.g_unstable(t, k, m, lam) * w[k])
      k = k + 1
    return y

  @staticmethod
  def f_unstable(t, k, m, lam): 
    s = 0.0
    i = k
    while(i<=m):
      p = decay.lprod(lam, k, m, 3, i)
      s = s + numpy.exp(-lam[i] * t) * (1.0 / p)
      i = i + 1
    s = s * (-1)**(m-k)  
    return s


  @staticmethod
  def g_unstable(t, k, m, lam): 
    # Term a
    p = decay.lprod(lam, k, m, 1)
    a = 1.0 / p
    # Term b
    s = 0.0
    i = k
    while(i<=m):
      p = decay.lprod(lam, k, m, 3, i)  
      s = s + (1 / lam[i]) * numpy.exp(-lam[i] * t) * (1.0 / p)
      i = i + 1
    s = s * (-1)**(m-k+1)           
    return a + s    

  @staticmethod
  def calc_stable(t, m, lam, b, w, n0):
    y = n0[m] + w[m] * t 
    k = 0
    while(k<=m-1):    
      y = y + decay.r(k, m, lam, b) * (decay.f_stable(t, k, m, lam) * n0[k] + decay.g_stable(t, k, m, lam) * w[k])
      k = k + 1
    return y    

  @staticmethod
  def f_stable(t, k, m, lam):  
    mm = m - 1
    p = decay.lprod(lam, k, mm, 1)
    a = 1.0 / p

    s = 0.0
    i = k
    while(i<=mm):
      p = decay.lprod(lam, k, mm, 3, i)
      s = s + (1 / lam[i]) * numpy.exp(-lam[i] * t) * (1.0 / p)
      i = i + 1
    s = s * (-1)**(mm-k+1)  
    return a + s
   
  @staticmethod 
  def g_stable(t, k, m, lam): 
    mm = m - 1

    p = decay.lprod(lam, k, mm, 1) 
    a = (t/p)

    s = 0.0
    i = k
    while(i<=mm):
      p = decay.lprod(lam, k, mm, 4, i) 
      s = s + p
      i = i + 1
    q = decay.lprod(lam, k, mm, 2)
    b = (-s / q)

    c = 0.0
    i = k
    while(i<= mm):
      p = lam[i]**2 * decay.lprod(lam, k, mm, 3, i) 
      c = c + numpy.exp(-1.0 * lam[i] * t) / p
      i = i + 1
    c = c * (-1.0)**(mm - k)
    nd = a + b + c


    
    return nd
    
    
    

  @staticmethod
  def r(k, m, lam, b):
    if(k == m):
      return 1  
    else:
      p = 1.0
      i = k
      while(i<=(m-1)):
        p = p * b[i] * lam[i]
        i = i + 1
      return p
 
  @staticmethod   
  def lprod(lam, k, m, t=1, i=None): 
    # PROD k,m lam[j]
    if(t == 1):
      p = 1.0
      j = k
      while(j<=m):
        p = p * lam[j]
        j = j + 1
      return p
    # PROD k,m lam[j]**2
    elif(t == 2):
      p = 1.0
      j = k
      while(j<=m):
        p = p * lam[j]**2
        j = j + 1
      return p
    # PROD k,m, i!=j (lam[i]-lam[j])
    elif(t == 3):
      p = 1.0
      j = k
      while(j<=m):
        if(i != j):
          p = p * (lam[i] - lam[j])
        j = j + 1
      return p
    # PROD k,m, i!=j lam[j]
    elif(t == 4):
      p = 1.0
      j = k
      while(j<=m):
        if(i != j):
          p = p * lam[j]
        j = j + 1
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
  def get_file_dir(file_path):
    file_path = file_path.strip()
    if(file_path[0] != "/"):
      root = os.getcwd()
      file_path = root + "/" + file_path
    file_path = file_path.split("/")
    path = ""
    for i in range(1,len(file_path) - 1):
      path = path + "/" + file_path[i]
    return path

  @staticmethod
  def make_dir(dir):
    dirs = dir.split("/")
    try:
      dir = ''
      for i in range(len(dirs)):
        dir = dir + dirs[i]
        if(not os.path.exists(dir) and dir.strip() != ''):
          os.mkdir(dir) 
        dir = dir + '/'
      return True
    except:
      return False


  @staticmethod
  def test():
    print("Decay")

    # Load isotopes dictionary
    decay.set("../data/isotopes.p")

    idata = {}
    parent = 84216
    time = 10
    idata[84216] = {'w': 0.20, 'n0': 100.0}
    idata[82212] = {'w': 0.0, 'n0': 5.0}
    idata[83212] = {'w': 0.07, 'n0': 15.0}
    idata[81208] = {'w': 0.005, 'n0': 0.0}
    # 84Po212 0 0 (default)
    idata[82208] = {'w': 0.01, 'n0': 300.0}
    decay.calculate(parent, time, idata, "testing/log_84216_new.txt")


  @staticmethod
  def make_plot(plot_name, times, activities, time_units, activity_units):
    if(plot_name is not None):
      plt.figure(figsize=[12, 8], dpi=144)
      styles = ['solid', 'dashed', 'dashdot', 'dotted']
      n = 0
      ymin = None
      ymax = None
      for key in activities.keys():
        if(isotopes.is_unstable(key)):          
          plt.plot(times, activities[key], label=isotopes.get_hr(key), ls=styles[n%len(styles)])
          n = n + 1
          if(ymin is None):
            ymin = numpy.amin(activities[key])
          else:
            ymin = min(ymin, numpy.amin(activities[key]))
          if(ymax is None):
            ymax = numpy.amax(activities[key])
          else:
            ymax = max(ymax, numpy.amin(activities[key]))
      ymin = max(ymin * 0.5, 1.0e-8)
      ymax = 2.0 * ymax
      plt.xscale('log')
      plt.yscale('log')
      plt.title('Activity over time')
      plt.xlabel('Time (' + time_units + ')')
      plt.ylabel('Activity (' + activity_units + ')')
      plt.ylim(ymin, ymax)
      plt.legend()
      plt.savefig(plot_name)
      

  @staticmethod
  def run():
    # Run with an input file
    print("##############################################")
    print("#                  DECAY                     #")
    print("#     Radioactive Decay Chain Calculator     #")
    print("#           Decay data from JEFF 3.3         #")
    print("##############################################")
    print()
    
    # Read and check isotope file    
    if(len(sys.argv) < 2):
      print("Specify input file.  Exiting.")
      exit()    
    inp_file = sys.argv[1]
    if(not os.path.isfile(inp_file)):
      print("Input file does not exist.  Exiting.")
      exit()
      
    isotope_file = None
    amounts = None
    time = None
    time_unit = 's'
    time_steps = 1
    material = []
      
    # Read input file  
    fh = open(inp_file, 'r')
    for line in fh:
      line = line.split('#')
      line = line[0].strip()
      if(line != ""):
        if(line[0:8].lower() == "isotopes"):
          isotope_file = line[8:].strip()
        elif(line[0:7].lower() == "amounts"): 
          amounts = line[7:].strip()
        elif(line[0:9].lower() == "time_unit"): 
          time_unit = line[10:].strip()
        elif(line[0:10].lower() == "time_steps"): 
          time_steps = int(line[11:])
        elif(line[0:4].lower() == "time"): 
          time = float(line[5:])
        else:
          d = line.split(" ")
          if(len(d) == 3):
            material.append([d[0], int(d[1]), float(d[2]), 0.0, None])
          elif(len(d) == 4):
            material.append([d[0], int(d[1]), float(d[2]), float(d[3]), None])
    fh.close()
    
    # check isotope file
    if(not os.path.isfile(isotope_file)):
      print("Isotope file does not exist.  Exiting.")
      exit()
    print("Isotope file: ", isotope_file)
    
    # Set isotope file
    decay.set(isotope_file)
    
    # Calculate activity
    activity_results = {}
    start = {}
    production_rate = {}
    
    for n in range(len(material)):
      material[n][4] = isotopes.inp(material[n][0], material[n][1])    
      # If a valid isotope
      if(material[n][4]['ok'] and material[n][4]['valid']):
        isotope_code = material[n][4]['code']
        if(isotope_code not in start.keys()):
          start[isotope_code] = 0.0
        start[isotope_code] = start[isotope_code] + material[n][2] 
        if(isotope_code not in production_rate.keys()):
          production_rate[isotope_code] = 0.0
        production_rate[isotope_code] = production_rate[isotope_code] + material[n][3]         
        parent_production_rate = material[n][3]
        if(amounts == 'activity'):
          parent_activity = material[n][2]
          parent_amount = None
        else:
          parent_activity = None
          parent_amount = material[n][2]  
        r = decay.calculate(isotope_code, time, i_data_in=None, log=None, parent_activity=parent_activity, parent_amount=parent_amount, parent_production_rate=parent_production_rate, custom_chain=None, time_units=time_unit, activity_units=None, time_steps=time_steps, plot_name=None)
        time_array = r['time']
        activity_arrays = r['activity']
        for k in activity_arrays.keys():
          if(k not in activity_results.keys()):
            activity_results[k] = activity_arrays[k]
          else:
            activity_results[k] = activity_results[k] + activity_arrays[k]
       
    # Plot results   
    decay.make_plot(plot_name='results.eps', times=time_array, activities=activity_results, time_units=time_unit, activity_units='')   
    
    # Output results
    fh = open('results.csv', 'w')
    fh.write('Time')
    for key in activity_results.keys():
      if(isotopes.is_unstable(key)):   
        fh.write(',')
        fh.write(isotopes.get_hr(key))
    fh.write('\n')  
    for n in range(len(time_array)):
      fh.write(str(time_array[n]))
      for key in activity_results.keys():
        if(isotopes.is_unstable(key)):   
          fh.write(',')
          fh.write(str(activity_results[key][n]))
      fh.write('\n')
    fh.close()    
      
    #    print(isotopes.get_half_life(isotope_code))
    #    print(isotopes.get_decay_constant(isotope_code))

    fh = open('startend.txt', 'w')
    fh.write("{:16s} {:24s} {:24s} {:24s} {:24s}\n".format("Isotope", "Half Life", "Production Rate", "Start Activity", "End Activity"))
    for key in activity_results.keys():
      if(isotopes.is_unstable(key)):
        s = 0.0
        if(key in start.keys()):
          s = start[key]
        w = 0.0
        if(key in production_rate.keys()):
          w = production_rate[key]
        fh.write("{:16s} {:24.12e} {:24.12e} {:24.12e} {:24.12e}\n".format(isotopes.get_hr(key), isotopes.get_half_life(key), w, s, activity_results[key][-1]))
    fh.close()

def main():
  decay.run()
   
  

if __name__ == "__main__":
    main()    


