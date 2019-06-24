"""
Configuration file for the Quasi Vertical Profile (QVP)

The values for a number of parameters that change depending on which radar is
being used.

"""



#############################################################################
# Default metadata
# 
# The DEFAULT_METADATA dictionary contains dictionaries which provide the
# default metadata for each vad file.
#############################################################################

_DEFAULT_METADATA = {
    #X-SAPR I4 QVP metadata
    'xsaprqvpI4': {
        'Convention' : 'ARM-1.2',
        'vap_name' : 'qvp',
        'sweep_angle' : '20.0 degrees',
        'instrument_name' : 'X-SAPR Quasi Vertical Profile',
        'process_version' : 'EVAL-0.5',
        'dod_version' : 'v1.0',
        'site_id' : 'SGP',
        'platform_id' : 'xsaprqvp',
        'facility_id' : 'I4 : Billings, OK',
        'data_level' : 'c1',
        'location_description' : (
            'Southern Great Plains (SGP)',
            'Garber, Oklahoma'),
        'datastream' : 'sgpxsaprqvpI4.c1',
        'doi' : '10.5439/1506645',
        'input_datastream' : 'sgpadicmac2I4.c1'},
    
    #X-SAPR I5 QVP metadata
    'xsaprqvpI5':{
        'Convention' : 'ARM-1.2',
        'vap_name' : 'qvp',
        'sweep_anlge' : '20.0 degrees',
        'instrument_name' : 'X-SAPR Quasi Vertical Profile',
        'process_version' : 'EVAL-0.5',
        'dod_version' : 'v1.0',
        'site_id' : 'SGP',
        'platform_id' : 'xsaprqvp',
        'facility_id' : 'I5 : Garber, OK',
        'data_level' : 'c1',
        'location_description' : (
            'Southern Great Plains (SGP)',
            'Garber, Oklahoma'),
        'datastream' : 'sgpxsaprqvpI5.c1',
        'doi' : '10.5439/1506645',
        'input_datastream' : 'sgpadicmac2I5.c1'},
    
    #X-SAPR I6 QVP metadata
    'xsaprqvpI6':{
        'Convention' : 'ARM-1.2',
        'vap_name' : 'qvp',
        'sweep_angle' : '20.0 degrees',
        'instrument_name' : 'X-SAPR Quasi Vertical Profile',
        'process_version' : 'EVAL-0.5',
        'dod_version' : 'v1.0',
        'site_id' : 'SGP',
        'platform_id' : 'xsaprqvp',
        'facility_id' : 'I6 : Deer Creek, OK',
        'data_level' : 'c1',
        'location_description' : (
            'Southern Great Plains (SGP)',
            'Garber, Oklahoma'),
        'datastream' : 'sgpxsaprqvpI6.c1',
        'doi' : '10.5439/1506645',
        'input_datastream' : 'sgpadicmac2I6.c1'}
}

###########################################################################
# Default plot values
#
# The DEFAULT_PLOT_VALUES dictionary contains dictionaries for radars that
# contains parameter values in the VAD quicklooks. Values in these radar
# dictionaries are used for defininf specifications for plotting specific
# radars. These values are all used within vad_quicklooks.py.
###########################################################################
import numpy as np
import matplotlib
import pyart

cmap = pyart.graph.cm_colorblind.HomeyerRainbow

_DEFAULT_PLOT_VALUES = {
    # X-SAPR I4 QVP plot values
    'xsaprqvpI4':{
        'save_name': 'sgpxsaprqvpI4.c1',
        'facility': 'I4',
        'title': 'SGP X-SAPR I4 QVP Profile ',
        'tilt': '20.0 degrees',
        'cmap': cmap},
    
    # X-SAPR I5 QVP plot values
    'xsaprqvpI5':{
        'save_name': 'sgpxsaprqvpI5.c1',
        'facility': 'I5',
        'title': 'SGP X-SAPR I5 QVP Profile ',
        'tilt': '20.0 degrees',
        'cmap': cmap},
    
    # X-SAPR I6 QVP plot values
    'xsaprqvpI6':{
        'save_name': 'sgpxsaprqvpI6.c1',
        'facility': 'I6',
        'title': 'SGP X-SAPR I6 QVP Profile ',
        'tilt': '20.0 degrees',
        'cmap': cmap}
}

_DEFAULT_FIELD_PARAMETERS = {
    # Field titles for radar fields
    'total_power':{'fld_title': 'Reflectivity',
                   'clb_title': 'Mean Reflectivity \nFactor (dBZ)',
                   'vmin':-20,
                   'vmax':64},
    'reflectivity':{'fld_title': 'Reflectivity',
                    'clb_title': 'Mean Reflectivity \nFactor (dBZ)',
                    'vmin': -20,
                    'vmax': 64},
    'velocity':{'fld_title': 'Doppler Velocity',
                'clb_title': 'Mean Doppler Velocity (m/s)',
                'vmin': None,
                'vmax': None},
    'spectrum_width':{'fld_title': 'Doppler Spectrum Width',
                      'clb_title': 'Mean Doppler \nSpectrum Width (m/s)',
                      'vmin': None,
                      'vmax': None},
    'differential_reflectivity':{'fld_title': 'Differential Reflectivity',
                                 'clb_title': 'Mean Differential \nReflectivity Factor (dB)',
                                 'vmin': None,
                                 'vmax': None},
    'specific_differential_phase':{'fld_title': 'Specific Differential Phase',
                                   'clb_title': 'Mean Specific \nDifferential Phase (deg/km)',
                                   'vmin': None,
                                   'vmax': None},
    'cross_correlation_ratio':{'fld_title': 'Correlation Coefficient Ratio',
                               'clb_title': 'Mean Correlation \nCofficient',
                               'vmin': 0,
                               'vmax': 1},
    'normalized_coherent_power':{'fld_title': 'Normalized Coherent Power',
                                 'clb_title': 'Mean Normalized \nCoherent Power',
                                 'vmin': None,
                                 'vmax': None},
    'differential_phase':{'fld_title': 'Differential Phase',
                          'clb_title': 'Mean Differential \nPhase (deg)',
                          'vmin': None,
                          'vmax': None},
    'xsapr_clutter':{'fld_title': 'X-SAPR Clutter',
                     'clb_title': 'Mean X-SAPR Clutter',
                     'vmin': None,
                     'vmax': None},
    'signal_to_noise_natio':{'fld_title': 'Signal to Noise Ratio',
                             'clb_title': 'Mean Signal to \nNoise Ratio',
                             'vmin': None,
                             'vmax': None},
    'velocity_texture':{'fld_title': 'Doppler Velocity Texture',
                        'clb_title': 'Mean Doppler \nVelocity Texture (m/s)',
                        'vmin': None,
                        'vmax': None},
    'gate_id':{'fld_title': 'Classification of Dominant Scatter',
               'clb_title': 'Classification of \nDominant Scatter',
               'vmin': None,
               'vmax': None},
    'radar_echo_classification':{'fld_title': 'Radar Echo Classification',
                                 'clb_title': 'Radar Echo Classification',
                                 'vmin': None,
                                 'vmax': None},
    'corrected_velocity':{'fld_title': 'Corrected Doppler Velocity',
                          'clb_title': 'Mean Doppler Velocity (m/s)',
                          'vmin': None,
                          'vmax': None},
    'unfolded_differential_phase':{'fld_title': 'Unfolded Differential Phase',
                                   'clb_title': 'Mean Differential \nPhase (deg)',
                                   'vmin': None,
                                   'vmax': None},
    'corrected_differential_phase':{'fld_title': 'Corrected Differential Phase',
                                    'clb_title': 'Mean Doppler Velocity (m/s)',
                                    'vmin': None,
                                    'vmax': None},
    'filtered_corrected_differential_phase':{'fld_title': 'Filtered Corrected Differential Phase',
                                             'clb_title': 'Mean Differential \nPhase (deg)',
                                             'vmin': None,
                                             'vmax': None},
    'corrected_specific_diff_phase':{'fld_title': 'Corrected Specific Differential Phase',
                                     'clb_title': 'Mean Specific \nDiff Phase (deg/km)',
                                     'vmin': None,
                                     'vmax': None},
    'filtered_corrected_specific_diff_phase':{'fld_title': 'Filtered Corrected Specific Differential Phase',
                                              'clb_title': 'Mean Specific \nDiff Phase (deg/km)',
                                              'vmin': None,
                                              'vmax': None},
    'corrected_differential_reflectivity':{'fld_title': 'Corrected Differential Reflectivity',
                                           'clb_title': 'Mean Differential \nReflectivity Factor (dB)',
                                           'vmin': None,
                                           'vmax': None},
    'corrected_reflectivity':{'fld_title': 'Corrected Reflectivity',
                              'clb_title': 'Mean Reflectivity \nFactor (dBZ)',
                              'vmin': -20,
                              'vmax': 64},
    'specific_attenuation':{'fld_title': 'Specific Attenuation',
                            'clb_title': 'Mean Specific \nAttenuation (dB/km)',
                            'vmin': None,
                            'vmax': None},
    'path_integrated_attenuation':{'fld_title': 'Path Integrated Attenuation',
                                   'clb_title': 'Mean Path Integrated \nAttenuation (dB)',
                                   'vmin': None,
                                   'vmax': None},
    'specific_differential_attenuation':{'fld_title': 'Specific Differential Attenuation',
                                         'clb_title': 'Mean Specific \nDiff Attenuation (db/km)',
                                         'vmin': None,
                                         'vmax': None},
    'path_integrated_differential_attenuation':{'fld_title': 'Path Integrated Defferential Attenuation',
                                                'clb_title': 'Mean Path Integrated \nDeff Attenuation (dB)',
                                                'vmin': None,
                                                'vmax': None},
    'rain_rate_A':{'fld_title': 'Rainfall Rate',
                   'clb_title': 'Mean Rain \nFall Rate (mm/hr)',
                   'vmin': None,
                   'vmax': None}
}