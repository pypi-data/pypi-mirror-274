# -*- coding: utf-8 -*-
"""
Created on Mon Mar 18 16:39:03 2024

@author: a5278
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Jul 25 11:25:10 2023

@author: a5278
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Apr 21 11:01:11 2023

@author: Administrator
"""


from skimage.transform import  resize
from skimage.transform import  resize_local_mean
import shutil
from skimage.transform import  resize

# from krillscan.echolab2.instruments import EK80, EK60
import configparser

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt
import glob 
import os
from PIL import Image

# from scipy.ndimage.filters import uniform_filter1d

from scipy.signal import convolve2d
# from skimage.transform import  resize

from krillscan.echopy import transform as transform
from krillscan.echopy import resample as rs
from krillscan.echopy import mask_impulse as mIN
from krillscan.echopy import mask_seabed as mSB
from krillscan.echopy import get_background as gBN
from krillscan.echopy import mask_range as mRG
from krillscan.echopy import mask_shoals as mSH
from krillscan.echopy import mask_signal2noise as mSN

import echopype as ep


from pyproj import Geod
geod = Geod(ellps="WGS84")
from pathlib import Path


# from matplotlib.colors import ListedColormap
import re
import traceback
# from pyproj import Proj, transform
import zipfile

import smtplib
import ssl
# import mimetypes
from email.mime.multipart import MIMEMultipart
from email import encoders
from email.message import Message
from email.mime.base import MIMEBase
from email.mime.text  import MIMEText

from threading import Timer

import xarray as xr
from scipy.interpolate import interp1d
from scipy import integrate



from functools import partial
import multiprocessing  


#%% load unet

# from skimage.transform import rescale, resize, downscale_local_mean
# from skimage import data, filters, measure, morphology
# from skimage.morphology import (erosion, dilation, opening, closing,  # noqa
#                                 white_tophat)
# from skimage.morphology import disk  # noqa
# import tensorflow as tf
# from tensorflow import keras
# from tensorflow.keras import layers


# model = tf.keras.models.load_model('tensorflow_unet.h5')

# image_n_pixels = 256

# num_classes=5


#%% automatic processing


class RepeatTimer(Timer):
    def run(self):
        while not self.finished.wait(self.interval):
            self.function(*self.args, **self.kwargs)

class krillscan_class():
    
             
    
    def start(self,ini_file):
        print('start')
        self.ini_file = ini_file
        self.callback_process_active=False
        self.callback_email_active=False
        # self.callback_plot_active=False
        self.df_files=pd.DataFrame([])
        # self.echogram=pd.DataFrame([])    
        self.positions=pd.DataFrame([])    
        
        config = configparser.ConfigParser()
        config.read(self.ini_file)            
        self.workpath=  str(config['GENERAL']['target_folder'])  
        os.makedirs(self.workpath, exist_ok=True)

        
        print('work dir: ' +os.getcwd())
        print('source dir: ' + str(config['GENERAL']['source_folder'])  )
        print('target dir: ' +self.workpath)
               
        # self.start_para_processing()
        
        self.timer_process = RepeatTimer(10, self.callback_process_raw)
        self.timer_process.start()
        self.timer_email = RepeatTimer(30, self.callback_email)
        self.timer_email.start()  
        
        # doc.add_periodic_callback( self.callback_process_raw,1000 ) 
        # doc.add_periodic_callback( self.callback_plot,3000 ) 
        # doc.add_periodic_callback( self.callback_email,5000 ) 

                
    def stop(self):
        self.timer_process.cancel()
        self.timer_email.cancel()  
        print('Krillscan stopped')


    def read_raw(self,rawfile):       
        # df_sv=pd.DataFrame( [] )
        # positions=pd.DataFrame( []  )
                
        # breakpoint()
        
        # print('Echsounder data are: ')
        self.config = configparser.ConfigParser()
        self.config.read(self.ini_file)   
        
        # rawfile=r"C:\Users\a5278\Documents\postdoc_krill\krillscan\source_folder\D20220410-T195719.raw"
        # rawfile=r"./source_folder\D20230128-T105149.raw"
   
        try:     
            ed = ep.open_raw(rawfile, sonar_model='EK80')  # for EK80 file
            # compute Sv values from raw input data
            try: 
                edSv = ep.calibrate.compute_Sv(ed, waveform_mode="CW", encode_mode="complex")
            except:
                edSv = ep.calibrate.compute_Sv(ed, waveform_mode="CW", encode_mode="power")
        except Exception as e:            
            print(e)       
            try:     
                ed = ep.open_raw(rawfile, sonar_model='EK60')  # for EK80 file
                # compute Sv values from raw input data
                edSv = ep.calibrate.compute_Sv(ed)
            except Exception as e:
                print(e)       
    
                    
        #breakpoint()                           
        frequencies = np.unique(edSv.frequency_nominal.values)
        frequencies = frequencies[~np.isnan(frequencies)]
                
        # from echopype.commongrid.utils import compute_raw_MVBS
        # from echopype import open_raw
        # from echopype.calibrate import compute_Sv



        # compute Sv values from raw input data
        # edSv = ep.calibrate.compute_Sv(ed, waveform_mode="CW", encode_mode="power")

        # remove depths>500m for faster processing
        # edSv = edSv.where(edSv.echo_range < 501, drop = True)

        # Convert the array of depth bins into an interval index
        edSv['echo_range'].max()
        
        maxDepth =         edSv['echo_range'].max()

     
        # range_interval = pd.IntervalIndex.from_breaks(np.linspace(0, maxDepth, edSv.Sv.shape[2]))
        # r = np.linspace(0, maxDepth, edSv.Sv.shape[2])
        
        r=np.arange( 0 , maxDepth , 0.5 )
     
            # t=sv_obj.ping_time
     
            
            

        # range_interval = pd.IntervalIndex.from_breaks(np.arange(0, maxDepth + range_meter_bin, range_meter_bin))

        # time_interval = pd.interval_range(start=pd.to_datetime(edSv["ping_time"].min().values),
        #                                   end = pd.to_datetime(edSv["ping_time"].max().values), 
        #                                   freq=pd.Timedelta(seconds = 1))
        t= edSv["ping_time"].values
        # resampledSv = ep.commongrid.utils.compute_raw_MVBS(edSv,
        #             range_interval=range_interval,
        #             ping_interval= edSv["ping_time"],
        #             range_var='echo_range')
        
        # resampledSv = ep.commongrid.compute_MVBS(
        #   edSv,
        #   range_bin='.5m')

        frequencies = np.unique(edSv.frequency_nominal.values)
        frequencies = frequencies[~np.isnan(frequencies)]

        # extract locations for raw file and save to csv file
        gps_loc = ed['Platform'][['latitude','longitude']]
        gps_loc = gps_loc.sortby('time1')
        gps_loc = gps_loc.drop_duplicates(dim='time1')
        gps_loc = gps_loc.resample(time1='1s').mean()
        gps_loc = gps_loc.to_dataframe() 
        
        la= np.interp(  edSv["ping_time"].values.astype(float) , gps_loc.index.values.astype(float), gps_loc['latitude'])
        lo= np.interp(  edSv["ping_time"].values.astype(float) , gps_loc.index.values.astype(float), gps_loc['longitude'])
        
        positions = pd.DataFrame([])     
        positions['ping_time']=edSv["ping_time"].values
        positions['latitude'] = la
        positions['longitude'] = lo
        
        # positions.index
        
        raw_freq= frequencies
        
        # breakpoint()
        
        
        
        # self.ekdata=dict()
        
        # for f in raw_freq:
        # f=float(self.config['GENERAL']['scrutinization_frequency'])
        # print(raw_freq)
        
        for f in raw_freq:
        #     # print(raw_obj.frequency_map[f])
            
        #     # single ping storage issue
        #     if len( raw_obj.raw_data[raw_obj.frequency_map[f][0]][:]) >1:
        #           raw_data = raw_obj.raw_data[raw_obj.frequency_map[f][0]][:]  
                  
        #           # new code:
        #           maxSamples = max([sublist.n_samples for sublist in raw_data])
        #           svr = np.empty([maxSamples , raw_obj.n_pings])   
                   
        #           for k in range(len(raw_data)):
        #               svr[list(range(0,(raw_data[k].power.size))),k] = raw_data[k].power
      
        #     else:
            
        #         raw_data = raw_obj.raw_data[raw_obj.frequency_map[f][0]][0]  
        
        #         if np.shape(raw_data)[0]>1:                     
        #             cal_obj = raw_data.get_calibration()
                    
        #             try: 
        #                 cal_obj.gain=float(self.config['CALIBRATION']['gain']       )
        #             except:
        #                 pass
        #             try: 
        #                 cal_obj.sa_correction=float(self.config['CALIBRATION']['sa_correction']       )
        #             except:
        #                 pass
        #             try: 
        #                 cal_obj.beam_width_alongship=float(self.config['CALIBRATION']['beam_width_alongship']       )
        #             except:
        #                 pass
        #             try: 
        #                 cal_obj.beam_width_athwartship=float(self.config['CALIBRATION']['beam_width_athwartship']       )
        #             except:
        #                 pass
        #             try: 
        #                 cal_obj.angle_offset_alongship=float(self.config['CALIBRATION']['angle_offset_alongship']       )
        #             except:
        #                 pass
        #             try: 
        #                 cal_obj.angle_offset_athwartship=float(self.config['CALIBRATION']['angle_offset_athwartship']       )
        #             except:
        #                 pass
                        
                    
        #             sv_obj = raw_data.get_sv(calibration = cal_obj)    
        #             # sv_obj = raw_data.get_sv()    
                      
        #             # positions =pd.DataFrame(  raw_obj.nmea_data.interpolate(sv_obj, 'GGA')[1] )
                   
        #             svr = np.transpose( 10*np.log10( sv_obj.data ) )

        #         # print(sv_obj.range.max())
        #         # r=np.arange( sv_obj.range.min() , sv_obj.range.max() , 0.5 )
        #     r=np.arange( 0 , sv_obj.range.max() , 0.5 )
     
        #     t=sv_obj.ping_time
     
        #     sv=  resize(svr,[ len(r) , len(t) ] )
             
            # print(sv.shape)
            
            ix_f= f == frequencies
            svr =np.squeeze(  edSv.Sv[ix_f,:,:].values.T )
            
            sv=  resize(svr,[ len(r) , len(t) ] )


            # r =resampledSv.echo_range_bins
            
            # edSv.Sv[ix_f,:,:].values.T
            
        # fig= plt.figure(0)
        # plt.clf()     
        # plt.imshow(edSv.Sv[ix_f,:,:].values.T ,aspect='auto',vmin=-90,vmax=-30)
        # plt.colorbar()
        # plt.grid()
        # plt.tight_layout()
        # plt.draw()
        
        
        # fig= plt.figure(1)
        # plt.clf()     
        # plt.imshow(resampledSv.Sv[ix_f,:,:].T,aspect='auto',vmin=-90,vmax=-30)
        # plt.colorbar()
        # plt.grid()
        # plt.tight_layout()
        # plt.draw()

        # fig= plt.figure(1)
        # plt.clf()     
        # plt.imshow(mb,aspect='auto')
        # plt.colorbar()
        # plt.grid()
        # plt.tight_layout()
        # plt.draw()
        
        # fig= plt.figure(1)
        # plt.clf()     
        # plt.plot(row_1)
        # plt.grid()
        # plt.tight_layout()
        # plt.draw()
        
        
            # breakpoint()
            # Clean impulse noise      
            sv_im, m120in_ = mIN.wang(sv, thr=(-90,0), erode=[(3,3)], # thre was -70 to -40 
                              dilate=[(7,7)], median=[(7,7)])
             
            if f== float(self.config['GENERAL']['scrutinization_frequency'] ):
                 
                  # positions =pd.DataFrame(  raw_obj.nmea_data.interpolate(sv_obj, 'GGA')[1] )

                  seafloor_sv_threshold_db = float(self.config['PROCESSING']['seafloor_sv_threshold_db'] )

                  mb = mSB.ariza(sv, r, r0=10, r1=1000, roff=0,
                                    thr=seafloor_sv_threshold_db, ec=1, ek=(3,3), dc=10, dk=(5,15))
                 
                  # print(mb.sum())
                  # breakpoint()
                  # sv_im[mb]=-999
                 
                  bottomdepth=[]         
                  for j in range(mb.shape[1]):
                      row_1=mb[:,j]
                      if np.sum(row_1==True)>0:
                          bottomdepth.append( np.min(r[row_1==True]) )
                      else:
                          bottomdepth.append( r.max() )
                  # print(bottomdepth)   
                  positions['bottomdepth_m']=bottomdepth


              # estimate and correct background noise       
            p         = np.arange(len(t))                
            s         = np.arange(len(r))          
            
            
            bn, m120bn_ = gBN.derobertis(sv, s, p, 5, 20, r, np.mean(edSv["sound_absorption"].values[ix_f]) ) # whats correct absoprtion?
            b=pd.DataFrame(bn)
            bn=  b.interpolate(axis=1).interpolate(axis=0).values                        
            sv_clean     = transform.log(transform.lin(sv_im) - transform.lin(bn))
           
            sv_SNR_threshold_db = float(self.config['PROCESSING']['sv_SNR_threshold_db'] )
            msn             = mSN.derobertis(sv_clean, bn, thr=sv_SNR_threshold_db)
            sv_clean[msn] = np.nan

           
            sv_x = xr.DataArray(sv_clean,coords={"time": t,"depth": r},  dims=("depth","time"))

            sv_x=sv_x.expand_dims(dim='frequency')                
              # fill holes
              # sv_x = sv_x.interpolate_na( dim='time', method="linear",max_gap=pd.Timedelta(seconds=2))
            sv_x = sv_x.interpolate_na( dim='depth', method="linear",max_gap=3)

            sv_x_raw = xr.DataArray(sv,coords={"time": t,"depth": r},  dims=("depth","time"))
            sv_x_raw=sv_x_raw.expand_dims(dim='frequency')                
              # breakpoint()

        # fig= plt.figure(1)
        # plt.clf()     
        # plt.subplot(211)
        # plt.imshow(sv_x_raw[0,:,:],aspect='auto',vmin=-90,vmax=-30)
        # plt.colorbar()
        # plt.grid()
        # plt.subplot(212)
        # plt.imshow(sv_x[0,:,:],aspect='auto',vmin=-90,vmax=-30)
        # plt.colorbar()
        # plt.grid()
                
        # plt.tight_layout()
        # plt.draw()
             
            if f==raw_freq[0]:
                  xr_sv=sv_x
                  xr_sv_raw=sv_x_raw
            else:
                  xr_sv = xr.concat([xr_sv,sv_x], dim="frequency")
                  xr_sv_raw = xr.concat([xr_sv_raw,sv_x_raw], dim="frequency")

                    
        xr_sv.coords['frequency'] = raw_freq
        xr_sv_raw.coords['frequency'] = raw_freq
        
        # duration =     ( xr_sv.coords['time'][-1] - xr_sv.coords['time'][0]).data  / np.timedelta64(1, 's')
        # dm=xr_sv.coords['depth'][-1].data
        
        # fig= plt.figure(0)
        # plt.clf()
        # fig.set_size_inches(10,10)
        # k=1
        # for f in xr_sv.coords['frequency']:
        #     if k==1:
        #         ax1=plt.subplot(len(xr_sv.coords['frequency']),1,k)
        #     else:
        #         plt.subplot(len(raw_freq),1,k,sharex=ax1,sharey=ax1)
        #     plt.imshow(xr_sv[k-1,:,:],aspect='auto',vmin=-90,vmax=-30,extent=[0,duration,dm,0])
        #     plt.title(str(xr_sv.coords['frequency'].data[k-1]))
        #     plt.colorbar()
        #     plt.grid()
        #     k=k+1
        # plt.tight_layout()
        
        # print(xr_sv)
        # print(positions)
               
        return xr_sv, positions , xr_sv_raw


    
    def calc_absorption(self,
        frequency,
        temperature=27,
        salinity=35,
        pressure=10,
        pH=8.1,
        sound_speed=None,
        formula_source="AM",
    ):
        """
        Calculate sea water absorption in units [dB/m].
    
        Parameters
        ----------
        frequency: int or numpy array
            frequency [Hz]
        temperature: num
            temperature [deg C]
        salinity: num
            salinity [PSU, part per thousand]
        pressure: num
            pressure [dbars]
        pH: num
            pH of water
        formula_source: str, {"AM", "FG", "AZFP"}
            Source of formula used to calculate sound speed.
            "AM" (default) uses the formula from Ainslie and McColm (1998).
            "FG" uses the formula from Francois and Garrison (1982).
            "AZFP" uses the the formula supplied in the AZFP Matlab code.
            See Notes below for the references.
    
        Returns
        -------
        Sea water absorption [dB/m].
    
        Notes
        -----
        Ainslie MA, McColm JG. (1998). A simplified formula for viscous
        and chemical absorption in sea water.
        The Journal of the Acoustical Society of America, 103(3), 1671–1672.
        https://doi.org/10.1121/1.421258
    
        Francois RE, Garrison GR. (1982). Sound absorption based on
        ocean measurements. Part II: Boric acid contribution and equation
        for total absorption.
        The Journal of the Acoustical Society of America, 72(6), 1879–1890.
        https://doi.org/10.1121/1.388673
    
        The accuracy of the simplified formula from Ainslie & McColm 1998
        compared with the original complicated formula from Francois & Garrison 1982
        was demonstrated between 100 Hz and 1 MHz.
        """
        if formula_source == "FG":
            f = frequency / 1000.0  # convert from Hz to kHz due to formula
            if sound_speed is None:
                c = 1412.0 + 3.21 * temperature + 1.19 * salinity + 0.0167 * pressure
            else:
                c = sound_speed
            A1 = 8.86 / c * 10 ** (0.78 * pH - 5)
            P1 = 1.0
            f1 = 2.8 * np.sqrt(salinity / 35) * 10 ** (4 - 1245 / (temperature + 273))
            A2 = 21.44 * salinity / c * (1 + 0.025 * temperature)
            P2 = 1.0 - 1.37e-4 * pressure + 6.2e-9 * pressure**2
            f2 = 8.17 * 10 ** (8 - 1990 / (temperature + 273)) / (1 + 0.0018 * (salinity - 35))
            P3 = 1.0 - 3.83e-5 * pressure + 4.9e-10 * pressure**2
            if np.all(temperature < 20):
                A3 = (
                    4.937e-4
                    - 2.59e-5 * temperature
                    + 9.11e-7 * temperature**2
                    - 1.5e-8 * temperature**3
                )
            else:
                A3 = (
                    3.964e-4
                    - 1.146e-5 * temperature
                    + 1.45e-7 * temperature**2
                    - 6.5e-10 * temperature**3
                )
            a = (
                A1 * P1 * f1 * f**2 / (f**2 + f1**2)
                + A2 * P2 * f2 * f**2 / (f**2 + f2**2)
                + A3 * P3 * f**2
            )
            sea_abs = a / 1000  # formula output is in unit [dB/km]
    
        elif formula_source == "AM":
            freq = frequency / 1000
            D = pressure / 1000
            f1 = 0.78 * np.sqrt(salinity / 35) * np.exp(temperature / 26)
            f2 = 42 * np.exp(temperature / 17)
            a1 = 0.106 * (f1 * (freq**2)) / ((f1**2) + (freq**2)) * np.exp((pH - 8) / 0.56)
            a2 = (
                0.52
                * (1 + temperature / 43)
                * (salinity / 35)
                * (f2 * (freq**2))
                / ((f2**2) + (freq**2))
                * np.exp(-D / 6)
            )
            a3 = 0.00049 * freq**2 * np.exp(-(temperature / 27 + D))
            sea_abs = (a1 + a2 + a3) / 1000  # convert to db/m from db/km
    
        elif formula_source == "AZFP":
            temp_k = temperature + 273.0
            f1 = 1320.0 * temp_k * np.exp(-1700 / temp_k)
            f2 = 1.55e7 * temp_k * np.exp(-3052 / temp_k)
    
            # Coefficients for absorption calculations
            k = 1 + pressure / 10.0
            a = 8.95e-8 * (1 + temperature * (2.29e-2 - 5.08e-4 * temperature))
            b = (
                (salinity / 35.0)
                * 4.88e-7
                * (1 + 0.0134 * temperature)
                * (1 - 0.00103 * k + 3.7e-7 * k**2)
            )
            c = (
                4.86e-13
                * (1 + temperature * (-0.042 + temperature * (8.53e-4 - temperature * 6.23e-6)))
                * (1 + k * (-3.84e-4 + k * 7.57e-8))
            )
            if salinity == 0:
                sea_abs = c * frequency**2
            else:
                sea_abs = (
                    (a * f1 * frequency**2) / (f1**2 + frequency**2)
                    + (b * f2 * frequency**2) / (f2**2 + frequency**2)
                    + c * frequency**2
                )
        else:
            ValueError("Unknown formula source")
    
        return sea_abs


    def parafunc(self,ini_file,df_files,index ):
        
        
        config = configparser.ConfigParser()
        config.read(ini_file)   
        
        row = df_files.iloc[ index ,:]

        rawfile=row['path']
        print('working on '+rawfile)
        try:
            
            echogram_file, positions_file , echogram_file_raw = self.read_raw(rawfile)
           
            # df_nasc_file, mask_swarm, mask_dbdiff = self.detect_krill_swarms(echogram_file,positions_file)   
            # df_nasc_file, mask_swarm, mask_dbdiff,segmentation_unet  = self.detect_krill_swarms(echogram_file,echogram_file_raw,positions_file)   
            # mask_unet= segmentation_unet==1
            df_nasc_file, mask_swarm, mask_dbdiff  = self.detect_krill_swarms(echogram_file,echogram_file_raw,positions_file)   
            
            name = os.path.basename( rawfile )
            # name = t.min().strftime('D%Y%m%d-T%H%M%S' )         
            print('saving: '+name)
            # df_sv_swarm[ new_echogram==-999 ] =-999
            
            workpath=  str(config['GENERAL']['target_folder'])  
                        
            df_nasc_file.to_hdf(workpath+'/'+ name + '_nasctable.h5', key='df', mode='w'  )
            
                        # add mask info to xarray
            t_mask= echogram_file.coords['time']
            r= echogram_file.coords['depth']
            
            # if len(np.shape(mask_dbdiff))>1:

            #     mas = np.stack([mask_swarm,mask_unet,mask_dbdiff],axis=-1)
            #     nc_masks = xr.DataArray(mas,coords={"time": t_mask,"depth": r,"method": ['Swarms','U-NET','dBdiff']},  dims=("depth","time","method"))
            # else:
            #     mas = np.stack([mask_swarm,mask_unet],axis=-1)
            #     nc_masks = xr.DataArray(mas,coords={"time": t_mask,"depth": r,"method": ['Swarms','U-NET']},  dims=("depth","time","method"))
            # nc_masks.to_netcdf(self.workpath+'/'+ name + '_krill_masks.nc')             
            if len(np.shape(mask_dbdiff))>1:

                mas = np.stack([mask_swarm,mask_dbdiff],axis=-1)
                nc_masks = xr.DataArray(mas,coords={"time": t_mask,"depth": r,"method": ['Swarms','dBdiff']},  dims=("depth","time","method"))
            else:
                mas = np.stack([mask_swarm],axis=-1)
                nc_masks = xr.DataArray(mas,coords={"time": t_mask,"depth": r,"method": ['Swarms']},  dims=("depth","time","method"))
            nc_masks.to_netcdf(self.workpath+'/'+ name + '_krill_masks.nc')             


            
            # dffloat=df_nasc_file.copy()
            # formats = {'lat': "{:.6f}", 'lon': "{:.6f}", 'distance_m': "{:.4f}",'bottomdepth_m': "{:.1f}",'nasc_swarm': "{:.2f}",'nasc_dbdiff': "{:.2f}"}
            # for col, f in formats.items():
            #     dffloat[col] = dffloat[col].map(lambda x: f.format(x))                           
            # # dffloat.to_csv( name + '_nasctable.gzip',compression='gzip' )
            # dffloat.to_csv(workpath+'/'+ name + '_nasctable.csv')
            
            # df_sv_swarm.astype('float16').to_hdf(self.workpath+'/'+ name + '_sv_swarm.h5', key='df', mode='w'  )
            

            # df_mask = pd.DataFrame( np.transpose(mask_swarm))
            # df_mask.index=t_mask
            # df_mask.columns=r
            # df_mask.astype('bool').to_hdf(workpath+'/'+ name + '_mask_swarm.h5', key='df', mode='w'  )
            # if bool(int(config['PROCESSING']['write_mask_as_csv'])) :
            #     df_mask.astype('int').to_csv(workpath+'/'+ name + '_mask_swarm.csv' )

            # if len(np.shape(mask_dbdiff))>1:
            #     df_mask = pd.DataFrame( np.transpose(mask_dbdiff))
            #     df_mask.index=t_mask
            #     df_mask.columns=r
            #     df_mask.astype('bool').to_hdf(workpath+'/'+ name + '_mask_dbdiff.h5', key='df', mode='w'  )
            #     if bool(int(config['PROCESSING']['write_mask_as_csv'])) :
            #         df_mask.astype('int').to_csv(workpath+'/'+ name + '_mask_dbdiff.csv' )


            
            echogram_file.to_netcdf(workpath+'/'+ name + '_echogram.nc')    
            echogram_file_raw.to_netcdf(workpath+'/'+ name + '_rawechogram.nc')    
                        
        except Exception as e:
            print(e)               
            print(traceback.format_exc())
            
    def start_para_processing(self,ini_file):
        
        print('start')
        # ini_file = ini_file
        self.ini_file = ini_file

        df_files=pd.DataFrame([])
        positions=pd.DataFrame([])    
        
        config = configparser.ConfigParser()
        config.read(self.ini_file)            
        workpath=  str(config['GENERAL']['target_folder'])  
        folder_source=  str(config['GENERAL']['source_folder'])  
       
        print('work dir: ' +os.getcwd())
        print('source dir: ' + str(config['GENERAL']['source_folder'])  )
        print('target dir: ' +workpath)
               
        # self.start_para_processing()
         
        new_df_files = pd.DataFrame([])   

        globstr =  os.path.join( glob.escape( folder_source),'*.raw')           
        new_df_files['path'] = glob.glob( globstr )  
        print('found '+str(len(new_df_files)) + ' raw files')
    
        dates=[]
        for fname in new_df_files['path']:
            
            datetimestring=re.search('D\d\d\d\d\d\d\d\d-T\d\d\d\d\d\d',fname).group()
            dates.append( pd.to_datetime( datetimestring,format='D%Y%m%d-T%H%M%S' ) )
        new_df_files['date'] = dates
    
    
        new_df_files['to_do']=True 
        
        
        df_files=pd.concat([df_files,new_df_files])
        df_files.drop_duplicates(inplace=True)
        
        df_files =  df_files.sort_values('date')
        df_files=df_files.reset_index(drop=True)
        

        # look for already processed data
        df_files['to_do']=True    
        
        if os.path.isfile(workpath+'/list_of_rawfiles.csv'):
            df_files_done =  pd.read_csv(workpath+'/list_of_rawfiles.csv',index_col=0)
            df_files_done=df_files_done.loc[ df_files_done['to_do']==False,: ]
        
            names = df_files['path'].apply(lambda x: Path(x).stem)       
            names_done = df_files_done['path'].apply(lambda x: Path(x).stem)  
            # breakpoint()
            
        # print(names)
        # print(nasc_done)
            ix_done= names.isin( names_done  )  
    
        # print(ix_done)
            df_files.loc[ix_done,'to_do'] = False        
        n_todo=np.sum(df_files['to_do'])
        print('To do: ' + str(n_todo))
                
        # unit_length_min=pd.to_timedelta(10,'min')
        
        ix_todo = np.where( df_files['to_do']==True )[0]
        
        # breakpoint()
        
        ###### parallel processing
        
        print( __name__  )
        if __name__ == 'krillscan.process':
            cpucounts=multiprocessing.cpu_count()
            pool = multiprocessing.Pool(processes=cpucounts)
            index_list=ix_todo
            pool.map( partial( self.parafunc,ini_file,  df_files), index_list)
            pool.close   

    def file2netcdf(self,inifile,rawfile):
        self.ini_file =inifile
        
        self.config = configparser.ConfigParser()
        self.config.read(inifile)   
        
        print('working on '+rawfile)
        try:
            
            echogram_file, positions_file , echogram_file_raw = self.read_raw(rawfile)
           
            df_nasc_file, mask_swarm, mask_dbdiff = self.detect_krill_swarms(echogram_file,positions_file)   
            
            
            name = os.path.basename( rawfile )
            # name = t.min().strftime('D%Y%m%d-T%H%M%S' )         
            print('saving: '+name)
            # df_sv_swarm[ new_echogram==-999 ] =-999
            
            workpath=  str(self.config['GENERAL']['target_folder'])  
                        
            df_nasc_file.to_hdf(workpath+'/'+ name + '_nasctable.h5', key='df', mode='w'  )
            
            dffloat=df_nasc_file.copy()
            formats = {'lat': "{:.6f}", 'lon': "{:.6f}", 'distance_m': "{:.4f}",'bottomdepth_m': "{:.1f}",'nasc_swarm': "{:.2f}",'nasc_dbdiff': "{:.2f}"}
            for col, f in formats.items():
                dffloat[col] = dffloat[col].map(lambda x: f.format(x))                           
            # dffloat.to_csv( name + '_nasctable.gzip',compression='gzip' )
            dffloat.to_csv(workpath+'/'+ name + '_nasctable.csv')
            
            # df_sv_swarm.astype('float16').to_hdf(self.workpath+'/'+ name + '_sv_swarm.h5', key='df', mode='w'  )
            
            # add mask info to xarray
            t_mask= echogram_file.coords['time']
            r= echogram_file.coords['depth']
            
            df_mask = pd.DataFrame( np.transpose(mask_swarm))
            df_mask.index=t_mask
            df_mask.columns=r
            df_mask.astype('bool').to_hdf(workpath+'/'+ name + '_mask_swarm.h5', key='df', mode='w'  )
            if bool(int(self.config['PROCESSING']['write_mask_as_csv'])) :
                df_mask.astype('int').to_csv(workpath+'/'+ name + '_mask_swarm.csv' )

            if len(np.shape(mask_dbdiff))>1:
                df_mask = pd.DataFrame( np.transpose(mask_dbdiff))
                df_mask.index=t_mask
                df_mask.columns=r
                df_mask.astype('bool').to_hdf(workpath+'/'+ name + '_mask_dbdiff.h5', key='df', mode='w'  )
                if bool(int(self.config['PROCESSING']['write_mask_as_csv'])) :
                    df_mask.astype('int').to_csv(workpath+'/'+ name + '_mask_dbdiff.csv' )


            
            echogram_file.to_netcdf(workpath+'/'+ name + '_echogram.nc')    
            echogram_file_raw.to_netcdf(workpath+'/'+ name + '_rawechogram.nc')    
                        
        except Exception as e:
            print(e)               
            print(traceback.format_exc())
            

                    
    def callback_process_raw(self):
              
      config = configparser.ConfigParser()
      config.read(self.ini_file)            
      self.folder_source=  str(config['GENERAL']['source_folder'])  
        
      if (self.callback_process_active==False) :
          
        self.callback_process_active==True
        # self.workpath=  os.path.join(self.folder_source,'krill_data')     
        # os.chdir(self.workpath)
    
        new_df_files = pd.DataFrame([])   

        globstr =  os.path.join( glob.escape( self.folder_source),'*.raw')           
        new_df_files['path'] = glob.glob( globstr )  
        print('found '+str(len(new_df_files)) + ' raw files')
    
        dates=[]
        for fname in new_df_files['path']:
            
            datetimestring=re.search('D\d\d\d\d\d\d\d\d-T\d\d\d\d\d\d',fname).group()
            dates.append( pd.to_datetime( datetimestring,format='D%Y%m%d-T%H%M%S' ) )
        new_df_files['date'] = dates
    
    
        new_df_files['to_do']=True 
        
        
        self.df_files=pd.concat([self.df_files,new_df_files])
        self.df_files.drop_duplicates(inplace=True)
        
        self.df_files =  self.df_files.sort_values('date')
        self.df_files=self.df_files.reset_index(drop=True)
        

        # look for already processed data
        self.df_files['to_do']=True    
        
        if os.path.isfile(self.workpath+'/list_of_rawfiles.csv'):
            df_files_done =  pd.read_csv(self.workpath+'/list_of_rawfiles.csv',index_col=0)
            df_files_done=df_files_done.loc[ df_files_done['to_do']==False,: ]
        
            names = self.df_files['path'].apply(lambda x: Path(x).stem)       
            names_done = df_files_done['path'].apply(lambda x: Path(x).stem)  
            # breakpoint()
            
        # print(names)
        # print(nasc_done)
            ix_done= names.isin( names_done  )  
    
        # print(ix_done)
            self.df_files.loc[ix_done,'to_do'] = False        
        self.n_todo=np.sum(self.df_files['to_do'])
        print('To do: ' + str(self.n_todo))
        
        # echogram=pd.DataFrame([])    
        # positions=pd.DataFrame([])    
        
        unit_length_min=pd.to_timedelta(10,'min')
        
        ix_todo = np.where( self.df_files['to_do']==True )[0]
        
        
        if self.n_todo>0:
                index = ix_todo[0]
                row = self.df_files.iloc[ index ,:]

        # for index, row in self.df_files.iterrows():
        #     if self.toggle_proc.active & (row['to_do']==True):
                rawfile=row['path']
                print('working on '+rawfile)
                try:
                    
                    # breakpoint()
                    # rawfile =r"C:\Users\a5278\Documents\postdoc_krill\krillscan\source_folder\D20220410-T195719.raw"
                    
                    echogram_file, positions_file , echogram_file_raw = self.read_raw(rawfile)
                    
                    if hasattr(self, 'echogram'):
                        self.echogram = xr.concat([self.echogram,echogram_file], dim="time")
                        self.echogram_raw = xr.concat([self.echogram_raw,echogram_file_raw], dim="time")
                    else:
                        self.echogram=echogram_file
                        self.echogram_raw=echogram_file_raw
                                            
                    # self.echogram = pd.concat([ self.echogram,echogram_file ])
                    
                    
                    self.positions = pd.concat([ self.positions,positions_file ])
                    self.positions=self.positions.reset_index(drop=True)
                    
                    # breakpoint()

                    
                    # t=pd.to_datetime( self.echogram.coords['time'].data )
                    t=pd.to_datetime( self.positions['ping_time'].values )
                    
                    # print(echogram)
                    
                    print( [ t.min() , t.max() ])
                    
                    while (t.max() - t.min()) > unit_length_min:
                        
                        print( (t.max() - t.min())  )
                        
                        # print(  (t.min() + unit_length_min) > t)
                        ix_end = np.where( (t.min() + unit_length_min) > t )[0][-1]
                        ix_start=t.argmin()
                        # print([ix_start,ix_end])
                        
                        # jump over snipps that are to small
                        if (ix_end-ix_start)<50:
                            # print('echogram to short, jumping over')
                            self.echogram = self.echogram[:,:,ix_end+1:]
                            self.positions = self.positions.iloc[ix_end+1:,:]
                            self.echogram_raw = self.echogram_raw[:,:,ix_end+1:]
                            t=pd.to_datetime( self.positions['ping_time'].values )

                            
                        else:    
                        
                            # accumulate 10 min snippet  
                            new_echogram = self.echogram[:,:,ix_start:ix_end]
                            new_positions = self.positions.iloc[ix_start:ix_end,:]
                            new_echogram_raw = self.echogram_raw[:,:,ix_start:ix_end]

                            self.echogram = self.echogram[:,:,ix_end+1:]
                            self.positions = self.positions.iloc[ix_end+1:,:]
                            self.echogram_raw = self.echogram_raw[:,:,ix_end+1:]

                            t=pd.to_datetime( self.positions['ping_time'].values )
    
                            # try:
                            # df_nasc_file, mask_swarm, mask_dbdiff,segmentation_unet,segmentation_unet_and_shapes  = self.detect_krill_swarms(new_echogram,new_echogram_raw,new_positions)   
                            # mask_unet= segmentation_unet==1
                            # mask_unet_and_shapes= segmentation_unet_and_shapes==1
                            df_nasc_file, mask_swarm, mask_dbdiff  = self.detect_krill_swarms(new_echogram,new_echogram_raw,new_positions)   
                            

                            name = new_positions['ping_time'].min().strftime('D%Y%m%d-T%H%M%S' )    
                            # name = t.min().strftime('D%Y%m%d-T%H%M%S' )         
                            print('saving: '+name)
                            # df_sv_swarm[ new_echogram==-999 ] =-999
                            
                            ###### save mask png
                            # cat_upsample=segmentation_unet.astype('uint8')
                            
                            # nam = self.workpath+'/'+ name + '_segmentation.png'                            
                            # im = Image.fromarray(cat_upsample *50)
                            # im.save( nam )

                            #####
                                                    
                            df_nasc_file.to_hdf(self.workpath+'/'+ name + '_nasctable.h5', key='df', mode='w'  )
                            
                            dffloat=df_nasc_file.copy()
                            # formats = {'lat': "{:.6f}", 'lon': "{:.6f}", 'distance_m': "{:.4f}",'bottomdepth_m': "{:.1f}",'nasc_swarm': "{:.2f}",'nasc_dbdiff': "{:.2f}",'nasc_unet': "{:.2f}"}
                            formats = {'lat': "{:.6f}", 'lon': "{:.6f}", 'distance_m': "{:.4f}",'bottomdepth_m': "{:.1f}",'nasc_swarm': "{:.2f}",'nasc_dbdiff': "{:.2f}"}
                            for col, f in formats.items():
                                dffloat[col] = dffloat[col].map(lambda x: f.format(x))                           
                            # dffloat.to_csv( name + '_nasctable.gzip',compression='gzip' )
                            dffloat.to_csv(self.workpath+'/'+ name + '_nasctable.csv')
                            
                            # df_sv_swarm.astype('float16').to_hdf(self.workpath+'/'+ name + '_sv_swarm.h5', key='df', mode='w'  )
                            
                            # add mask info to xarray
                            t_mask= new_echogram.coords['time']
                            r= new_echogram.coords['depth']
                            
                            # df_mask = pd.DataFrame( np.transpose(mask_swarm))
                            # df_mask.index=t_mask
                            # df_mask.columns=r
                            # df_mask.astype('bool').to_hdf(self.workpath+'/'+ name + '_mask_swarm.h5', key='df', mode='w'  )
                            # if bool(int(config['PROCESSING']['write_mask_as_csv'])) :
                            #     df_mask.astype('int').to_csv(self.workpath+'/'+ name + '_mask_swarm.csv' )
                               
                            ### U-NET
                            # df_mask = pd.DataFrame( np.transpose(mask_unet))
                            # df_mask.index=t_mask
                            # df_mask.columns=r
                            # df_mask.astype('bool').to_hdf(self.workpath+'/'+ name + '_mask_unet.h5', key='df', mode='w'  )
                       
                            
                            
                            # new_echogram = xr.concat([new_echogram,xx], dim="frequency")
                            
                            
                            # if len(np.shape(mask_dbdiff))>1:
                            #     df_mask = pd.DataFrame( np.transpose(mask_dbdiff))
                            #     df_mask.index=t_mask
                            #     df_mask.columns=r
                            #     df_mask.astype('bool').to_hdf(self.workpath+'/'+ name + '_mask_dbdiff.h5', key='df', mode='w'  )
                               
                            #     if bool(int(config['PROCESSING']['write_mask_as_csv'])) :
                            #         df_mask.astype('int').to_csv(self.workpath+'/'+ name + '_mask_dbdiff.csv' )
       
                            #    xx = xr.DataArray(mask_dbdiff,coords={"time": t,"depth": r,"frequency": 1},  dims=("depth","time"))
                            #    new_echogram = xr.concat([new_echogram,xx], dim="frequency")
                                          
                            # breakpoint()
                            if len(np.shape(mask_dbdiff))>1:

                                mas = np.stack([mask_swarm,mask_dbdiff],axis=-1)
                                nc_masks = xr.DataArray(mas,coords={"time": t_mask,"depth": r,"method": ['Swarms','dBdiff']},  dims=("depth","time","method"))
                            else:
                                mas = np.stack([mask_swarm],axis=-1)
                                nc_masks = xr.DataArray(mas,coords={"time": t_mask,"depth": r,"method": ['Swarms']},  dims=("depth","time","method"))
                            nc_masks.to_netcdf(self.workpath+'/'+ name + '_krill_masks.nc')             
                            
                            # if len(np.shape(mask_dbdiff))>1:

                            #     mas = np.stack([mask_swarm,mask_unet,mask_unet_and_shapes,mask_dbdiff],axis=-1)
                            #     nc_masks = xr.DataArray(mas,coords={"time": t_mask,"depth": r,"method": ['Swarms','U-NET','U-NET and Swarms','dBdiff']},  dims=("depth","time","method"))
                            # else:
                            #     mas = np.stack([mask_swarm,mask_unet,mask_unet_and_shapes],axis=-1)
                            #     nc_masks = xr.DataArray(mas,coords={"time": t_mask,"depth": r,"method": ['Swarms','U-NET','U-NET and Swarms']},  dims=("depth","time","method"))
                            # nc_masks.to_netcdf(self.workpath+'/'+ name + '_krill_masks.nc')             

                            
                            new_echogram.to_netcdf(self.workpath+'/'+ name + '_echogram.nc')    
                            new_echogram_raw.to_netcdf(self.workpath+'/'+ name + '_rawechogram.nc')    
                            # self.df_files.loc[i,'to_do'] = False
                            # except Exception as e:
                            #   print(e)                      
                    self.df_files.loc[index,'to_do']=False            
                    self.df_files.drop_duplicates(inplace=True)
                    self.df_files=self.df_files.reset_index(drop=True)
                    self.df_files.to_csv(self.workpath+'/list_of_rawfiles.csv')
                   
                except Exception as e:
                    print(e)               
                    print(traceback.format_exc())
                    # breakpoint()
                    self.df_files.loc[index,'to_do']=False            
                    self.df_files.drop_duplicates(inplace=True)
                    self.df_files=self.df_files.reset_index(drop=True)
                    self.df_files.to_csv(self.workpath+'/list_of_rawfiles.csv')                    
                    
                    
        self.callback_process_active==False
                
    def detect_krill_swarms(self,xr_sv,xr_sv_raw,positions):
          # sv= self.echodata[rawfile][ 120000.0] 
          # sv= self.ekdata[ 120000.0]          
          # 
          # breakpoint()
         
          config = configparser.ConfigParser()
          config.read(self.ini_file)            
          f=float(config['GENERAL']['scrutinization_frequency'])
                  
          surface_exclusion_depth_m    = float(self.config['PROCESSING']['surface_exclusion_depth_m'] )
          maximum_depth_m    = float(self.config['PROCESSING']['maximum_depth_m'] )

         
            
          t120 =xr_sv.coords['time'].data
          r120 =xr_sv.coords['depth'].data
         
          # xr_sv.sel(frequency=f).data

          Sv120= xr_sv.sel(frequency=f).data.copy() 
         
          # bottom = self.bottom_detection(Sv120,-38,0)
          # positions['bottom_depth'] = np.take(  r120,bottom.astype(int)  )

          # remove bttom
         
          for i in range(len(t120)):
              ix_na = r120>=  positions['bottomdepth_m'].values[i] 
              Sv120[ix_na,i]=-999

          # plt.figure(0)
          # plt.clf()
          # plt.imshow(Sv120,aspect='auto',vmin=-80)
          # plt.plot( np.arange(len(bottom)), bottom,'-r')
          # plt.colorbar()
          # plt.draw()
          # plt.savefig('t.png')
       
          # breakpoint()
         
          # # get mask for seabed
          # sv2 = Sv120.copy()
          # sv2[np.isnan(sv2)]=-999
         
          # mb = mSB.ariza(sv2, r120, r0=20, r1=1000, roff=0,
          #                  thr=-38, ec=1, ek=(3,3), dc=10, dk=(5,15))
         
          # print('bottom='+str(mb.sum()))
          # Sv120[mb]=-999
        
          ## swarm method

          swarm_sv_threshold_db  = float(self.config['PROCESSING']['swarm_sv_threshold_db'] )

          # get swarms mask
          k = np.ones((3, 3))/3**2
          Sv120cvv = transform.log(convolve2d(transform.lin( Sv120 ), k,'same',boundary='symm'))   
 
          p120           = np.arange(np.shape(Sv120cvv)[1]+1 )                 
          s120           = np.arange(np.shape(Sv120cvv)[0]+1 )           
          m120sh, m120sh_ = mSH.echoview(Sv120cvv, s120, p120, thr=swarm_sv_threshold_db ,
                                    mincan=(3,10), maxlink=(3,15), minsho=(3,15))

          Sv120sw =  Sv120.copy()
          mask_swarm = m120sh.copy()
  
          # Sv120sw[~m120sh] = np.nan  
          # ixdepthvalid= (r120>=20) & (r120<=500)
          # Sv120sw[ ~ixdepthvalid,: ] =np.nan 
         
          Sv120sw[~m120sh] = -999  
          ixdepthvalid= (r120>=surface_exclusion_depth_m) & (r120<=maximum_depth_m )
          Sv120sw[ ~ixdepthvalid,: ] =-999          
         
          cell_thickness=np.abs(np.mean(np.diff( r120) ))               

          r_new = np.arange(0,r120.max(),10)
          # t_new= np.arange(0,Sv120sw.shape[1],10)
        
        
          sv_lin=np.power(10, Sv120sw /10)
        
          sv_downsampled=  resize_local_mean(sv_lin,[ len(r_new) , Sv120sw.shape[1] ] ,grid_mode =True)

          sv_dep=np.transpose(  np.tile(r_new,[sv_downsampled.shape[1],1] ) )
                          
          sa =  integrate.trapezoid(sv_downsampled,sv_dep,axis=0)  
          nasc_swarm_rs =  4*np.pi*1852**2 * sa
         
          # nasc_swarm_rs =nasc_swarm


          df_sv_swarm=pd.DataFrame( np.transpose(Sv120) )
          df_sv_swarm.index=t120
          df_sv_swarm.columns=r120
          # print('df_sv')
         
          df_nasc_file=pd.DataFrame([])
          # df_nasc_file['time']=positions['ping_time']
          df_nasc_file['lat']=positions['latitude']
          df_nasc_file['lon']=positions['longitude']
          df_nasc_file['distance_m']=np.append(np.array([0]),geod.line_lengths(lons=positions['longitude'],lats=positions['latitude']) )
          df_nasc_file['bottomdepth_m']=positions['bottomdepth_m']
         
          # # breakpoint()
          # bottomdepth=[]         
          # for j in range(Sv120.shape[1]):
          #     row_1=Sv120[:,j]
          #     if np.sum(row_1==-999)>0:
          #         bottomdepth.append( np.min(r120[row_1==-999]) )
          #     else:
          #         bottomdepth.append( r120.max() )
          # # print(bottomdepth)   
          # df_nasc_file['bottomdepth_m']=bottomdepth
            
           
          df_nasc_file['nasc_swarm']=nasc_swarm_rs
          df_nasc_file.index=positions['ping_time']
         
          # df_nasc_file=df_nasc_file.resample('5s').mean()
          # print('Krill detection complete: '+str(np.mean(nasc_swarm)) ) 
         
         
          ## db difference method
          dbdiff_sv_threshold_db   = float(self.config['PROCESSING']['dbdiff_sv_threshold_db'] )

          if np.sum( np.isin( [38000.0, 120000.0],xr_sv.coords['frequency'].data ) ) ==2 :
         
              Sv38= xr_sv.sel(frequency=38000.0).data 
              # remove bttom
              for i in range(len(t120)):
                  ix_na = r120>=  positions['bottomdepth_m'].values[i]-10 
                  Sv38[ix_na,i]=np.nan 
             
              db_diff= Sv120 -Sv38
             
              mask_dbdiff = db_diff>dbdiff_sv_threshold_db 
             
              Sv120db=Sv120.copy()
              Sv120db[~mask_dbdiff]=np.nan
             
              ixdepthvalid= (r120>=surface_exclusion_depth_m) & (r120<=maximum_depth_m )
              Sv120db[~ixdepthvalid,:]=np.nan
             
              cell_thickness=np.abs(np.mean(np.diff( r120) ))               
              nasc_dbdiff=4*np.pi*1852**2 * np.nansum( np.power(10, Sv120db /10)*cell_thickness ,axis=0)   
              df_nasc_file['nasc_dbdiff']=nasc_dbdiff
          else:
              df_nasc_file['nasc_dbdiff']=np.nan
              mask_dbdiff=np.nan
              
          ########## U-NET
          
          # # f =  xr_sv_raw.coords['frequency'].max().data
          # sv_threshold_low=-90
          # sv_threshold_high=-20
         
          # sv= xr_sv_raw.sel(frequency=f).data.copy() 
          # r=xr_sv_raw.coords['depth'].values
          # t=xr_sv_raw.coords['time'].values
          
        
          #  # estimate and correct background noise       
          # p         = np.arange(len(t))                
          # s         = np.arange(len(r))          
 
          # bn, m120bn_ = gBN.derobertis(sv, s, p, 5, 20, r, self.calc_absorption(f,6) ) # whats correct absoprtion?
          # b=pd.DataFrame(bn)
          # bn=  b.interpolate(axis=1).interpolate(axis=0).values                        
          # sv_clean     = transform.log(transform.lin(sv) - transform.lin(bn))
          
          # sv_SNR_threshold_db = 1
          # msn             = mSN.derobertis(sv_clean, bn, thr=sv_SNR_threshold_db)
          # sv_clean[msn] = np.nan

          # ix_f = xr_sv_raw.coords['frequency'] ==  f
          # ix_d = (xr_sv_raw.coords['depth']>0) & (xr_sv_raw.coords['depth']<500)
          # sv = np.squeeze( xr_sv_raw[ix_f,ix_d,:].values ) 
          # sv = np.squeeze( sv_clean[ix_d,:] )

          # sv_normalized = sv.copy()
          # sv_normalized[sv_normalized>sv_threshold_high]= sv_threshold_high
          # sv_normalized[sv_normalized<sv_threshold_low]=sv_threshold_low
          # ix = np.isnan(sv_normalized)
          # sv_normalized[ix]=sv_threshold_low  
          # sv_normalized =  (sv_normalized - sv_threshold_low) / ( sv_threshold_high - sv_threshold_low   )

          # image_n_pixels=256  
          # sv_input= resize(sv_normalized,[image_n_pixels, image_n_pixels])           
          # img = np.expand_dims(sv_input, axis=0)
         
          # # apply unet  
          # pred_mask = model.predict(img)
          # pred=pred_mask[0,:,:,:]
          
          # #filter predictions
          # thrs =  [0.95,0.76,0.70,0.43]
          # minimum_area = [10,10,5,10]
          # masks=np.zeros(pred.shape)

          # for k in range(4):
            
          #   mpred = pred[:,:,k+1]>thrs[k]
          #   labels =  measure.label(  mpred)
            
          #   # probs=measure.regionprops_table(labels,sv120,properties=['label','area','mean_intensity','orientation','major_axis_length','minor_axis_length','weighted_centroid','bbox'])
        
          #   probs=measure.regionprops_table(labels,properties=['label','area','orientation','major_axis_length','minor_axis_length','centroid','bbox'])
        
          #   ix_del =probs['area']<minimum_area[k]
            
          #   if k==1:
          #       ix_del_swarmtosurface =  probs['bbox-0']>(256/500 * 50) # delete pacthes start start below 50m 
          #       ix_del[ix_del_swarmtosurface]=True
          #       # print('del predator ')
            
          #   label_del = probs['label'][ix_del]
          #   for lb in label_del:
          #       ix = labels==lb
          #       labels[ix]=0
          #   m = labels>0
          #   masks[:,:,k]=m    
            
          # footprint = disk(3)
          # masks[:,:,3] = dilation(    masks[:,:,3], footprint)
        
          # mask=np.zeros(pred.shape[0:2])
          # mask [masks[:,:,3]==1]=4
          # mask [masks[:,:,2]==1]=3
          # mask [masks[:,:,1]==1]=2
          # mask [masks[:,:,0]==1]=1
        
          # for ix_t in range( mask.shape[1] ):
          #   profile=mask[:,ix_t] 
            
          #   ix_bottom = np.where(profile==4)[0]
          #   ix_krill = np.where(profile==1)[0]
          #   ix_surfacepredator = np.where(profile==2)[0]
            
          #   if (len(ix_surfacepredator)>0) & (len(ix_krill)>0):
          #       ixdel=ix_surfacepredator[ix_surfacepredator > ix_krill.max()]
          #       mask[ixdel,ix_t]=0
          #   if (len(ix_surfacepredator)>0) & (len(ix_bottom)>0):
          #       ixdel=ix_surfacepredator[ix_surfacepredator > ix_bottom.max()]
          #       mask[ixdel,ix_t]=0
          #   if (len(ix_krill)>0) & (len(ix_bottom)>0):
          #       ixdel=ix_krill[ix_krill > ix_bottom.max()]
          #       mask[ixdel,ix_t]=0
                
      

          
          # n1 =       np.sum(ix_d)
          # n2 = mask_swarm.shape[1]
          # segmentation_unet = np.zeros(mask_swarm.shape)
          # segmentation_unet[ix_d,:]=resize(mask,[n1,n2],preserve_range=True,order=0)  
          # segmentation_unet=np.round(segmentation_unet)
          # segmentation_unet=segmentation_unet.astype(int)
          
          
          # # combine unet and shapes, add patches from swarms
          # segmentation_unet_and_shapes = np.zeros(mask_swarm.shape)
          # ix = (mask_swarm) & ((segmentation_unet!=2) | (segmentation_unet!=3))
          # segmentation_unet_and_shapes[ix]=1          
          # ix = (segmentation_unet==2) 
          # segmentation_unet_and_shapes[ix]=2      
          # ix = (segmentation_unet==3) 
          # segmentation_unet_and_shapes[ix]=3    
          # ix = (segmentation_unet==4) 
          # segmentation_unet_and_shapes[ix]=4       
          
          # sv_lin=np.power(10, Sv120 /10)
          # sv_lin[segmentation_unet_and_shapes!=1]=0       
          # sv_downsampled=  resize_local_mean(sv_lin,[ len(r_new) , Sv120.shape[1] ] ,grid_mode =True)
          # sv_dep=np.transpose(  np.tile(r_new,[sv_downsampled.shape[1],1] ) )                       
          # sa =  integrate.trapezoid(sv_downsampled,sv_dep,axis=0)  
          # nasc_unet =  4*np.pi*1852**2 * sa
          # df_nasc_file['nasc_unet_and_shapes']=nasc_unet
          
                               
          # # breakpoint()
          # # nasc unet
          
          # sv_lin=np.power(10, Sv120 /10)
          # sv_lin[segmentation_unet!=1]=0       
          # sv_downsampled=  resize_local_mean(sv_lin,[ len(r_new) , Sv120.shape[1] ] ,grid_mode =True)
          # sv_dep=np.transpose(  np.tile(r_new,[sv_downsampled.shape[1],1] ) )                       
          # sa =  integrate.trapezoid(sv_downsampled,sv_dep,axis=0)  
          # nasc_unet =  4*np.pi*1852**2 * sa
          # df_nasc_file['nasc_unet']=nasc_unet
          

          print('Shapes avg NASC: '+str(df_nasc_file['nasc_swarm'].mean()) ) 
          # print('U-NET avg NASC: '+str(df_nasc_file['nasc_unet'].mean()) ) 

          
          print('Shapes: '+ str( np.round((np.sum(mask_swarm) / mask_swarm.size )*100,2)) + ' % krill pixels' )
          try:
              print('db diff: '+ str( np.round((np.sum(mask_dbdiff) / mask_dbdiff.size )*100,2)) + ' % krill pixels' )
          except:
              pass
          # print('U-NET: '+ str( np.round((np.sum(mask==1) / mask.size )*100,2)) + ' % krill pixels' )


            
             
          return df_nasc_file, mask_swarm, mask_dbdiff #segmentation_unet #,segmentation_unet_and_shapes
 
        
         
    # def start():
    #     print('start')

    def callback_email(self):
      if  (self.callback_email_active==False) :      
        self.callback_email_active==True
        print('checking wether to send email')
        self.config = configparser.ConfigParser()
        self.config.read(self.ini_file)   
                
        emailfrom = self.config['EMAIL']['email_from']
        emailto = self.config['EMAIL']['email_to']
        password = str(self.config['EMAIL']['pw'])
        # fileToSend = r"D20220212-T180420_nasctable.h5"
        # username = "raw2nasc"
        # password = "raw2nasckrill"
        # print(self.config['EMAIL']['email_send'])
        email_send =int(self.config['EMAIL']['email_send'])
        # print(email_send)
        if email_send>0:
            # breakpoint()
            
            # self.workpath=  os.path.join(self.folder_source,'krill_data')
            
            # os.chdir(self.workpath)
            # self.df_files=pd.read_csv(self.workpath+'/list_of_rawfiles.csv')
           
            nasc_done =  pd.DataFrame( glob.glob( self.workpath+'/*_nasctable.h5' ) )
            if len(nasc_done)>0:               
                if os.path.isfile(self.workpath+'/list_of_sent_files.csv'):
                    df_files_sent =  pd.read_csv(self.workpath+'/list_of_sent_files.csv',index_col=0)
                    ix_done= nasc_done.iloc[:,0].isin( df_files_sent.iloc[:,0]  )  
                    nasc_done=nasc_done[~ix_done]
                
                else:    
                    df_files_sent=pd.DataFrame([])
                
                nascfile_times=[]
                for fname in nasc_done.iloc[:,0]:         
                    datetimestring=re.search('D\d\d\d\d\d\d\d\d-T\d\d\d\d\d\d',fname).group()
                    nascfile_times.append( pd.to_datetime( datetimestring,format='D%Y%m%d-T%H%M%S' ) )
                
                # nascfile_times=pd.to_datetime( nasc_done.iloc[:,0] ,format='D%Y%m%d-T%H%M%S_nasctable.h5' )
                nasc_done=nasc_done.iloc[np.argsort(nascfile_times),0].values
                     
                n_files=int(self.config['EMAIL']['files_per_email'])
                send_echograms=int(self.config['EMAIL']['send_echograms'])
                echogram_resolution_in_seconds=str(self.config['EMAIL']['echogram_resolution_in_seconds'])
                print( str(len(nasc_done)) +' files that can be sent')
    
                while (len(nasc_done)>n_files) :
                    
                    
                    files_to_send=nasc_done[0:n_files]
                    # print(nasc_done)
                    
                    msg = MIMEMultipart()
                    msg["From"] = emailfrom
                    msg["To"] = emailto
                    msg["Subject"] = "Krillscan data from "+ self.config['GENERAL']['vessel_name']+' ' +files_to_send[0][-30:-13]+'_to_'+files_to_send[-1][-30:-13]
                  
                    msgtext = str(dict(self.config['GENERAL']))
                    msg.attach(MIMEText( msgtext   ,'plain'))
    
                    loczip = msg["Subject"]+'.zip'
                    zip = zipfile.ZipFile(loczip, "w", zipfile.ZIP_DEFLATED)
                    zip.write(self.ini_file)
    
                    for fi in files_to_send:   
                        zip.write(fi,arcname=fi[-30:]  )                                  
    
                    if send_echograms>0:                       
                        for fi in files_to_send:      
                            
                            
                            # breakpoint()

                            xr_sv = xr.open_dataarray(self.workpath+'/'+fi[-30:-13] + '_echogram.nc')
                            
                            # f=float(self.config['GENERAL']['scrutinization_frequency'])

              
                            # ix_f = np.where( xr_sv.coords['frequency'].values==f)[0][0] 
                            
                            xr_mail= xr_sv.resample(time=echogram_resolution_in_seconds+'s').mean()
                            # xr_mail.astype('float16')
                            targetname=fi[-30:-13] + '_mail_echogram.nc' 
                            xr_mail.to_netcdf(targetname)    
                            zip.write(targetname)                                                      
                            os.remove(targetname)
                            
    

                            # sv = np.transpose( np.squeeze( xr_sv[ix_f,:,:].data) )

                            # df=pd.DataFrame(sv)
                            # df.index= xr_sv.coords['time'].values
                            # df.columns= xr_sv.coords['depth'].values
                                                                                    
                            # df=df.resample(echogram_resolution_in_seconds+'s').mean()
                            # targetname=fi[-30:-13] + '_sv_swarm_mail.h5' 
                            # df.astype('float16').to_hdf(targetname,key='df',mode='w')
                            # # df.astype('float16').to_csv(targetname,compression='gzip')
                            # zip.write(targetname)                                                      
                            # os.remove(targetname)
                            
                            # resample mask
                            mask_swarm= pd.read_hdf( self.workpath+'/'+fi[-30:-13] + '_mask_swarm.h5',key='df' ) 
                            mask_swarm=mask_swarm.resample(echogram_resolution_in_seconds+'s').mean()
                            mask_swarm[mask_swarm>=0.5]=1
                            mask_swarm[mask_swarm<0.5]=0
                            mask_swarm=mask_swarm.astype(bool)                            
                            targetname=fi[-30:-13] + '_mail_mask_swarm.h5' 
                            mask_swarm.astype('bool').to_hdf(targetname,key='df',mode='w')
                            zip.write(targetname)                                                      
                            os.remove(targetname)
                            
                    zip.close()
                    fp = open(loczip, "rb")
                    attachment = MIMEBase('application', 'x-zip')
                    attachment.set_payload(fp.read())
                    fp.close()
                    encoders.encode_base64(attachment)
                    attachment.add_header("Content-Disposition", "attachment", filename=loczip)
                    msg.attach(attachment)    
                    
                    os.remove(loczip)
    
                    try:        
                        ctx = ssl.create_default_context()
                        server = smtplib.SMTP_SSL("smtp.gmail.com", port=465, context=ctx)
                        
                        server.login(emailfrom, password)
                        
                        # print(df_files_sent)
                    
                        server.sendmail(emailfrom, emailto.split(','), msg.as_string())
                        if len(df_files_sent)>0:
                            df_files_sent= pd.concat([pd.Series(df_files_sent.iloc[:,0].values),pd.DataFrame(files_to_send)],ignore_index=True)
                        else:
                            df_files_sent=pd.DataFrame(files_to_send)
                            
                        # df_files_sent=df_files_sent.reset_index(drop=True)
                        df_files_sent=df_files_sent.drop_duplicates()
                        df_files_sent.to_csv(self.workpath+'/list_of_sent_files.csv')
                        
                        
                        print('email sent: ' +   msg["Subject"] )
                        nasc_done=nasc_done[n_files::]
                        server.quit()
    
                    except Exception as e:
                        print(e)
                                        
        
        self.callback_email_active==False
        
#%%
# os.chdir( r'C:\Users\a5278\Documents\postdoc_krill\krillscan\krillscan_github' )


ks=krillscan_class()
# ks.start(r'C:\Users\a5278\Documents\postdoc_krill\krillscan\krillscan_github\settings.ini')

# ks.start(r'C:\Users\a5278\Documents\postdoc_krill\CCAMLR_data\settings_ccamlr.ini')
# ks.start(r"E:\krillscan_cruise_2024_2\settings2024.ini")
# ks.start(r"F:\krillscan2016\settings.ini")

# ks.start_para_processing('settings.ini')

# ks.stop()
# ks.inspect()