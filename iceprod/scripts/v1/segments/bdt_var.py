###
### Taken from
### /data/user/zchen/data_process/merge_main.py
### /home/zzhang1/private_cascade_filter/cascade-final-filter
###
### copied to /data/user/tvaneede/GlobalFit/selection 
###
from icecube import icetray,dataclasses
from icecube.dataclasses import I3Double, I3Particle
from icecube import recclasses

import numpy as np
import pandas as pd

def taupede_monopod_bdt_var( frame, monopod_key, taupede_key ):

    if 'Taupede_Distance' in frame: return
    
    if 'SPEFit16' not in frame: return # for old reco

    # variables
    taupede1,taupede2 = frame[f"{taupede_key}Particles"]
    frame["Taupede_Distance"] = I3Double(taupede1.length)

    E1 = taupede1.energy
    E2 = taupede2.energy
    frame["Taupede1_Particles_energy"] = I3Double( taupede1.energy )
    frame["Taupede2_Particles_energy"] = I3Double( taupede2.energy )

    # frame['Taupede_Asymmetry'] = I3Double( (E1-E2)/(E1+E2) )
    frame['Taupede_Asymmetry'] = I3Double( (E1-E2)/(E1+E2) ) if E1+E2 >= 1e3 else I3Double(1.)

    fitparams = frame[f'{taupede_key}FitParams']
    frame["Taupede_ftpFitParams_rlogl"] = I3Double( frame[f'{taupede_key}FitParams'].rlogl )
    frame["cscdSBU_MonopodFit4_noDCFitParams_rlogl"] = I3Double( frame[f'{monopod_key}FitParams'].rlogl )
    
    frame['TauMonoDiff_rlogl'] = I3Double( frame[f'{taupede_key}FitParams'].rlogl - frame[f'{monopod_key}FitParams'].rlogl )
    frame["Taupede_spice3FitParams_nmini"] = I3Double( frame[f'{taupede_key}FitParams'].nmini )

    frame["LineFit_zenith"] = I3Double( frame["LineFit"].dir.zenith )

    # obtained using cscdSBU_misc
    cscdSBU_Qtot_HLC_log = np.log10(frame['cscdSBU_Qtot_HLC'].value)
    frame['cscdSBU_Qtot_HLC_log']= I3Double( cscdSBU_Qtot_HLC_log )

    if "CVStatistics" in frame:
        frame["CVStatistics_q_max_doms"] = I3Double( frame['CVStatistics'].q_max_doms )
        frame["CVStatistics_z_travel"] = I3Double( frame['CVStatistics'].z_travel )

    frame["CscdL3_SPEFit16_zenith"] = I3Double( frame['SPEFit16'].dir.zenith )
    frame["CscdL3_SPEFit16FitParams_rlogl"] = I3Double( frame['SPEFit16FitParams'].rlogl )

    frame["CascadeLlhVertexFitParams_rlogL"] = I3Double( frame["CascadeLlhVertexFit_L3Params"].ReducedLlh ) 

    frame["cscdSBU_MonopodFit4_noDC_z"] =  I3Double( frame[monopod_key].pos.z )
    frame["cscdSBU_MonopodFit4_noDC_zenith"] =  I3Double( frame[monopod_key].dir.zenith )

    ### all for cscdSBU_VertexRecoDist_CscdLLh
    x1 = frame['CascadeLlhVertexFit_L3'].pos.x
    y1 = frame['CascadeLlhVertexFit_L3'].pos.y
    z1 = frame['CascadeLlhVertexFit_L3'].pos.z
    x2 = frame[taupede_key].pos.x
    y2 = frame[taupede_key].pos.y
    z2 = frame[taupede_key].pos.z
    distance = np.sqrt( (x1-x2)**2 + (y1-y2)**2 + (z1-z2)**2 )
    frame["cscdSBU_VertexRecoDist_CscdLLh"]= I3Double( distance )

    x = frame["MonopodFit_iMIGRAD_PPB0_Delay_ice"]

    return True


