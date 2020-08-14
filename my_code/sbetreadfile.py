
import os
from datetime import datetime, timezone
from numpy import pi, cos, sin, log, exp
import numpy as np
import matplotlib.pyplot as plt

class sbet:
    
    
    def __init__(self):
        self.time_list = list()
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
            
             # OK Read file
        sbet_txt_file = open(fullpath)
        sbet_data = sbet_txt_file.read()
        sbet_txt_file.close()


        #Tokenize
        sbet_lines = sbet_data.splitlines()

        # Read each line
        sbet_list = []
        for line in sbet_lines:
            sbet_list.append(line.splitlines())


        #Grab the data/headings
        sbet_headers = []
        for headers in sbet_list[24]:
            headers = headers.split()
            sbet_headers.append(headers)
            
             
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
                
                self.time_list.append(time)
                self.distance_list.append(distance)
                self.easting_list.append(easting)
                self.northing_list.append(northing)
                self.ellipsoid_height_list.append(ellipsoid_height)
                self.lat_list.append(latitude)
                self.lon_list.append(longitude)
                self.roll_list.append(roll)
                self.pitch_list.append(pitch)
                self.heading_list.append(heading)
                self.east_velocity_list.append(east_velocity)
                self.north_velocity_list.append(north_velocity)
                self.up_velocity_list.append(up_velocity)
                self.east_sd_list.append(east_sd)
                self.north_sd_list.append(north_sd)
                self.height_sd_list.append(height_sd)
                self.roll_sd_list.append(roll_sd)
                self.pitch_sd_list.append(pitch_sd)
                self.heading_sd_list.append(heading_sd)
                
                
        print (self.easting_list )
              

    