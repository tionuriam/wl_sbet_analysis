import os
import datetime
from datetime import timezone, time
from numpy import pi, cos, sin, log, exp
import numpy as np
import matplotlib.pyplot as plt
import csv

class WaterLevel:
    """A Class for handling Water Level Data"""
    
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
                    
        #open csv file
        with open(fullpath, 'r') as file:
            reader = csv.reader(file)
            #print(reader)
            for row in reader:
                self.wl_data.append(row)
                
      #Extract values from wl_data list and populate list            
        for data in self.wl_data[1:]:
            #data.split()
            date_time_str = data[0]
            date_time_obj = datetime.datetime.strptime(date_time_str, '%Y-%m-%d %H:%M')
            #print(date_time_obj.timestamp())
            epoch = date_time_obj.timestamp()
            readable = datetime.datetime.fromtimestamp(epoch).isoformat()
            print(readable)
            self.times.append(readable)
           #print(data[0])
            self.waterlevel.append(float(data[1]))
            self.sigma.append(float(data[2]))

        print(self.times)

    def draw(self):

        print("Drawing Water Level Data")

        plt.figure(figsize=(10, 100))

        plt.plot(self.times, self.waterlevel)
        plt.title("Water Level Data")
        plt.ylabel("Water Level in [m] above Chart Datum")
        plt.xticks()
        plt.xlabel("Time[UTC]")

        plt.figure(figsize=(10, 100))

        plt.gcf().autofmt_xdate()
        plt.show()