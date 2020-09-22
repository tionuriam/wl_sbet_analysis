import os
import sys
sys.path.append(os.getcwd())
import matplotlib.pyplot as plt
from my_code.sbetreadfile import Sbet
import numpy as np
from numpy import pi, cos, sin, fft, arctan
from datetime import timedelta, datetime
#from my_code.waterlevel_xmlread import WaterLevel
import pandas as pd


abs_path=os.path.abspath(os.path.curdir)+"/Data/"

sbet_data = Sbet()
sbet_data.read_sbet_file(abs_path+"20180618_00.txt")
sbet_data.fft(0.005)
sbet_data.fft_window()
# sbet_data.filter(500)

