# -*- coding: utf-8 -*-
"""
Created on Fri Apr 21 11:01:11 2023

@author: Administrator
"""

import configparser
from scipy.signal import find_peaks

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt
import glob 
import os
import logging
from matplotlib.backend_bases import MouseButton

from scipy.ndimage.filters import uniform_filter1d

from scipy.signal import convolve2d
from scipy.interpolate import interp1d


from skimage.transform import rescale, resize 

from pyproj import Geod
geod = Geod(ellps="WGS84")

import sys
import matplotlib

from PyQt5 import QtCore, QtGui, QtWidgets

from matplotlib.gridspec import GridSpec
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import qdarktheme
import time

from matplotlib.path import Path as MPL_Path

from mpl_toolkits.axes_grid1.inset_locator import inset_axes

from matplotlib.colors import ListedColormap
import re
import traceback
import zipfile

import xarray as xr
import matplotlib.dates as mdates

import cartopy
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from matplotlib import gridspec

#%% inspection GUI

class MplCanvas(FigureCanvasQTAgg ):

    def __init__(self, parent=None, dpi=150):
        self.fig = Figure(figsize=None, dpi=dpi,facecolor='gray')
        super(MplCanvas, self).__init__(self.fig)

        
class MainWindow(QtWidgets.QMainWindow):
    

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.canvas =  MplCanvas(self, dpi=150)
                
        self.echodata=dict()
        self.echodata_swarm=dict()
        self.df_nasc=pd.DataFrame([])

        
        self.filecounter=-1
        self.filenames = None
        self.df_files = pd.DataFrame([])

        self.folder_source=''
        self.statusBar().setStyleSheet("background-color : k")


        menuBar = self.menuBar()

        # Creating menus using a title
        openMenu = menuBar.addAction("Select echogram files")
        openMenu.triggered.connect(self.openfiles_fun)

        
        self.showfolderbutton =  menuBar.addAction('Show data folder')
        # self.showfolderbutton.setEnabled(False)
        self.showfolderbutton.triggered.connect(self.showfoldefunc)     

        
        self.showfolderbutton =  menuBar.addAction('Undo mask change')
        # self.showfolderbutton.setEnabled(False)
        self.showfolderbutton.triggered.connect(self.undo_mask)     
        
        self.freresp_button =  menuBar.addAction('Measure frequency response')
        # self.showfolderbutton.setEnabled(False)
        self.freresp_button.triggered.connect(self.measure_frec_response)     
        
        
  
        quitMenu = menuBar.addAction("Quit")
        quitMenu.triggered.connect(self.func_quit)     
    

        toolbar = QtWidgets.QToolBar()

        self.checkbox_mask=QtWidgets.QCheckBox('Save changes')
        self.checkbox_mask.setChecked(False)            
        toolbar.addWidget(self.checkbox_mask)
        
        self.checkbox_raw=QtWidgets.QCheckBox('Raw')
        self.checkbox_raw.setChecked(False)           
        self.checkbox_raw.clicked.connect(self.choose_raw_changed)          
        toolbar.addWidget(self.checkbox_raw)

        toolbar.addWidget(QtWidgets.QLabel('Freq.:'))        
        self.choose_freq = QtWidgets.QComboBox()
        self.choose_freq.addItem('38')
        self.choose_freq.addItem('120')
        self.choose_freq.addItem('200')
        self.choose_freq.setCurrentIndex(1)
        toolbar.addWidget(  self.choose_freq)
        toolbar.addWidget(QtWidgets.QLabel('kHz'))            
        self.choose_freq.activated[str].connect(self.choose_freq_changed) 
        
        self.checkbox_showmask=QtWidgets.QCheckBox('Show mask')
        self.checkbox_showmask.setChecked(True)           
        self.checkbox_showmask.clicked.connect(self.choose_raw_changed)          
        toolbar.addWidget(self.checkbox_showmask)
        
        
        toolbar.addWidget(QtWidgets.QLabel('Mask method:'))        
        self.choose_maskmethod = QtWidgets.QComboBox()
        self.choose_maskmethod.addItem('Swarms')
        self.choose_maskmethod.addItem('dB-diff')
        # self.choose_maskmethod.addItem('U-NET')
        self.default_method='Swarms'
        self.choose_maskmethod.setCurrentIndex(2)
        toolbar.addWidget(  self.choose_maskmethod)
        self.choose_maskmethod.activated[str].connect(self.choose_maskmethod_changed) 



        toolbar.addWidget(QtWidgets.QLabel('Color:'))        
        self.choose_color = QtWidgets.QComboBox()
        self.choose_color.addItem('viridis')
        self.choose_color.addItem('plasma')
        self.choose_color.addItem('jet')
        self.choose_color.setCurrentIndex(2)
        toolbar.addWidget(  self.choose_color)
        self.choose_color.activated[str].connect(self.choose_color_changed) 
        
        

        toolbar.addWidget(QtWidgets.QLabel('Min. depth:'))        
        self.excl_depth_spin = QtWidgets.QSpinBox()
        self.excl_depth_spin.setMinimum(0)
        self.excl_depth_spin.setMaximum(8000)
        self.excl_depth_spin.setValue(20)
        toolbar.addWidget(  self.excl_depth_spin)
        toolbar.addWidget(QtWidgets.QLabel('m'))        

        toolbar.addWidget(QtWidgets.QLabel('Max. depth:'))        
        self.max_depth_spin = QtWidgets.QSpinBox()
        self.max_depth_spin.setMinimum(0)
        self.max_depth_spin.setMaximum(8000)
        self.max_depth_spin.setValue(500)

        toolbar.addWidget(  self.max_depth_spin)
        toolbar.addWidget(QtWidgets.QLabel('m'))              
        
        self.butt_prev=QtWidgets.QPushButton('<-- previous')
        self.butt_prev.clicked.connect(self.plot_prev)        
        toolbar.addWidget(self.butt_prev)

        self.butt_next=QtWidgets.QPushButton('Next -->')
        self.butt_next.clicked.connect(self.plot_next)        
        toolbar.addWidget(self.butt_next)
        
                #### hotkeys
        self.msgSc1 = QtWidgets.QShortcut(QtCore.Qt.Key_Right, self)
        self.msgSc1.activated.connect(self.plot_next)
        self.msgSc2 = QtWidgets.QShortcut(QtCore.Qt.Key_Left, self)
        self.msgSc2.activated.connect(self.plot_prev)        


        self.butt_removearea=QtWidgets.QPushButton('Remove area')
        self.butt_removearea.clicked.connect(self.mask_removearea)        
        toolbar.addWidget(self.butt_removearea)
        
        self.butt_addarea=QtWidgets.QPushButton('Add area')
        self.butt_addarea.clicked.connect(self.mask_addarea)        
        toolbar.addWidget(self.butt_addarea)
        
        toolbar.addSeparator()

         
        tnav = NavigationToolbar( self.canvas, self)       
        toolbar.addWidget(tnav)
       
        outer_layout = QtWidgets.QVBoxLayout()
        outer_layout.addWidget(toolbar)
        outer_layout.addWidget(self.canvas)
    
        # Create a placeholder widget to hold our toolbar and canvas.
        widget = QtWidgets.QWidget()
        widget.setLayout(outer_layout)
        self.setCentralWidget(widget)
        
        
        self.show()  
   

        self.cmap_mask = ListedColormap( np.array([[1,0,0, 1. ]] ) )
        
        
        self.t=[-1,-1]
        self.plotwindow_startsecond=0
        self.plotwindow_length=0
        self.choosen_f_index=0
        
    def settings_edit(self):
        os.startfile(self.ini_file)    
   
                  
    def showfoldefunc(self):    
         os.startfile(self.workpath)
         
    def openfiles_fun(self):
        
        fname_canidates, ok = QtWidgets.QFileDialog.getOpenFileNames(self,"QFileDialog.getOpenFileNames()",'',"Echogram Files (*_echogram.nc)")
         
        if len( fname_canidates ) >0:
            
            self.filenames = np.array( fname_canidates )   
            print(  fname_canidates )
            
            self.workpath = os.path.dirname( fname_canidates[0])
        
            self.filecounter=-1
               
            # breakpoint()
            ### read track
            self.track_all=pd.DataFrame([])
            for fname in self.filenames:        
                # fname= self.filenames[0]
                
                # if fname.split('.')[-1]=='nc':
  
                a = pd.read_csv( fname[:-12] + '_nasctable.csv' )
                track=a.loc[:,['lat','lon']]
                track.index=pd.to_datetime(a['ping_time'])
                track=track.interpolate().resample('1min').mean()
                self.track_all = pd.concat([self.track_all,track])
            
            self.plot_next()
            
            
    def choose_color_changed(self):
        if self.filecounter>=0:        
            self.plot_echogram()

    def choose_raw_changed(self):
        if self.filecounter>=0:        
            self.plot_echogram()
            
    def plot_echogram(self):    
        
                
        # breakpoint()
        
        ix_f = self.xr_sv.coords['frequency']== int(self.choose_freq.currentText()) *1000
        sv = np.squeeze( self.xr_sv[ix_f,:,:])
        

            
                
        # sv = sv.interpolate_na( dim='time', method="linear")
        
        # sv = sv.interpolate_na(  'depth',max_gap=3,method="linear")
        # sv = sv.interpolate_na(  'time' ,max_gap=pd.Timedelta(seconds=5))
        
        # sv = sv.interp(time=sv.time , depth=sv.depth, method="linear")
        # ix_method = self.xr_masks.coords['method']== 'Manual'
        # manual=np.squeeze( self.xr_masks[:,:,ix_method])
        
        ix_method = self.xr_masks.coords['method'].values.tolist().index(self.choose_maskmethod.currentText()) 

        mask_plot =np.squeeze( self.xr_masks[:,:,ix_method])
        
        # self.mask_plot[manual==True]=True
        # self.mask_plot[manual==False]=False
        
        ixdepthvalid= ( self.xr_sv.coords['depth'] >= self.excl_depth_spin.value() ) & ( self.xr_sv.coords['depth']  <= self.max_depth_spin.value())
        mask_plot[~ixdepthvalid,:]=False  

        sv_mask=sv.values.copy()
        sv_mask[mask_plot.values==0]=np.nan

        
        cell_thickness=np.abs(np.mean(np.diff( self.xr_sv.coords['depth']) ))        
        
        track= pd.DataFrame([])
        track.index= self.xr_sv.coords['time']      
        track['nasc_swarm'] =4*np.pi*1852**2 * np.nansum( np.power(10, sv_mask /10)*cell_thickness ,axis=0)   
          
        # peak filter
        x = track['nasc_swarm'].values.copy()
        peaks, peak_meta = find_peaks(x,prominence=10000,width=[0,2] )
        # x[peaks]=np.nan
        
        ix1 = np.round( peak_meta['left_ips']).astype(int)-1
        ix2 = np.round( peak_meta['right_ips']).astype(int)+1
        
        ix1[ix1<0]=0
        ix2[ix2>len(x)-1]=len(x)-1
        
        for i1,i2 in zip(ix1,ix2):
            x[i1:i2]=np.nan

        track['nasc_swarm']=x
        track['nasc_swarm']=track['nasc_swarm'].interpolate()
        
        # duration =     ( self.xr_sv.coords['time'][-1] - self.xr_sv.coords['time'][0]).data  / np.timedelta64(1, 's')
        # dm=self.xr_sv.coords['depth'][-1].data
        
        
        self.canvas.fig.clf() 
                
        # self.ax = self.canvas.fig.subplots(2, 2,gridspec_kw={'height_ratios': [1, 3],'width_ratios': [4, 1]},sharex='col')
        
        
        gs = self.canvas.fig.add_gridspec(2,2,width_ratios=[4, 1],height_ratios=[1, 3])
        
        # breakpoint()

        # gs = gridspec.GridSpec(2, 2,figure=self.canvas.fig, width_ratios=[4, 1],height_ratios=[1, 3]) 
        ax2 = self.canvas.fig.add_subplot(gs[1,0])
        ax1 = self.canvas.fig.add_subplot(gs[0,0],sharex=ax2)

        ax3 = self.canvas.fig.add_subplot(gs[1,1], projection=ccrs.PlateCarree())
        ax4 = self.canvas.fig.add_subplot(gs[0,1])

        self.ax0=ax1
        self.ax1=ax2
        self.ax2=ax3
        self.ax3=ax4
        
        # ax4 = self.canvas.fig.subplot(gs[1])

        # self.ax=[ax1,ax2,ax3]
        
        # ax1 = plt.subplot(221,gridspec_kw={'height_ratios': [1, 3],'width_ratios': [4, 1]},sharex='col')
        # ax2 = plt.subplot(223)
        # ax3 = plt.subplot(122, projection=ccrs.PlateCarree())

        
        # ax=self.ax

        ax1.plot( track['nasc_swarm'] , '-k')
        ax1.plot( track['nasc_swarm'].resample('1min').mean(), '.-b')
        
        
        ax1.grid()
        # ax[0].set_xlim( self.xr_sv.coords['time'].min() , self.xr_sv.coords['time'].max())
        ax1.set_ylabel('NASC')
        
        # plt.gca=ax[1]
        
        x_lims = mdates.date2num( [  self.xr_sv.coords['time'].min().values , self.xr_sv.coords['time'].max().values ])
        
        x_lims_larger = mdates.date2num( [  self.xr_sv.coords['time'].min().values - pd.Timedelta(10,'s') , self.xr_sv.coords['time'].max().values+ pd.Timedelta(10,'s') ])


        range_max = self.xr_sv.coords['depth'].max()
        # ext=[x_lims[0] ,x_lims[1],-range_max ,0 ]
        ext=[x_lims[0] ,x_lims[1],-range_max ,0 ]
       
        fname= self.filenames[self.filecounter]
        self.xr_sv_raw = xr.open_dataarray(fname[:-12] + '_rawechogram.nc')
        
        if self.checkbox_raw.isChecked():         
            sv_raw = np.squeeze( self.xr_sv_raw[ix_f,:,:])
            im = ax2.imshow( sv_raw,cmap= self.choose_color.currentText()   ,aspect='auto',vmin=-90,vmax=-30,extent=ext)
            
        else:    
            im = ax2.imshow( sv,cmap= self.choose_color.currentText()   ,aspect='auto',vmin=-90,vmax=-30,extent=ext)
        
        masked_data = np.ma.masked_where(mask_plot == 1, mask_plot)
        
        if self.checkbox_showmask.isChecked():         
            ax2.imshow( masked_data  ,aspect='auto',extent=ext,cmap=self.cmap_mask,alpha=0.3)
        
        
        # cbar3 = plt.colorbar(im)
        ax2.xaxis_date()
        ax2.grid()
        ax2.set_ylabel('Depth in m')
        y_lims = -self.max_depth_spin.value(),0
        ax2.set_ylim(y_lims)
        ax2.set_xlim(x_lims_larger)


        ax2.plot(x_lims_larger,[-self.excl_depth_spin.value(),-self.excl_depth_spin.value()] ,'-r' )
        
        

        cbaxes = inset_axes(ax2, width="15%", height="3%", loc='lower left',  bbox_to_anchor=(0.05, 0.15, 1, 1) ,bbox_transform= ax2.transAxes) 
        self.canvas.fig.colorbar(im,cax=cbaxes,label='$s_v$', orientation='horizontal')        
            
        
            #         cbaxes = inset_axes(self.canvas.axes4, width="100%", height="100%", loc=3,bbox_to_anchor=(.05, .15, .4, .04),bbox_transform=self.canvas.axes4.transAxes) 
            # cbar=self.canvas.fig.colorbar(sc,cax=cbaxes, orientation='horizontal')
            
        # ax4.axis('off')


        ########## map
        la = self.track['lat']
        lo = self.track['lon']
        
        
        # ax[1,1] 
        # axmap = plt.axes(projection=cartopy.crs.PlateCarree())



        axmap = ax3

        axmap.add_feature(cfeature.LAND)
        axmap.add_feature(cfeature.OCEAN)
        axmap.add_feature(cfeature.COASTLINE)
        axmap.add_feature(cfeature.BORDERS, linestyle=':')
        axmap.add_feature(cfeature.LAKES, alpha=0.5)
        axmap.add_feature(cfeature.RIVERS)

        axmap.plot(self.track_all['lon'],self.track_all['lat'],'-k'  , transform=ccrs.PlateCarree())

        
        axmap.plot(lo,la,'.r'  , transform=ccrs.PlateCarree())
        axmap.plot(lo.values[-1],la.values[-1],'.b'  , transform=ccrs.PlateCarree())



          
        g1=axmap.gridlines(draw_labels=True)
        g1.xlabels_top = False
        g1.ylabels_left = False


        f = self.xr_sv_raw.coords['frequency'].values

        # fr_min = self.xr_sv_raw.min(dim=['depth','time']).values
        # fr_max = self.xr_sv_raw.max(dim=['depth','time']).values

        # fr_min = fr_min - fr_min.min()
        # fr_max = fr_max - fr_max.min()
        # breakpoint()
        
        fr_min =(self.xr_sv_raw - self.xr_sv_raw.min(dim='frequency')) .min(dim=['depth','time'])
        fr_max =(self.xr_sv_raw - self.xr_sv_raw.min(dim='frequency')) .max(dim=['depth','time'])


        ax4.fill_between(f,fr_min, fr_max,color='b',alpha=0.2)
         
        self.fr_plot,  = ax4.plot([],[], 'o-b')
        ax4.grid()
        ax4.set_xlabel('Hz')
        ax4.set_ylabel('dB difference')
        

        # ax4.draw(renderer)

        # 
        ######## interactive
        
        # def on_move(event):
        #     if event.inaxes:
        #         print(f'data coords {event.xdata} {event.ydata},',
        #               f'pixel coords {event.x} {event.y}')
        
        # plt.connect('motion_notify_event', on_move)
        # renderer = self.canvas.fig.canvas.renderer   

        
        # def on_move(event):
        #  # print('you pressed', event.button, event.xdata, event.ydata)
        #  # try:   
        #  if event.xdata is not None:
        #     if (event.xdata>x_lims[0]) & (event.xdata<x_lims[1]) & (event.ydata>y_lims[0]) & (event.ydata<y_lims[1]) :
              
        #         # print('you pressed', event.button, event.xdata, event.ydata)
                
        #         xx = event.xdata
        #         ix_t=  int(np.round( (xx-x_lims[0] )/(x_lims[1]-x_lims[0]) * (len(self.xr_sv_raw.coords['time'])-1) ))
        #         ix_d = int(np.argmin(np.abs(event.ydata - (-self.xr_sv_raw.coords['depth'].values))))
                
        #         sv_fr = self.xr_sv_raw[:,ix_d,ix_t].values
        #         sv_fr = sv_fr - sv_fr.min()


        #         f = self.xr_sv_raw.coords['frequency'].values
                
        #         self.fr_plot.set_xdata(f)
        #         self.fr_plot.set_ydata(sv_fr)
        #         # ax4.relim()
        #         # ax4.autoscale_view()

        #         # ax4.draw(renderer)
        #         self.canvas.draw()
         # except:
         #    pass
        
        # self.cid_hover=self.canvas.fig.canvas.mpl_connect('button_press_event', on_move)

        self.canvas.fig.tight_layout()
        self.canvas.draw()

   
    def choose_freq_changed(self):
        if self.filecounter>=0:   
            self.plot_echogram()
            self.choosen_f_index = int(self.choose_freq.currentText()) *1000

            
           

    def choose_maskmethod_changed(self):
        self.default_method=str(self.choose_maskmethod.currentText()) 
        print(self.default_method)
        if self.filecounter>=0: 

            self.plot_echogram()
            
        
    def read_file_and_mask(self):    
        if self.filecounter>=0:        
            fname= self.filenames[self.filecounter]
            
            # if fname.split('.')[-1]=='nc':
            
            
            self.xr_sv = xr.open_dataarray(fname)
            
            self.track = pd.read_csv( fname[:-12] + '_nasctable.csv' ,index_col=0)

            
            # breakpoint()
            
            f_list = (self.xr_sv.coords['frequency'].values / 1000).astype(int).astype(str)
            self.choose_freq.clear()
            if isinstance(f_list, str):
                f_list=[f_list]
            self.choose_freq.addItems(f_list)
            
            try:
                ix_120 = np.where( self.xr_sv.coords['frequency'].values==self.choosen_f_index)[0][0] 
            except:
                ix_120 = np.argmax( self.xr_sv.coords['frequency'].values)
            
            self.choose_freq.setCurrentIndex( ix_120 )
            # self.choose_freq.setCurrentIndex( np.argmax(self.xr_sv.coords['frequency'].values) )

            self.xr_masks = xr.open_dataarray( fname[:-12] + '_krill_masks.nc' )
            self.xr_masks.load()
            
            # add manual mask?
            if self.xr_masks.coords['method'].values.tolist().count('Manual')==0:
                s2=len( self.xr_masks.coords['time'])
                s1=len( self.xr_masks.coords['depth'])
                mask_manual= np.zeros([s1,s2]).astype(bool)   
                mask_manual= np.expand_dims(mask_manual, axis=-1)
                man = xr.DataArray(mask_manual,coords={"time": self.xr_masks.coords['time'],"depth":  self.xr_masks.coords['depth'],"method": ['Manual']},  dims=("depth","time","method"))
    
                self.xr_masks = xr.concat([self.xr_masks,man], dim='method')
                
            m_list = self.xr_masks.coords['method'].values.astype(str)
            self.choose_maskmethod.clear()
            if isinstance(m_list, str):
                m_list=[m_list]
            self.choose_maskmethod.addItems(m_list)
            
            
    
            
            # ["foo", "bar", "baz"].index("bar")
            
            # try:
            ix_me = self.xr_masks.coords['method'].values.tolist().  index(self.default_method)
            # except:
            #     ix_me = 0 
            
            self.choose_maskmethod.setCurrentIndex( ix_me )
            

         
            # ixdepthvalid= ( self.xr_sv.coords['depth'] >= self.excl_depth_spin.value() ) & ( self.xr_sv.coords['depth']  <= self.max_depth_spin.value())
            # self.mask_manual.values[~ixdepthvalid,:]=False
             
            # if os.path.isfile(fname[:-12] + '_mask_manual.h5' ):     
            #     self.mask_manual= np.transpose(  pd.read_hdf( fname[:-12] + '_mask_manual.h5',key='df' ) )
            # else:
            #     if os.path.isfile(fname[:-12] + '_mask_swarm.h5' ):     
            #         self.mask_swarm= np.transpose(  pd.read_hdf( fname[:-12] + '_mask_swarm.h5',key='df' ) )
            #         self.mask_manual = self.mask_swarm.copy()
            #         ixdepthvalid= ( self.xr_sv.coords['depth'] >= self.excl_depth_spin.value() ) & ( self.xr_sv.coords['depth']  <= self.max_depth_spin.value())
            #         self.mask_manual.values[~ixdepthvalid,:]=False  
            #     else:
                    
            #         s2=len( self.xr_sv.coords['time'])
            #         s1=len( self.xr_sv.coords['depth'])
            #         self.mask_manual=pd.DataFrame( np.ones([s1,s2]).astype(bool)   )
            #         self.mask_manual.columns=self.xr_sv.coords['time']
            #         self.mask_manual.index=self.xr_sv.coords['depth']
            #         ixdepthvalid= ( self.xr_sv.coords['depth'] >= self.excl_depth_spin.value() ) & ( self.xr_sv.coords['depth']  <= self.max_depth_spin.value())
            #         self.mask_manual.values[~ixdepthvalid,:]=False                  
          
            self.mask_manual_old=self.xr_masks[:,:,-1]
  
                
            # self.mask_dbdiff= np.transpose( pd.read_hdf( fname[:-12] + '_mask_dbdiff.h5',key='df' ) )
            
    def measure_frec_response(self):
        x_lims = mdates.date2num( [  self.xr_sv.coords['time'].min().values , self.xr_sv.coords['time'].max().values ])
        y_lims = -self.max_depth_spin.value(),0

        def on_move(event):
         # print('you pressed', event.button, event.xdata, event.ydata)
         # try:   
         if event.xdata is not None:
            if (event.xdata>x_lims[0]) & (event.xdata<x_lims[1]) & (event.ydata>y_lims[0]) & (event.ydata<y_lims[1]) :
              
                # print('you pressed', event.button, event.xdata, event.ydata)
                
                xx = event.xdata
                ix_t=  int(np.round( (xx-x_lims[0] )/(x_lims[1]-x_lims[0]) * (len(self.xr_sv_raw.coords['time'])-1) ))
                ix_d = int(np.argmin(np.abs(event.ydata - (-self.xr_sv_raw.coords['depth'].values))))
                
                sv_fr = self.xr_sv_raw[:,ix_d,ix_t].values
                sv_fr = sv_fr - sv_fr.min()


                f = self.xr_sv_raw.coords['frequency'].values
                
                self.fr_plot.set_xdata(f)
                self.fr_plot.set_ydata(sv_fr)
                # ax4.relim()
                # ax4.autoscale_view()

                # ax4.draw(renderer)
                self.canvas.draw()
         # except:
         #    pass
        
        self.cid_hover=self.canvas.fig.canvas.mpl_connect('button_press_event', on_move)

            
    def undo_mask(self):
        
        ix_method = self.xr_masks.coords['method']== str(self.choose_maskmethod.currentText()) 
        self.xr_masks[:,:,ix_method] = self.mask_manual_old.copy() 
        
        
            # self.xr_masks[:,:,ix_method]=np.expand_dims(mm,axis=-1)

        self.plot_echogram()            

                
    def onclick_draw(self,event):
            # print('%s click: button=%d, x=%d, y=%d, xdata=%f, ydata=%f' %
            #       ('double' if event.dblclick else 'single', event.button,
            #        event.x, event.y, event.xdata, event.ydata))
            if event.button==1 & event.dblclick:
                self.draw_x= pd.concat([self.draw_x,pd.Series(event.xdata) ],ignore_index=True )
                self.draw_y=pd.concat([self.draw_y,pd.Series(event.ydata) ],ignore_index=True )
                # self.f_limits=self.canvas.axes.get_ylim()
                # self.t_limits=self.canvas.axes.get_xlim()   
                
                line = self.line_2.pop(0)
                line.remove()        
                self.line_2 =self.ax1.plot(self.draw_x,self.draw_y,'.-r')      
                self.canvas.draw()    
                         
                # func_draw_shape_plot()   
              
            if event.button==3:
                self.draw_x=self.draw_x.head(-1)
                self.draw_y=self.draw_y.head(-1)
                # self.f_limits=self.canvas.axes.get_ylim()
                # self.t_limits=self.canvas.axes.get_xlim()
                # func_draw_shape_plot()              
                line = self.line_2.pop(0)
                line.remove()        
                self.line_2 =self.ax1.plot(self.draw_x,self.draw_y,'.-r')     
                self.canvas.draw()                   
 
    def mask_removearea(self):
            
        # msg = QtWidgets.QMessageBox()
        # msg.setIcon(QtWidgets.QMessageBox.Information)   
        # msg.setText("Add points with double left click.\nRemove latest point with single right click. \nExit draw mode by pushing enter")
        # msg.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
        # returnValue = msg.exec()    
        # if returnValue == QtWidgets.QMessageBox.Ok:
            self.butt_removearea.setEnabled(False)   
            print('drawing')  
            self.draw_x=pd.Series(dtype='float')
            self.draw_y=pd.Series(dtype='float')
            self.d_limits=self.ax1.get_ylim()
            self.t_limits=self.ax1.get_xlim()
            self.plot_echogram()
            
            # self.canvas.fig.canvas.mpl_disconnect(self.cid_hover)    
            self.cid2=self.canvas.fig.canvas.mpl_connect('button_press_event', self.onclick_draw)
            self.line_2 =self.ax1.plot(self.draw_x,self.draw_y,'.-r')        
            # self.plot_echogram()   
            self.drawexitm = QtWidgets.QShortcut(QtCore.Qt.Key_Return, self)
            self.drawexitm.activated.connect(self.func_draw_shape_exit_remove)  
            
            
         
    def func_draw_shape_exit_remove(self):
        # print('save shape' + str(self.draw_x.shape))
        self.canvas.fig.canvas.mpl_disconnect(self.cid2)
        ## deactive shortcut
        self.drawexitm.setEnabled(False)  

        if self.draw_x.shape[0]>2:

            
            # breakpoint()
            
            ix_method = self.xr_masks.coords['method']== str(self.choose_maskmethod.currentText()) 

            m =np.squeeze( self.xr_masks[:,:,ix_method])
            self.mask_manual_old=  self.xr_masks[:,:,ix_method] .copy() 

            # m = np.transpose( self.mask_manual )
            t = mdates.date2num(self.xr_masks.coords['time'] )
            d = -self.xr_masks.coords['depth']
            

            kk_t,kk_d=np.meshgrid( t,d)   
            # kernel=np.zeros( [ k_f.shape[0] ,k_t.shape[0] ] )
            x, y = kk_t.flatten(), kk_d.flatten()
            points = np.vstack((x,y)).T 
            
            p = MPL_Path(list(zip( self.draw_x.values , self.draw_y.values))) # make a polygon
            grid = p.contains_points(points)
            m_shapemask = grid.reshape(kk_t.shape) # now you have a mask with points inside a polygon  
            
            # ix1,ix2=np.where(m_shapemask)
            
            mm = np.squeeze(self.xr_masks[:,:,ix_method].values)
            mm[m_shapemask]=False
            self.xr_masks[:,:,ix_method]=np.expand_dims(mm,axis=-1)
            
            # self.mask_manual.values[ m_shapemask ] = False
                  
        self.plot_echogram()
        self.butt_removearea.setEnabled(True)   

         
    def func_draw_shape_exit_add(self):
        # print('save shape' + str(self.draw_x.shape))
        self.canvas.fig.canvas.mpl_disconnect(self.cid2)
        ## deactive shortcut
        self.drawexitm.setEnabled(False)  

        if self.draw_x.shape[0]>2:

            # 
            # breakpoint()
            
            ix_method = self.xr_masks.coords['method']== str(self.choose_maskmethod.currentText()) 

            m =np.squeeze( self.xr_masks[:,:,ix_method])
            self.mask_manual_old=  self.xr_masks[:,:,ix_method] .copy() 

            # m = np.transpose( self.mask_manual )
            t = mdates.date2num(self.xr_masks.coords['time'] )
            d = -self.xr_masks.coords['depth']
            

            kk_t,kk_d=np.meshgrid( t,d)   
            # kernel=np.zeros( [ k_f.shape[0] ,k_t.shape[0] ] )
            x, y = kk_t.flatten(), kk_d.flatten()
            points = np.vstack((x,y)).T 
            
            p = MPL_Path(list(zip( self.draw_x.values , self.draw_y.values))) # make a polygon
            grid = p.contains_points(points)
            m_shapemask = grid.reshape(kk_t.shape) # now you have a mask with points inside a polygon  
            # self.mask_manual.values[ m_shapemask ] = True

            # ix1,ix2=np.where(m_shapemask)
            # self.xr_masks[ix1,ix2,ix_method]= True
            mm = np.squeeze(self.xr_masks[:,:,ix_method].values)
            mm[m_shapemask]=True
            self.xr_masks[:,:,ix_method]=np.expand_dims(mm,axis=-1)
            
        self.plot_echogram()   
        self.butt_addarea.setEnabled(True)     
         


    def mask_addarea(self):
        # msg = QtWidgets.QMessageBox()
        # msg.setIcon(QtWidgets.QMessageBox.Information)   
        # msg.setText("Add points with double left click.\nRemove latest point with single right click. \nExit draw mode by pushing enter")
        # msg.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
        # returnValue = msg.exec()    
        # if returnValue == QtWidgets.QMessageBox.Ok:
            self.butt_addarea.setEnabled(False)     

            print('drawing')  
            # breakpoint()
            
            self.draw_x=pd.Series(dtype='float')
            self.draw_y=pd.Series(dtype='float')
            self.d_limits=self.ax1.get_ylim()
            self.t_limits=self.ax1.get_xlim()
            self.plot_echogram()
            
            # self.canvas.fig.canvas.mpl_disconnect(self.cid_hover)     
            self.cid2=self.canvas.fig.canvas.mpl_connect('button_press_event', self.onclick_draw)
            self.line_2 =self.ax1.plot(self.draw_x,self.draw_y,'.-g')        
            # self.plot_echogram()   
            self.drawexitm = QtWidgets.QShortcut(QtCore.Qt.Key_Return, self)
            self.drawexitm.activated.connect(self.func_draw_shape_exit_add)  
        
        
        
    def save_changes(self):
       
        # xr.backends.file_manager.FILE_CACHE.clear()
        
        # m = np.transpose( self.mask_manual )
        fname= self.filenames[self.filecounter]
        # m.to_hdf( fname[:-12] + '_mask_manual.h5',key='df' )
        
        # if os.path.exists(fname[:-12] + '_krill_masks.nc'):
        #   os.remove(fname[:-12] + '_krill_masks.nc')        
        # 
        self.xr_masks_write = self.xr_masks.copy()
        self.xr_masks.close()
        
        self.xr_masks_write.to_netcdf( fname[:-12] + '_krill_masks.nc',mode='w'  )
        




        # calc nasc
        ix_f = self.xr_sv.coords['frequency']== int(self.choose_freq.currentText()) *1000
        sv = np.squeeze( self.xr_sv[ix_f,:,:])
        
        
            
                
        # sv = sv.interpolate_na( dim='time', method="linear")
        
        # sv = sv.interpolate_na(  'depth',max_gap=3,method="linear")
        # sv = sv.interpolate_na(  'time' ,max_gap=pd.Timedelta(seconds=5))
        
        # sv = sv.interp(time=sv.time , depth=sv.depth, method="linear")
        # ix_method = self.xr_masks.coords['method']== 'Manual'
        # manual=np.squeeze( self.xr_masks[:,:,ix_method])
        
        ix_method = self.xr_masks.coords['method'].values.tolist().index(self.choose_maskmethod.currentText()) 
        
        mask_plot =np.squeeze( self.xr_masks[:,:,ix_method])
        
        # self.mask_plot[manual==True]=True
        # self.mask_plot[manual==False]=False
        
        ixdepthvalid= ( self.xr_sv.coords['depth'] >= self.excl_depth_spin.value() ) & ( self.xr_sv.coords['depth']  <= self.max_depth_spin.value())
        mask_plot[~ixdepthvalid,:]=False  
        
        sv_mask=sv.values.copy()
        sv_mask[mask_plot.values==0]=np.nan
        
        
        cell_thickness=np.abs(np.mean(np.diff( self.xr_sv.coords['depth']) ))        
        
        # breakpoint()
        
        track = pd.read_csv( fname[:-12] + '_nasctable.csv',index_col=0 )
        labels = ['nasc_swarm','nasc_dbdiff','nasc_manual']

        # labels = ['nasc_swarm','nasc_dbdiff','nasc_unet_and_shapes','nasc_unet','nasc_manual']
        label = labels[ix_method]
        
        # track= pd.DataFrame([])
        # track.index= self.xr_sv.coords['time']      
        track[label] =4*np.pi*1852**2 * np.nansum( np.power(10, sv_mask /10)*cell_thickness ,axis=0)   
          
        # peak filter
        x = track[label].values.copy()
        peaks, peak_meta = find_peaks(x,prominence=10000,width=[0,2] )
        # x[peaks]=np.nan
        
        ix1 = np.round( peak_meta['left_ips']).astype(int)-1
        ix2 = np.round( peak_meta['right_ips']).astype(int)+1
        
        ix1[ix1<0]=0
        ix2[ix2>len(x)-1]=len(x)-1
        
        for i1,i2 in zip(ix1,ix2):
            x[i1:i2]=np.nan
        
        track[label]=x
        track[label]=track['nasc_swarm'].interpolate()
        

        # track['nasc_manual'] =nasc
        track.to_hdf( fname[:-12] + '_nasctable.h5',key='df'  )
        track.to_csv( fname[:-12] + '_nasctable.csv' )
        
        
        
    def plot_next(self):
         if len(self.filenames)>0:
            print('old filecounter is: '+str(self.filecounter))
            
            if self.checkbox_mask.isChecked():
                self.save_changes()
                
           
            self.filecounter=self.filecounter+1
            if self.filecounter>len(self.filenames)-1:
                self.filecounter=len(self.filenames)-1
                print('That was it')
            self.read_file_and_mask()
            self.plot_echogram()
            
            

    def plot_prev(self):
         if len(self.filenames)>0:   
            print('old filecounter is: '+str(self.filecounter))
            
            if self.checkbox_mask.isChecked():
                self.save_changes()

         
            self.filecounter=self.filecounter-1
            if self.filecounter<0:
                self.filecounter=0
                print('That was it')
            # new file    
            # self.filecounter=self.filecounter+1
            self.read_file_and_mask()
            self.plot_echogram()
                
         
     
######
             

    def func_quit(self):
        self.statusBar().setStyleSheet("background-color : k")
        # self.statusBar().removeWidget(self.label_1)   
        # self.startautoMenu.setEnabled(True)
        # self.exitautoMenu.setEnabled(False)     
        QtWidgets.QApplication.instance().quit()     
        # QCoreApplication.quit()
        self.close()    
        

class gui():
    def __init__(self, *args, **kwargs):
        app = QtWidgets.QApplication(sys.argv)
        app.setApplicationName("Krillscan")    
        app.setStyleSheet(qdarktheme.load_stylesheet())
        w = MainWindow()
        sys.exit(app.exec_())

# inspect=ks()

# app = QtWidgets.QApplication(sys.argv)
# app.setApplicationName("Krillscan")    
# app.setStyleSheet(qdarktheme.load_stylesheet())
# w = MainWindow()
# sys.exit(app.exec_())
     
    
        
