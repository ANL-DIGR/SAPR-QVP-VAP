import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import datetime
import xarray
import datetime
import os

from .config import get_plot_values, get_field_parameters

def quicklooks_1panel(file, field, config, image_directory=None, **kwargs):
    """
    Quciklooks, produces a one panel image using a QVP object NetCDF file.
    
    Parameters
    ----------
    file : str
        File path to the QVP NetCDF file
    field : str
        String of the radar field
    config : str
        A string of the radar name found from config.py that contains values
        for writing, specific to that radar.
    
    Optional Parameters
    -------------------
    image_directory : str
        File path to the image folder to save the QVP image. If no
        image file path is given, image path deafults to users home directory.
    
    """
    if image_directory is None:
        image_directory = os.path.expanduser('~')
        
    plot_values = get_plot_values(config)
    fld_params = get_field_parameters()
    qvp = xarray.open_dataset(file)
    
    time = qvp.time.data
    z = qvp.height.data/1000
    fld = qvp[field].data
    date = pd.to_datetime(time[0]).strftime('%Y%m%d')
    ts = datetime.datetime.strptime(date, '%Y%m%d')
    
    fig = plt.figure(figsize=[25, 12])
    font = {'family': 'normal', 'size': 20}
    matplotlib.rc('font', **font)
    matplotlib.rcParams.update({'font.size': 20})
    matplotlib.rcParams.update({'axes.titlesize': 20})
    
    img = plt.pcolormesh(time, z, fld.transpose(), cmap=plot_values['cmap'],
                         vmin=fld_params[field]['vmin'],
                         vmax=fld_params[field]['vmax'])
    plt.xlim(ts, (ts + datetime.timedelta(days=1)))
    plt.xticks(rotation=45)
    plt.ylim(0,12)
    plt.ylabel('Height (km)')
    plt.xlabel('Time (UTC)')
    plt.title(plot_values['title'] + ' ' + fld_params[field]['fld_title'] + ' '
              + plot_values['tilt'] + ' ' + str(ts) 
              + '-' + str(ts + datetime.timedelta(days=1)))
    cb = plt.colorbar(img, cmap=plot_values['cmap'])
    cb.set_label(fld_params[field]['clb_title'])
    plt.savefig(image_directory + '/' + plot_values['save_name']
                + '.' + str(date) + '.000000.png', bbox_inches='tight')

def quicklooks_4panel(file, fields, config, image_directory=None):
    """
    Quciklooks, produces a four panel image using a QVP object NetCDF file.
    
    Parameters
    ----------
    file : str
        File path to the QVP NetCDF file
    fields : tuple/list
        Tuple or list of strings of radar fields
    config : str
        A string of the radar name found from config.py that contains values
        for writing, specific to that radar.
    
    Optional Parameters
    -------------------
    image_directory : str
        File path to the image folder to save the QVP image. If no
        image file path is given, image path deafults to users home directory.
    
    """
    if image_directory is None:
        image_directory = os.path.expanduser('~')
    plot_values = get_plot_values(config)
    fld_params = get_field_parameters()
    qvp = xarray.open_dataset(file)
    cmap = plot_values['cmap']
    
    time = qvp.time.data
    z = qvp.height.data/1000
    date = pd.to_datetime(time[0]).strftime('%Y%m%d')
    ts = datetime.datetime.strptime(date, '%Y%m%d')
    fld1 = qvp[fields[0]].data
    fld2 = qvp[fields[1]].data
    fld3 = qvp[fields[2]].data
    fld4 = qvp[fields[3]].data
    
    fig, ax = plt.subplots(nrows=4, ncols=1, sharex=True,
                           sharey=True, figsize=(50,37))
    font = {'family': 'normal',
            'size': 30}
    matplotlib.rc('font', **font)
    matplotlib.rcParams.update({'font.size': 30})
    matplotlib.rcParams.update({'axes.titlesize': 30})
    
    fig.suptitle(x=0.435, y=0.93, t=plot_values['title'] + ' '
                 + plot_values['tilt'] + ' ' + str(ts)
                 + '-' + str(ts + datetime.timedelta(days=1)),
                 fontsize=40)
    fig.text(0.435, 0.065, 'Time (UTC)', ha='center', fontsize=30)
    fig.text(0.09, 0.5, 'Height (km)', va='center',
             rotation='vertical', fontsize=30)
    
    ax = plt.subplot(411)
    img = plt.pcolormesh(time, z, fld1.transpose(), cmap=cmap,
                         vmin=fld_params[fields[0]]['vmin'],
                         vmax=fld_params[fields[0]]['vmax'])
    plt.ylim(0,12)
    plt.xlim(ts, (ts + datetime.timedelta(days=1)))
    plt.xticks([])
    ax.set_title(fld_params[fields[0]]['fld_title'])
    cb = plt.colorbar(img, cmap=cmap)
    cb.set_label(fld_params[fields[0]]['clb_title'])
    
    ax = plt.subplot(412)
    img = plt.pcolormesh(time, z, fld2.transpose(), cmap=cmap,
                         vmin=fld_params[fields[1]]['vmin'],
                         vmax=fld_params[fields[1]]['vmax'])
    plt.ylim(0,12)
    plt.xlim(ts, (ts + datetime.timedelta(days=1)))
    plt.xticks([])
    ax.set_title(fld_params[fields[1]]['fld_title'])
    cb = plt.colorbar(img, cmap=cmap)
    cb.set_label(fld_params[fields[1]]['clb_title'])
    
    ax = plt.subplot(413)
    img = plt.pcolormesh(time, z, fld3.transpose(), cmap=cmap,
                         vmin=fld_params[fields[2]]['vmin'],
                         vmax=fld_params[fields[2]]['vmax'])
    plt.ylim(0,12)
    plt.xlim(ts, (ts + datetime.timedelta(days=1)))
    plt.xticks([])
    ax.set_title(fld_params[fields[2]]['fld_title'])
    cb = plt.colorbar(img, cmap=cmap)
    cb.set_label(fld_params[fields[2]]['clb_title'])
    
    ax = plt.subplot(414)
    img = plt.pcolormesh(time, z, fld4.transpose(), cmap=cmap,
                         vmin=fld_params[fields[3]]['vmin'],
                         vmax=fld_params[fields[3]]['vmax'])
    plt.ylim(0,12)
    plt.xlim(ts, (ts + datetime.timedelta(days=1)))
    plt.xticks(rotation=45)
    ax.set_title(fld_params[fields[3]]['fld_title'])
    cb = plt.colorbar(img, cmap=cmap)
    cb.set_label(fld_params[fields[3]]['clb_title'])
    
    plt.savefig(image_directory + '/' + plot_values['save_name']
                + '.' + str(date) + '.000000.png', bbox_inches='tight')
    
    