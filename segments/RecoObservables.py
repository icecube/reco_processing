# IceCube imports
from icecube import dataio, icetray, dataclasses
from icecube import millipede, MuonGun
from icecube.dataclasses import I3Double, I3Particle, I3Direction, I3Position, I3VectorI3Particle, I3Constants
from icecube.dataclasses import I3RecoPulse, I3RecoPulseSeriesMap, I3RecoPulseSeriesMapMask
from icecube.icetray import I3Units, I3Frame, I3ConditionalModule, traysegment
from I3Tray import I3Tray
from .ContainementCheck import iscontained, ispointinpolygon, getclosestdistance

# Python system imports
import sys, datetime, os
from glob import glob
from optparse import OptionParser
import numpy as n



"""
calculation of the energy ratio
"""
def getenergyratio(double_particles):
    energythreshold=1e3
    
    cascade1, cascade2 = double_particles
    eratio = (cascade1.energy-cascade2.energy)/(cascade1.energy+cascade2.energy) if cascade1.energy+cascade2.energy >= energythreshold else 1.
    return eratio

"""
calculation of the energy confinement
"""
def getenergyconfinement(double_particles, track_particles, key):
    energythreshold=1e3
    distancethreshold = 40
    # the double cascade
    cascade1, cascade2 = double_particles

    # due to a falsely configured muon spacing in millipede, need to split the cascade and track segments and then rebin
    if key == 'reco':
        particle_buffer = []
        track_dx_buffer, track_dy_buffer, track_dz_buffer, track_de_buffer = [], [], [], []
        for particle in track_particles:
            if particle.shape == I3Particle.Cascade:
                track_dx_buffer.append(particle.pos.x)
                track_dy_buffer.append(particle.pos.y)
                track_dz_buffer.append(particle.pos.z)
                track_de_buffer.append(particle.energy)
            else:
                particle_buffer.append(particle)
        track_dx_buffer = n.asarray(track_dx_buffer)
        track_dy_buffer = n.asarray(track_dy_buffer)
        track_dz_buffer = n.asarray(track_dz_buffer)
        track_de_buffer = n.asarray(track_de_buffer)
        for particle in particle_buffer:
            argmin = n.argmin(n.sqrt((track_dx_buffer - particle.pos.x)**2
                                   + (track_dy_buffer - particle.pos.y)**2
                                   + (track_dz_buffer - particle.pos.z)**2))
            track_de_buffer[argmin] += particle.energy
    elif key == 'true':
        track_dx_buffer, track_dy_buffer, track_dz_buffer, track_de_buffer = [], [], [], []
        for particle in track_particles:
            track_dx_buffer.append(particle.pos.x)
            track_dy_buffer.append(particle.pos.y)
            track_dz_buffer.append(particle.pos.z)
            track_de_buffer.append(particle.energy)
        track_dx_buffer = n.asarray(track_dx_buffer)
        track_dy_buffer = n.asarray(track_dy_buffer)
        track_dz_buffer = n.asarray(track_dz_buffer)
        track_de_buffer = n.asarray(track_de_buffer)

    # find energy depositions in the vicinity of the double cascade vertices
    mask1 = ( n.sqrt((track_dx_buffer-cascade1.pos.x)**2
                   + (track_dy_buffer-cascade1.pos.y)**2
                   + (track_dz_buffer-cascade1.pos.z)**2) < distancethreshold )
    mask2 = ( n.sqrt((track_dx_buffer-cascade2.pos.x)**2
                   + (track_dy_buffer-cascade2.pos.y)**2
                   + (track_dz_buffer-cascade2.pos.z)**2) < distancethreshold )
    # calculate the energy confinement
    esum = n.sum(track_de_buffer)
    edep = n.sum(track_de_buffer[mask1 | mask2])
    econfinement = edep/esum if esum >= energythreshold else 0.
    return econfinement




"""
calculate reco observables
"""
def eventgen_eratio(frame,key):
    energythreshold=1e3
    if key not in frame:
        print("could not find", key)
        return

    reco = frame[key]
    
    energy1 = reco["cascade_energy"]
    energy2 = reco["cascade_cascade_00001_energy"]
    eratio = (energy1 - energy2)/(energy1 + energy2) if energy1+energy2 >= energythreshold else 1.

    frame.Put(f'RecoERatio_{key}', I3Double(eratio))

def calculaterecoobservables(frame,innerboundary,outeredge_x, outeredge_y,monopod_key,taupede_key,millipede_key,suffix):
    
    if f"RecoContainedSingle{suffix}" in frame: return

    if any(k not in frame for k in (monopod_key, taupede_key, millipede_key)):
        print(f"Reco keys missing! Not doing Neha reco observables")
        return
    
    energythreshold=1e3
    # the single vertex containment
    cascade = frame[monopod_key] # MonopodFit_iMIGRAD_PPB0
    contained = iscontained(cascade.pos.x, cascade.pos.y, cascade.pos.z, innerboundary,outeredge_x, outeredge_y)

    # the double vertex properties and containment
    cascade1, cascade2 = frame[f"{taupede_key}Particles"] # TaupedeFit_iMIGRAD_PPB0Particles
    contained1 = iscontained(cascade1.pos.x, cascade1.pos.y, cascade1.pos.z, innerboundary,outeredge_x, outeredge_y)
    contained2 = iscontained(cascade2.pos.x, cascade2.pos.y, cascade2.pos.z, innerboundary,outeredge_x, outeredge_y)
    length = n.log10((cascade1.pos-cascade2.pos).magnitude)
    reco_l = (cascade1.pos-cascade2.pos).magnitude
    eratio = getenergyratio([cascade1, cascade2])
    e1 = n.log10(cascade1.energy)
    e2 = n.log10(cascade2.energy)
    
    # the direction is taken from the HESEMillipedeFit (i.e. best fit out of three hypotheses)
    zenith = frame[millipede_key].dir.zenith
    azimuth = frame[millipede_key].dir.azimuth
    
    # if truncated deposited energy is below threshold switch over to non-truncated energy deposition
    etot = n.log10(frame[f'{millipede_key}TruncatedDepositedEnergy'].value)
    reco_e = frame[f'{millipede_key}TruncatedDepositedEnergy'].value
    if frame.Has('energy_reco'):
	      frame.Delete('energy_reco')
    usetruncated = True
    if etot < n.log10(energythreshold):
        etot = n.log10(frame[f'{millipede_key}DepositedEnergy'].value)
        reco_e = (frame[f'{millipede_key}DepositedEnergy'].value)
        usetruncated = False
        
    # the calculation of the energy confinement
    if usetruncated:
        econfinement = getenergyconfinement([cascade1, cascade2], frame[f'{millipede_key}TruncatedParticles'], 'reco')
    else:
        econfinement = getenergyconfinement([cascade1, cascade2], frame[f'{millipede_key}Particles'], 'reco')
    # sanitize values
    if not n.isfinite(length):
        length = 0 # limit to 1 m
        reco_l = 1
    if not n.isfinite(e1):
        e1 = 0 # limit to 1 GeV
    if not n.isfinite(e2):
        e2 = 0 # limit to 1 GeV
    if not n.isfinite(etot):
        etot = 0 # limit to 1 GeV
        reco_e = 1


    # limit length to > 1m and < ~2km and smear the boundary region
    if length <= 0:
        length = n.minimum(0.0 + n.abs(n.random.normal(loc=0., scale=0.3)),0.99) 
        reco_l = 10**length
    elif length >= 3.3:
         length = n.maximum(3.3 - n.abs(n.random.normal(loc=0., scale=0.05)),3.2)
         reco_l = 10**length
         
    # save it to the frame
    frame.Put(f'RecoContainedSingle{suffix}', icetray.I3Bool(contained))
    frame.Put(f'RecoContained1{suffix}', icetray.I3Bool(contained1))
    frame.Put(f'RecoContained2{suffix}', icetray.I3Bool(contained2))

    frame.Put(f'RecoL{suffix}', I3Double(reco_l))
    frame.Put(f'RecoERatio{suffix}', I3Double(eratio))
    frame.Put(f'RecoEConfinement{suffix}', I3Double(econfinement))
    frame.Put(f'RecoETot{suffix}', I3Double(reco_e))
    frame.Put(f'RecoLogE1{suffix}', I3Double(e1))
    frame.Put(f'RecoLogE2{suffix}', I3Double(e2))
    frame.Put(f'RecoZenith{suffix}', I3Double(zenith))
    frame.Put(f'RecoAzimuth{suffix}', I3Double(azimuth))

    frame.Put(f'{taupede_key}_1', I3Particle(cascade1))
    frame.Put(f'{taupede_key}_2', I3Particle(cascade2))

    for coord in ['x', 'y', 'z']:
        frame.Put(f'{monopod_key}_{coord}', I3Double(getattr(cascade.pos, coord)))
        frame.Put(f'{taupede_key}_1_{coord}', I3Double(getattr(cascade1.pos, coord)))
        frame.Put(f'{taupede_key}_2_{coord}', I3Double(getattr(cascade2.pos, coord)))

    # add fit params information
    for key in [monopod_key, taupede_key, millipede_key]:
        if key in frame:
            frame.Put(key + 'Logl', I3Double(frame[key + 'FitParams'].logl))
            frame.Put(key + 'LoglNdof', I3Double(frame[key + 'FitParams'].ndof))
            frame.Put(key + 'Chi2', I3Double(frame[key + 'FitParams'].chi_squared))
            frame.Put(key + 'Chi2Ndof', I3Double(frame[key + 'FitParams'].chi_squared_dof))
            
            
    return True
