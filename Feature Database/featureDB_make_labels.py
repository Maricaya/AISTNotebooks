#!/usr/bin/env python
# coding: utf-8

# In[1]:


import cc3d
import netCDF4
import glob
import numpy
import sys
import datetime
import pickle
import time
import pandas


# In[2]:

flexfs_mountpoint = '/flexfs/bayesics/'
data_dir = flexfs_mountpoint + 'source/GPM/'
            # '/tablespace/xcal/')


# # Loading the data

# In[3]:


def load_imerg(file_path, variable_name):
    netcdf = netCDF4.Dataset(file_path, 'r', format='NETCDF4')
    data = netcdf.groups['Grid'][variable_name][:][0].T[::-1]
    file_header = netcdf.FileHeader.split(';\n')
    file_header.remove('')
    header = {r.split('=')[0]: r.split('=')[1] for r in file_header}
    return data, header


# In[4]:


file_paths = sorted(glob.glob(data_dir + 'IMERG/2021/01/3B-HHR.MS.MRG.3IMERG.20210124-S000000*'))

print("file_paths", file_paths, "\n")

# /flexfs/bayesics/source/GPM/IMERG/2021/01
# IMERG/2021/01/3B-HHR.MS.MRG.3IMERG.20210125*
variable_name = 'precipitationCal'

stack = []
headers = []
timestamps = []
for file_path in file_paths:
    print('{}'.format(len(file_paths)-len(stack)), end='\r')
    sys.stdout.flush()
    data, header = load_imerg(file_path, variable_name)
    stack.append(data)
    headers.append(header)
    timestamps.append(header['StartGranuleDateTime'])
    
data = numpy.array(stack)

timestamps_dt = [datetime.datetime.strptime(date, '%Y-%m-%dT%H:%M:%S.000Z') for date in timestamps]
timestamps_np = numpy.array(timestamps_dt, dtype='datetime64[m]')


# In[5]:


#data = numpy.flip(data, 1)


# In[6]:


with open('./pickles/data.pickle', 'wb') as f:
    pickle.dump(data, f)
    
with open('./pickles/timestamps.pickle', 'wb') as f:
    pickle.dump(timestamps_dt, f)


# In[7]:


with open('./pickles/data.pickle', 'rb') as f:
    imerg = pickle.load(f)


# # Thresholding and CCLs

# In[8]:


data = imerg


# In[9]:


thresh = 0.5
data[data<thresh] = 0
data[data>=thresh] = 1

connectivity = 6 
min_voxels = 1000


# In[10]:


start = time.time()
labels, N = cc3d.connected_components(data, delta=0,connectivity=connectivity, return_N=True)
print(time.time() - start)


# In[11]:


start = time.time()
cc3d.dust(labels, threshold=min_voxels, connectivity=connectivity, in_place=True)
print(time.time() - start)


# In[12]:


label_names = numpy.unique(labels[labels>0])
label_names.shape


# In[13]:


start = time.time()
largest_20, N = cc3d.largest_k(labels, k=20, connectivity=connectivity, delta=0, return_N=True)
largest_100, N = cc3d.largest_k(labels, k=100, connectivity=connectivity, delta=0, return_N=True)
print(time.time() - start)


# # Pickle

# In[14]:


with open('./pickles/largest_20.pickle', 'wb') as f:
    pickle.dump(largest_20, f)
    
with open('./pickles/largest_100.pickle', 'wb') as f:
    pickle.dump(largest_100, f)

with open('./pickles/labels.pickle', 'wb') as f:
    pickle.dump(labels, f)


# In[15]:


1

