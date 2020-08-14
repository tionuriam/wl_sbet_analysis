from xml.etree import ElementTree
import numpy as np

print("Station Datasets")
print('Fort Station (A)')
# Subordinate station (A)
subordinate = ElementTree.parse('fp.xml')
subdata = subordinate.getroot()

#HHW
#x = subdata[1][0]
#for i in x[]


#create emplty list
HH = []
LL = []
H = []
L = []

#iterate through the values in xml
for values in subdata[1]:
    data = values.attrib
    HH_LL = data['ty']
    time = data['t'][-5:]
    date = data['t'][ :-5]
    waterlevel = data['v']
    station_value = (date, time, waterlevel)
    #print(HH_LL, tide_value)
    if HH_LL == 'HH':
        #HH.append(date)
        #HH.append(time)
        #HH.append(waterlevel)
        HH.append(station_value)
    elif HH_LL == 'LL':
        #LL.append(date)
        #LL.append(time)
        #LL.append(waterlevel)
         LL.append(station_value)
    elif HH_LL == 'H ':
       # H.append(date)
       # H.append(time)
         H.append(station_value)

    elif HH_LL == 'L ':
        #L.append(date)
        #L.append(time)
        #L.append(waterlevel)
        L.append(station_value)

#L for station A

print('HHW = %s' % HH)
print('LLW = %s' % LL)
print('LHW = %s' % H)
print('HLW = %s' % L)

# Functions
#Averages
def Average(lst):
    return sum(lst) / len(lst)

print('----------------------------------------------------------------------------')

print("Computations")
#HH for Station A
#extract the values for just water HH water levels
#HHW water level for main station (A)
HHW_A = []
for wl in HH:
    HHW_A.append(float(wl[:][2]))

#LLW wl for station A
LLW_A = []
for wl in LL:
    LLW_A.append(float(wl[:][2]))

#LHW wl for station A
HLW_A = []
for wl in L:
    HLW_A.append(float(wl[:][2]))

#H for station A
LHW_A = []
for wl in H:
    LHW_A.append(float(wl[:][2]))

print("Station A statistics")

#Averages
print("Averages:")
print("MHHW: %s" %Average(HHW_A))
print("MLLW: %s" %Average(LLW_A))
print("MHLW: %s" %Average(HLW_A))
print("MLHW: %s" %Average(LHW_A))

#sums
print("Sums:")
print("Sums HHW: %s" %sum(HHW_A))
print("Sum LLW: %s" %sum(LLW_A))
print("Sums HLW: %s" %sum(HLW_A))
print("Sums LHW: %s" %sum(LHW_A))

print("---------------------------------------------------------")

print('Portland Station (B)')

# Main station (B)
main= ElementTree.parse('port_main.xml')
maindata = main.getroot()

#create emplty list
MHH = []
MLL = []
ML = []
MH = []

#iterate through the values in xml
for values in maindata[1]:
    data = values.attrib
    HH_LL = data['ty']
    time = data['t'][-5:]
    date = data['t'][ :-5]
    waterlevel = data['v']
    station_value = (date, time, waterlevel)
    #print(HH_LL, tide_value)
    if HH_LL == 'HH':
        MHH.append(station_value)
        #datesHH.append(date)
    elif HH_LL == 'LL':
        MLL.append(station_value)
    elif HH_LL == 'H ':
        MH.append(station_value)
    elif HH_LL == 'L ':
        ML.append(station_value)

print('HHW = %s' % MHH)
print('LLW = %s' % MLL)
print('HLW = %s' % MH)
print('LHW = %s' % ML)


print("Computations")
#HH for Station B
#extract the values for just water HH water levels
#HHW water level for main station (B)
HHW_B = []
for wl in MHH:
    HHW_B.append(float(wl[:][2]))

#LLW wl for station B
LLW_B = []
for wl in MLL:
    LLW_B.append(float(wl[:][2]))

#LHW wl for station B
HLW_B = []
for wl in ML:
    HLW_B.append(float(wl[:][2]))

#H for station B
LHW_B = []
for wl in MH:
    LHW_B.append(float(wl[:][2]))

print("Station B statistics")

#Averages
print("Averages:")
print("MHHW_B: %s" %Average(HHW_B))
print("MLLW_B: %s" %Average(LLW_B))
print("MHLW_B: %s" %Average(HLW_B))
print("MLHW_B: %s" %Average(LHW_B))

#sums
print("Sums:")
print("Sums HHW: %s" %sum(HHW_B))
print("Sum LLW: %s" %sum(LLW_B))
print("Sums HLW: %s" %sum(HLW_B))
print("Sums LHW: %s" %sum(LHW_B))

print("---------------------------------------------------------")

# Compute differences
print("Compute differences")
#print("dHHW")
dHHW = []
for A, B in zip(HHW_A, HHW_B):
    diff = A - B
    dHHW.append(diff)
    #print(diff)

#print("dLLW")
dLLW = []
for A, B in zip(LLW_A, LLW_B):
    diff = A - B
    dLLW.append(diff)
    #print(diff)

#print("dHLW")
dHLW = []
for A, B in zip(HLW_A, HLW_B):
    diff = A - B
    dHLW.append(diff)
    #print(diff)

#print("dLHW")
dLHW = []
for A, B in zip(LHW_A, LHW_B):
    diff = A - B
    dLHW.append(diff)
    #print(diff)

#sums of differences
print("Sums of differences")
print("Sums dHHW: %s" %sum(dHHW))
print("Sum dLLW: %s" %sum(dLLW))
print("Sums dHLW: %s" %sum(dHLW))
print("Sums dLHW: %s" %sum(dLHW))

print("Outputs")

#DHQ_A = 0.5*(Mean HHW_A - Mean LHW_A)
DHQ_A = 0.5 * (Average(HHW_A) - Average(LHW_A))
print("DHQ_A: %s" % DHQ_A)

#DLQ_A = 0.5*(HLW_A - LLW_A)
DLQ_A = 0.5*(Average(HLW_A) - Average(LLW_A))
print("DHLQ_A: %s" % DLQ_A)

#LW_A = MHLW_A - MLLW_A
LW_A = Average(HLW_A) - Average(LLW_A)

#Average(HHW_A)


#print("---------------------------------------------------------------")
