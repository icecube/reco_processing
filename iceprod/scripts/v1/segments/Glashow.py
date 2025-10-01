from icecube import dataio, icetray, dataclasses, simclasses
from scipy.interpolate import interp1d
import pandas as pd

#Following both functions
#for glashow correction and Tau Polarization are
# Taken from Aswathi
def glashow_correction(frame):
    
    nutype=int(frame["I3MCWeightDict"]["PrimaryNeutrinoType"])
    inter_type=int(frame['I3MCWeightDict']['InteractionType'])
    en = float(frame['I3MCWeightDict']['PrimaryNeutrinoEnergy'])
    if (abs(nutype)==12 and inter_type==3.0 and en>4e6):
        old_spline=pd.read_csv('/home/abalagopalv/diffuse/TauStudies/Glashow_old.csv',header=None)
        new_spline=pd.read_csv('/home/abalagopalv/diffuse/TauStudies/Glashow_new.csv',header=None)

        x = old_spline[0]
        y = old_spline[1]

        xn = new_spline[0]
        yn = new_spline[1]
        f1 = interp1d(x, y, kind='cubic')
        f2 = interp1d(xn, yn, kind='cubic')
        if en<9.9e6:

            num = f2(en/1e6)
            denom = f1(en/1e6)
            ratio = num/denom
            frame['TotalWeight'] = dataclasses.I3Double(frame['I3MCWeightDict']['TotalWeight']*ratio)
        elif en>=9.9e6:
            num = f2(9.89)
            denom = f1(9.89)
            ratio = num/denom
            frame['TotalWeight'] = dataclasses.I3Double(frame['I3MCWeightDict']['TotalWeight']*ratio)
    else:
        frame['TotalWeight'] = dataclasses.I3Double(frame['I3MCWeightDict']['TotalWeight'])
