#!/usr/bin/env python
# coding: utf-8

# In[2]:


import os
os.environ['PROJ_LIB'] = '/usr/local/share/proj/'

import pandas
import starepandas
import pystare
import netCDF4
import pickle
import numpy
import shapely
import geopandas
import starepandas
import sqlalchemy
import dask


# In[3]:


n_workers = 62
flexfs_mountpoint = '/flexfs/bayesics'
data_dir = flexfs_mountpoint + '/tablespace/xcal/'


# In[4]:


print(starepandas.__version__)


# # Load Labels

# In[5]:


with open('./pickles/timestamps.pickle', 'rb') as f:
    timestamps = pickle.load(f)
    
with open('./pickles/data.pickle', 'rb') as f:
    data = pickle.load(f)

with open('./pickles/largest_100.pickle', 'rb') as f:
    labels = pickle.load(f)
    
#with open('{}/pickles/labels.pickle'.format(data_dir), 'rb') as f:
#    labels = pickle.load(f)


# In[6]:


#length = 10
#timestamps = timestamps[0:length]
#labels = labels[0:length]
#data = data[0:length]


# # Load STARE Sidecar

# ## Adapt in lat direction

# In[7]:


lats = numpy.tile(numpy.arange(-89.95, 90, 0.1), (3600, 1))
lats = numpy.ascontiguousarray(numpy.flip(lats).transpose())

lons = numpy.tile(numpy.arange(-179.95, 180, 0.1), (1800, 1))
lons = numpy.ascontiguousarray(lons)

sids = pystare.from_latlon_2d(lats, lons, adapt_level=True)
res = pystare.spatial_resolution(sids)
sidecar = pystare.spatial_coerce_resolution(sids, res-1)


# ## Adapt in lon direction

# In[8]:


lats = numpy.tile(numpy.arange(-89.95, 90, 0.1), (3600, 1))
lats = numpy.ascontiguousarray(numpy.flip(lats))

lons = numpy.tile(numpy.arange(-179.95, 180, 0.1), (1800, 1))
lons = numpy.ascontiguousarray(lons.transpose())

sids = pystare.from_latlon_2d(lats, lons, adapt_level=True).transpose()
res = pystare.spatial_resolution(sids)
sidecar = pystare.spatial_coerce_resolution(sids, res-1)


# # Create Areas with haversine formula:
# 
# - We assume one degree latitude to be constantly ```R * Δφ```. For 0.1 degrees, this is +-11 km
# - The 0.1 degree
# 
# ```
# a = sin²(Δφ/2) + cos φ1 ⋅ cos φ2 ⋅ sin²(Δλ/2)
# c = 2 ⋅ atan2( √a, √(1−a) )
# d = R ⋅ c
# ```

# In[9]:


def lon_dist(lats, r, delta_lon):    
    a = numpy.cos(numpy.radians(lats))**2 * numpy.sin(numpy.radians(delta_lon))**2
    c = numpy.arctan2(numpy.sqrt(a), numpy.sqrt(1-a))
    d_lon = r*c 
    return d_lon

r = 6371e3

lats0 = numpy.ascontiguousarray(numpy.tile(numpy.arange(-90, 90, 0.1), (3600, 1)).transpose())
lats1 = numpy.ascontiguousarray(numpy.tile(numpy.arange(-89.9, 90.1, 0.1), (3600, 1)).transpose())

delta_lon = 0.1
a = lon_dist(lats0, r, delta_lon)
b = lon_dist(lats1, r, delta_lon)

delta_lat = 0.1
h = r * numpy.radians(delta_lat) 
areas = (a+b)/2 * h # square meters


# # Create STAREDF

# In[10]:


def make_row(label, timestep):
    x, y = (labels[timestep]==label).nonzero()
    sids = sidecar[x, y]
    area = areas[x, y]
    precip = data[timestep, x, y]
    tot_precip = sum(area * precip/1000/2) # Convert from mm to m and multipy by two because it is a half-hour
    row = {'label': label,            
           'timestep': timestep, 
           'timestamp': timestamps[timestep],                                  
           'x': x, 'y': y,
           'cell_areas': area,
           'tot_area':  sum(areas[x, y]),
           'precips': precip,           
           'tot_precip': tot_precip, # cubic meters
           'sids': sids}
    return row

def make_label_sdf(label):
    rows = []
    for timestep in range(len(timestamps)):
        row = make_row(label=label, timestep=timestep)
        if len(row['sids']) > 0:
            rows.append(row)
    sdf = starepandas.STAREDataFrame(rows, sids='sids')
    return sdf


# In[11]:


label_names = numpy.unique(labels[labels>0])
print(label_names)


# In[ ]:


sdfs = []
for label in label_names:
    print(label)
    sdf = make_label_sdf(label=label)
    cover = sdf.stare_dissolve(by='timestep', num_workers=n_workers*10)['sids'].rename('cover')
    sdf = sdf.set_index('timestep').join(cover)    
    sdfs.append(sdf)


# In[ ]:


merged = pandas.concat(sdfs, ignore_index=True)
merged.set_sids('cover', inplace=True)


# In[ ]:


with open('./pickles/featuredb.pickle', 'wb') as f:
    pickle.dump(merged, f)


# In[ ]:


with open('./pickles/featuredb.pickle', 'rb') as f:
    merged = pickle.load( f)


# # Making geometries

# In[ ]:


trixels = merged.make_trixels(num_workers=n_workers*10, wrap_lon=False)


# ## Splitting Antimeridian

# In[ ]:


merged.set_trixels(trixels, inplace=True)
merged.split_antimeridian(inplace=True, drop=True, n_workers=n_workers*10)
merged.set_geometry('trixels', inplace=True, crs='EPSG:4326')


# In[ ]:


merged[merged.timestamp=='2021-01-24 00:00:00'].plot()


# In[ ]:


with open('./pickles/featuredb.pickle', 'wb') as f:
    pickle.dump(merged, f)


# In[ ]:


with open('./pickles/featuredb.pickle', 'rb') as f:
    merged = pickle.load( f)


# ## Write to gpkg

# In[ ]:


import copy 
# Only taking n 
sdf = copy.copy(merged[merged.label<=99])

sdf['sids_s'] = sdf.apply(lambda row : str(list(row['sids'])), axis = 1)
sdf['cover_s'] = sdf.apply(lambda row : str(list(row['cover'])), axis = 1)
sdf['precip_s'] = sdf.apply(lambda row : str(list(row['precips'])), axis = 1)
sdf['areas_s'] = sdf.apply(lambda row : str(list(row['cell_areas'])), axis = 1)
sdf['x_s'] = sdf.apply(lambda row : str(list(row['x'])), axis = 1)
sdf['y_s'] = sdf.apply(lambda row : str(list(row['y'])), axis = 1)

sub_df = sdf[['label','timestamp', 'sids_s', 'cover_s', 'precip_s', 'areas_s', 'x_s', 'y_s', 'trixels']]
sub_df.to_file('./pickles/featuredb.gpkg', driver='GPKG')


# # Create daily aggregate

# In[ ]:


merged['date'] = merged['label'].astype('str') + '_' + merged['timestamp'].dt.date.astype('str')


# In[ ]:


dates = merged.stare_dissolve(by='date', num_workers=n_workers*10)

trixels = dates.make_trixels(num_workers=n_workers*10, wrap_lon=False)
dates.set_trixels(trixels, inplace=True)
dates.split_antimeridian(inplace=True, drop=True)
dates.set_geometry('trixels', inplace=True, crs='EPSG:4326')


# In[ ]:


tot = merged[['date', 'tot_area', 'tot_precip']].groupby(by='date').agg('sum')
dates = dates[['label', 'timestamp', 'sids', 'trixels']].join(tot)


# In[ ]:


with open('./pickles/dates.pickle', 'wb') as f:
    pickle.dump(dates, f)


# In[ ]:


dates['sids'] = dates.apply(lambda row : str(list(row['sids'])), axis=1)
dates.to_file('./pickles/dates.gpkg', driver='GPKG')


# In[ ]:


#dates['sids'] = dates.apply(lambda row: row['sids'].strip('][').split(', '), axis=1)
#dates['sids'] = dates['sids'].apply(lambda row: list(map(int, row)))


# In[ ]:


1


# In[ ]:




