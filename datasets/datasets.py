


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
### large reco batch
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
### neha spice files
###

neha_spice = {}

neha_spice["NuTau_midE1"] = {
    "dataset" : "22049",
    "subfolders" : 
    ["0000000-0000999"],
    "flavor" : "NuTau",
    "reco_base_path" : "/data/ana/Diffuse/GlobalFit_Flavor/taupede/SnowStorm/RecowithBfr/Baseline",
}

neha_spice["NuTau_highE1"] = {
    "dataset" : "22050",
    "subfolders" : 
    ["0000000-0000999", "0001000-0001999", "0002000-0002999"],
    "flavor" : "NuTau",
    "reco_base_path" : "/data/ana/Diffuse/GlobalFit_Flavor/taupede/SnowStorm/RecowithBfr/Baseline",
}

neha_spice["NuTau_midE2"] = {
    "dataset" : "22085",
    "subfolders" : 
    ["0000000-0000999", "0001000-0001999"],
    "flavor" : "NuTau",
    "reco_base_path" : "/data/ana/Diffuse/GlobalFit_Flavor/taupede/SnowStorm/RecowithBfr/Baseline",
}

neha_spice["NuTau_highE2"] = {
    "dataset" : "22086",
    "subfolders" : 
    ["0000000-0000999", "0001000-0001999", "0002000-0002999","0003000-0003999", "0004000-0004999", "0005000-0005999", "0006000-0006999"],
    "flavor" : "NuTau",
    "reco_base_path" : "/data/ana/Diffuse/GlobalFit_Flavor/taupede/SnowStorm/RecowithBfr/Baseline",
}

neha_spice["NuE_midE1"] = {
    "dataset" : "22046",
    "subfolders" : 
    ["0000000-0000999"],
    "flavor" : "NuE",
    "reco_base_path" : "/data/ana/Diffuse/GlobalFit_Flavor/taupede/SnowStorm/RecowithBfr/Baseline",
}

neha_spice["NuE_highE1"] = {
    "dataset" : "22047",
    "subfolders" : 
    ["0000000-0000999", "0001000-0001999", "0002000-0002999"],
    "flavor" : "NuE",
    "reco_base_path" : "/data/ana/Diffuse/GlobalFit_Flavor/taupede/SnowStorm/RecowithBfr/Baseline",
}

neha_spice["NuE_midE2"] = {
    "dataset" : "22082",
    "subfolders" : 
    ["0000000-0000999", "0001000-0001999"],
    "flavor" : "NuE",
    "reco_base_path" : "/data/ana/Diffuse/GlobalFit_Flavor/taupede/SnowStorm/RecowithBfr/Baseline",
}

neha_spice["NuE_highE2"] = {
    "dataset" : "22083",
    "subfolders" : 
    ["0000000-0000999", "0001000-0001999", "0002000-0002999","0003000-0003999", "0004000-0004999", "0005000-0005999", "0006000-0006999"],
    "flavor" : "NuE",
    "reco_base_path" : "/data/ana/Diffuse/GlobalFit_Flavor/taupede/SnowStorm/RecowithBfr/Baseline",
}

neha_spice["NuMu_midE1"] = {
    "dataset" : "22043",
    "subfolders" : 
    ["0000000-0000999"],
    "flavor" : "NuMu",
    "reco_base_path" : "/data/ana/Diffuse/GlobalFit_Flavor/taupede/SnowStorm/RecowithBfr/Baseline",
}

neha_spice["NuMu_highE1"] = {
    "dataset" : "22044",
    "subfolders" : 
    ["0000000-0000999", "0001000-0001999", "0002000-0002999"],
    "flavor" : "NuMu",
    "reco_base_path" : "/data/ana/Diffuse/GlobalFit_Flavor/taupede/SnowStorm/RecowithBfr/Baseline",
}

neha_spice["NuMu_midE2"] = {
    "dataset" : "22079",
    "subfolders" : 
    ["0000000-0000999", "0001000-0001999"],
    "flavor" : "NuMu",
    "reco_base_path" : "/data/ana/Diffuse/GlobalFit_Flavor/taupede/SnowStorm/RecowithBfr/Baseline",
}

neha_spice["NuMu_highE2"] = {
    "dataset" : "22080",
    "subfolders" : 
    ["0000000-0000999", "0001000-0001999", "0002000-0002999","0003000-0003999", "0004000-0004999", "0005000-0005999"],
    "flavor" : "NuMu",
    "reco_base_path" : "/data/ana/Diffuse/GlobalFit_Flavor/taupede/SnowStorm/RecowithBfr/Baseline",
}



