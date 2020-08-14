import os
import sys
sys.path.append(os.getcwd())

from my_code.waterlevel_xmlread import WaterLevel
#from my_code.waterlevel_xmlread import WaterLevel
abs_path=os.path.abspath(os.path.curdir)+"/Data/"

water_levels = WaterLevel()

water_levels.read_jhc_file(abs_path+"wl20180614.xml")
water_levels.draw()



