# encoding: utf-8
"""
createFitsIDI.py
=============

Creates a basic FITS IDI file, with headers created from an XML configuration file.

Created by Danny Price on 2011-04-20.
Copyright (c) 2011 The University of Oxford. All rights reserved.

"""

# Required modules
import sys, os
import astropy.io.fits as pf, numpy as np
from lxml import etree

# modules from this package
from pyFitsidi import *


def main():
  """
  Generate a blank FITS IDI file.
  """
  
  # What are the filenames for our datasets?
  fitsfile = 'blank.fits'
  config   = 'config/config.xml'
  
  # Make a new blank FITS HDU
  print('Creating Primary HDU')
  print('------------------------------------\n')
  hdu = make_primary(config)
  print repr(hdu.header)
  
  # Go through and generate required tables
  print('\nCreating ARRAY_GEOMETRY')
  print('------------------------------------')
  tbl_array_geometry = make_array_geometry(config=config, num_rows=32)
  print repr(tbl_array_geometry.header)

  print('\nCreating FREQUENCY')
  print('------------------------------------')
  tbl_frequency = make_frequency(config=config, num_rows=1)
  print repr(tbl_frequency.header)

  print('\nCreating SOURCE')
  print('------------------------------------')
  tbl_source = make_source(config=config, num_rows=1)
  print repr(tbl_source.header)

  print('\nCreating ANTENNA')
  print('------------------------------------')
  tbl_antenna = make_antenna(config=config, num_rows=32)
  print repr(tbl_antenna.header)

  print('\nCreating UV_DATA')
  print('------------------------------------')
  # Number of rows req. depends on num. time dumps and num. of baselines
  # Once you have data, it would be worth setting these dimensions automatically
  # For now, we're hard-wiring in 1 time dump, 528 baselines (32 element array)
  (t_len, bl_len) = (1,528) 
  tbl_uv_data = make_uv_data(config=config, num_rows=t_len*bl_len)
  print repr(tbl_antenna.header)

  print('\nCreating HDU list')
  print('------------------------------------')  
  hdulist = pf.HDUList(
              [hdu, 
              tbl_array_geometry,
              tbl_frequency,
              tbl_antenna,
              tbl_source, 
              tbl_uv_data
              ])
  
  print('\nVerifying integrity...')            
  hdulist.verify()
  
  if(os.path.isfile(fitsfile)):
    print('Removing existing file %s...')%fitsfile
    os.remove(fitsfile)
  print('Writing to file %s...')%fitsfile
  hdulist.writeto(fitsfile)

  print('Done.')


if __name__ == '__main__':
  main()
