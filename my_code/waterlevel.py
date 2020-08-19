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
    """A Class for handling Water Level Data"""

    ## Last Changes

    def __init__(self):


        self.wl_data = list()
        self.date_time = list()
        self.times = list()
        self.waterlevel = list()
        self.sigma = list()

        # self.water_levels = list()
        self.data_path = str()
        self.metadata = dict()
        # self.metadata["units"] = "m"
        # self.metadata["datum_type"] ="None"
        # self.metadata["datum_name"] ="None"
        # self.metadata["time_base"] ="UTC"
        # self.metadata["location_name"] = "Unknown"

        # download paramters
        # user inputs; enter the required parameters
        self.begin_date = "20130101 10:00"  # format YYMMDD HHMM
        self.end_date = "20130101 10:24"  # format YYMMDD HHMM
        self.station = "8454000"  # enter station ID
        self.product = "water_level"  # enter water_level
        self.datum = "mllw"  # enter datum type
        self.units = "metric"  # enter required units
        self.time_zone = "gmt"  # enter timezone
        self.application = "web_services"  # enter web application
        self.format = 'csv'  # enter format of data output e.g. xml, csv or json

    def read_csv_file(self, fullpath):
        # Check the File's existence
        if os.path.exists(fullpath):
            self.metadata["Source File"] = fullpath
            print('Opening water level data file:' + fullpath)
        else:  # Raise a meaningful error
            raise RuntimeError('Unable to locate the input file' + fullpath)

        # identify file extension

        file_name, file_extension = os.path.splitext(fullpath)
        # print("File name: %s" %file_name)
        print("File extension:", file_extension)

        # open csv file
        with open(fullpath, 'r') as file:
            reader = csv.reader(file)
            # print(reader)
            for row in reader:
                self.wl_data.append(row)

        # Extract values from wl_data list and populate list
        for data in self.wl_data[1:]:
            # data.split()
            date_time_str = data[0]
            date_time_obj = datetime.datetime.strptime(date_time_str, '%Y-%m-%d %H:%M')
            # print(date_time_obj.timestamp())
            epoch = date_time_obj.timestamp()
            readable = datetime.datetime.fromtimestamp(epoch).isoformat()
            print(readable)
            self.times.append(readable)
            # print(data[0])
            self.waterlevel.append(float(data[1]))
            self.sigma.append(float(data[2]))

        print(self.times)

    def read_xml_file(self, fullpath):
        # Check the File's existence
        if os.path.exists(fullpath):
            self.metadata["Source File"] = fullpath
            print('Opening water level data file:' + fullpath)
        else:  # Raise a meaningful error
            raise RuntimeError('Unable to locate the input file' + fullpath)

        # identify file extension

        file_name, file_extension = os.path.splitext(fullpath)
        # print("File name: %s" %file_name)
        print("File extension:", file_extension)

        # open, read and close file
        with open(fullpath, 'r') as file:
            tree = ET.parse(file)
            root = tree.getroot()

        # accessing values in child directory (observations)
        for values in root.iter('wl'):
            self.date_time.append(values.attrib['t'])
            # print(type(values.attrib['t']))
            self.waterlevel.append(float(values.attrib['v']))
            self.sigma.append(float(values.attrib['s']))

        # time_only = []
        for time in self.date_time:
            # print(time[11:])
            date_time_obj = datetime.datetime.strptime(time[11:], '%H:%M')
            self.times.append(time[11:])
            # time_only.append(date_time_obj.time())

        # print(self.times)
        #
        # print(self.date_time)
        # print(self.waterlevel)
        # print(self.sigma)

    def download_wl_file(self):
        """reads user input and downloads the relevant water level file that will be downloaded from internet"""
        # combine parameters and send a request to download data from website
        url_parameters = str(
            "begin_date=" + self.begin_date + "&end_date=" + self.end_date + "&station=" + self.station + "&product=" + self.product + "&datum=" + self.datum + "&units=" + self.units + "&time_zone=" + self.time_zone + "&application=" + self.application + "&format=" + self.format)
        url_api = "https://api.tidesandcurrents.noaa.gov/api/prod/datagetter?"
        url_download = url_api + url_parameters
        result = requests.get(url_download)

        # Parameters will be printed out
        print("file downloaded from:" + url_download)
        print("Following parameters were used: ")
        print("begin_date:", self.begin_date)  # yyMMDD HH:MM
        print("end_date:", self.end_date)
        print("station:", self.station)
        print("product:", self.product)
        print("datum:", self.datum)
        print("units:", self.units)
        print("timezone:", self.time_zone)
        print("application:", self.application)
        print("format:", self.format)
        print("************************************************")

        # print output
        print(result.text)

        # export output as xml file intow file directory
        # enter file output file name,format and destination folder
        filename = "20130101_wl_data"
        fileformat = str('.' + self.format)  # takes the format of what you entered earlier
        abs_path = os.path.abspath(os.path.curdir) + "/Data/"
        with open(abs_path + filename + fileformat, 'wb') as file:
            file.write(result.content)

        return print("file saved in:" + abs_path + filename + fileformat)

    def draw(self):

        # find peaks of water levels

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