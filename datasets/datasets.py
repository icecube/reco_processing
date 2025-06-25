
v1_wpid = {}

v1_wpid["NuTau_midE"] = {
    "dataset" : "22634",
    "subfolders" : 
    ["0000000-0000999"],
    "flavor" : "NuTau",
    "reco_base_path" : "/data/user/tvaneede/GlobalFit/reco_processing/pid_neha/output/v1",
}

v1_wpid["NuTau_highE"] = {
    "dataset" : "22635",
    "subfolders" : 
    ["0000000-0000999"],
    "flavor" : "NuTau",
    "reco_base_path" : "/data/user/tvaneede/GlobalFit/reco_processing/pid_neha/output/v1",
}

v1_wpid["NuE_midE"] = {
    "dataset" : "22613",
    "subfolders" : 
    ["0000000-0000999"],
    "flavor" : "NuE",
    "reco_base_path" : "/data/user/tvaneede/GlobalFit/reco_processing/pid_neha/output/v1",
}

v1_wpid["NuE_highE"] = {
    "dataset" : "22612",
    "subfolders" : 
    ["0000000-0000999"],
    "flavor" : "NuE",
    "reco_base_path" : "/data/user/tvaneede/GlobalFit/reco_processing/pid_neha/output/v1",
}

v1_wpid["NuMu_midE"] = {
    "dataset" : "22645",
    "subfolders" : 
    ["0000000-0000999"],
    "flavor" : "NuMu",
    "reco_base_path" : "/data/user/tvaneede/GlobalFit/reco_processing/pid_neha/output/v1",
}

v1_wpid["NuMu_highE"] = {
    "dataset" : "22644",
    "subfolders" : 
    ["0000000-0000999"],
    "flavor" : "NuMu",
    "reco_base_path" : "/data/user/tvaneede/GlobalFit/reco_processing/pid_neha/output/v1",
}




###
### Including bright doms
###

rec_v1_bright = {}

rec_v1_bright["NuTau_midE"] = {
    "dataset" : "22634",
    "subfolders" : 
    ["0000000-0000999"],
    "flavor" : "NuTau",
    "reco_base_path" : "/data/user/celdridg/bright/v1",
}

rec_v1_bright["NuTau_highE"] = {
    "dataset" : "22635",
    "subfolders" : 
    ["0000000-0000999"],
    "flavor" : "NuTau",
    "reco_base_path" : "/data/user/celdridg/bright/v1/",
}

###
### evtgen v0, based on recov1
###

evtgen_v0_rec_v1 = {}

evtgen_v0_rec_v1["NuTau_midE"] = {
    "dataset" : "22634",
    "subfolders" : 
    ["0000000-0000999"],
    "flavor" : "NuTau",
    "reco_base_path" : "/data/user/tvaneede/GlobalFit/reco_processing/evtgen/output/v0",
}

evtgen_v0_rec_v1["NuTau_highE"] = {
    "dataset" : "22635",
    "subfolders" : 
    ["0000000-0000999"],
    "flavor" : "NuTau",
    "reco_base_path" : "/data/user/tvaneede/GlobalFit/reco_processing/evtgen/output/v0",
}

evtgen_v0_rec_v1["NuE_midE"] = {
    "dataset" : "22613",
    "subfolders" : 
    ["0000000-0000999"],
    "flavor" : "NuE",
    "reco_base_path" : "/data/user/tvaneede/GlobalFit/reco_processing/evtgen/output/v0",
}

evtgen_v0_rec_v1["NuE_highE"] = {
    "dataset" : "22612",
    "subfolders" : 
    ["0000000-0000999"],
    "flavor" : "NuE",
    "reco_base_path" : "/data/user/tvaneede/GlobalFit/reco_processing/evtgen/output/v0",
}

###
### Proper HESE selection, added Millipede reco to reco script 
###

v2 = {}

v2["NuTau_midE"] = {
    "dataset" : "22634",
    "subfolders" : 
    ["0000000-0000999"],
    "flavor" : "NuTau",
    "reco_base_out_path" : "/data/user/tvaneede/GlobalFit/reco_processing/output/v2",
    "reco_base_in_path" : "/data/sim/IceCube/2023/filtered/level3/cascade/neutrino-generator",
}

###
### Large batch reconstruction
###

v1 = {}

v1["NuTau_midE"] = {
    "dataset" : "22634",
    "subfolders" : 
    ["0000000-0000999"],
    "flavor" : "NuTau",
    "reco_base_path" : "/data/user/tvaneede/GlobalFit/reco_processing/output/v1",
}

v1["NuTau_highE"] = {
    "dataset" : "22635",
    "subfolders" : 
    ["0000000-0000999"],
    "flavor" : "NuTau",
    "reco_base_path" : "/data/user/tvaneede/GlobalFit/reco_processing/output/v1",
}

v1["NuE_midE"] = {
    "dataset" : "22613",
    "subfolders" : 
    ["0000000-0000999"],
    "flavor" : "NuE",
    "reco_base_path" : "/data/user/tvaneede/GlobalFit/reco_processing/output/v1",
}

v1["NuE_highE"] = {
    "dataset" : "22612",
    "subfolders" : 
    ["0000000-0000999"],
    "flavor" : "NuE",
    "reco_base_path" : "/data/user/tvaneede/GlobalFit/reco_processing/output/v1",
}

v1["NuMu_midE"] = {
    "dataset" : "22645",
    "subfolders" : 
    ["0000000-0000999"],
    "flavor" : "NuMu",
    "reco_base_path" : "/data/user/tvaneede/GlobalFit/reco_processing/output/v1",
}

v1["NuMu_highE"] = {
    "dataset" : "22644",
    "subfolders" : 
    ["0000000-0000999"],
    "flavor" : "NuMu",
    "reco_base_path" : "/data/user/tvaneede/GlobalFit/reco_processing/output/v1",
}

###
### Ftp files
### Selection: l3 muon
### Name: ftp_l3muon
###

ftp_l3muon = {}

ftp_l3muon["NuTau_midE1"] = {
    "dataset" : "22634",
    "subfolders" : 
    ["0000000-0000999"],
    "flavor" : "NuTau",
    "reco_base_path" : "/data/sim/IceCube/2023/filtered/level3/muon/neutrino-generator/",
}

###
### Ftp level2
### Selection: level
### Name: ftp_generated
###

ftp_l2 = {}

ftp_l2["NuTau_midE1"] = {
    "dataset" : "22634",
    "subfolders" : 
    ["0000000-0000999"],
    "flavor" : "NuTau",
    "reco_base_path" : "/data/sim/IceCube/2023/filtered/level2/neutrino-generator",
}


###
### Ftp generated files
### Selection: No selection
### Name: ftp_generated
###

ftp_generated = {}

ftp_generated["NuTau_midE1"] = {
    "dataset" : "22634",
    "subfolders" : 
    ["0000000-0000999"],
    "flavor" : "NuTau",
    "reco_base_path" : "/data/sim/IceCube/2023/generated/neutrino-generator",
}

###
### Ftp files
### Selection: I thought no selection, but I think there is the cascade selection already applied
### Name: ftp_l3casc, previous: ftp
###

ftp_l3casc = {}

ftp_l3casc["NuTau_midE1"] = {
    "dataset" : "22634",
    "subfolders" : 
    ["0000000-0000999"],
    "flavor" : "NuTau",
    "reco_base_path" : "/data/sim/IceCube/2023/filtered/level3/cascade/neutrino-generator/",
}


###
### Spice l3 cascade
### No selection
### Name: spice_generated
###

spice_l3casc = {}

spice_l3casc["NuTau_midE1"] = {
    "dataset" : "22049",
    "subfolders" : 
    ["0000000-0000999"],
    "flavor" : "NuTau",
    "reco_base_path" : "/data/sim/IceCube/2020/filtered/level3/cascade/neutrino-generator",
}


###
### Spice generated files
### No selection
### Name: spice_generated
###

spice_generated = {}

spice_generated["NuTau_midE1"] = {
    "dataset" : "22049",
    "subfolders" : 
    ["0000000-0000999"],
    "flavor" : "NuTau",
    "reco_base_path" : "/data/sim/IceCube/2020/generated/neutrino-generator",
}

###
### Reconstructed files by Neha
### Selection: VHESelfVeto == false, CausalQTot > 6000, no energy cut!!
### Name: spice_tau_reco, before: neha_spice
###

spice_tau_reco = {}

spice_tau_reco["NuTau_midE1"] = {
    "dataset" : "22049",
    "subfolders" : 
    ["0000000-0000999"],
    "flavor" : "NuTau",
    "reco_base_path" : "/data/ana/Diffuse/GlobalFit_Flavor/taupede/SnowStorm/RecowithBfr/Baseline",
}

spice_tau_reco["NuTau_highE1"] = {
    "dataset" : "22050",
    "subfolders" : 
    ["0000000-0000999", "0001000-0001999", "0002000-0002999"],
    "flavor" : "NuTau",
    "reco_base_path" : "/data/ana/Diffuse/GlobalFit_Flavor/taupede/SnowStorm/RecowithBfr/Baseline",
}

spice_tau_reco["NuTau_midE2"] = {
    "dataset" : "22085",
    "subfolders" : 
    ["0000000-0000999", "0001000-0001999"],
    "flavor" : "NuTau",
    "reco_base_path" : "/data/ana/Diffuse/GlobalFit_Flavor/taupede/SnowStorm/RecowithBfr/Baseline",
}

spice_tau_reco["NuTau_highE2"] = {
    "dataset" : "22086",
    "subfolders" : 
    ["0000000-0000999", "0001000-0001999", "0002000-0002999","0003000-0003999", "0004000-0004999", "0005000-0005999", "0006000-0006999"],
    "flavor" : "NuTau",
    "reco_base_path" : "/data/ana/Diffuse/GlobalFit_Flavor/taupede/SnowStorm/RecowithBfr/Baseline",
}

spice_tau_reco["NuE_midE1"] = {
    "dataset" : "22046",
    "subfolders" : 
    ["0000000-0000999"],
    "flavor" : "NuE",
    "reco_base_path" : "/data/ana/Diffuse/GlobalFit_Flavor/taupede/SnowStorm/RecowithBfr/Baseline",
}

spice_tau_reco["NuE_highE1"] = {
    "dataset" : "22047",
    "subfolders" : 
    ["0000000-0000999", "0001000-0001999", "0002000-0002999"],
    "flavor" : "NuE",
    "reco_base_path" : "/data/ana/Diffuse/GlobalFit_Flavor/taupede/SnowStorm/RecowithBfr/Baseline",
}

spice_tau_reco["NuE_midE2"] = {
    "dataset" : "22082",
    "subfolders" : 
    ["0000000-0000999", "0001000-0001999"],
    "flavor" : "NuE",
    "reco_base_path" : "/data/ana/Diffuse/GlobalFit_Flavor/taupede/SnowStorm/RecowithBfr/Baseline",
}

spice_tau_reco["NuE_highE2"] = {
    "dataset" : "22083",
    "subfolders" : 
    ["0000000-0000999", "0001000-0001999", "0002000-0002999","0003000-0003999", "0004000-0004999", "0005000-0005999", "0006000-0006999"],
    "flavor" : "NuE",
    "reco_base_path" : "/data/ana/Diffuse/GlobalFit_Flavor/taupede/SnowStorm/RecowithBfr/Baseline",
}

spice_tau_reco["NuMu_midE1"] = {
    "dataset" : "22043",
    "subfolders" : 
    ["0000000-0000999"],
    "flavor" : "NuMu",
    "reco_base_path" : "/data/ana/Diffuse/GlobalFit_Flavor/taupede/SnowStorm/RecowithBfr/Baseline",
}

spice_tau_reco["NuMu_highE1"] = {
    "dataset" : "22044",
    "subfolders" : 
    ["0000000-0000999", "0001000-0001999", "0002000-0002999"],
    "flavor" : "NuMu",
    "reco_base_path" : "/data/ana/Diffuse/GlobalFit_Flavor/taupede/SnowStorm/RecowithBfr/Baseline",
}

spice_tau_reco["NuMu_midE2"] = {
    "dataset" : "22079",
    "subfolders" : 
    ["0000000-0000999", "0001000-0001999"],
    "flavor" : "NuMu",
    "reco_base_path" : "/data/ana/Diffuse/GlobalFit_Flavor/taupede/SnowStorm/RecowithBfr/Baseline",
}

spice_tau_reco["NuMu_highE2"] = {
    "dataset" : "22080",
    "subfolders" : 
    ["0000000-0000999", "0001000-0001999", "0002000-0002999","0003000-0003999", "0004000-0004999", "0005000-0005999"],
    "flavor" : "NuMu",
    "reco_base_path" : "/data/ana/Diffuse/GlobalFit_Flavor/taupede/SnowStorm/RecowithBfr/Baseline",
}



