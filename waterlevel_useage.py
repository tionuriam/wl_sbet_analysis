import os
import datetime
from datetime import datetime
import numpy as np
import sys

sys.path.append(os.getcwd())

from my_code.waterlevel import WaterLevel

abs_path=os.path.abspath(os.path.curdir)+"/Data/"

water_levels = WaterLevel()

water_levels.read_jhc_file(abs_path+"CO-OPS__8423898__wl.csv")
water_levels.draw()

