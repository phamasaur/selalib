#python $sll_py/multi_thdiag.py thdiag min max dt_value1 dt_value2 ...
#reads thdiag_i.dat for i=min..max
#returns t+str(dt_value1)+val.dat which is composed of lines of thdiag_i.dat at time t=t_value1
import os
import sys
import numpy as np
from scipy.interpolate import griddata

#check that the number of arguments is ok
if(len(sys.argv)<5):
  print("Error: Usage python multi_thdiag.py thdiag min max t_value1 t_value2 ...")
  sys.exit()


thdiag=str(sys.argv[1])
i_min = int(sys.argv[2])
i_max = int(sys.argv[3])

#print("thdiag="+thdiag)
#print("i_min="+str(i_min))
#print("i_max="+str(i_max))

#compute the list of files
list_file=[0 for i in range(i_min,i_max+1)]
for i in range(i_min,i_max+1):
  list_file[i-i_min] = thdiag+"_"+str(i)+".dat"
#print(list_file)  


#check that the files exist
for f in list_file:
  if(not os.path.isfile(f)):
    print("Error: file "+str(f)+" does not exist")
    sys.exit()

array_list=[0 for i in range(i_min,i_max+1)]
#checks that the files exist
for i in range(i_min,i_max+1):
  f = list_file[i-i_min]
  array_list[i-i_min] = np.loadtxt(f,ndmin=2)

num_col = np.size(array_list[0][0,:]) 
num_row = np.size(array_list[0][:,0])  

#print(num_row,num_col)

#check that each file has same num_row and num_col 
for i in range(i_min,i_max+1):
  f = array_list[i-i_min]
  num_col_loc = np.size(f[0,:]) 
  num_row_loc = np.size(f[:,0])
  #if(num_row_loc != num_row):  
  #  print("Error num_row differ for file "+list_file[i-i_min])
  #  print("num_row="+str(num_row)+" num_row_loc="+str(num_row_loc))
  #  sys.exit()
  if(num_col_loc != num_col):  
    print("Error num_col differ for file "+list_file[i-i_min])
    print("num_col="+str(num_col)+" num_col_loc="+str(num_col_loc))
    sys.exit()

for val in sys.argv[4:]:
  time_val = float(val)
  time_grid_ref = [time_val] #array_list[0][:,0]
  array_list_unif=[0 for i in range(i_min,i_max+1)]
  M = np.zeros((i_max-i_min+1,num_col+1))
  for i in range(i_min,i_max+1):
    f = array_list[i-i_min]
    dt = f[1,0]-f[0,0]
    #print("dt=",dt)
    #print(len(time_grid_ref),len(f[:,1]),len(f[:,0]))
    #print(f[:,0])
    array_list_unif[i-i_min] = griddata(f[:,0], f[:,:], time_grid_ref, method='cubic')
    g = array_list_unif[i-i_min][0]
    M[i-i_min,0] = dt
    M[i-i_min,1:] = g
  
  print("t"+str(val)+"val.dat")
  
  np.savetxt("t"+str(val)+"val.dat",M)

  
  

  