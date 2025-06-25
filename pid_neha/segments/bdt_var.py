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

def taupede_monopod_bdt_var( frame ):
    taupede1,taupede2 = frame["TaupedeFit_iMIGRAD_PPB0Particles"]
    frame["Taupede_Distance"] = I3Double(taupede1.length)

    E1 = taupede1.energy
    E2 = taupede2.energy
    frame["Taupede1_Particles_energy"] = I3Double( taupede1.energy )
    frame["Taupede2_Particles_energy"] = I3Double( taupede2.energy )

    frame['Taupede_Asymmetry'] = I3Double( (E1-E2)/(E1+E2) )

    fitparams = frame['TaupedeFit_iMIGRAD_PPB0FitParams']
    frame["Taupede_ftpFitParams_rlogl"] = I3Double( frame['TaupedeFit_iMIGRAD_PPB0FitParams'].rlogl )
    frame["cscdSBU_MonopodFit4_noDCFitParams_rlogl"] = I3Double( frame['MonopodFit_iMIGRAD_PPB0FitParams'].rlogl )
    
    frame['TauMonoDiff_rlogl'] = I3Double( frame['TaupedeFit_iMIGRAD_PPB0FitParams'].rlogl - frame['MonopodFit_iMIGRAD_PPB0FitParams'].rlogl )
    frame["Taupede_spice3FitParams_nmini"] = I3Double( frame['TaupedeFit_iMIGRAD_PPB0FitParams'].nmini )

    # obtained using cscdSBU_misc
    cscdSBU_Qtot_HLC_log = np.log10(frame['cscdSBU_Qtot_HLC'].value)
    frame['cscdSBU_Qtot_HLC_log']= I3Double( cscdSBU_Qtot_HLC_log )

    frame["CVStatistics_q_max_doms"] = I3Double( frame['CVStatistics'].q_max_doms )
    frame["CVStatistics_z_travel"] = I3Double( frame['CVStatistics'].z_travel )

    frame["CscdL3_SPEFit16_zenith"] = I3Double( frame['CscdL3_SPEFit16'].dir.zenith )
    frame["CscdL3_SPEFit16FitParams_rlogl"] = I3Double( frame['CscdL3_SPEFit16FitParams'].rlogl )

    frame["LineFit_zenith"] = I3Double( frame["LineFit"].dir.zenith )

    # also possible with CascadeLlhVertexFit_L3Params CascadeLlhVertexFit_L2Params CascadeLlhVertexFit_ICParams
    frame["CascadeLlhVertexFitParams_rlogL"] = I3Double( frame["CscdL3_CascadeLlhVertexFitParams"].ReducedLlh ) 


    frame["cscdSBU_MonopodFit4_noDC_z"] =  I3Double( frame["MonopodFit_iMIGRAD_PPB0"].pos.z )
    frame["cscdSBU_MonopodFit4_noDC_zenith"] =  I3Double( frame["MonopodFit_iMIGRAD_PPB0"].dir.zenith )

    ### all for cscdSBU_VertexRecoDist_CscdLLh
    x1 = frame['CascadeLlhVertexFit_L3'].pos.x
    y1 = frame['CascadeLlhVertexFit_L3'].pos.y
    z1 = frame['CascadeLlhVertexFit_L3'].pos.z
    x2 = frame["TaupedeFit_iMIGRAD_PPB0"].pos.x
    y2 = frame["TaupedeFit_iMIGRAD_PPB0"].pos.y
    z2 = frame["TaupedeFit_iMIGRAD_PPB0"].pos.z
    distance = np.sqrt( (x1-x2)**2 + (y1-y2)**2 + (z1-z2)**2 )
    frame["cscdSBU_VertexRecoDist_CscdLLh"]= I3Double( distance )


    return True


