import os
from datetime import datetime, timezone
import calendar
from numpy import pi, cos, sin, log, exp
import numpy as np
import matplotlib.pyplot as plt
from datetime import timedelta
import requests
from math import floor
from my_code.waterlevel_xmlread import WaterLevel
from xml.etree import ElementTree as ET

import matplotlib.dates as mdates
import utide
from utide import solve, reconstruct
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

from my_code.specter import specter
import scipy

from scipy import signal
import pandas as pd


class Sbet:
    """ Class to read sbet txt files"""
    
    def __init__(self):
        self.time_list = list()
        self.times = list()
        self.easting_list = list()
        self.northing_list = list()
        self.distance_list = list()
        self.ellipsoid_height_list = list()
        self.lat_list= list()
        self.lon_list = list()
        self.roll_list= list()
        self.pitch_list = list()
        self.heading_list = list()
        self.east_velocity_list =list()
        self.north_velocity_list = list()
        self.up_velocity_list = list()
        self.east_sd_list = list()
        self.north_sd_list = list()
        self.height_sd_list= list()
        self.roll_sd_list = list()
        self.pitch_sd_list = list()
        self.heading_sd_list = list()

        #url paramters
        # self.start_date_time_str = str()
        # self.end_date_time_str = str()
        self.format_start_time = str()
        self.format_start_date = str()
        self.format_end_time = str()
        self.format_end_date = str()

        # user inputs; enter the required parameters
        self.filename = "wlsbet_0830"
        self.begin_date = str()  # format YYMMDD HHMM
        self.end_date = str()  # format YYMMDD HHM
        self.station = "8423898"  # enter station ID
        self.product = "water_level"  # enter water_level
        self.datum = "mllw"  # enter datum type
        self.units = "metric"  # enter required units
        self.time_zone = "gmt"  # enter timezone
        self.application = "web_services"  # enter web application
        self.format = 'xml'  # enter format of data output e.g. xml, csv or json

        #resamling component
        self.interp_data = ([])


        #self.sbet_list = list()
        self.fullpath = str()
        self.metadata = dict()
        self.metadata["units"] = "m"
        self.metadata["datum_type"] ="None"
        self.metadata["datum_name"] ="None"
        self.metadata["time_base"] ="UTC"
        self.metadata["location_name"] = "Unknown"
        
    def read_sbet_file(self,fullpath):
        if os.path.exists(fullpath):
            self.metadata["Source File"] = fullpath
            print('Opening sbet data file:' + fullpath)
        else:  # Raise a meaningful error
            raise RuntimeError('Unable to locate the input file' + fullpath)
            
        #      # OK Read file

        # with open(fullpath) as f:
        #     for line in f:
        #         sbet_lines = line.split()
        #         self.time_list.append(sbet_lines)

        sbet_txt_file = open(fullpath)
        sbet_data = sbet_txt_file.read()
        sbet_txt_file.close()

        #Tokenize
        sbet_lines = sbet_data.splitlines()

        # Read each line
        sbet_list = []
        for line in sbet_lines:
            sbet_list.append(line.splitlines())
        #
        #
        #Grab the data/headings
        sbet_headers = []
        for headers in sbet_list[24]:
            headers = headers.split()
            sbet_headers.append(headers)


        #iterating through the data only and appending output into appropriate list
        for lines in sbet_list[28:]:
            for value in lines:
                sbetvalues = value.split()
                time = sbetvalues[0]
                distance = sbetvalues[1]
                easting = sbetvalues[2]
                northing = sbetvalues[3]
                ellipsoid_height = sbetvalues[4]
                latitude = sbetvalues[5]
                longitude = sbetvalues[6]
                roll = sbetvalues[8]
                pitch = sbetvalues[9]
                heading = sbetvalues[10]
                east_velocity = sbetvalues[11]
                north_velocity = sbetvalues[12]
                up_velocity = sbetvalues[13]
                east_sd = sbetvalues[14]
                north_sd = sbetvalues[15]
                height_sd = sbetvalues[16]
                roll_sd = sbetvalues[17]
                pitch_sd = sbetvalues[-2]
                heading_sd = sbetvalues[-1]

                self.time_list.append(float(time))
                #np.append(self.time_list.append(time))
                self.distance_list.append(float(distance))
                self.easting_list.append(easting)
                self.northing_list.append(northing)
                self.ellipsoid_height_list.append(float(ellipsoid_height))
                self.lat_list.append(latitude)
                self.lon_list.append(longitude)
                self.roll_list.append(float(roll))
                self.pitch_list.append(float(pitch))
                self.heading_list.append(float(heading))
                self.east_velocity_list.append(east_velocity)
                self.north_velocity_list.append(north_velocity)
                self.up_velocity_list.append(up_velocity)
                self.east_sd_list.append(east_sd)
                self.north_sd_list.append(north_sd)
                self.height_sd_list.append(height_sd)
                self.roll_sd_list.append(roll_sd)
                self.pitch_sd_list.append(pitch_sd)
                self.heading_sd_list.append(heading_sd)


        # find mission start date and time and store as datetime variable. Information is taken from the sbet file
        start_date = str()
        start_time = str()

        for dates in sbet_list[15]:
            splitlines = dates.split()
            start_date = splitlines[3]
        for times in sbet_list[16]:
            splitlines = times.split()
            start_time = splitlines[2]

        self.start_date_time_str = start_date + " " + start_time
        #print(self.start_date_time_str)
        mission_start_date_time = datetime.strptime(self.start_date_time_str, '%Y-%m-%d %H:%M:%S')

        mission_start_day = mission_start_date_time.weekday()
        #print("Day of survey:", calendar.day_name[current_day])
        print("Mission Start:", mission_start_date_time,calendar.day_name[mission_start_day])
        # breaking down hours to current day(time) of day to hr, min, sec
        time = mission_start_date_time.time() #extract time only from date and time
        hr = time.hour
        min = time.minute
        sec = time.second

        # Find date of start of week day (Monday midnight of that week) from when the data was collected
        n = mission_start_date_time.weekday()  # int value of day of week
        count = 0
        while n > 0:
            n = n - 1
            count = count + 1
        else:
            day_of_week = (mission_start_date_time - timedelta(days=count)).weekday()
            start_of_week_date = mission_start_date_time - timedelta(days=count, hours=hr, minutes=min, seconds=sec)
            #print("Start of week day date and time:", day_of_week, calendar.day_name[day_of_week])

        #Find end date and time of mission
        mission_end_date_time = start_of_week_date + timedelta(seconds=self.time_list[-1]) - timedelta(days=1) #because in counting number of days, Monday is also included (Monday = 1 day, Tue = 1 day etc.)
        end_day = mission_end_date_time.weekday()
        print("Mission end:", mission_end_date_time, calendar.day_name[end_day])


        #Convert week of day seconds to date and time in survey file
        for secs in self.time_list:

            conversion = start_of_week_date + timedelta(seconds=secs) - timedelta(days=1) #subtracting a day, because in counting number of days, Monday is also included (Monday = 1 day, Tue = 1 day etc.)
            #print(date_time)
            date_time_format = conversion.strftime('%Y-%m-%d %H:%M:%S')
            date_time_format_object = datetime.strptime(date_time_format,'%Y-%m-%d %H:%M:%S')
            self.times.append(date_time_format_object)



        # changing start/end date and time format for api request
        date_mission_start = mission_start_date_time.date()
        time_mission_start = mission_start_date_time.time()
        self.format_start_time = time_mission_start.strftime('%H:%M')
        self.format_start_date = date_mission_start.strftime('%Y%m%d')

        date_mission_end = mission_end_date_time.date()
        time_mission_end = mission_end_date_time.time()
        self.format_end_time = time_mission_end.strftime('%H:%M')
        self.format_end_date = date_mission_end.strftime('%Y%m%d')

       # print("time:", self.times[0:10])
                
    def time_distance(self):
        """handling time and distance variables"""

        #total time vessel travelled
        time_array = np.array([self.time_list])
        time_cumsum = np.sum(np.diff(time_array))

        #print(np.shape(time_cumsum))
        print("Total time travelled(sec): ", time_cumsum)# adding the difference between each time interval in the dataset

        # total distance vessel travelled
        distance_travelled = (self.distance_list[-1])
        print("Total distance travelled(m): ", distance_travelled)


    # def waterlevel(self):
    #     """downloads relevant water level data based on station ID start and stop date in sbet file"""
    #     from my_code.waterlevel import WaterLevel
    #     water_levels = WaterLevel()


    def extract_wl_data(self,fullpath):
        """download from internet relevant tide files based on mission start and end dates"""
        #Take mission start and mission end dates
        self.begin_date = self.format_start_date + " " + self.format_start_time
        self.end_date = self.format_end_date + " " + self.format_end_time

        #combine parameters and send a request to download data from website
        url_parameters = str("begin_date=" + self.begin_date + "&end_date=" + self.end_date + "&station=" + self.station + "&product=" + self.product + "&datum=" + self.datum + "&units=" + self.units + "&time_zone=" + self.time_zone + "&application=" + self.application + "&format=" + self.format)
        url_api = "https://api.tidesandcurrents.noaa.gov/api/prod/datagetter?"
        url_download = url_api + url_parameters
        result = requests.get(url_download)
        # #
        # # # Parameters will be printed out
        print("Water level data extracted from " + url_download)
        print("Water level date/time period is from " + self.format_start_date + " " + self.format_start_time + " to " + self.format_end_date + " " + self.format_end_time)
        # print("Following parameters were used: ")
        # print("begin_date:", self.begin_date)  # yyMMDD HH:MM
        # print("end_date:", self.end_date)
        # print("station:", self.station)
        # print("product:", self.product)
        # print("datum:", self.datum)
        # print("units:", self.units)
        # print("timezone:", self.time_zone)
        # print("application:", self.application)
        # print("format:", self.format)

        # export output as xml or csv file into file directory
        # enter file output file name,format and destination folder
        # print(fullpath)
        filename = self.filename
        fileformat = str('.' + self.format)  # takes the format of what you entered earlier
        # abs_path = fullpath " # folder directory of where the data will be stored
        with open(fullpath + filename + fileformat, 'wb') as file:
            file.write(result.content)

        return print("Water Level data file has been written to a file located in " + fullpath + filename + fileformat)

    def f_spectrum_sbet(self,m,dt,ave ):

        """Function accepts 3 arguments, three parameters required for the specter function
         which are m, dt, and ave (refer to specter class for descriptions of each)"""

        wl_fp = np.array(self.ellipsoid_height_list)  # nr_records x 1 array to hold the water levels from Fort Point
        spec_fp = specter(wl_fp,m,dt,ave)


    def sample_rate(self):
        times_array = np.array(self.time_list)

        sample_rate = np.diff(times_array)
        f_max = np.max(sample_rate) # units in hz
        f_min = np.min(sample_rate) # units in hz

        print("number of samples:", len(self.times))
        print("max sample_rate:", f_max)
        print("min sample_rate:", f_min)

        # cut off frequency is 1 sample every 720 seconds
        f_cut_off = 1 / 720  # hz
        print("Cut off frequency is:", f_cut_off)  # hz

        # preparing the data
        time_interval = np.cumsum(np.diff(np.array(self.time_list)))
        data = np.array(self.ellipsoid_height_list)
        signal = zip(time_interval,data)
        #time_vector = np.arange(0,len(self.ellipsoid_height_list),sample_rate)

        # print(tuple(signal))
        #
        # plt.plot(signal)
        # plt.show()
        #
        # period = time_interval[-1]
        # print(period)

        # # Fourier transform frequency
        # n = len(self.ellipsoid_height_list)
        # signal = np.array(self.ellipsoid_height_list)
        # # n = signal.size
        # print(n)
        # fourier = np.fft.fft(signal) / n  # fft of the signal
        # timestep = 720
        # freq = np.fft.fftfreq(n,d=timestep) # frequencies
        #
        # PSD = fourier * np.conj(fourier) / n # Power spectrum
        #
        # plt.plot(freq,PSD)
        # plt.show()
        # plt.ylabel("Frequency")
        # plt.xlabel("PSD")


    def fft(self,sr):
        #sr refer to sampling rate. The sampling rate is entered by the user.
        #this method is an fft that resamples the data and then does the fft; this can be done independent of the resample method
        # the resample method is used to visualise the difference between the resampled data and the original
        time = np.array(self.time_list)
        magnitude = np.array(self.ellipsoid_height_list)

        #varaibles for resampling
        time_start = time[0] #you may change this value for a subset
        time_end = time[-1] #you may change this value for a subset
        sampling_rate = sr
        time_interval = np.arange(time_start,time_end,sampling_rate)

        #interpolation of dataset based on time interval and sample rate
        interp_data = np.interp(time_interval,time,magnitude)

        # Frequency domain representation
        fourierTransform = np.fft.fft(interp_data) / len(interp_data)  # Normalize amplitude
        fourierTransform = fourierTransform[range(int(len(interp_data) / 2))]  # Exclude sampling frequency
        tpCount = len(interp_data)
        values = np.arange(int(tpCount / 2))
        timePeriod = tpCount / sampling_rate
        frequencies = values / timePeriod

        # Frequency domain representation
        plt.title('Fourier transform depicting the frequency components')
        plt.plot(frequencies, abs(fourierTransform))
        plt.xlabel('frequency[hz]')
        plt.ylabel('amplitude[m]')
        plt.legend()
        plt.show()

    def resample(self,sr):
        #sr refer to sampling rate. The sampling rate is entered by the user.
        #data set
        time = np.array(self.time_list)
        magnitude = np.array(self.ellipsoid_height_list)

        #varaibles for resampling
        time_start = time[0] #you may change this value for a subset
        time_end = time[-1] #you may change this value for a subset
        sampling_rate = sr
        time_interval = np.arange(time_start,time_end,sampling_rate)

        #interpolation of dataset based on time interval and sample rate
        interp_data = np.interp(time_interval,time,magnitude)

        #plot results; original data vs resmpled
        plt.plot(time,magnitude, label="Original")
        plt.plot(time_interval,interp_data,label="Resampled")
        plt.xlabel('time[seconds]')
        plt.ylabel('elevation[m]')
        plt.title('Sbet plotted data')
        plt.legend()
        plt.gcf().autofmt_xdate()
        plt.show()



    def draw(self):

        print("Drawing Motion Data")
        plt.figure(figsize=(10, 20))
        plt.title("Plot of Motion data")
        ax1 = plt.subplot(4, 1, 1)
        plt.plot(self.times,self.ellipsoid_height_list)
        plt.ylabel("Ellipsoidal height [m]")
        #
        ax2 = plt.subplot(4, 1, 2, sharex=ax1)
        plt.plot(self.times,self.pitch_list)
        plt.ylabel("pitch[m]")
        #
        ax3 = plt.subplot(4, 1, 3, sharex=ax1)
        plt.plot(self.times,self.roll_list)
        plt.ylabel("Roll[deg]")
        #
        ax4 = plt.subplot(4, 1, 4, sharex=ax1)
        plt.plot(self.times,self.heading_list)
        plt.ylabel("Heading[deg]")
        plt.xlabel("Time[UTC]")
        #
        plt.setp(ax1.get_xticklabels(), visible=False)
        plt.setp(ax2.get_xticklabels(), visible=False)
        plt.setp(ax3.get_xticklabels(), visible=False)

        plt.gcf().autofmt_xdate()
        plt.show()