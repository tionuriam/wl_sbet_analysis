import os
import sys
import matplotlib.pyplot as plt
from my_code.waterlevel import WaterLevel
from my_code.sbetreadfile import sbet

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


    def read_wl_sbet(self,abs_path,filename):
    # create sbet_file object read sbet files
        sbet_txt = sbet()
        sbet_txt.read_sbet_file(abs_path + filename)
        sbet_txt.extract_wl_data(abs_path)
        #print(sbet_txt.filename)
        #sbet_txt.draw()

    #sbet values
        self.ellipsoid_height_list = sbet_txt.ellipsoid_height_list
        self.times = sbet_txt.times
        self.pitch_list = sbet_txt.pitch_list
        self.roll_list = sbet_txt.roll_list
        self.heading_list = sbet_txt.heading_list

    # create water level object, read wl files
        water_levels = WaterLevel()
        water_levels.read_csv_file(abs_path + sbet_txt.filename + "." + sbet_txt.format) # extracting the file that has been saved based from reading the sbet file

    #water_levels values
        self.wl_times = water_levels.times
        self.wl_waterlevels= water_levels.waterlevel

        print("times:",self.times[-1])
        print("wl_times:", self.wl_times[-1])

    def draw(self):

        print("Drawing Motion Data")
        # # print(self.times)
        # # print(self.wl_times)
        # #
        # #
        # plt.plot(self.wl_times, self.wl_waterlevels)
        # plt.title("Water Level Data")
        # plt.ylabel("Water Level in [m] above Chart Datum")
        # plt.xticks()
        # plt.xlabel("Time[UTC]")
        # #plt.figure(figsize=(10, 10))


        plt.figure(figsize=(10, 20))
        plt.title("Plot of Motion data")
        ax1 = plt.subplot(5, 1, 1)
        plt.plot(self.times,self.ellipsoid_height_list)
        plt.ylabel("Ellipsoidal height [m]")
        #
        ax2 = plt.subplot(5, 1, 2, sharex=ax1)
        plt.plot(self.times,self.pitch_list)
        plt.ylabel("pitch[m]")
        #
        ax3 = plt.subplot(5, 1, 3, sharex=ax1)
        plt.plot(self.times,self.roll_list)
        plt.ylabel("Roll[deg]")
        #
        ax4 = plt.subplot(5, 1, 4, sharex=ax1)
        plt.plot(self.times,self.heading_list)
        plt.ylabel("Heading[deg]")
        plt.xlabel("Time[UTC]")
        #
        ax5 = plt.subplot(5, 1, 5, sharex=ax1)
        plt.plot(self.wl_times,self.wl_waterlevels)
        plt.ylabel("Water Levels [m]")
        plt.xlabel("Time[UTC]")


        plt.setp(ax1.get_xticklabels(), visible=False)
        plt.setp(ax2.get_xticklabels(), visible=False)
        plt.setp(ax3.get_xticklabels(), visible=False)
        plt.setp(ax4.get_xticklabels(), visible=False)

        plt.gcf().autofmt_xdate()
        plt.show()





