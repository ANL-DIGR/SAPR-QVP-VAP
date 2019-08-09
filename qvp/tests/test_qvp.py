"""
Unit Test for SAPR_QVP_VAP qvp.quicklooks
and qvp.qvp modules.
"""

import numpy as np
from numpy.testing import assert_equal
import qvp
import glob
import os

def test_qvp_profile():
    # Test qvp.qvp
    input_files = glob.glob('2017*', recursive=True)
    input_files.sort()

    desired_angle = 20.0
    config = 'xsaprqvpI5'
    outdir = '.'
    
    test_qvp = qvp.qvp(files=input_files, desired_angle=desired_angle)

    test_qvp.write(file_directory=outdir, config=config)
    
    assert_equal(os.path.exists('sgpxsaprqvpI5.c1.20171005.000000.nc'), True)
    
def test_qvp_1panel():
    input_file = 'example_qvp.nc'
    config = 'xsaprqvpI5'
    image_directory = '.'
    field = 'corrected_reflectivity'
    
    qvp.quicklooks_1panel(file=input_file, config=config,
                          image_directory=image_directory,
                          field=field)
    
    assert_equal(os.path.exists('sgpxsaprqvpI5.c1.20180831.000000.png'), True)

def test_qvp_4panel():
    input_file = 'example_qvp.nc'
    config = 'xsaprqvpI5'
    fields = ('corrected_reflectivity', 'corrected_differential_reflectivity',
              'corrected_specific_diff_phase', 'cross_correlation_ratio')
    image_directory = '.'
    
    qvp.quicklooks_4panel(file=input_file, config=config,
                          image_directory=image_directory,
                          fields=fields)
    
    assert_equal(os.path.exists('sgpxsaprqvpI5.c1.20180831.000000.png'), True)
    

    
