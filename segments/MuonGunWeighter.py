from I3Tray import *
from icecube import icetray, phys_services, dataio, dataclasses,MuonGun
from icecube.simprod import segments
from icecube.simclasses import I3MMCTrack
from icecube import MuonGun, simclasses
from icecube.icetray import traysegment, I3Module
import sys, math
import copy
import glob
import numpy as np
from icecube.icetray import traysegment, I3Module
import os
import glob

import re

def get_muon_files( dataset ):
    return glob.glob(f"/data/sim/IceCube/2016/filtered/level2/MuonGun/{dataset}/*/*")

def get_muon_file( dataset ):
    return glob.glob(f"/data/sim/IceCube/2016/filtered/level2/MuonGun/{dataset}/0000000-0000999/*")[0]

def get_simulated_events( dataset ):
    # taken from https://wiki.icecube.wisc.edu/index.php/Simulation_and_Data_Used_in_ESTES_10_year
    # evts/file*nfiles
    if dataset == "21315": return 500*15000
    if dataset == "21316": return 25000*40000
    if dataset == "21317": return 50000*20000
    if dataset == "21318": return 100000*100000
    if dataset == "21319": return 100000*100000

def get_nfiles( dataset ):
    # taken from https://wiki.icecube.wisc.edu/index.php/Simulation_and_Data_Used_in_ESTES_10_year
    # evts/file*nfiles
    if dataset == "21315": return 15000
    if dataset == "21316": return 40000
    if dataset == "21317": return 20000
    if dataset == "21318": return 100000
    if dataset == "21319": return 100000

def get_dataset( infile ):

    match = re.search(r'\b(\d{5})\b', infile)
    if match:
        run_id = match.group(1)

    return run_id
        
@traysegment
def Get_MuonWeight(tray,name,infile,flux_model,prefix):
    
    def harvest_generators(infile):
        """
        Harvest serialized generator configurations from a set of I3 files.
        """
        from icecube.icetray.i3logging import log_info as log
        generator = None
        
        for fname in infile:
            if "GCD" in fname: continue # I sometimes have a gcd in the infiles list as well

            f = dataio.I3File(fname)
            while(f.more()):
                    try:
                        fr = f.pop_frame(icetray.I3Frame.Stream('S'))
                    except Exception:
                        continue
                    f.close() 
                   
                    if fr is not None:
                        for k in fr.keys():
                            v = fr[k]
                            if isinstance(v, MuonGun.GenerationProbability):
                                log('%s: found "%s" (%s)' % (f, k, type(v).__name__), unit="MuonGun")
                                if generator is None:
                                    generator = v
                                else:
                                    generator += v

        return generator

    def harvest_generator(infile):
        """
        Harvest serialized generator configurations from a set of I3 files.
        """
        from icecube.icetray.i3logging import log_info as log
        generator = None
    
        print(infile)
        f = dataio.I3File(infile)
        try:
            fr = f.pop_frame(icetray.I3Frame.Stream('S'))
        except Exception:
            sys.exit("could nog find s stream harvest generator")
        f.close() 
        
        for k in fr.keys():
            v = fr[k]
            if isinstance(v, MuonGun.GenerationProbability):
                log('%s: found "%s" (%s)' % (f, k, type(v).__name__), unit="MuonGun")
                generator = v

        if generator == None:
            sys.exit("could nog find generator")

        return generator


    dataset = get_dataset( infile[1] )

    print("Muongun dataset", dataset)

    generator = harvest_generator( get_muon_file(dataset) )*get_nfiles( dataset )

    model = MuonGun.load_model(flux_model)
    
    tray.AddModule('I3MuonGun::WeightCalculatorModule', 'MuonWeight'+prefix, Model=model, Generator=generator)