import os
import datetime
from datetime import timezone, time
from numpy import pi, cos, sin, log, exp
import numpy as np
import matplotlib.pyplot as plt
import csv
from xml.etree import ElementTree as ET
import pandas as pd
from scipy.signal import find_peaks
import plotly.graph_objects as go
import requests


class WaterLevel:
    """A Class for handling Water Level Data (xml version)"""
    
    ## Last Changes

    def __init__(self):
        
        self.times = list()
        self.water_levels = list()
        self.data_path = str()
        self.metadata = dict()
        self.metadata["units"] = "m"
        self.metadata["datum_type"] ="None"
        self.metadata["datum_name"] ="None"
        self.metadata["time_base"] ="UTC"
        self.metadata["location_name"] = "Unknown"
        
        self.wl_data = list()
        self.date_time = list()
        self.waterlevel = list()
        self.sigma = list()
        self.date = list()
        #self.time = list()

        #download paramters
        self.begin_data = str() # yyMMDD HH:MM
        self.end_date = str()
        self.station = str()
        self.product = str()
        self.datum = str()
        self.units = str()
        self.time_zone = str()
        self.application = str()
        self.services = str()
        self.format = str()
      
    def read_jhc_file(self, fullpath):
            # Check the File's existence
        if os.path.exists(fullpath):
            self.metadata["Source File"] = fullpath
            print('Opening water level data file:' + fullpath)
        else:  # Raise a meaningful error
            raise RuntimeError('Unable to locate the input file' + fullpath)
            
        #identify file extension
        
        file_name, file_extension = os.path.splitext(fullpath)
        #print("File name: %s" %file_name)
        print("File extension:", file_extension)
                    
        #open, read and close file
        with open(fullpath, 'r') as file:
            tree = ET.parse(file)
            root = tree.getroot()
            # print(reader)

            # identify elements in root of xml

        #for elements in root:
            #print(elements.tag, elements.attrib)

        #for elements in root[0]:
            #print(elements.text)

        # accessing values in child directory (observations)
        for values in root.iter('wl'):
            self.date_time.append(values.attrib['t'])
            #print(type(values.attrib['t']))
            self.waterlevel.append(float(values.attrib['v']))
            self.sigma.append(float(values.attrib['s']))

        #time_only = []
        for time in self.date_time:
            #print(time[11:])
            date_time_obj = datetime.datetime.strptime(time[11:],'%H:%M')
            self.times.append(time[11:])
            #time_only.append(date_time_obj.time())

        # for times in self.date_time:
        #     x = time.split()
        print(self.times)

        print(self.date_time)
        print(self.waterlevel)
        print(self.sigma)
        #print(s)

    def download_wl_file(self):
        """reads user input and downloads the relevant water level file"""
        #user data inputs
        self.begin_date = "20130101 10:00"
        self.end_date = "20130101 10:24"
        self.station = "8454000"
        self.product = "water_level"
        self.datum = "mllw"
        self.units = "metric"
        self.time_zone = "gmt"
        self.application = "web_services"
        self.format = 'xml'

        url_parameters = str("begin_date=" + self.begin_date + "&end_date=" + self.end_date + "&station=" + self.station + "&product=" + self.product + "&datum=" + self.datum + "&units=" + self.units + "&time_zone=" + self.time_zone + "&application=" + self.application + "&format=" + self.format)
        url_api = "https://api.tidesandcurrents.noaa.gov/api/prod/datagetter?"
        url_download = url_api + url_parameters
        result = requests.get(url_download)
        print("file download from:" + url_download)
        print("Following parameters were used: ")
        print("begin_date:", self.begin_date)  # yyMMDD HH:MM
        print("end_date:", self.end_date)
        print("station:", self.station)
        print("product:", self.product)
        print("datum:", self.datum)
        print("units:", self.units)
        print("timezone:", self.time_zone)
        print("application:", self.application)
        print("format:", format)
        print(result.text)
        return print("done")



    def draw(self):

        #find peaks of water levels

        time_series = list(zip(range(len(self.waterlevel)), self.waterlevel))
        print("time series:", time_series)



        # df = pd.to_datetime(self.date_time)
        # date_time_str = '2018-06-16 00:06'
        # date_time_obj = datetime.datetime.strptime(date_time_str,'%Y-%m-%d %H:%M')
        # print(date_time_obj)
        # print('Time:', date_time_obj.time())
        #
        # plt.figure(figsize=(10, 100))
        #
        # plt.plot(self.times, self.waterlevel)
        # plt.title("Water Level Data")
        # # Y axis
        # plt.ylabel("Water Level in [m] above Chart Datum")
        # #plt.yticks(np.arange())
        #
        # # #X axis
        # # minimum = max(self.waterlevel)
        # # print(minimum)
        # frequency=100
        # plt.xticks(self.times[::frequency])
        # #
        # plt.xlabel("Time[UTC]")
        # #
        # plt.figure(figsize=(10, 100))
        # #
        # plt.gcf().autofmt_xdate()
        # plt.show()