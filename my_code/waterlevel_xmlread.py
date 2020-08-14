import os
import datetime
from datetime import timezone, time
from numpy import pi, cos, sin, log, exp
import numpy as np
import matplotlib.pyplot as plt
import csv
from xml.etree import ElementTree as ET


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
            self.waterlevel.append(float(values.attrib['v']))
            self.sigma.append(float(values.attrib['s']))

        print(self.date_time)
        print(self.waterlevel)
        print(self.sigma)
        #print(s)

    def draw(self):

        print("Drawing Water Level Data")

        plt.figure(figsize=(10, 100))

        plt.plot(self.date_time,self.waterlevel)
        plt.title("Water Level Data")
        plt.ylabel("Water Level in [m] above Chart Datum")
        plt.xticks()
        plt.xlabel("Time[UTC]")

        plt.figure(figsize=(10, 100))

        plt.gcf().autofmt_xdate()
        plt.show()