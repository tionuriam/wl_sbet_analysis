import os
import sys
from xml.etree import ElementTree as ET

sys.path.append(os.getcwd())
#from my_code.waterlevel import WaterLevel
abs_path=os.path.abspath(os.path.curdir)+"/Data/"
fullpath = abs_path+"wl20180614.xml"

def read_jhc_file(self, fullpath):
    # Check the File's existence
    if os.path.exists(fullpath):
        self.metadata["Source File"] = fullpath
        print('Opening water level data file:' + fullpath)
    else:  # Raise a meaningful error
        raise RuntimeError('Unable to locate the input file' + fullpath)

#file extension
file_name, file_extension = os.path.splitext(fullpath)
#print("File name: %s" %file_name)
print("File extension:", file_extension)

with open(fullpath, 'r') as file:
    tree = ET.parse(file)
    root = tree.getroot()
    # print(reader)
# root tag
print(root.tag)

# identify elements in root of xml
for elements in root:
    print(elements.tag, elements.attrib)

for elements in root[0]:
    print(elements.text)

date_time = []
waterlevel = []
s = []
#accessing values in child directory (observations)
for values in root.iter('wl'):
    date_time.append(values.attrib['t'])
    waterlevel.append(values.attrib['v'])
    s.append(values.attrib['s'])

print(date_time)
print(waterlevel)
print(s)


from my_code.waterlevel_xmlread import WaterLevel
water_levels = WaterLevel()

water_levels.read_jhc_file(abs_path+"wl20180614.xml")
water_levels.draw()








