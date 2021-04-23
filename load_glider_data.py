#=========================================
# Dependencies

#=================================================================
# Initialize access to PyFerret.
# Understanding the following lines of code is not part of the course.
# Acknowlegements:
# -> Pyferret: NOAA, https://ferret.pmel.noaa.gov/Ferret/
# -> ferretmagic: Patrick Brockmann, https://pypi.org/project/ferretmagic/
# -> These exact lines for running PyFerret on the Bowdoin HPC Grid: DJ Merrill
#=================================================================
import sys
sys.path.append('/mnt/local/pyferret/lib/python3.6/site-packages')
import pyferret
pyferret.addenv(FER_DIR='/mnt/local/pyferret', FER_DAT='/mnt/local/FerretDatasets')
pyferret.start(journal=False, quiet=True, unmapped=True)
import numpy as np
import pandas as pd

#==========================================
# This is a very simple function for the
# purposes of testing.
#==========================================
def add_one(x):
    y = x + 1
    return y

#==========================================
# Function to load glider data from mission
# NetCDF files
#==========================================
# This block of code will load the 
# temperature, salinity, and density
# of the seawater the glider observed
# during a the given dive_number.  The
# source data is in Seaglider mission
# summary NetCDF format.
#
# The outputs of this function are four
# lists: the depth, temperature, salinity,
# and density measured by the glider
# during its dive.
#
# Stefan Gary, 2021
# This code is distributed under the terms
# of the GNU GPL v3 and any later version.
# See LICENSE.txt
#==========================================
def load_mnc_profile(sgid,dive_number):
    # Wipe any previously loaded data and variables in
    # Ferret.  These lines allow for multiple reuse of
    # this function in a given kernel session.
    (e_v, e_m) = pyferret.run('cancel data /all')
    (e_v, e_m) = pyferret.run('cancel variables /all')
    
    # Set a shorter variable name for number of dives.
    # If the glider data has climbs and dives, mult
    # by 2 and subtract 1 to index just the dives.
    dn = dive_number*2 - 1

    # Load the requested data into the notebook
    (e_v, e_m) = pyferret.run(
        'use /mnt/courses/eos1505/sg'+str(sgid)+'/sg'+str(sgid)+'_m03.nc')
    
    # Assign subsets of the data in Ferret - we want to pull out
    # just the data for this particular dive, not the whole mission.
    (e_v, e_m) = pyferret.run('let temp = theta[l='+str(dn)+']')
    (e_v, e_m) = pyferret.run('let salt = salinity[l='+str(dn)+']')
    (e_v, e_m) = pyferret.run('let dens = density[l='+str(dn)+']')
    (e_v, e_m) = pyferret.run('let dept = ctd_depth[l='+str(dn)+']')
            
    # Bring the data from Ferret into the Notebook
    temp = np.squeeze(pyferret.getdata('temp',False)['data'])
    salt = np.squeeze(pyferret.getdata('salt',False)['data'])
    dens = np.squeeze(pyferret.getdata('dens',False)['data'])
    dept = np.squeeze(pyferret.getdata('dept',False)['data'])
    
    # Filter out missing values (usually the placeholder is
    # a very large negative number, 1e-34)
    temp[temp<-4.0] = np.nan
    salt[salt<0] = np.nan
    dens[dens<900] = np.nan

    return dept, temp, salt, dens

#==========================================
# Function to load glider data from 
# Hydrobase format files.
#==========================================
# This block of code will load the 
# temperature, salinity, and density
# of the seawater the glider observed
# during a the given the Seaglider ID and
# dive_number.  Input
# data is in Hydrobase format.
#
# The outputs of this function are four
# lists: the depth, temperature, salinity,
# and density measured by the glider
# during its dive.  The position of the glider
# (lon, lat) and date (year, month, day) 
# is also returned.
#
# Stefan Gary, 2021
# This code is distributed under the terms
# of the GNU GPL v3 and any later version.
# See LICENSE.txt
#==========================================
def load_hb_profile(sgid,dive_number):

    # Read data into a Pandas dataframe (df_)
    # header -> to use the variable list as column headers
    # comment -> for the trailing ** at end of .hb stations
    # delim_whitespace -> enable whitespace delimiter
    df_profile = pd.read_csv(
        '/mnt/courses/eos1505/sg'+str(sgid)+'/p'+str(sgid)+str(dive_number)+'.hb',
        header=1,
        comment='*',  
        delim_whitespace=True)
    
    # Filter out missing values (usually the placeholder is
    # a very large negative number, -9)
    df_profile_filtered = df_profile.replace(
        to_replace=-9.0,
        value=np.nan)

    de = df_profile_filtered['de']
    te = df_profile_filtered['te']
    sa = df_profile_filtered['sa']
    th = df_profile_filtered['th']
    s0 = df_profile_filtered['s0']
    
    # Even nan can be an issue, so drop those too,
    #de = de[~np.isnan(de)]
    #te = te[~np.isnan(te)]
    #sa = sa[~np.isnan(sa)]
    #th = th[~np.isnan(th)]
    #s0 = s0[~np.isnan(s0)]
    
    # Get the lon and lat associated with this profile
    # Also, get the year, month, day.
    df_lonlat = pd.read_csv(
        '/mnt/courses/eos1505/sg'+str(sgid)+'/p'+str(sgid)+str(dive_number)+'.hb',
        nrows=1,
        usecols=[4,5,6,8,9],
        names=["year","month","day","lat","lon"],
        comment='*',  
        delim_whitespace=True)
    
    year = df_lonlat['year']
    month= df_lonlat['month']
    day = df_lonlat['day']
    lon = df_lonlat['lon']
    lat = df_lonlat['lat']
    
    return lon, lat, de, te, sa, th, s0, year, month, day

#==========================================
# Function to load global topography
#==========================================
# This block of code will load the 
# depth of the seafloor and the hieght
# of continents across the globe.
#
# The outputs of this function are 3 quantity
# 2D arrays: lon, lat, and height at each
# pixel.  Negative heights are below sea
# level and positive heights are above
# sea level.
#
# Stefan Gary, 2021
# This code is distributed under the terms
# of the GNU GPL v3 and any later version.
# See LICENSE.txt
#==========================================
def load_topo():
    # Load the data set and store as a Python variable
    # Python dictionaries are a type of variable that
    # stores the data along with its metadata.
    #
    # The pyferret.getdata commands are accessing data
    # by variable name in the given file. If you ever
    # need to explore the available variables in a
    # NetCDF file, use the following command at the
    # *terminal*:
    #
    # ncdump -h /mnt/courses/eos2680/ETOPO1/topo_tenthdeg_ice_gline.nc
    #
    # and all the information about the NetCDF file
    # will be displayed.
    (e_v, e_m) = pyferret.run('cancel data /all')
    (e_v, e_m) = pyferret.run('cancel variables /all')
    (error_value, error_message) = pyferret.run(
        'use /mnt/courses/eos2680/ETOPO1/topo_tenthdeg_ice_gline.nc')
    lon_dict = pyferret.getdata('lon1',False)
    lat_dict = pyferret.getdata('lat1',False)
    topo_dict = pyferret.getdata('z1',False)

    # The "keys" are the names of the entries in the
    # dictionary - its pieces.  You can access the values
    # associated with a dictionary's keys with
    # dict_name['key_name'].
    #print(topo_dict.keys())

    # Put the data into Python arrays
    lon = lon_dict['data']
    lat = lat_dict['data']
    topo = topo_dict['data']

    # And you can see the size of the data array
    # which is a grid in the x, y, directions but
    # the z (depth), time, and other dimensions
    # are placeholder dimensions in that they have
    # only a length of 1.
    #print('Array size:')
    #print(np.shape(topo))

    # To cut out these singleton dimensions, use
    # the squeeze command:
    lon = np.squeeze(lon)
    lat = np.squeeze(lat)
    topo = np.squeeze(topo)

    #print('Array size after squeeze:')
    #print(np.shape(topo))
    
    # Note that all of the above can be condensed
    # into one line, but it's much harder to 
    # understand and verify that the code is working
    # in the condensed version (commented out below).
    #lon = np.squeeze(pyferret.getdata('lon1',False)['data'])
    #lat = np.squeeze(pyferret.getdata('lat1',False)['data'])
    #topo = np.squeeze(pyferret.getdata('z1',False)['data'])
    
    # Finally, lon and lat are given as
    # vectors, for plotting it is easier
    # to expand them into 2D arrays to
    # have the same size as topo.
    [y,x] = np.meshgrid(lat,lon)
    
    return x, y, topo