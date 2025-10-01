
from icecube import dataio, icetray, dataclasses, simclasses
from scipy.interpolate import interp1d
import pandas as pd

pol_hadr_0 = '/home/abalagopalv/diffuse/TauStudies/tau_polarization/Hadron_polarization_0.csv'
pol_hadr_minus1='/home/abalagopalv/diffuse/TauStudies/tau_polarization/Hadron_polarization_-1.csv'
pol_lep_0 = '/home/abalagopalv/diffuse/TauStudies/tau_polarization/Lepton_polarization_0.csv'
pol_lep_minus1='/home/abalagopalv/diffuse/TauStudies/tau_polarization/Lepton_polarization_-1.csv'

def tau_polarization(frame):
    leptons = [dataclasses.I3Particle.MuPlus,dataclasses.I3Particle.MuMinus,\
          dataclasses.I3Particle.EMinus, dataclasses.I3Particle.EPlus]
    neutrinos = [dataclasses.I3Particle.NuE, dataclasses.I3Particle.NuEBar,
                     dataclasses.I3Particle.NuMu, dataclasses.I3Particle.NuMuBar,
                     dataclasses.I3Particle.NuTau, dataclasses.I3Particle.NuTauBar]
    nutype=frame["I3MCWeightDict"]["PrimaryNeutrinoType"]
    inter_type=frame['I3MCWeightDict']['InteractionType']
    had_energy = []
    lep_energy = []
    print(frame['I3EventHeader'].run_id,frame['I3EventHeader'].event_id)
    if (abs(nutype)==16 and inter_type==1.0):
        MCTreeName = 'I3MCTree'
        if frame.Has(MCTreeName):
            for p in frame[MCTreeName].get_primaries():
                    
                if (p.type != dataclasses.I3Particle.NuTau and p.type != dataclasses.I3Particle.NuTauBar):
                    continue
                for c in frame[MCTreeName].children(p):
                    if c.type == dataclasses.I3Particle.TauMinus or c.type == dataclasses.I3Particle.TauPlus:
                        E_Tau = c.energy

                        for d in frame[MCTreeName].get_daughters(c):
                            if d.type == dataclasses.I3Particle.NuTau or d.type == dataclasses.I3Particle.NuTauBar:
                                time_of_int = d.time
                                break
                            else:
                                time_of_int = 0.   #to account for Tau decays outside of detector where theres no daughter neutrino

                        

                        for d in frame[MCTreeName].get_daughters(c):
                            if d.time == time_of_int and d.type not in neutrinos:
                                    if d.type not in leptons:

                                        had_energy.append(d.energy)
                                        
                                    else:
                                        lep_energy.append(d.energy)
                                        
                        y_lep = sum(lep_energy)/E_Tau
                        y_had = sum(had_energy)/E_Tau
                        frame['y_lep'] = dataclasses.I3Double(y_lep)
                        frame['y_had']= dataclasses.I3Double(y_had)
                

    if sum(lep_energy)!=0:
        old_spline=pd.read_csv(pol_lep_0,header=None)
        new_spline=pd.read_csv(pol_lep_minus1,header=None)
        x = old_spline[0]
        y = old_spline[1]
        xn = new_spline[0]
        yn = new_spline[1]
        f1 = interp1d(x, y, kind='cubic')
        f2 = interp1d(xn, yn, kind='cubic')

        num = f2(y_lep)
        denom = f1(y_lep)
        ratio = num/denom
        frame['TotalWeightPol'] = dataclasses.I3Double(frame['TotalWeight'].value*ratio)
        
    elif sum(had_energy)!=0:
        old_spline=pd.read_csv(pol_hadr_0,header=None)
        new_spline=pd.read_csv(pol_hadr_minus1,header=None)
        x = old_spline[0]
        y = old_spline[1]
        xn = new_spline[0]
        yn = new_spline[1]
        f1 = interp1d(x, y, kind='cubic')
        f2 = interp1d(xn, yn, kind='cubic')

        num = f2(y_had)
        denom = f1(y_had)
        ratio = num/denom
        frame['TotalWeightPol'] = dataclasses.I3Double(frame['TotalWeight'].value*ratio)
        
                            
    if not frame.Has('TotalWeightPol'):
        frame['TotalWeightPol'] = dataclasses.I3Double(frame['TotalWeight'].value)