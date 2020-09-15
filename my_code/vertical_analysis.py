import os
import sys
import matplotlib.pyplot as plt
from my_code.waterlevel import WaterLevel
from my_code.sbetreadfile import Sbet
import statistics
import numpy as np
from my_code.specter import specter



class vanalysis_sbet_wl:
    """Class to analzse sbet and water level data"""

    def __init__(self):
        self.abs_path = str()
        self.filename = str()
        self.ellipsoid_height_list = list()
        self.times = list()
        self.pitch_list = list()
        self.roll_list = list()
        self.heading_list = list()

        self.wl_times = list()
        self.wl_waterlevels = list()

        #spectral frequency analysis
        self.spec_wl = None
        self.spec_sbet = None

        #Variables for waterlevels
        self.m_wl = float()
        self.dt_wl = float()
        self.ave_wl = float()
        #Variables for set
        self.m_sbet = float()
        self.dt_sbet = float()
        self.ave_sbet = float()



    def read_wl_sbet(self,abs_path,filename):
    # create sbet_file object read sbet files
        sbet = Sbet()
        sbet.read_sbet_file(abs_path + filename)
        sbet.extract_wl_data(abs_path) # the extracted file is in xml format by default
        #print(sbet_txt.filename)
        #sbet_txt.draw()

    #retrieve sbet values
        self.ellipsoid_height_list = sbet.ellipsoid_height_list # list of ellipsoid values
        self.times = sbet.times # list of times in the sbet file
        self.pitch_list = sbet.pitch_list
        self.roll_list = sbet.roll_list
        self.heading_list = sbet.heading_list
    #
    # # create water level object, read wl file
        water_levels = WaterLevel()
        water_levels.read_xml_file(abs_path + sbet.filename + "." + sbet.format) # extracting the file that has been saved based from reading the sbet file
    #
    # #water_levels values - extracted from the xml file
        self.wl_times = water_levels.times
        self.wl_waterlevels = water_levels.waterlevel

        # print("las for sbet file:",self.times[-1])
        # print("wl_times:", self.wl_times[-1])

    def draw(self):

       #draw ellipsoid height and water level only

        print("Drawing Motion and water level data")
        plt.figure(figsize=(10, 20))
        plt.title("Plot of Motion data")
        ax1 = plt.subplot(2, 1, 1)
        plt.plot(self.times,self.ellipsoid_height_list)
        plt.ylabel("Ellipsoidal height [m]")

        # mean_wl = [statistics.mean(self.wl_waterlevels)] * len(self.wl_times)
        # heave_times = [statistics.mean(self.wl_waterlevels)] * len(self.times)
        # xs = np.array(self.wl_times)
        # ys = np.array(self.wl_waterlevels)

        ax2 = plt.subplot(2, 1, 2, sharex=ax1)
        plt.plot(self.wl_times, self.wl_waterlevels)
        # plt.plot(self.wl_times, mean_wl,'g--')
        #plt.plot(heave_times,self.ellipsoid_height_list)
        plt.ylabel("Water Levels [m]")
        plt.xlabel("Time[UTC]")


        plt.setp(ax1.get_xticklabels(), visible=True)
        plt.setp(ax2.get_xticklabels(), visible=True)


        # draw all
        # print("Drawing Motion and water level data")
        # plt.figure(figsize=(10, 20))
        # plt.title("Plot of Motion data")
        # ax1 = plt.subplot(5, 1, 1)
        # plt.plot(self.times,self.ellipsoid_height_list)
        # plt.ylabel("Ellipsoidal height [m]")
        # #
        # ax2 = plt.subplot(5, 1, 2, sharex=ax1)
        # plt.plot(self.times,self.pitch_list)
        # plt.ylabel("pitch[m]")
        # #
        # ax3 = plt.subplot(5, 1, 3, sharex=ax1)
        # plt.plot(self.times,self.roll_list)
        # plt.ylabel("Roll[deg]")
        # #
        # ax4 = plt.subplot(5, 1, 4, sharex=ax1)
        # plt.plot(self.times,self.heading_list)
        # plt.ylabel("Heading[deg]")
        # plt.xlabel("Time[UTC]")
        # #
        # ax5 = plt.subplot(5, 1, 5, sharex=ax1)
        # plt.plot(self.wl_times,self.wl_waterlevels)
        # plt.ylabel("Water Levels [m]")
        # plt.xlabel("Time[UTC]")

        #
        # plt.setp(ax1.get_xticklabels(), visible=False)
        # plt.setp(ax2.get_xticklabels(), visible=False)
        # plt.setp(ax3.get_xticklabels(), visible=False)
        # plt.setp(ax4.get_xticklabels(), visible=False)

        plt.gcf().autofmt_xdate()
        plt.show()

    def f_spectrum_wl(self,m,dt,ave):
        self.m_wl = m
        self.dt_wl = dt
        self.ave_wl = ave

        #draw spectral densities for water level
        wl_fp = np.array(self.wl_waterlevels)  # data points in an array
        self.spec_wl = specter(wl_fp, m, dt, ave)
        #print(len(self.wl_waterlevels))


    def f_spectrum_sbet(self,m,dt,ave):
        self.m_sbet = m
        self.dt_sbet = dt
        self.ave_sbet = ave
        # draw spectral densities for sbet
        sbet_fp = np.array(self.ellipsoid_height_list)
        self.spec_sbet = specter(sbet_fp, m, dt, ave)

    def spec_analysis(self):
        wl_fp = np.array(self.wl_waterlevels)  # data points in an array
        sbet_fp = np.array(self.ellipsoid_height_list)

        # draw spectral densities for sbet and wl
        spec_sbet = specter(sbet_fp, self.m_sbet, self.dt_sbet, self.ave_sbet)
        spec_wl = specter(wl_fp, self.m_wl, self.dt_wl, self.ave_wl)

        plt.figure(figsize=(10, 10))
        plt.loglog(spec_sbet,spec_sbet,'r',label=u'SBET')
        plt.loglog(spec_wl,spec_wl,'b',label=u'Water Level')
        plt.title('Spectral Densities: SBET vs Water Level')
        plt.xlabel('Frequency')
        plt.ylabel('Spectral Density')
        plt.legend(ncol=2, loc='upper center')
        plt.show()


    # def spec_residual(self):

















