import numpy as np
import numpy.ma as ma
import pandas as pd
import pyart
import xarray
import netCDF4
import datetime
import sys
import socket
import os

from .config import get_metadata

class qvp():

    def __init__(self, files, desired_angle=None, fields=None):
        self.time = []
        self.base_time = []
        self.range = []
        self.total_power = []
        self.reflectivity = []
        self.velocity = []
        self.spectrum_width = []
        self.differential_reflectivity = []
        self.specific_differential_phase = []
        self.cross_correlation_ratio = []
        self.normalized_coherent_power = []
        self.differential_phase = []
        self.xsapr_clutter = []
        self.velocity_texture = []
        self.gate_id = []
        self.corrected_velocity = []
        self.unfolded_differential_phase = []
        self.corrected_differential_phase = []
        self.filtered_corrected_differential_phase = []
        self.corrected_specific_diff_phase = []
        self.filtered_corrected_specific_diff_phase = []
        self.corrected_differential_reflectivity = []
        self.specific_attenuation = []
        self.signal_to_noise_ratio = []
        self.corrected_reflectivity = []
        self.radar_echo_classification = []
        self.path_integrated_attenuation = []
        self.specific_differential_attenuation = []
        self.path_integrated_differential_attenuation = []
        self.rain_rate_A = []
        
        self.desired_angle = desired_angle
        self.fields = fields
        
        self.create_qvp(files)

    def create_qvp(self, files, **kwargs):
        """
        
        """
        for file in files:
            try:
                radar = pyart.io.read(file)
            except TypeError:
                continue
            

            time = netCDF4.num2date(radar.time['data'][0],
                                    radar.time['units'])
            rtime = datetime.datetime.strftime(
                time, '%Y-%m-%dT%H:%M:%S')
            qvp = pyart.retrieve.quasi_vertical_profile(
                radar, self.desired_angle, self.fields, **kwargs)
            
            self.time.append(rtime)
            self.base_time.append(time)
            self.range.append(qvp['range'])
            self.total_power.append(qvp['total_power'])
            self.reflectivity.append(qvp['reflectivity'])
            self.velocity.append(qvp['mean_doppler_velocity'])
            self.spectrum_width.append(qvp['spectral_width'])
            self.differential_reflectivity.append(qvp['differential_reflectivity'])
            self.specific_differential_phase.append(qvp['specific_differential_phase'])
            self.cross_correlation_ratio.append(qvp['cross_correlation_ratio_hv'])
            self.normalized_coherent_power.append(qvp['normalized_coherent_power'])
            self.differential_phase.append(qvp['differential_phase'])
            self.xsapr_clutter.append(qvp['ground_clutter'])
            self.velocity_texture.append(qvp['velocity_texture'])
            self.gate_id.append(qvp['gate_id'])
            self.corrected_velocity.append(qvp['corrected_velocity'])
            self.unfolded_differential_phase.append(qvp['unfolded_differential_phase'])
            self.corrected_differential_phase.append(
                qvp['corrected_differential_phase'])
            self.filtered_corrected_differential_phase.append(
                qvp['filtered_corrected_differential_phase'])
            self.corrected_specific_diff_phase.append(
                qvp['corrected_specific_diff_phase'])
            self.filtered_corrected_specific_diff_phase.append(
                qvp['filtered_corrected_specific_diff_phase'])
            self.corrected_differential_reflectivity.append(
                qvp['corrected_differential_reflectivity'])
            self.specific_attenuation.append(qvp['specific_attenuation'])
            self.signal_to_noise_ratio.append(qvp['SNR'])
            self.corrected_reflectivity.append(qvp['corrected_reflectivity'])
            
            if 'radar_echo_classification' in list(radar.fields.keys()):
                self.radar_echo_classification.append(qvp['radar_echo_classification'])
                
            self.path_integrated_attenuation.append(qvp['path_integrated_attenuation'])
            self.specific_differential_attenuation.append(
                qvp['specific_differential_attenuation'])
            self.path_integrated_differential_attenuation.append(
                qvp['path_integrated_differential_attenuation'])
            self.rain_rate_A.append(qvp['rain_rate_A'])
            self.height = qvp['height']
            self.alt = radar.altitude['data']
            self.lon = radar.longitude['data']
            self.lat = radar.latitude['data']
            
            del qvp
            del radar
        
    def write(self, config, file_directory=None):
        if file_directory is None:
            file_directory = os.path.expanduser('~')
        
        attributes = get_metadata(config)
        
        ds = xarray.Dataset()
        ds['base_time'] = xarray.Variable('base_time', ma.array([netCDF4.date2num(
            self.base_time[0], 'seconds since 1970-1-1 0:00:00 0:00')], dtype=np.int32),
                                  attrs={'string': datetime.datetime.strftime(
                                      self.base_time[0], '%d-%b-%Y,%H:%M:%S GMT'),
                                         'units': 'seconds since 1970-1-1 0:00:00 0:00',
                                         'long_name': 'Base time in Epoch',
                                         'ancillary_variables': 'time_offset',
                                         'calendar': 'gregorian'})
        ds['time_offset'] = xarray.Variable('time',
                                            ma.array(self.time, dtype='datetime64[ns]'),
                                             attrs={'long_name': 'Time offset from base_time',
                                                    'ancillary_variables': 'base_time'})
        ds['time'] = xarray.Variable(['time'],
                                     ma.array(self.time, dtype='datetime64[ns]'),
                                     attrs={'long_name': 'Time offset from midnight', 
                                            'standard_name': 'time'})
        ds['height'] = xarray.Variable(['height'],
                                       ma.array(self.height),
                                       attrs={'stadard_name': 'height',
                                              'units': 'meters',
                                              'long_name': 'Height above ground',
                                              '_FillValue': False})
        ds['total_power'] = xarray.Variable(['time', 'height'],
                                            ma.array(self.total_power), 
                                            attrs={'units': 'dBZ', 
                                                   'long_name': 'Total power', 
                                                   'standard_name': 'equivalent_reflectivity_factor',
                                                   '_FillValue': -9999})
        ds['reflectivity'] = xarray.Variable(['time', 'height'],
                                             ma.array(self.reflectivity), 
                                             attrs={'units': 'dBZ', 
                                                    'long_name': 'Reflectivity',
                                                    'standard_name': 'equivalent_reflectivity_factor',
                                                    '_FillValue': -9999})
        ds['velocity'] = xarray.Variable(['time', 'height'],
                                          ma.array(self.velocity), 
                                         attrs={'units': 'm/s', 
                                                'long_name': 'Mean doppler velocity', 
                                                'standard_name': 'radial_velocity_of_scatterers_away_from_instrument',
                                                '_FillValue': -9999})
        ds['spectrum_width'] = xarray.Variable(['time', 'height'],
                                               ma.array(self.spectrum_width),
                                               attrs={'units': 'm/s', 
                                                      'long_name': 'Doppler spectrum width',
                                                      '_FillValue': -9999})
        ds['differential_reflectivity'] = xarray.Variable(['time', 'height'],
                                                          ma.array(self.differential_reflectivity), 
                                                          attrs={'units': 'dB', 
                                                                 'long_name': 'Differential reflectivity',
                                                                 '_FillValue': -9999})
        ds['specific_differential_phase'] = xarray.Variable(['time', 'height'],
                                                            ma.array(self.specific_differential_phase), 
                                                            attrs={'units': 'degree/km', 
                                                                   'long_name': 'Specific differential phase (KDP)',
                                                                   '_FillValue': -9999})
        ds['cross_correlation_ratio'] = xarray.Variable(['time', 'height'],
                                                        ma.array(self.cross_correlation_ratio), 
                                                        attrs={'units': '1', 
                                                               'long_name': 'Cross correlation ratio (RHOHV)', 
                                                               'valid_max': 1.0,
                                                               'valid_min': 0.0,
                                                               '_FillValue': -9999})
        ds['normalized_coherent_power'] = xarray.Variable(['time', 'height'],
                                                          ma.array(self.normalized_coherent_power),
                                                          attrs={'units': '1', 
                                                                 'long_name': 'Normalized coherent power',
                                                                 'valid_max': 1.0,
                                                                 'valid_min': 0.0, 
                                                                 'comment': 'Also known as signal quality index (SQI)',
                                                                 '_FillValue': -9999})
        ds['differential_phase'] = xarray.Variable(['time', 'height'],
                                                   ma.array(self.differential_phase),
                                                   attrs={'units': 'degree', 
                                                          'long_name': 'Differential phase (PhiDP)',
                                                          'valid_max': 180.0,
                                                          'valid_min': -180.0,
                                                          '_FillValue': -9999})
        ds['xsapr_clutter'] = xarray.Variable(['time', 'height'],
                                              ma.array(self.xsapr_clutter), 
                                              attrs={'units': '1', 
                                                     'long_name': 'X-SAPR clutter', 
                                                     'flag_values': '0,1',
                                                     'flag_meanings': 'no_clutter, clutter',
                                                     '_FillValue': -9999})
        ds['signal_to_noise_ratio'] = xarray.Variable(['time', 'height'],
                                                      ma.array(self.signal_to_noise_ratio),
                                                      attrs={'units': 'dB', 
                                                             'long_name': 'Signal to noise ratio',
                                                             '_FillValue': -9999})
        ds['velocity_texture'] = xarray.Variable(['time', 'height'],
                                                 ma.array(self.velocity_texture),
                                                 attrs={'units': 'm/s', 
                                                        'long_name': 'Mean doppler velocity texture',
                                                        'standard_name': 'radial_velocity_of_scatters_away_from_instrument',
                                                        '_FillValue': -9999})
        ds['gate_id'] = xarray.Variable(['time', 'height'],
                                        ma.array(self.gate_id),
                                        attrs={'units': '1', 
                                               'long_name': 'Classification of dominant scatter',
                                               'flag_values': '0,,1,,2, 3, 4, 5', 
                                               'flag_meanings': 'multi_trip, rain, snow, no_scatter, melting, clutter',
                                               'valid_min': 0, 'valid_max': 5,
                                               '_FillValue': -9999})
        
        if self.radar_echo_classification:
            ds['radar_echo_classification'] = xarray.Variable(['time', 'height'],
                                                              ma.array(self.radar_echo_classification),
                                                              attrs={'units': '1',
                                                                     'long_name': 'Radar echo classification',
                                                                     'flag_values': '0, 1, 2, 3, 4, 5, 6, 255, 65535',
                                                                     'flag_meanings': ('no_data_available, non_meteorological_target,'
                                                                                       + ' rain, wet_snow, snow, graupel, hail,'
                                                                                       + ' area_not_scanned, area_not_scanned'),
                                                                     '_FillValue': -9999})
            
        ds['corrected_velocity'] = xarray.Variable(['time', 'height'],
                                                   ma.array(self.corrected_velocity),
                                                   attrs={'units': 'm/s', 
                                                          'long_name': 'Corrected mean doppler velocity',
                                                          'standard_name': 'radial_velocity_of_scatterers_away_from_instrument',
                                                          'valid_min': ma.array(self.corrected_velocity).min(), 
                                                          'valid_max': ma.array(self.corrected_velocity).max(),
                                                          '_FillValue': -9999})
        ds['unfolded_differential_phase'] = xarray.Variable(['time', 'height'],
                                                            ma.array(self.unfolded_differential_phase),
                                                            attrs={'units': 'degree', 
                                                                   'long_name': 'Unfolded differential phase (PhiDP)',
                                                                   'valid_max': 180.0,
                                                                   'valid_min': -180.0,
                                                                   '_FillValue': -9999})
        ds['corrected_differential_phase'] = xarray.Variable(['time', 'height'],
                                                             ma.array(self.corrected_differential_phase),
                                                             attrs={'units': 'degree', 
                                                                    'long_name': 'Corrected differential phase (PhiDP)',
                                                                    'valid_max': 400.0,
                                                                    'valid_min': 0.0,
                                                                    '_FillValue': -9999})
        ds['filtered_corrected_differential_phase'] = xarray.Variable(['time', 'height'],
                                                                      ma.array(self.filtered_corrected_differential_phase),
                                                                      attrs={'units': 'degree', 
                                                                             'long_name': 'Filtered differential phase (PhiDP)',
                                                                             'valid_max': 400.0,
                                                                             'valid_min': 0.0,
                                                                             '_FillValue': -9999})
        ds['corrected_specific_diff_phase'] = xarray.Variable(['time', 'height'],
                                                              ma.array(self.corrected_specific_diff_phase),
                                                              attrs={'units': 'degrees/km', 
                                                                     'long_name': 'Corrected specific differential phase (KDP)',
                                                                     '_FillValue': -9999})
        ds['filtered_corrected_specific_diff_phase'] = xarray.Variable(['time', 'height'],
                                                                       ma.array(self.filtered_corrected_specific_diff_phase),
                                                                       attrs={'units': 'degree/km', 
                                                                              'long_name': 'Filtered specific differential phase (KDP)',
                                                                              '_FillValue': -9999})
        ds['corrected_differential_reflectivity'] = xarray.Variable(['time', 'height'],
                                                                    ma.array(self.corrected_differential_reflectivity),
                                                                    attrs={'units': 'dB', 
                                                                           'long_name': 'Corrected differential reflectivity',
                                                                           '_FillValue': -9999})
        ds['corrected_reflectivity'] = xarray.Variable(['time', 'height'],
                                                       ma.array(self.corrected_reflectivity),
                                                       attrs={'units': 'dBZ', 
                                                              'long_name': 'Corrected reflectivity',
                                                              'standard_name': 'equivalent_reflectivity_factor',
                                                              '_FillValue': -9999})
        ds['specific_attenuation'] = xarray.Variable(['time', 'height'],
                                                     ma.array(self.specific_attenuation),
                                                     attrs={'units': 'dB/km', 
                                                            'long_name': 'Specific attenuation',
                                                            'valid_min': 0.0,
                                                            'valid_max': 1.0,
                                                            '_FillValue': -9999})
        ds['path_integrated_attenuation'] = xarray.Variable(['time', 'height'],
                                                            ma.array(self.path_integrated_attenuation),
                                                            attrs={'units': 'dB', 
                                                                   'long_name': 'Path integrated attenuation',
                                                                   '_FillValue': -9999})
        ds['specific_differential_attenuation'] = xarray.Variable(['time', 'height'],
                                                                  ma.array(self.specific_differential_attenuation),
                                                                  attrs={'units': 'dB/km', 
                                                                         'long_name': 'Specific differential attenuation',
                                                                         '_FillValue': -9999})
        ds['path_integrated_differential_attenuation'] = xarray.Variable(['time', 'height'],
                                                                         ma.array(self.path_integrated_differential_attenuation),
                                                                         attrs={'units': 'dB', 
                                                                                'long_name': 'Path integrated differential attenuation',
                                                                                '_FillValue': -9999})
        ds['rain_rate_A'] = xarray.Variable(['time', 'height'],
                                            ma.array(self.rain_rate_A),
                                            attrs={'units': 'mm/hr', 
                                                   'long_name': 'Rainfall rate',
                                                   'standard_name': 'rainfall_rate', 
                                                   'valid_min': 0.0,
                                                   'valid_max': 400.0, 
                                                   'comment': 'Rain rate calculated from specific_attenuation' + 
                                                              ' R=51.3*specific_attenuation**0.81, note R=0.0' + 
                                                              ' where norm coherent power < 0.4 or rhohv < 0.8',
                                                   '_FillValue': -9999})
        ds['lon'] = xarray.Variable('longitude',
                                    ma.array(self.lon),
                                    attrs={'long_name': 'East longitude', 
                                           'units': 'degree_E',
                                           'standard_name': 'longitude', 
                                           'valid_min': -180.0,
                                           'valid_max': 180.0,
                                           '_FillValue': False})
        ds['lat'] = xarray.Variable('latitude',
                                    ma.array(self.lat),
                                    attrs={'long_name': 'North latitude', 
                                           'units': 'degree_N',
                                           'standard_name': 'latitude', 
                                           'valid_min': -90.0,
                                           'valid_max': 90.0,
                                           '_FillValue': False})
        ds['alt'] = xarray.Variable('altitude', 
                                    ma.array(self.alt),
                                    attrs={'long_name': 'Altitude above mean sea level', 
                                           'units': 'm',
                                           'standard_name': 'altitude',
                                           '_FillValue': False})
        
        encoding = {'time_offset': {'units': 'seconds since '
                                    + str(ma.array(self.time[0], dtype='datetime64[ns]')),
                                    'calendar': 'gregorian'},
                    'time': {'units': 'seconds since '
                             + str(ma.array(self.time[0], dtype='datetime64[ns]')),
                             'calendar': 'gregorian'}}
        
        ds.attrs = attributes
        date = pd.to_datetime(
            ma.array(self.time[0], dtype='datetime64[ns]')).strftime('%Y%m%d')

        
        command_line = ''
        for item in sys.argv:
            command_line = command_line + '' + item
        ds.attrs['command_line'] = command_line
        ds.attrs['history'] = ('Created by jhemedinger on '
                               + socket.gethostname() + ' at '
                               + datetime.datetime.utcnow().strftime(
                                   '%Y-%m-%dT%H:%M:%S.%f')
                               + ' using PyART')
        
        ds.squeeze(dim=None, drop=False).to_netcdf(path= file_directory + '/' + attributes['datastream'] 
                                                   + '.' + str(date) + '.000000.nc', encoding=encoding,
                                                   unlimited_dims='time')
        
                
            
