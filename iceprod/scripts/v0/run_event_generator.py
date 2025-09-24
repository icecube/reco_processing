#!/usr/bin/env python3
from icecube import icetray, dataio, dataclasses
from I3Tray import I3Tray
import datetime
import numpy as np
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter

from egenerator.ic3.segments import ApplyEventGeneratorReconstruction

model_base_dir = "/cvmfs/icecube.opensciencegrid.org/users/tvaneede/exported_models/egenerator/v2_0/"

def generate_egen_seed_from_cascade(frame, seed_key):
    seed_particle = frame[seed_key]

    seed_dict = {}
    seed_dict['x'] = seed_particle.pos.x
    seed_dict['y'] = seed_particle.pos.y
    seed_dict['z'] = seed_particle.pos.z
    seed_dict['zenith'] = seed_particle.dir.zenith
    seed_dict['azimuth'] = seed_particle.dir.azimuth
    seed_dict['time'] = seed_particle.time

    # For now just guess that the energy is divided evenly and assume
    # 50m / PeV for the avg. decay length
    avg_inel = 0.3
    seed_dict['energy'] = seed_particle.energy * avg_inel
    seed_dict['cascade_00001_energy'] = seed_particle.energy * (1 - avg_inel)
    seed_dict['cascade_00001_distance'] = 50 * (seed_particle.energy * (1 - avg_inel) / 1e6)

    frame[f'dc_from_{seed_key}'] = dataclasses.I3MapStringDouble(seed_dict)
    return True

def generate_egen_seed_from_taupede(frame):
    seed1, seed2 = frame["TaupedeFit_iMIGRAD_PPB0Particles"]

    seed_dict = {}
    seed_dict['x'] = seed1.pos.x
    seed_dict['y'] = seed1.pos.y
    seed_dict['z'] = seed1.pos.z
    seed_dict['zenith'] = seed1.dir.zenith
    seed_dict['azimuth'] = seed1.dir.azimuth
    seed_dict['time'] = seed1.time
    seed_dict['energy'] = seed1.energy 
    
    seed_dict['cascade_00001_energy'] = seed2.energy
    seed_dict['cascade_00001_distance'] = seed1.length

    frame[f'dc_from_TaupedeFit_iMIGRAD_PPB0'] = dataclasses.I3MapStringDouble(seed_dict)
    return True

def add_monopod_seeds(frame):
    seed_map = dataclasses.I3MapStringDouble()
    monopod = frame["MonopodFit_iMIGRAD_PPB0"]
    seed_map["x"] = monopod.pos.x
    seed_map["y"] = monopod.pos.y
    seed_map["z"] = monopod.pos.z
    seed_map["time"] = monopod.time
    seed_map["zenith"] = monopod.dir.zenith
    seed_map['azimuth'] = monopod.dir.azimuth
    seed_map['energy'] = monopod.energy/2
    seed_map['cascade_00001_distance'] = 0
    seed_map['cascade_00001_energy'] = monopod.energy/2
    frame[f"MonopodSeed_length0"] = seed_map

    seed_map50 = seed_map.copy()
    seed_map50['cascade_00001_distance'] = 50
    frame[f"MonopodSeed_length50"] = seed_map50

    seed_map100 = seed_map.copy()
    seed_map100['cascade_00001_distance'] = 100
    frame[f"MonopodSeed_length100"] = seed_map100

    seed_map200 = seed_map.copy()
    seed_map200['cascade_00001_distance'] = 200
    frame[f"MonopodSeed_length200"] = seed_map200

def main():

    import sys

    print("Command-line arguments:")
    for arg in sys.argv:
        print(arg)

    parser = ArgumentParser(description=__doc__, formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument("--Inputfile",type=str,help='Input file',dest="inputfile")
    parser.add_argument("--Outputfile",type=str,help='Output file',dest="outputfile")

    opts = parser.parse_args()

    # initialize timers
    starttimes, stoptimes = {}, {}
    timekeys = ['EventGeneratorDC_Max','EventGeneratorDC_Thijs']
    for timekey in timekeys:
        starttimes[timekey] = []
        stoptimes[timekey] = []

    def timer(frame,tag,key):
        if tag == 'start':
            starttimes[key].append(datetime.datetime.now())
        elif tag == 'stop':
            stoptimes[key].append(datetime.datetime.now())

    starttime = datetime.datetime.now()

    tray = I3Tray()

    tray.AddModule('I3Reader', 'reader', filenamelist=[opts.inputfile])

    tray.AddModule(generate_egen_seed_from_cascade, 'make_seed_max',
                   seed_key='MonopodFit_iMIGRAD_PPB0')
    
    tray.Add(timer, tag='start', key='EventGeneratorDC_Max')
    tray.AddSegment(
        ApplyEventGeneratorReconstruction,
        'apply_egen_reco_dc_max',
        pulse_key='SplitInIceDSTPulses',
        dom_and_tw_exclusions=['BadDomsList', 'CalibrationErrata', 'SaturationWindows'],
        partial_exclusion=True,
        exclude_bright_doms=True,
        model_names=['starting_multi_cascade_7param_noise_ftpv3m__big_n002_01'],
        seed_keys=['dc_from_MonopodFit_iMIGRAD_PPB0'],
        model_base_dir=model_base_dir,
        output_key='EventGeneratorDC_Max',
    )
    tray.Add(timer, tag='stop', key='EventGeneratorDC_Max')

    tray.AddModule(generate_egen_seed_from_taupede, 'make_seed_thijs' )
    tray.Add(add_monopod_seeds, f"add_monopod_seeds_for_egen")

    tray.Add(timer, tag='start', key='EventGeneratorDC_Thijs')
    tray.AddSegment(
        ApplyEventGeneratorReconstruction,
        'apply_egen_reco_dc_thijs',
        pulse_key='SplitInIceDSTPulses',
        dom_and_tw_exclusions=['BadDomsList', 'CalibrationErrata', 'SaturationWindows'],
        partial_exclusion=True,
        exclude_bright_doms=True,
        model_names=['starting_multi_cascade_7param_noise_ftpv3m__big_n002_01'],
        seed_keys=['dc_from_TaupedeFit_iMIGRAD_PPB0', 'MonopodSeed_length0'],
        model_base_dir=model_base_dir,
        output_key='EventGeneratorDC_Thijs',
    )
    tray.Add(timer, tag='stop', key='EventGeneratorDC_Thijs')


    tray.AddModule('I3Writer', 'writer_i3',
                   filename=opts.outputfile,
                    Streams=[icetray.I3Frame.Geometry, icetray.I3Frame.Calibration,
                        icetray.I3Frame.DetectorStatus, icetray.I3Frame.DAQ, icetray.I3Frame.Physics, icetray.I3Frame.Simulation, icetray.I3Frame.Stream('M')],
                   DropOrphanStreams=[icetray.I3Frame.DAQ, icetray.I3Frame.Stream('M')])

    tray.Execute()
    tray.Finish()

    duration = datetime.datetime.now() - starttime
    print("\t\tFinished I3Tray..")
    print("")
    print("This took:",duration)
    print("")
    print("Timing information for each modules is as follows:")
    print("")
    for timekey in timekeys:

        if len(starttimes[timekey]) == 0:
            continue
        tstart, tstop = np.asarray(starttimes[timekey]), np.asarray(stoptimes[timekey])
        if len(tstart) != len(tstop):
            durations = tstop - tstart[:len(tstop)]
        else:
            durations = tstop - tstart

        print ("\t{} took {}".format(timekey,durations.sum()))

if __name__ == '__main__':
    main()

