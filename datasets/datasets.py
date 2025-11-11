
###
### muongun spice v3.2.1
###

muongun = {}

muongun["MuonGun_lowlowlowE"] = { # 700 GeV - 1 TeV
    "dataset" : "21319",
    "subfolders" : [f"{i:07d}-{i+999:07d}" for i in range(0, 100000, 1000)],
    "flavor" : "MuonGun",
    "level2_path" : "/data/sim/IceCube/2016/filtered/level2/MuonGun",
    "cascade_finallevel_path" : "/data/ana/analyses/diffuse/cascades/pass2/sim/mgun/finallevel/",
    "cascade_reco_path" : "/data/user/tvaneede/GlobalFit/reco_processing/muons/cascade/output",
    "hese_filter_path" : "/data/user/tvaneede/GlobalFit/reco_processing/muons/hese/filter/output/v1/",
    "hese_reco_path" : "/data/user/tvaneede/GlobalFit/reco_processing/muons/hese/output/"
}

muongun["MuonGun_lowlowE"] = { # 1 TeV - 5 TeV
    "dataset" : "21318",
    "subfolders" : [f"{i:07d}-{i+999:07d}" for i in range(0, 100000, 1000)],
    "flavor" : "MuonGun",
    "level2_path" : "/data/sim/IceCube/2016/filtered/level2/MuonGun",
    "cascade_finallevel_path" : "/data/ana/analyses/diffuse/cascades/pass2/sim/mgun/finallevel/",
    "cascade_reco_path" : "/data/user/tvaneede/GlobalFit/reco_processing/muons/cascade/output",
    "hese_filter_path" : "/data/user/tvaneede/GlobalFit/reco_processing/muons/hese/filter/output/v1/",
    "hese_reco_path" : "/data/user/tvaneede/GlobalFit/reco_processing/muons/hese/output/"
}

muongun["MuonGun_lowE"] = { # 5 TeV - 10 TeV
    "dataset" : "21317",
    "subfolders" : [f"{i:07d}-{i+999:07d}" for i in range(0, 20000, 1000)],
    "flavor" : "MuonGun",
    "level2_path" : "/data/sim/IceCube/2016/filtered/level2/MuonGun",
    "cascade_finallevel_path" : "/data/ana/analyses/diffuse/cascades/pass2/sim/mgun/finallevel/",
    "cascade_reco_path" : "/data/user/tvaneede/GlobalFit/reco_processing/muons/cascade/output",
    "hese_filter_path" : "/data/user/tvaneede/GlobalFit/reco_processing/muons/hese/filter/output/v1/",
    "hese_reco_path" : "/data/user/tvaneede/GlobalFit/reco_processing/muons/hese/output/"
}

muongun["MuonGun_midE"] = { # 10 TeV - 100 TeV
    "dataset" : "21316",
    "subfolders" : [f"{i:07d}-{i+999:07d}" for i in range(0, 40000, 1000)],
    "flavor" : "MuonGun",
    "level2_path" : "/data/sim/IceCube/2016/filtered/level2/MuonGun",
    "cascade_finallevel_path" : "/data/ana/analyses/diffuse/cascades/pass2/sim/mgun/finallevel/",
    "cascade_reco_path" : "/data/user/tvaneede/GlobalFit/reco_processing/muons/cascade/output",
    "hese_filter_path" : "/data/user/tvaneede/GlobalFit/reco_processing/muons/hese/filter/output/v1/",
    "hese_reco_path" : "/data/user/tvaneede/GlobalFit/reco_processing/muons/hese/output/"
}

muongun["MuonGun_highE"] = { # 100 TeV - 1 EeV
    "dataset" : "21315",
    "subfolders" : [f"{i:07d}-{i+999:07d}" for i in range(0, 15000, 1000)],
    "flavor" : "MuonGun",
    "level2_path" : "/data/sim/IceCube/2016/filtered/level2/MuonGun",
    "cascade_finallevel_path" : "/data/ana/analyses/diffuse/cascades/pass2/sim/mgun/finallevel/",
    "cascade_reco_path" : "/data/user/tvaneede/GlobalFit/reco_processing/muons/cascade/output",
    "hese_filter_path" : "/data/user/tvaneede/GlobalFit/reco_processing/muons/hese/filter/output/v1/",
    "hese_reco_path" : "/data/user/tvaneede/GlobalFit/reco_processing/muons/hese/output/"
}



###
### test crystal density 2
###
test_crystal_density_low_2 = {}

test_crystal_density_low_2["NuTau_midE"] = {
    "dataset" : "23501",
    "subfolders" : 
    ["0000000-0000999"],
    "flavor" : "NuTau",
    "year" : "2023",
    "nfiles" : 20,
    # "levels" : ["level2","level3_cascade", "level3_muon"]
    "levels" : ["HESE"]
}

test_crystal_density_low_2["NuTau_highE"] = {
    "dataset" : "23500",
    "subfolders" : 
    ["0000000-0000999"],
    "flavor" : "NuTau",
    "year" : "2023",
    "nfiles" : 20,
    # "levels" : ["level2","level3_cascade", "level3_muon"]
    "levels" : ["HESE"]
}

test_crystal_density_high_2 = {}

test_crystal_density_high_2["NuTau_midE"] = {
    "dataset" : "23499",
    "subfolders" : 
    ["0000000-0000999"],
    "flavor" : "NuTau",
    "year" : "2023",
    "nfiles" : 20,
    # "levels" : ["level2","level3_cascade", "level3_muon"]
    "levels" : ["HESE"]
}

test_crystal_density_high_2["NuTau_highE"] = {
    "dataset" : "23498",
    "subfolders" : 
    ["0000000-0000999"],
    "flavor" : "NuTau",
    "year" : "2023",
    "nfiles" : 20,
    # "levels" : ["level2","level3_cascade", "level3_muon"]
    "levels" : ["HESE"]
}


###
### testing crystal density
###


test_crystal_density_low = {}

test_crystal_density_low["NuTau_midE"] = {
    "dataset" : "23492",
    "subfolders" : 
    ["0000000-0000999"],
    "flavor" : "NuTau",
    "year" : "2023",
    "nfiles" : 10,
    # "levels" : ["level2","level3_cascade", "level3_muon","HESE"]
    "levels" : ["level3_muon"]
}

test_crystal_density_low["NuTau_highE"] = {
    "dataset" : "23493",
    "subfolders" : 
    ["0000000-0000999"],
    "flavor" : "NuTau",
    "year" : "2023",
    "nfiles" : 10,
    # "levels" : ["level2","level3_cascade", "level3_muon","HESE"]
    "levels" : ["level3_muon"]
}

test_crystal_density_high = {}

test_crystal_density_high["NuTau_midE"] = {
    "dataset" : "23494",
    "subfolders" : 
    ["0000000-0000999"],
    "flavor" : "NuTau",
    "year" : "2023",
    "nfiles" : 10,
    # "levels" : ["level2","level3_cascade", "level3_muon","HESE"]
    "levels" : ["level3_muon"]
}

test_crystal_density_high["NuTau_highE"] = {
    "dataset" : "23495",
    "subfolders" : 
    ["0000000-0000999"],
    "flavor" : "NuTau",
    "year" : "2023",
    "nfiles" : 10,
    # "levels" : ["level2","level3_cascade", "level3_muon","HESE"]
    "levels" : ["level3_muon"]
}

###
### checking my iceprod datasets
###


snowstorm_iceprod_benchmark = {}

snowstorm_iceprod_benchmark["NuTau_lowE"] = {
    "dataset" : "23458",
    "subfolders" : 
    ["0000000-0000999"],
    "flavor" : "NuTau",
    "year" : "2023",
    "nfiles" : 10,
    "levels" : ["level2","level3_cascade", "level3_muon","level8_cascade"]
}

snowstorm_iceprod_benchmark["NuTau_midE"] = {
    "dataset" : "23459",
    "subfolders" : 
    ["0000000-0000999"],
    "flavor" : "NuTau",
    "year" : "2023",
    "nfiles" : 10,
    "levels" : ["level2","level3_cascade", "level3_muon","level8_cascade","HESE_evtgen"]
}

snowstorm_iceprod_benchmark["NuTau_highE"] = {
    "dataset" : "23460",
    "subfolders" : 
    ["0000000-0000999"],
    "flavor" : "NuTau",
    "year" : "2023",
    "nfiles" : 10,
    "levels" : ["level2","level3_cascade", "level3_muon","level8_cascade","HESE_evtgen"]
}

snowstorm_iceprod_benchmark["NuE_lowE"] = {
    "dataset" : "23455",
    "subfolders" : 
    ["0000000-0000999"],
    "flavor" : "NuE",
    "year" : "2023",
    "nfiles" : 10,
    "levels" : ["level2","level3_cascade", "level3_muon","level8_cascade"]
}

snowstorm_iceprod_benchmark["NuE_midE"] = {
    "dataset" : "23456",
    "subfolders" : 
    ["0000000-0000999"],
    "flavor" : "NuE",
    "year" : "2023",
    "nfiles" : 10,
    "levels" : ["level2","level3_cascade", "level3_muon","level8_cascade","HESE_evtgen"]    
}

snowstorm_iceprod_benchmark["NuE_highE"] = {
    "dataset" : "23457",
    "subfolders" : 
    ["0000000-0000999"],
    "flavor" : "NuE",
    "year" : "2023",
    "nfiles" : 10,
    "levels" : ["level2","level3_cascade", "level3_muon","level8_cascade","HESE_evtgen"]    
}

snowstorm_iceprod_benchmark["NuMu_lowlowE"] = {
    "dataset" : "23451",
    "subfolders" : 
    ["0000000-0000999"],
    "flavor" : "NuMu",
    "year" : "2023",
    "nfiles" : 10,
    "levels" : ["level2","level3_cascade", "level3_muon","level8_cascade"]    
}

snowstorm_iceprod_benchmark["NuMu_lowE"] = {
    "dataset" : "23452",
    "subfolders" : 
    ["0000000-0000999"],
    "flavor" : "NuMu",
    "year" : "2023",
    "nfiles" : 10,
    "levels" : ["level2","level3_cascade", "level3_muon","level8_cascade"]    
}

snowstorm_iceprod_benchmark["NuMu_midE"] = {
    "dataset" : "23453",
    "subfolders" : 
    ["0000000-0000999"],
    "flavor" : "NuMu",
    "year" : "2023",
    "nfiles" : 10,
    "levels" : ["level2","level3_cascade", "level3_muon","level8_cascade","HESE_evtgen"]
}

snowstorm_iceprod_benchmark["NuMu_highE"] = {
    "dataset" : "23454",
    "subfolders" : 
    ["0000000-0000999"],
    "flavor" : "NuMu",
    "year" : "2023",
    "nfiles" : 10,
    "levels" : ["level2","level3_cascade", "level3_muon","level8_cascade","HESE_evtgen"]
}

###

taureco_iceprod_benchmark = {}

taureco_iceprod_benchmark["NuTau_lowE"] = {
    "dataset" : "22633",
    "subfolders" : 
    ["0000000-0000999"],
    "flavor" : "NuTau",
    "year" : "2023",
    "nfiles" : 10,
    # "levels" : ["level6_cascade", "level7_cascade", "level8_cascade"]
    "levels" : ["level7_cascade", "level8_cascade"]
}

taureco_iceprod_benchmark["NuTau_midE"] = {
    "dataset" : "22634",
    "subfolders" : 
    ["0000000-0000999"],
    "flavor" : "NuTau",
    "year" : "2023",
    "nfiles" : 10,
    # "levels" : ["level2", "HESE_taupede","HESE_evtgen","level6_cascade","level7_cascade", "level8_cascade"]
    "levels" : ["HESE_taupede","HESE_evtgen","level7_cascade", "level8_cascade"]
}

taureco_iceprod_benchmark["NuTau_highE"] = {
    "dataset" : "22635",
    "subfolders" : 
    ["0000000-0000999"],
    "flavor" : "NuTau",
    "year" : "2023",
    "nfiles" : 10,
    # "levels" : ["level2", "HESE_taupede","HESE_evtgen","level6_cascade","level7_cascade", "level8_cascade"]
    "levels" : ["HESE_taupede","HESE_evtgen","level7_cascade", "level8_cascade"]
}

taureco_iceprod_benchmark["NuE_lowE"] = {
    "dataset" : "22614",
    "subfolders" : 
    ["0000000-0000999"],
    "flavor" : "NuE",
    "year" : "2023",
    "nfiles" : 10,
    # "levels" : ["level6_cascade", "level7_cascade", "level8_cascade"]
    "levels" : ["level7_cascade", "level8_cascade"]
}

taureco_iceprod_benchmark["NuE_midE"] = {
    "dataset" : "22613",
    "subfolders" : 
    ["0000000-0000999"],
    "flavor" : "NuE",
    "year" : "2023",
    "nfiles" : 10,
    # "levels" : ["level2", "HESE_taupede","HESE_evtgen","level6_cascade","level7_cascade", "level8_cascade"]
    "levels" : ["HESE_taupede","HESE_evtgen","level7_cascade", "level8_cascade"]
}

taureco_iceprod_benchmark["NuE_highE"] = {
    "dataset" : "22612",
    "subfolders" : 
    ["0000000-0000999"],
    "flavor" : "NuE",
    "year" : "2023",
    "nfiles" : 10,
    # "levels" : ["level2", "HESE_taupede","HESE_evtgen","level6_cascade","level7_cascade", "level8_cascade"]
    "levels" : ["HESE_taupede","HESE_evtgen","level7_cascade", "level8_cascade"]
}

taureco_iceprod_benchmark["NuMu_lowE"] = {
    "dataset" : "22646",
    "subfolders" : 
    ["0000000-0000999"],
    "flavor" : "NuMu",
    "year" : "2023",
    "nfiles" : 10,
    # "levels" : ["level6_cascade", "level7_cascade", "level8_cascade"]
    "levels" : ["level7_cascade", "level8_cascade"]
}

taureco_iceprod_benchmark["NuMu_midE"] = {
    "dataset" : "22645",
    "subfolders" : 
    ["0000000-0000999"],
    "flavor" : "NuMu",
    "year" : "2023",
    "nfiles" : 10,
    # "levels" : ["level2", "HESE_taupede","HESE_evtgen","level6_cascade","level7_cascade", "level8_cascade"]
    "levels" : ["HESE_taupede","HESE_evtgen","level7_cascade", "level8_cascade"]
}

taureco_iceprod_benchmark["NuMu_highE"] = {
    "dataset" : "22644",
    "subfolders" : 
    ["0000000-0000999"],
    "flavor" : "NuMu",
    "year" : "2023",
    "nfiles" : 10,
    # "levels" : ["level2", "HESE_taupede","HESE_evtgen","level6_cascade","level7_cascade", "level8_cascade"]
    "levels" : ["HESE_taupede","HESE_evtgen","level7_cascade", "level8_cascade"]
}

###
###
###


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
### evtgen v2, based on reco v5
###

evtgen_v4_rec_v9 = {}

evtgen_v4_rec_v9["NuTau_midE"] = {
    "dataset" : "22634",
    "subfolders" : 
    ["0000000-0000999","0001000-0001999"], # 1000 + 1000
    "flavor" : "NuTau",
    "reco_base_out_path" : "/data/user/tvaneede/GlobalFit/reco_processing/evtgen/output/v4",
    "hdf_file_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/evtgen_v4_rec_v9/NuTau_22634.h5",
    "hdf_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/evtgen_v4_rec_v9",
    "nfiles" : 2000,
}

evtgen_v4_rec_v9["NuTau_highE"] = {
    "dataset" : "22635",
    "subfolders" : 
    ["0000000-0000999","0001000-0001999"], # 1000 + 1000
    "flavor" : "NuTau",
    "reco_base_out_path" : "/data/user/tvaneede/GlobalFit/reco_processing/evtgen/output/v4",
    "hdf_file_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/evtgen_v4_rec_v9/NuTau_22635.h5",
    "hdf_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/evtgen_v4_rec_v9",
    "nfiles" : 2000,
}

evtgen_v4_rec_v9["NuE_midE"] = {
    "dataset" : "22613",
    "subfolders" : 
    ["0000000-0000999","0001000-0001999"], # 1000 + 1000
    "flavor" : "NuE",
    "reco_base_out_path" : "/data/user/tvaneede/GlobalFit/reco_processing/evtgen/output/v4",
    "hdf_file_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/evtgen_v4_rec_v9/NuE_22613.h5",
    "hdf_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/evtgen_v4_rec_v9",
    "nfiles" : 1997,
}

evtgen_v4_rec_v9["NuE_highE"] = {
    "dataset" : "22612",
    "subfolders" : 
    ["0000000-0000999","0001000-0001999"], # 1000 + 1000
    "flavor" : "NuE",
    "reco_base_out_path" : "/data/user/tvaneede/GlobalFit/reco_processing/evtgen/output/v4",
    "hdf_file_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/evtgen_v4_rec_v9/NuE_22612.h5",
    "hdf_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/evtgen_v4_rec_v9",
    "nfiles" : 2000,
}

evtgen_v4_rec_v9["NuMu_midE"] = {
    "dataset" : "22645",
    "subfolders" : 
    ["0000000-0000999","0001000-0001999"], # 1000 + 1000
    "flavor" : "NuMu",
    "reco_base_out_path" : "/data/user/tvaneede/GlobalFit/reco_processing/evtgen/output/v4",
    "hdf_file_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/evtgen_v4_rec_v9/NuMu_22645.h5",
    "hdf_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/evtgen_v4_rec_v9",
    "nfiles" : 2000,
}

evtgen_v4_rec_v9["NuMu_highE"] = {
    "dataset" : "22644",
    "subfolders" : 
    ["0000000-0000999","0001000-0001999"], # 1000 + 1000
    "flavor" : "NuMu",
    "reco_base_out_path" : "/data/user/tvaneede/GlobalFit/reco_processing/evtgen/output/v4",
    "hdf_file_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/evtgen_v4_rec_v9/NuMu_22644.h5",
    "hdf_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/evtgen_v4_rec_v9",
    "nfiles" : 2000,
}

###
### evtgen v2, based on reco v5
###

evtgen_v3_rec_v5 = {}

evtgen_v3_rec_v5["NuTau_midE"] = {
    "dataset" : "22634",
    "subfolders" : 
    ["0000000-0000999"],
    "flavor" : "NuTau",
    "reco_base_out_path" : "/data/user/tvaneede/GlobalFit/reco_processing/evtgen/output/v3",
    "hdf_file_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/evtgen_v3_rec_v5/NuTau_22634.h5",
    "hdf_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/evtgen_v3_rec_v5",
    "nfiles" : 2000,
}

evtgen_v3_rec_v5["NuTau_highE"] = {
    "dataset" : "22635",
    "subfolders" : 
    ["0000000-0000999"], # 1000 + 1000
    "flavor" : "NuTau",
    "reco_base_out_path" : "/data/user/tvaneede/GlobalFit/reco_processing/evtgen/output/v3",
    "hdf_file_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/evtgen_v3_rec_v5/NuTau_22635.h5",
    "hdf_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/evtgen_v3_rec_v5",
    "nfiles" : 201,
}

evtgen_v3_rec_v5["NuE_midE"] = {
    "dataset" : "22613",
    "subfolders" : 
    ["0000000-0000999"],
    "flavor" : "NuE",
    "reco_base_out_path" : "/data/user/tvaneede/GlobalFit/reco_processing/evtgen/output/v3",
    "hdf_file_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/evtgen_v3_rec_v5/NuE_22613.h5",
    "hdf_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/evtgen_v3_rec_v5",
    "nfiles" : 200,
}

evtgen_v3_rec_v5["NuE_highE"] = {
    "dataset" : "22612",
    "subfolders" : 
    ["0000000-0000999"], 
    "flavor" : "NuE",
    "reco_base_out_path" : "/data/user/tvaneede/GlobalFit/reco_processing/evtgen/output/v3",
    "hdf_file_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/evtgen_v3_rec_v5/NuE_22612.h5",
    "hdf_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/evtgen_v3_rec_v5",
    "nfiles" : 200,
}

evtgen_v3_rec_v5["NuMu_midE"] = {
    "dataset" : "22645",
    "subfolders" : 
    ["0000000-0000999"],
    "flavor" : "NuMu",
    "reco_base_out_path" : "/data/user/tvaneede/GlobalFit/reco_processing/evtgen/output/v3",
    "hdf_file_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/evtgen_v3_rec_v5/NuMu_22645.h5",
    "hdf_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/evtgen_v3_rec_v5",
    "nfiles" : 200,
}

evtgen_v3_rec_v5["NuMu_highE"] = {
    "dataset" : "22644",
    "subfolders" : 
    ["0000000-0000999"], 
    "flavor" : "NuMu",
    "reco_base_out_path" : "/data/user/tvaneede/GlobalFit/reco_processing/evtgen/output/v3",
    "hdf_file_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/evtgen_v3_rec_v5/NuMu_22644.h5",
    "hdf_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/evtgen_v3_rec_v5",
    "nfiles" : 200,
}

###
### evtgen v2, based on reco v5
###

evtgen_v2_rec_v5 = {}

evtgen_v2_rec_v5["NuTau_midE"] = {
    "dataset" : "22634",
    "subfolders" : 
    ["0000000-0000999","0001000-0001999"], # 1000 + 1000
    "flavor" : "NuTau",
    "reco_base_out_path" : "/data/user/tvaneede/GlobalFit/reco_processing/evtgen/output/v2",
    "hdf_file_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/evtgen_v2_rec_v5/NuTau_22634.h5",
    "hdf_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/evtgen_v2_rec_v5",
    "nfiles" : 2000,
}

evtgen_v2_rec_v5["NuTau_highE"] = {
    "dataset" : "22635",
    "subfolders" : 
    ["0000000-0000999","0001000-0001999"], # 1000 + 1000
    "flavor" : "NuTau",
    "reco_base_out_path" : "/data/user/tvaneede/GlobalFit/reco_processing/evtgen/output/v2",
    "hdf_file_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/evtgen_v2_rec_v5/NuTau_22635.h5",
    "hdf_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/evtgen_v2_rec_v5",
    "nfiles" : 2000,
}

evtgen_v2_rec_v5["NuE_midE"] = {
    "dataset" : "22613",
    "subfolders" : 
    ["0000000-0000999","0001000-0001999"], # 1000 + 997
    "flavor" : "NuE",
    "reco_base_out_path" : "/data/user/tvaneede/GlobalFit/reco_processing/evtgen/output/v2",
    "hdf_file_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/evtgen_v2_rec_v5/NuE_22613.h5",
    "hdf_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/evtgen_v2_rec_v5",
    "nfiles" : 1997,
}

evtgen_v2_rec_v5["NuE_highE"] = {
    "dataset" : "22612",
    "subfolders" : 
    ["0000000-0000999","0001000-0001999"], # 1000 + 1000
    "flavor" : "NuE",
    "reco_base_out_path" : "/data/user/tvaneede/GlobalFit/reco_processing/evtgen/output/v2",
    "hdf_file_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/evtgen_v2_rec_v5/NuE_22612.h5",
    "hdf_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/evtgen_v2_rec_v5",
    "nfiles" : 2000,
}

evtgen_v2_rec_v5["NuMu_midE"] = {
    "dataset" : "22645",
    "subfolders" : 
    ["0000000-0000999","0001000-0001999"], # 1000 + 1000
    "flavor" : "NuMu",
    "reco_base_out_path" : "/data/user/tvaneede/GlobalFit/reco_processing/evtgen/output/v2",
    "hdf_file_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/evtgen_v2_rec_v5/NuMu_22645.h5",
    "hdf_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/evtgen_v2_rec_v5",
    "nfiles" : 2000,
}

evtgen_v2_rec_v5["NuMu_highE"] = {
    "dataset" : "22644",
    "subfolders" : 
    ["0000000-0000999","0001000-0001999"], # 1000 + 1000
    "flavor" : "NuMu",
    "reco_base_out_path" : "/data/user/tvaneede/GlobalFit/reco_processing/evtgen/output/v2",
    "hdf_file_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/evtgen_v2_rec_v5/NuMu_22644.h5",
    "hdf_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/evtgen_v2_rec_v5",
    "nfiles" : 2000,
}

###
### evtgen v1, based on reco v2
###

evtgen_v1_rec_v2 = {}

evtgen_v1_rec_v2["NuTau_midE"] = {
    "dataset" : "22634",
    "subfolders" : 
    ["0000000-0000999","0001000-0001999"], # 1000 + 1000
    "flavor" : "NuTau",
    "reco_base_out_path" : "/data/user/tvaneede/GlobalFit/reco_processing/evtgen/output/v1",
    "hdf_file_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/evtgen_v1_rec_v2/NuTau_22634.h5",
    "hdf_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/evtgen_v1_rec_v2",
    "nfiles" : 2000,
}

evtgen_v1_rec_v2["NuTau_highE"] = {
    "dataset" : "22635",
    "subfolders" : 
    ["0000000-0000999","0001000-0001999"], # 1000 + 1000
    "flavor" : "NuTau",
    "reco_base_out_path" : "/data/user/tvaneede/GlobalFit/reco_processing/evtgen/output/v1",
    "hdf_file_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/evtgen_v1_rec_v2/NuTau_22635.h5",
    "hdf_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/evtgen_v1_rec_v2",
    "nfiles" : 2000,
}

evtgen_v1_rec_v2["NuE_midE"] = {
    "dataset" : "22613",
    "subfolders" : 
    ["0000000-0000999","0001000-0001999"], # 1000 + 997
    "flavor" : "NuE",
    "reco_base_out_path" : "/data/user/tvaneede/GlobalFit/reco_processing/evtgen/output/v1",
    "hdf_file_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/evtgen_v1_rec_v2/NuE_22613.h5",
    "hdf_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/evtgen_v1_rec_v2",
    "nfiles" : 1997,
}

evtgen_v1_rec_v2["NuE_highE"] = {
    "dataset" : "22612",
    "subfolders" : 
    ["0000000-0000999","0001000-0001999"], # 1000 + 1000
    "flavor" : "NuE",
    "reco_base_out_path" : "/data/user/tvaneede/GlobalFit/reco_processing/evtgen/output/v1",
    "hdf_file_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/evtgen_v1_rec_v2/NuE_22612.h5",
    "hdf_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/evtgen_v1_rec_v2",
    "nfiles" : 2000,
}

evtgen_v1_rec_v2["NuMu_midE"] = {
    "dataset" : "22645",
    "subfolders" : 
    ["0000000-0000999","0001000-0001999"], # 1000 + 1000
    "flavor" : "NuMu",
    "reco_base_out_path" : "/data/user/tvaneede/GlobalFit/reco_processing/evtgen/output/v1",
    "hdf_file_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/evtgen_v1_rec_v2/NuMu_22645.h5",
    "hdf_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/evtgen_v1_rec_v2",
    "nfiles" : 2000,
}

evtgen_v1_rec_v2["NuMu_highE"] = {
    "dataset" : "22644",
    "subfolders" : 
    ["0000000-0000999","0001000-0001999"], # 1000 + 1000
    "flavor" : "NuMu",
    "reco_base_out_path" : "/data/user/tvaneede/GlobalFit/reco_processing/evtgen/output/v1",
    "hdf_file_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/evtgen_v1_rec_v2/NuMu_22644.h5",
    "hdf_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/evtgen_v1_rec_v2",
    "nfiles" : 2000,
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
### v10, check new gcd
###
v10 = {}

v10["NuTau_midE"] = {
    "dataset" : "22634",
    "subfolders" : 
    ["0000000-0000999"],
    "flavor" : "NuTau",
    "reco_base_out_path" : "/data/user/tvaneede/GlobalFit/reco_processing/output/v10",
    "reco_base_in_path" : "/data/sim/IceCube/2023/filtered/level2/neutrino-generator",
    "hdf_file_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/v10/NuTau_22634.h5",
    "hdf_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/v10",
    "nfiles" : 200,
}

v10["NuTau_highE"] = {
    "dataset" : "22635",
    "subfolders" : 
    ["0000000-0000999"],
    "flavor" : "NuTau",
    "reco_base_out_path" : "/data/user/tvaneede/GlobalFit/reco_processing/output/v10",
    "reco_base_in_path" : "/data/sim/IceCube/2023/filtered/level2/neutrino-generator",
    "hdf_file_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/v10/NuTau_22635.h5",
    "hdf_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/v10",
    "nfiles" : 200,
}

###
### v9, cleaned up from v8, larger dataset
###
v9 = {}

v9["NuTau_midE"] = {
    "dataset" : "22634",
    "subfolders" : 
    # ["0000000-0000999","0001000-0001999"], # 1000 + 1000
    ["0000000-0000999"], # 1000 + 1000
    # ["0001000-0001999"], # 1000 + 1000
    "flavor" : "NuTau",
    "reco_base_out_path" : "/data/user/tvaneede/GlobalFit/reco_processing/output/v9",
    "reco_base_in_path" : "/data/sim/IceCube/2023/filtered/level2/neutrino-generator",
    "hdf_file_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/v9/NuTau_22634.h5",
    "hdf_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/v9",
    "nfiles" : 200,
}

v9["NuTau_highE"] = {
    "dataset" : "22635",
    "subfolders" : 
    # ["0000000-0000999","0001000-0001999"], # 1000 + 1000
    ["0000000-0000999"], # 1000 + 1000
    # ["0001000-0001999"], # 1000 + 1000
    "flavor" : "NuTau",
    "reco_base_out_path" : "/data/user/tvaneede/GlobalFit/reco_processing/output/v9",
    "reco_base_in_path" : "/data/sim/IceCube/2023/filtered/level2/neutrino-generator",
    "hdf_file_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/v9/NuTau_22635.h5",
    "hdf_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/v9",
    "nfiles" : 200,
}

v9["NuE_midE"] = {
    "dataset" : "22613",
    "subfolders" : 
    # ["0000000-0000999","0001000-0001999"], # 1000 + 1000
    ["0000000-0000999"], # 1000 + 1000
    # ["0001000-0001999"], # 1000 + 1000
    "flavor" : "NuE",
    "reco_base_out_path" : "/data/user/tvaneede/GlobalFit/reco_processing/output/v9",
    "reco_base_in_path" : "/data/sim/IceCube/2023/filtered/level2/neutrino-generator",
    "hdf_file_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/v9/NuE_22613.h5",
    "hdf_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/v9",
    "nfiles" : 200,
}

v9["NuE_highE"] = {
    "dataset" : "22612",
    "subfolders" : 
    # ["0000000-0000999","0001000-0001999"], # 1000 + 1000
    ["0000000-0000999"], # 1000 + 1000
    # ["0001000-0001999"], # 1000 + 1000
    "flavor" : "NuE",
    "reco_base_out_path" : "/data/user/tvaneede/GlobalFit/reco_processing/output/v9",
    "reco_base_in_path" : "/data/sim/IceCube/2023/filtered/level2/neutrino-generator",
    "hdf_file_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/v9/NuE_22612.h5",
    "hdf_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/v9",
    "nfiles" : 200,
}

v9["NuMu_midE"] = {
    "dataset" : "22645",
    "subfolders" : 
    # ["0000000-0000999","0001000-0001999"], # 1000 + 1000
    ["0000000-0000999"], # 1000 + 1000
    # ["0001000-0001999"], # 1000 + 1000
    "flavor" : "NuMu",
    "reco_base_out_path" : "/data/user/tvaneede/GlobalFit/reco_processing/output/v9",
    "reco_base_in_path" : "/data/sim/IceCube/2023/filtered/level2/neutrino-generator",
    "hdf_file_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/v9/NuMu_22645.h5",
    "hdf_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/v9",
    "nfiles" : 200,
}

v9["NuMu_highE"] = {
    "dataset" : "22644",
    "subfolders" : 
    # ["0000000-0000999","0001000-0001999"], # 1000 + 1000
    ["0000000-0000999"], # 1000 + 1000
    # ["0001000-0001999"], # 1000 + 1000
    "flavor" : "NuMu",
    "reco_base_out_path" : "/data/user/tvaneede/GlobalFit/reco_processing/output/v9",
    "reco_base_in_path" : "/data/sim/IceCube/2023/filtered/level2/neutrino-generator",
    "hdf_file_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/v9/NuMu_22644.h5",
    "hdf_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/v9",
    "nfiles" : 200,
}

###
### v8 I think that the problem is fixed, let's create a larger dataset
###

v8 = {}

v8["NuTau_highE"] = {
    "dataset" : "22635",
    "subfolders" : 
    ["0000000-0000999"],
    "flavor" : "NuTau",
    "reco_base_out_path" : "/data/user/tvaneede/GlobalFit/reco_processing/output/v8",
    "reco_base_in_path" : "/data/sim/IceCube/2023/filtered/level2/neutrino-generator",
    "hdf_file_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/v8/NuTau_22635.h5",
    "hdf_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/v8",
    "nfiles" : 200,
}

###
### v7, trying to fix the Millipedefit
###
v7 = {}

v7["NuTau_midE"] = {
    "dataset" : "22634",
    "subfolders" : 
    ["0000000-0000999"],
    "flavor" : "NuTau",
    "reco_base_out_path" : "/data/user/tvaneede/GlobalFit/reco_processing/output/v7",
    "reco_base_in_path" : "/data/sim/IceCube/2023/filtered/level2/neutrino-generator",
    "hdf_file_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/v7/NuTau_22634.h5",
    "hdf_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/v7",
    "nfiles" : 200,
}

v7["NuTau_highE"] = {
    "dataset" : "22635",
    "subfolders" : 
    ["0000000-0000999"],
    "flavor" : "NuTau",
    "reco_base_out_path" : "/data/user/tvaneede/GlobalFit/reco_processing/output/v7",
    "reco_base_in_path" : "/data/sim/IceCube/2023/filtered/level2/neutrino-generator",
    "hdf_file_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/v7/NuTau_22635.h5",
    "hdf_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/v7",
    "nfiles" : 200,
}

###
### v6, trying to fix the Millipedefit
###
v6 = {}

v6["NuTau_midE"] = {
    "dataset" : "22634",
    "subfolders" : 
    ["0000000-0000999"], # 1000 + 1000
    "flavor" : "NuTau",
    "reco_base_out_path" : "/data/user/tvaneede/GlobalFit/reco_processing/output/v6",
    "reco_base_in_path" : "/data/sim/IceCube/2023/filtered/level2/neutrino-generator",
    "hdf_file_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/v6/NuTau_22634.h5",
    "hdf_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/v6",
    "nfiles" : 200,
}

v6["NuTau_highE"] = {
    "dataset" : "22635",
    "subfolders" : 
    ["0000000-0000999"], # 1000 + 1000
    "flavor" : "NuTau",
    "reco_base_out_path" : "/data/user/tvaneede/GlobalFit/reco_processing/output/v6",
    "reco_base_in_path" : "/data/sim/IceCube/2023/filtered/level2/neutrino-generator",
    "hdf_file_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/v6/NuTau_22635.h5",
    "hdf_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/v6",
    "nfiles" : 200,
}

v6["NuE_midE"] = {
    "dataset" : "22613",
    "subfolders" : 
    ["0000000-0000999"], # 1000 + 997
    "flavor" : "NuE",
    "reco_base_out_path" : "/data/user/tvaneede/GlobalFit/reco_processing/output/v6",
    "reco_base_in_path" : "/data/sim/IceCube/2023/filtered/level2/neutrino-generator",
    "hdf_file_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/v6/NuE_22613.h5",
    "hdf_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/v6",
    "nfiles" : 200,
}

v6["NuE_highE"] = {
    "dataset" : "22612",
    "subfolders" : 
    ["0000000-0000999"], # 1000 + 1000
    "flavor" : "NuE",
    "reco_base_out_path" : "/data/user/tvaneede/GlobalFit/reco_processing/output/v6",
    "reco_base_in_path" : "/data/sim/IceCube/2023/filtered/level2/neutrino-generator",
    "hdf_file_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/v6/NuE_22612.h5",
    "hdf_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/v6",
    "nfiles" : 200,
}

v6["NuMu_midE"] = {
    "dataset" : "22645",
    "subfolders" : 
    ["0000000-0000999"], # 1000 + 1000
    "flavor" : "NuMu",
    "reco_base_out_path" : "/data/user/tvaneede/GlobalFit/reco_processing/output/v6",
    "reco_base_in_path" : "/data/sim/IceCube/2023/filtered/level2/neutrino-generator",
    "hdf_file_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/v6/NuMu_22645.h5",
    "hdf_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/v6",
    "nfiles" : 200,
}

v6["NuMu_highE"] = {
    "dataset" : "22644",
    "subfolders" : 
    ["0000000-0000999"], # 1000 + 1000
    "flavor" : "NuMu",
    "reco_base_out_path" : "/data/user/tvaneede/GlobalFit/reco_processing/output/v6",
    "reco_base_in_path" : "/data/sim/IceCube/2023/filtered/level2/neutrino-generator",
    "hdf_file_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/v6/NuMu_22644.h5",
    "hdf_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/v6",
    "nfiles" : 200,
}

###
### v5, right hese selection, all the variables, seems I am getting close
###
v5 = {}

v5["NuTau_midE"] = {
    "dataset" : "22634",
    "subfolders" : 
    ["0000000-0000999","0001000-0001999"], # 1000 + 1000
    "flavor" : "NuTau",
    "reco_base_out_path" : "/data/user/tvaneede/GlobalFit/reco_processing/output/v5",
    "reco_base_in_path" : "/data/sim/IceCube/2023/filtered/level2/neutrino-generator",
    "hdf_file_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/v5/NuTau_22634.h5",
    "hdf_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/v5",
    "nfiles" : 2000,
}

v5["NuTau_highE"] = {
    "dataset" : "22635",
    "subfolders" : 
    ["0000000-0000999","0001000-0001999"], # 1000 + 1000
    "flavor" : "NuTau",
    "reco_base_out_path" : "/data/user/tvaneede/GlobalFit/reco_processing/output/v5",
    "reco_base_in_path" : "/data/sim/IceCube/2023/filtered/level2/neutrino-generator",
    "hdf_file_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/v5/NuTau_22635.h5",
    "hdf_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/v5",
    "nfiles" : 2000,
}

v5["NuE_midE"] = {
    "dataset" : "22613",
    "subfolders" : 
    ["0000000-0000999","0001000-0001999"], # 1000 + 997
    "flavor" : "NuE",
    "reco_base_out_path" : "/data/user/tvaneede/GlobalFit/reco_processing/output/v5",
    "reco_base_in_path" : "/data/sim/IceCube/2023/filtered/level2/neutrino-generator",
    "hdf_file_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/v5/NuE_22613.h5",
    "hdf_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/v5",
    "nfiles" : 1997,
}

v5["NuE_highE"] = {
    "dataset" : "22612",
    "subfolders" : 
    ["0000000-0000999","0001000-0001999"], # 1000 + 1000
    "flavor" : "NuE",
    "reco_base_out_path" : "/data/user/tvaneede/GlobalFit/reco_processing/output/v5",
    "reco_base_in_path" : "/data/sim/IceCube/2023/filtered/level2/neutrino-generator",
    "hdf_file_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/v5/NuE_22612.h5",
    "hdf_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/v5",
    "nfiles" : 2000,
}

v5["NuMu_midE"] = {
    "dataset" : "22645",
    "subfolders" : 
    ["0000000-0000999","0001000-0001999"], # 1000 + 1000
    "flavor" : "NuMu",
    "reco_base_out_path" : "/data/user/tvaneede/GlobalFit/reco_processing/output/v5",
    "reco_base_in_path" : "/data/sim/IceCube/2023/filtered/level2/neutrino-generator",
    "hdf_file_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/v5/NuMu_22645.h5",
    "hdf_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/v5",
    "nfiles" : 2000,
}

v5["NuMu_highE"] = {
    "dataset" : "22644",
    "subfolders" : 
    ["0000000-0000999","0001000-0001999"], # 1000 + 1000
    "flavor" : "NuMu",
    "reco_base_out_path" : "/data/user/tvaneede/GlobalFit/reco_processing/output/v5",
    "reco_base_in_path" : "/data/sim/IceCube/2023/filtered/level2/neutrino-generator",
    "hdf_file_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/v5/NuMu_22644.h5",
    "hdf_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/v5",
    "nfiles" : 2000,
}


###
### Proper HESE selection, turns out v2 was the cascade selection! I was missing muons
###

v4 = {}

v4["NuTau_midE"] = {
    "dataset" : "22634",
    "subfolders" : 
    ["0000000-0000999"], # 1000
    # ["0000000-0000999","0001000-0001999"], # 1000 + 1000
    "flavor" : "NuTau",
    "reco_base_out_path" : "/data/user/tvaneede/GlobalFit/reco_processing/output/v4",
    "reco_base_in_path" : "/data/sim/IceCube/2023/filtered/level2/neutrino-generator",
    "hdf_file_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/v4/NuTau_22634.h5",
    "hdf_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/v4",
    "nfiles" : 100,
}

v4["NuTau_highE"] = {
    "dataset" : "22635",
    "subfolders" : 
    ["0000000-0000999"], # 1000
    # ["0000000-0000999","0001000-0001999"], # 1000 + 1000
    "flavor" : "NuTau",
    "reco_base_out_path" : "/data/user/tvaneede/GlobalFit/reco_processing/output/v4",
    "reco_base_in_path" : "/data/sim/IceCube/2023/filtered/level2/neutrino-generator",
    "hdf_file_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/v4/NuTau_22635.h5",
    "hdf_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/v4",
    "nfiles" : 100,
}

v4["NuE_midE"] = {
    "dataset" : "22613",
    "subfolders" : 
    ["0000000-0000999"], # 1000
    # ["0000000-0000999","0001000-0001999"], # 1000 + 997
    "flavor" : "NuE",
    "reco_base_out_path" : "/data/user/tvaneede/GlobalFit/reco_processing/output/v4",
    "reco_base_in_path" : "/data/sim/IceCube/2023/filtered/level2/neutrino-generator",
    "hdf_file_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/v4/NuE_22613.h5",
    "hdf_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/v4",
    "nfiles" : 100,
}

v4["NuE_highE"] = {
    "dataset" : "22612",
    "subfolders" : 
    ["0000000-0000999"], # 1000
    # ["0000000-0000999","0001000-0001999"], # 1000 + 1000
    "flavor" : "NuE",
    "reco_base_out_path" : "/data/user/tvaneede/GlobalFit/reco_processing/output/v4",
    "reco_base_in_path" : "/data/sim/IceCube/2023/filtered/level2/neutrino-generator",
    "hdf_file_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/v4/NuE_22612.h5",
    "hdf_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/v4",
    "nfiles" : 100,
}

v4["NuMu_midE"] = {
    "dataset" : "22645",
    "subfolders" : 
    ["0000000-0000999"], # 1000
    # ["0000000-0000999","0001000-0001999"], # 1000 + 1000
    "flavor" : "NuMu",
    "reco_base_out_path" : "/data/user/tvaneede/GlobalFit/reco_processing/output/v4",
    "reco_base_in_path" : "/data/sim/IceCube/2023/filtered/level2/neutrino-generator",
    "hdf_file_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/v4/NuMu_22645.h5",
    "hdf_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/v4",
    "nfiles" : 100,
}

v4["NuMu_highE"] = {
    "dataset" : "22644",
    "subfolders" : 
    ["0000000-0000999"], # 1000
    # ["0000000-0000999","0001000-0001999"], # 1000 + 1000
    "flavor" : "NuMu",
    "reco_base_out_path" : "/data/user/tvaneede/GlobalFit/reco_processing/output/v4",
    "reco_base_in_path" : "/data/sim/IceCube/2023/filtered/level2/neutrino-generator",
    "hdf_file_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/v4/NuMu_22644.h5",
    "hdf_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/v4",
    "nfiles" : 100,
}

v3 = {}

v3["NuTau_midE"] = {
    "dataset" : "22634",
    "subfolders" : 
    ["0000000-0000999"], # 1000
    # ["0000000-0000999","0001000-0001999"], # 1000 + 1000
    "flavor" : "NuTau",
    "reco_base_out_path" : "/data/user/tvaneede/GlobalFit/reco_processing/output/v3",
    "reco_base_in_path" : "/data/sim/IceCube/2023/filtered/level2/neutrino-generator",
    "hdf_file_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/v3/NuTau_22634.h5",
    "hdf_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/v3",
    "nfiles" : 100,
}

v3["NuTau_highE"] = {
    "dataset" : "22635",
    "subfolders" : 
    ["0000000-0000999"], # 1000
    # ["0000000-0000999","0001000-0001999"], # 1000 + 1000
    "flavor" : "NuTau",
    "reco_base_out_path" : "/data/user/tvaneede/GlobalFit/reco_processing/output/v3",
    "reco_base_in_path" : "/data/sim/IceCube/2023/filtered/level2/neutrino-generator",
    "hdf_file_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/v3/NuTau_22635.h5",
    "hdf_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/v3",
    "nfiles" : 100,
}

v3["NuE_midE"] = {
    "dataset" : "22613",
    "subfolders" : 
    ["0000000-0000999"], # 1000
    # ["0000000-0000999","0001000-0001999"], # 1000 + 997
    "flavor" : "NuE",
    "reco_base_out_path" : "/data/user/tvaneede/GlobalFit/reco_processing/output/v3",
    "reco_base_in_path" : "/data/sim/IceCube/2023/filtered/level2/neutrino-generator",
    "hdf_file_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/v3/NuE_22613.h5",
    "hdf_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/v3",
    "nfiles" : 100,
}

v3["NuE_highE"] = {
    "dataset" : "22612",
    "subfolders" : 
    ["0000000-0000999"], # 1000
    # ["0000000-0000999","0001000-0001999"], # 1000 + 1000
    "flavor" : "NuE",
    "reco_base_out_path" : "/data/user/tvaneede/GlobalFit/reco_processing/output/v3",
    "reco_base_in_path" : "/data/sim/IceCube/2023/filtered/level2/neutrino-generator",
    "hdf_file_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/v3/NuE_22612.h5",
    "hdf_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/v3",
    "nfiles" : 100,
}

v3["NuMu_midE"] = {
    "dataset" : "22645",
    "subfolders" : 
    ["0000000-0000999"], # 1000
    # ["0000000-0000999","0001000-0001999"], # 1000 + 1000
    "flavor" : "NuMu",
    "reco_base_out_path" : "/data/user/tvaneede/GlobalFit/reco_processing/output/v3",
    "reco_base_in_path" : "/data/sim/IceCube/2023/filtered/level2/neutrino-generator",
    "hdf_file_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/v3/NuMu_22645.h5",
    "hdf_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/v3",
    "nfiles" : 100,
}

v3["NuMu_highE"] = {
    "dataset" : "22644",
    "subfolders" : 
    ["0000000-0000999"], # 1000
    # ["0000000-0000999","0001000-0001999"], # 1000 + 1000
    "flavor" : "NuMu",
    "reco_base_out_path" : "/data/user/tvaneede/GlobalFit/reco_processing/output/v3",
    "reco_base_in_path" : "/data/sim/IceCube/2023/filtered/level2/neutrino-generator",
    "hdf_file_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/v3/NuMu_22644.h5",
    "hdf_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/v3",
    "nfiles" : 100,
}

###
### Proper HESE selection, added Millipede reco to reco script 
###

v2 = {}

v2["NuTau_midE"] = {
    "dataset" : "22634",
    "subfolders" : 
    ["0000000-0000999","0001000-0001999"], # 1000 + 1000
    "flavor" : "NuTau",
    "reco_base_out_path" : "/data/user/tvaneede/GlobalFit/reco_processing/output/v2",
    "reco_base_in_path" : "/data/sim/IceCube/2023/filtered/level3/cascade/neutrino-generator",
    "hdf_file_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/v2/NuTau_22634.h5",
    "hdf_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/v2",
    "nfiles" : 2000,
}

v2["NuTau_highE"] = {
    "dataset" : "22635",
    "subfolders" : 
    ["0000000-0000999","0001000-0001999"], # 1000 + 1000
    "flavor" : "NuTau",
    "reco_base_out_path" : "/data/user/tvaneede/GlobalFit/reco_processing/output/v2",
    "reco_base_in_path" : "/data/sim/IceCube/2023/filtered/level3/cascade/neutrino-generator",
    "hdf_file_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/v2/NuTau_22635.h5",
    "hdf_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/v2",
    "nfiles" : 2000,
}

v2["NuE_midE"] = {
    "dataset" : "22613",
    "subfolders" : 
    ["0000000-0000999","0001000-0001999"], # 1000 + 997
    "flavor" : "NuE",
    "reco_base_out_path" : "/data/user/tvaneede/GlobalFit/reco_processing/output/v2",
    "reco_base_in_path" : "/data/sim/IceCube/2023/filtered/level3/cascade/neutrino-generator",
    "hdf_file_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/v2/NuE_22613.h5",
    "hdf_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/v2",
    "nfiles" : 1997,
}

v2["NuE_highE"] = {
    "dataset" : "22612",
    "subfolders" : 
    ["0000000-0000999","0001000-0001999"], # 1000 + 1000
    "flavor" : "NuE",
    "reco_base_out_path" : "/data/user/tvaneede/GlobalFit/reco_processing/output/v2",
    "reco_base_in_path" : "/data/sim/IceCube/2023/filtered/level3/cascade/neutrino-generator",
    "hdf_file_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/v2/NuE_22612.h5",
    "hdf_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/v2",
    "nfiles" : 2000,
}

v2["NuMu_midE"] = {
    "dataset" : "22645",
    "subfolders" : 
    ["0000000-0000999","0001000-0001999"], # 1000 + 1000
    "flavor" : "NuMu",
    "reco_base_out_path" : "/data/user/tvaneede/GlobalFit/reco_processing/output/v2",
    "reco_base_in_path" : "/data/sim/IceCube/2023/filtered/level3/cascade/neutrino-generator",
    "hdf_file_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/v2/NuMu_22645.h5",
    "hdf_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/v2",
    "nfiles" : 2000,
}

v2["NuMu_highE"] = {
    "dataset" : "22644",
    "subfolders" : 
    ["0000000-0000999","0001000-0001999"], # 1000 + 1000
    "flavor" : "NuMu",
    "reco_base_out_path" : "/data/user/tvaneede/GlobalFit/reco_processing/output/v2",
    "reco_base_in_path" : "/data/sim/IceCube/2023/filtered/level3/cascade/neutrino-generator",
    "hdf_file_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/v2/NuMu_22644.h5",
    "hdf_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/v2",
    "nfiles" : 2000,
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
    "reco_base_out_path" : "/data/user/tvaneede/GlobalFit/reco_processing/output/v1",
    "hdf_file_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/v1/NuTau_22634.h5",
    "hdf_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/v1",
}

v1["NuTau_highE"] = {
    "dataset" : "22635",
    "subfolders" : 
    ["0000000-0000999"],
    "flavor" : "NuTau",
    "reco_base_out_path" : "/data/user/tvaneede/GlobalFit/reco_processing/output/v1",
    "hdf_file_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/v1/NuTau_22635.h5",
    "hdf_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/v1",
}

v1["NuE_midE"] = {
    "dataset" : "22613",
    "subfolders" : 
    ["0000000-0000999"],
    "flavor" : "NuE",
    "reco_base_out_path" : "/data/user/tvaneede/GlobalFit/reco_processing/output/v1",
    "hdf_file_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/v1/NuE_22613.h5",
    "hdf_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/v1",
}

v1["NuE_highE"] = {
    "dataset" : "22612",
    "subfolders" : 
    ["0000000-0000999"],
    "flavor" : "NuE",
    "reco_base_out_path" : "/data/user/tvaneede/GlobalFit/reco_processing/output/v1",
    "hdf_file_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/v1/NuE_22612.h5",
    "hdf_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/v1",
}

v1["NuMu_midE"] = {
    "dataset" : "22645",
    "subfolders" : 
    ["0000000-0000999"],
    "flavor" : "NuMu",
    "reco_base_out_path" : "/data/user/tvaneede/GlobalFit/reco_processing/output/v1",
    "hdf_file_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/v1/NuMu_22645.h5",
    "hdf_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/v1",
}

v1["NuMu_highE"] = {
    "dataset" : "22644",
    "subfolders" : 
    ["0000000-0000999"],
    "flavor" : "NuMu",
    "reco_base_out_path" : "/data/user/tvaneede/GlobalFit/reco_processing/output/v1",
    "hdf_file_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/v1/NuMu_22644.h5",
    "hdf_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/v1",
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
### Ftp files
###

ftp_baseline_level2 = {}

ftp_baseline_level2["NuTau_midE1"] = {
    "dataset" : "22634",
    "subfolders" : ["0000000-0000999"],
    # ["0000000-0000999", "0001000-0001999", "0002000-0002999", "0003000-0003999"],
    "flavor" : "NuTau",
    "reco_base_out_path" : "/data/sim/IceCube/2023/filtered/level2/neutrino-generator/",
    "hdf_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/ftp_baseline_level2",
    'nfiles' : 1000, # 4000,
}

ftp_baseline_level2["NuTau_highE1"] = {
    "dataset" : "22635",
    "subfolders" : ["0000000-0000999"],
    # ["0000000-0000999", "0001000-0001999", "0002000-0002999", "0003000-0003999", "0004000-0004999",
    #  "0005000-0005999", "0006000-0006999", "0007000-0007999", "0008000-0008999", "0009000-0009999",
    #  "0010000-0010999", "0011000-0011999", "0012000-0012999", "0013000-0013999", "0014000-0014999",
    #  "0015000-0015999", "0016000-0016999", "0017000-0017999", "0018000-0018999", "0019000-0019999"],
    "flavor" : "NuTau",
    "reco_base_out_path" : "/data/sim/IceCube/2023/filtered/level2/neutrino-generator/",
    "hdf_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/ftp_baseline_level2",
    'nfiles' : 1000, # 19997,
}


ftp_baseline_level2["NuE_midE1"] = {
    "dataset" : "22613",
    "subfolders" : ["0000000-0000999"],
    # ["0000000-0000999", "0001000-0001999", "0002000-0002999", "0003000-0003999"],
    "flavor" : "NuE",
    "reco_base_out_path" : "/data/sim/IceCube/2023/filtered/level2/neutrino-generator/",
    "hdf_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/ftp_baseline_level2",
    'nfiles' : 1000, # 3987,
}

ftp_baseline_level2["NuE_highE1"] = {
    "dataset" : "22612",
    "subfolders" : ["0000000-0000999"],
    # ["0000000-0000999", "0001000-0001999", "0002000-0002999", "0003000-0003999", "0004000-0004999",
    #  "0005000-0005999", "0006000-0006999", "0007000-0007999", "0008000-0008999", "0009000-0009999",
    #  "0010000-0010999", "0011000-0011999", "0012000-0012999", "0013000-0013999", "0014000-0014999",
    #  "0015000-0015999", "0016000-0016999", "0017000-0017999", "0018000-0018999", "0019000-0019999"],
    "flavor" : "NuE",
    "reco_base_out_path" : "/data/sim/IceCube/2023/filtered/level2/neutrino-generator/",
    "hdf_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/ftp_baseline_level2",
    'nfiles' : 1000, # 19960,
}

ftp_baseline_level2["NuMu_midE1"] = {
    "dataset" : "22645",
    "subfolders" : ["0000000-0000999"],
    # ["0000000-0000999", "0001000-0001999", "0002000-0002999", "0003000-0003999", "0004000-0004999"],
    "flavor" : "NuMu",
    "reco_base_out_path" : "/data/sim/IceCube/2023/filtered/level2/neutrino-generator/",
    "hdf_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/ftp_baseline_level2",
    'nfiles' : 1000, # 5000,
}



ftp_baseline_level2["NuMu_highE1"] = {
    "dataset" : "22644",
    "subfolders" : ["0000000-0000999"],
    # ["0000000-0000999", "0001000-0001999", "0002000-0002999", "0003000-0003999", "0004000-0004999",
    #  "0005000-0005999", "0006000-0006999", "0007000-0007999", "0008000-0008999", "0009000-0009999",
    #  "0010000-0010999", "0011000-0011999", "0012000-0012999", "0013000-0013999", "0014000-0014999"],
    "flavor" : "NuMu",
    "reco_base_out_path" : "/data/sim/IceCube/2023/filtered/level2/neutrino-generator/",
    "hdf_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/ftp_baseline_level2",
    'nfiles' : 1000, # 14998,
}

### l3 casc

ftp_baseline_level3casc = {}

ftp_baseline_level3casc["NuTau_midE1"] = {
    "dataset" : "22634",
    "subfolders" : ["0000000-0000999"],
    # ["0000000-0000999", "0001000-0001999", "0002000-0002999", "0003000-0003999"],
    "flavor" : "NuTau",
    "reco_base_out_path" : "/data/sim/IceCube/2023/filtered/level3/cascade/neutrino-generator/",
    "hdf_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/ftp_baseline_level3casc",
    'nfiles' : 1000, # 4000,
}

ftp_baseline_level3casc["NuTau_highE1"] = {
    "dataset" : "22635",
    "subfolders" : ["0000000-0000999"],
    # ["0000000-0000999", "0001000-0001999", "0002000-0002999", "0003000-0003999", "0004000-0004999",
    #  "0005000-0005999", "0006000-0006999", "0007000-0007999", "0008000-0008999", "0009000-0009999",
    #  "0010000-0010999", "0011000-0011999", "0012000-0012999", "0013000-0013999", "0014000-0014999",
    #  "0015000-0015999", "0016000-0016999", "0017000-0017999", "0018000-0018999", "0019000-0019999"],
    "flavor" : "NuTau",
    "reco_base_out_path" : "/data/sim/IceCube/2023/filtered/level3/cascade/neutrino-generator/",
    "hdf_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/ftp_baseline_level3casc",
    'nfiles' : 1000, # 19997,
}


ftp_baseline_level3casc["NuE_midE1"] = {
    "dataset" : "22613",
    "subfolders" : ["0000000-0000999"],
    # ["0000000-0000999", "0001000-0001999", "0002000-0002999", "0003000-0003999"],
    "flavor" : "NuE",
    "reco_base_out_path" : "/data/sim/IceCube/2023/filtered/level3/cascade/neutrino-generator/",
    "hdf_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/ftp_baseline_level3casc",
    'nfiles' : 1000, # 3987,
}

ftp_baseline_level3casc["NuE_highE1"] = {
    "dataset" : "22612",
    "subfolders" : ["0000000-0000999"],
    # ["0000000-0000999", "0001000-0001999", "0002000-0002999", "0003000-0003999", "0004000-0004999",
    #  "0005000-0005999", "0006000-0006999", "0007000-0007999", "0008000-0008999", "0009000-0009999",
    #  "0010000-0010999", "0011000-0011999", "0012000-0012999", "0013000-0013999", "0014000-0014999",
    #  "0015000-0015999", "0016000-0016999", "0017000-0017999", "0018000-0018999", "0019000-0019999"],
    "flavor" : "NuE",
    "reco_base_out_path" : "/data/sim/IceCube/2023/filtered/level3/cascade/neutrino-generator/",
    "hdf_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/ftp_baseline_level3casc",
    'nfiles' : 1000, # 19960,
}

ftp_baseline_level3casc["NuMu_midE1"] = {
    "dataset" : "22645",
    "subfolders" : ["0000000-0000999"],
    # ["0000000-0000999", "0001000-0001999", "0002000-0002999", "0003000-0003999", "0004000-0004999"],
    "flavor" : "NuMu",
    "reco_base_out_path" : "/data/sim/IceCube/2023/filtered/level3/cascade/neutrino-generator/",
    "hdf_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/ftp_baseline_level3casc",
    'nfiles' : 1000, # 5000,
}



ftp_baseline_level3casc["NuMu_highE1"] = {
    "dataset" : "22644",
    "subfolders" : ["0000000-0000999"],
    # ["0000000-0000999", "0001000-0001999", "0002000-0002999", "0003000-0003999", "0004000-0004999",
    #  "0005000-0005999", "0006000-0006999", "0007000-0007999", "0008000-0008999", "0009000-0009999",
    #  "0010000-0010999", "0011000-0011999", "0012000-0012999", "0013000-0013999", "0014000-0014999"],
    "flavor" : "NuMu",
    "reco_base_out_path" : "/data/sim/IceCube/2023/filtered/level3/cascade/neutrino-generator/",
    "hdf_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/ftp_baseline_level3casc",
    'nfiles' : 1000, # 14998,
}

### l3 muon


ftp_baseline_level3muon = {}

ftp_baseline_level3muon["NuTau_midE1"] = {
    "dataset" : "22634",
    "subfolders" : ["0000000-0000999"],
    # ["0000000-0000999", "0001000-0001999", "0002000-0002999", "0003000-0003999"],
    "flavor" : "NuTau",
    "reco_base_out_path" : "/data/sim/IceCube/2023/filtered/level3/muon/neutrino-generator/",
    "hdf_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/ftp_baseline_level3muon",
    'nfiles' : 1000, # 4000,
}

ftp_baseline_level3muon["NuTau_highE1"] = {
    "dataset" : "22635",
    "subfolders" : ["0000000-0000999"],
    # ["0000000-0000999", "0001000-0001999", "0002000-0002999", "0003000-0003999", "0004000-0004999",
    #  "0005000-0005999", "0006000-0006999", "0007000-0007999", "0008000-0008999", "0009000-0009999",
    #  "0010000-0010999", "0011000-0011999", "0012000-0012999", "0013000-0013999", "0014000-0014999",
    #  "0015000-0015999", "0016000-0016999", "0017000-0017999", "0018000-0018999", "0019000-0019999"],
    "flavor" : "NuTau",
    "reco_base_out_path" : "/data/sim/IceCube/2023/filtered/level3/muon/neutrino-generator/",
    "hdf_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/ftp_baseline_level3muon",
    'nfiles' : 1000, # 19997,
}


ftp_baseline_level3muon["NuE_midE1"] = {
    "dataset" : "22613",
    "subfolders" : ["0000000-0000999"],
    # ["0000000-0000999", "0001000-0001999", "0002000-0002999", "0003000-0003999"],
    "flavor" : "NuE",
    "reco_base_out_path" : "/data/sim/IceCube/2023/filtered/level3/muon/neutrino-generator/",
    "hdf_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/ftp_baseline_level3muon",
    'nfiles' : 1000, # 3987,
}

ftp_baseline_level3muon["NuE_highE1"] = {
    "dataset" : "22612",
    "subfolders" : ["0000000-0000999"],
    # ["0000000-0000999", "0001000-0001999", "0002000-0002999", "0003000-0003999", "0004000-0004999",
    #  "0005000-0005999", "0006000-0006999", "0007000-0007999", "0008000-0008999", "0009000-0009999",
    #  "0010000-0010999", "0011000-0011999", "0012000-0012999", "0013000-0013999", "0014000-0014999",
    #  "0015000-0015999", "0016000-0016999", "0017000-0017999", "0018000-0018999", "0019000-0019999"],
    "flavor" : "NuE",
    "reco_base_out_path" : "/data/sim/IceCube/2023/filtered/level3/muon/neutrino-generator/",
    "hdf_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/ftp_baseline_level3muon",
    'nfiles' : 1000, # 19960,
}

ftp_baseline_level3muon["NuMu_midE1"] = {
    "dataset" : "22645",
    "subfolders" : ["0000000-0000999"],
    # ["0000000-0000999", "0001000-0001999", "0002000-0002999", "0003000-0003999", "0004000-0004999"],
    "flavor" : "NuMu",
    "reco_base_out_path" : "/data/sim/IceCube/2023/filtered/level3/muon/neutrino-generator/",
    "hdf_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/ftp_baseline_level3muon",
    'nfiles' : 1000, # 5000,
}



ftp_baseline_level3casc["NuMu_highE1"] = {
    "dataset" : "22644",
    "subfolders" : ["0000000-0000999"],
    # ["0000000-0000999", "0001000-0001999", "0002000-0002999", "0003000-0003999", "0004000-0004999",
    #  "0005000-0005999", "0006000-0006999", "0007000-0007999", "0008000-0008999", "0009000-0009999",
    #  "0010000-0010999", "0011000-0011999", "0012000-0012999", "0013000-0013999", "0014000-0014999"],
    "flavor" : "NuMu",
    "reco_base_out_path" : "/data/sim/IceCube/2023/filtered/level3/cascade/neutrino-generator/",
    "hdf_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/ftp_baseline_level3casc",
    'nfiles' : 1000, # 14998,
}




###
### ftp baseline, second batch
###

ftp_baseline_2nd_level2 = {}


ftp_baseline_2nd_level2["NuTau_midE2"] = {
    "dataset" : "22667",
    "subfolders" : 
    ["0000000-0000999", "0001000-0001999", "0002000-0002999", "0003000-0003999"],
    "flavor" : "NuTau",
    "reco_base_out_path" : "/data/sim/IceCube/2023/filtered/level2/neutrino-generator/",
    'nfiles' : 3764,
}

ftp_baseline_2nd_level2["NuTau_highE2"] = {
    "dataset" : "22668",
    "subfolders" : 
    ["0000000-0000999", "0001000-0001999", "0002000-0002999", "0003000-0003999", "0004000-0004999",
     "0005000-0005999", "0006000-0006999", "0007000-0007999", "0008000-0008999", "0009000-0009999",
     "0010000-0010999", "0011000-0011999", "0012000-0012999", "0013000-0013999", "0014000-0014999",
     "0015000-0015999", "0016000-0016999", "0017000-0017999", "0018000-0018999", "0019000-0019999"],
    "flavor" : "NuTau",
    "reco_base_out_path" : "/data/sim/IceCube/2023/filtered/level2/neutrino-generator/",
    'nfiles' : 16563,
}


ftp_baseline_2nd_level2["NuE_midE2"] = {
    "dataset" : "22664",
    "subfolders" : 
    ["0000000-0000999", "0001000-0001999", "0002000-0002999", "0003000-0003999"],
    "flavor" : "NuE",
    "reco_base_out_path" : "/data/sim/IceCube/2023/filtered/level2/neutrino-generator/",
    'nfiles' : 3747,
}


ftp_baseline_2nd_level2["NuE_highE2"] = {
    "dataset" : "22663",
    "subfolders" : 
    ["0000000-0000999", "0001000-0001999", "0002000-0002999", "0003000-0003999", "0004000-0004999",
     "0005000-0005999", "0006000-0006999", "0007000-0007999", "0008000-0008999", "0009000-0009999",
     "0010000-0010999", "0011000-0011999", "0012000-0012999", "0013000-0013999", "0014000-0014999",
     "0015000-0015999", "0016000-0016999", "0017000-0017999", "0018000-0018999", "0019000-0019999"],
    "flavor" : "NuE",
    "reco_base_out_path" : "/data/sim/IceCube/2023/filtered/level2/neutrino-generator/",
    'nfiles' : 19693,
}


ftp_baseline_2nd_level2["NuMu_midE2"] = {
    "dataset" : "22671",
    "subfolders" : 
    ["0000000-0000999", "0001000-0001999", "0002000-0002999", "0003000-0003999", "0004000-0004999"],
    "flavor" : "NuMu",
    "reco_base_out_path" : "/data/sim/IceCube/2023/filtered/level2/neutrino-generator/",
    'nfiles' : 4687,
}

ftp_baseline_2nd_level2["NuMu_highE2"] = {
    "dataset" : "22670",
    "subfolders" : 
    ["0000000-0000999", "0001000-0001999", "0002000-0002999", "0003000-0003999", "0004000-0004999",
     "0005000-0005999", "0006000-0006999", "0007000-0007999", "0008000-0008999", "0009000-0009999",
     "0010000-0010999", "0011000-0011999", "0012000-0012999", "0013000-0013999", "0014000-0014999"],
    "flavor" : "NuMu",
    "reco_base_out_path" : "/data/sim/IceCube/2023/filtered/level2/neutrino-generator/",
    "level2_path" : "/data/sim/IceCube/2023/filtered/level2/neutrino-generator/",
    "level6_path" : "/data/sim/IceCube/2020/filtered/level6/cascade/neutrino-generator/",
    'nfiles' : 9688,
}

###
### Ftp ensemble files
### Selection: I thought no selection, but I think there is the cascade selection already applied
### Name: ftp_l3casc_ensemble, previous: ftp
###

ftp_l2_ensemble = {}

ftp_l2_ensemble["NuTau_midE"] = {
    "dataset" : "22859",
    "subfolders" : 
    ["0000000-0000999", "0001000-0001999", "0002000-0002999", "0003000-0003999"],
    "flavor" : "NuTau",
    "reco_base_out_path" : "/data/sim/IceCube/2020/filtered/level2/neutrino-generator/",
    "year" : "2020",
    "hdf_path" : "",
}

ftp_l2_ensemble["NuTau_highE"] = {
    "dataset" : "22860",
    "subfolders" : 
    ["0000000-0000999", "0001000-0001999", "0002000-0002999", "0003000-0003999", "0004000-0004999",
     "0005000-0005999", "0006000-0006999", "0007000-0007999", "0008000-0008999", "0009000-0009999",
     "0010000-0010999", "0011000-0011999", "0012000-0012999", "0013000-0013999", "0014000-0014999",
     "0015000-0015999", "0016000-0016999", "0017000-0017999", "0018000-0018999", "0019000-0019999",
     "0020000-0020999", "0021000-0021999"],
    "flavor" : "NuTau",
    "reco_base_out_path" : "/data/sim/IceCube/2020/filtered/level2/neutrino-generator/",
    "year" : "2020",
    "hdf_path" : "",
}

ftp_l2_ensemble["NuE_midE"] = {
    "dataset" : "22856",
    "subfolders" : 
    ["0000000-0000999", "0001000-0001999", "0002000-0002999", "0003000-0003999", "0004000-0004999"],
    "flavor" : "NuE",
    "reco_base_out_path" : "/data/sim/IceCube/2020/filtered/level2/neutrino-generator/",
    "year" : "2020",
    "hdf_path" : "",
}

ftp_l2_ensemble["NuE_highE"] = {
    "dataset" : "22857",
    "subfolders" : 
    ["0000000-0000999", "0001000-0001999", "0002000-0002999", "0003000-0003999", "0004000-0004999",
     "0005000-0005999", "0006000-0006999", "0007000-0007999", "0008000-0008999", "0009000-0009999",
     "0010000-0010999", "0011000-0011999", "0012000-0012999", "0013000-0013999", "0014000-0014999",
     "0015000-0015999", "0016000-0016999", "0017000-0017999", "0018000-0018999", "0019000-0019999",
     "0020000-0020999", "0021000-0021999", "0022000-0022999", "0023000-0023999"],
    "flavor" : "NuE",
    "reco_base_out_path" : "/data/sim/IceCube/2020/filtered/level2/neutrino-generator/",
    "year" : "2020",
    "hdf_path" : "",
}

ftp_l2_ensemble["NuMu_midE"] = {
    "dataset" : "22853",
    "subfolders" : 
    ["0000000-0000999", "0001000-0001999", "0002000-0002999", "0003000-0003999", "0004000-0004999", "0005000-0005999"],
    "flavor" : "NuMu",
    "reco_base_out_path" : "/data/sim/IceCube/2020/filtered/level2/neutrino-generator/",
    "year" : "2020",
    "hdf_path" : "",
}

ftp_l2_ensemble["NuMu_highE"] = {
    "dataset" : "22854",
    "subfolders" : 
    ["0000000-0000999", "0001000-0001999", "0002000-0002999", "0003000-0003999", "0004000-0004999",
     "0005000-0005999", "0006000-0006999", "0007000-0007999", "0008000-0008999", "0009000-0009999",
     "0010000-0010999", "0011000-0011999", "0012000-0012999", "0013000-0013999", "0014000-0014999",
     "0015000-0015999", "0016000-0016999", "0017000-0017999"],
    "flavor" : "NuMu",
    "reco_base_out_path" : "/data/sim/IceCube/2020/filtered/level2/neutrino-generator/",
    "year" : "2020",
    "hdf_path" : "",
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
    "reco_base_out_path" : "/data/sim/IceCube/2020/filtered/level3/cascade/neutrino-generator",
    "hdf_file_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/spice_l3casc/NuTau_22049.h5",
    "hdf_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/spice_l3casc",
    "nfiles" : 495,
}

spice_l3casc["NuTau_highE1"] = {
    "dataset" : "22050",
    "subfolders" : 
    ["0000000-0000999", "0001000-0001999", "0002000-0002999"],
    "flavor" : "NuTau",
    "reco_base_out_path" : "/data/sim/IceCube/2020/filtered/level3/cascade/neutrino-generator",
    "hdf_file_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/spice_l3casc/NuTau_22050.h5",
    "hdf_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/spice_l3casc",
    "nfiles" : 2773,
}

spice_l3casc["NuTau_midE2"] = {
    "dataset" : "22085",
    "subfolders" : 
    ["0000000-0000999", "0001000-0001999"],
    "flavor" : "NuTau",
    "reco_base_out_path" : "/data/sim/IceCube/2020/filtered/level3/cascade/neutrino-generator",
    "hdf_file_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/spice_l3casc/NuTau_22085.h5",
    "hdf_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/spice_l3casc",
    "nfiles" : 1155,
}

spice_l3casc["NuTau_highE2"] = {
    "dataset" : "22086",
    "subfolders" : 
    ["0000000-0000999", "0001000-0001999", "0002000-0002999","0003000-0003999", "0004000-0004999", "0005000-0005999", "0006000-0006999"],
    "flavor" : "NuTau",
    "reco_base_out_path" : "/data/sim/IceCube/2020/filtered/level3/cascade/neutrino-generator",
    "hdf_file_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/spice_l3casc/NuTau_22086.h5",
    "hdf_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/spice_l3casc",
    "nfiles" : 6465,
}

spice_l3casc["NuE_midE1"] = {
    "dataset" : "22046",
    "subfolders" : 
    ["0000000-0000999"],
    "flavor" : "NuE",
    "reco_base_out_path" : "/data/sim/IceCube/2020/filtered/level3/cascade/neutrino-generator",
    "hdf_file_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/spice_l3casc/NuE_22046.h5",
    "hdf_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/spice_l3casc",
    "nfiles" : 525,
}

spice_l3casc["NuE_highE1"] = {
    "dataset" : "22047",
    "subfolders" : 
    ["0000000-0000999", "0001000-0001999", "0002000-0002999"],
    "flavor" : "NuE",
    "reco_base_out_path" : "/data/sim/IceCube/2020/filtered/level3/cascade/neutrino-generator",
    "hdf_file_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/spice_l3casc/NuE_22047.h5",
    "hdf_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/spice_l3casc",
    "nfiles" : 2998,
}

spice_l3casc["NuE_midE2"] = {
    "dataset" : "22082",
    "subfolders" : 
    ["0000000-0000999", "0001000-0001999"],
    "flavor" : "NuE",
    "reco_base_out_path" : "/data/sim/IceCube/2020/filtered/level3/cascade/neutrino-generator",
    "hdf_file_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/spice_l3casc/NuE_22082.h5",
    "hdf_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/spice_l3casc",
    "nfiles" : 1225,
}

spice_l3casc["NuE_highE2"] = {
    "dataset" : "22083",
    "subfolders" : 
    ["0000000-0000999", "0001000-0001999", "0002000-0002999","0003000-0003999", "0004000-0004999", "0005000-0005999", "0006000-0006999"],
    "flavor" : "NuE",
    "reco_base_out_path" : "/data/sim/IceCube/2020/filtered/level3/cascade/neutrino-generator",
    "hdf_file_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/spice_l3casc/NuE_22083.h5",
    "hdf_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/spice_l3casc",
    "nfiles" : 6987,
}

spice_l3casc["NuMu_midE1"] = {
    "dataset" : "22043",
    "subfolders" : 
    ["0000000-0000999"], # 675 files min 1 corrupt: run 196
    "flavor" : "NuMu",
    "reco_base_out_path" : "/data/sim/IceCube/2020/filtered/level3/cascade/neutrino-generator",
    "hdf_file_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/spice_l3casc/NuMu_22043.h5",
    "hdf_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/spice_l3casc",
    "nfiles" : 674,
}

spice_l3casc["NuMu_highE1"] = {
    "dataset" : "22044",
    "subfolders" : 
    ["0000000-0000999", "0001000-0001999", "0002000-0002999"],
    "flavor" : "NuMu",
    "reco_base_out_path" : "/data/sim/IceCube/2020/filtered/level3/cascade/neutrino-generator",
    "hdf_file_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/spice_l3casc/NuMu_22044.h5",
    "hdf_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/spice_l3casc",
    "nfiles" : 2250,
}

spice_l3casc["NuMu_midE2"] = {
    "dataset" : "22079",
    "subfolders" : 
    ["0000000-0000999", "0001000-0001999"],
    "flavor" : "NuMu",
    "reco_base_out_path" : "/data/sim/IceCube/2020/filtered/level3/cascade/neutrino-generator",
    "hdf_file_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/spice_l3casc/NuMu_22079.h5",
    "hdf_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/spice_l3casc",
    "nfiles" : 1579,
}

spice_l3casc["NuMu_highE2"] = {
    "dataset" : "22080",
    "subfolders" : 
    ["0000000-0000999", "0001000-0001999", "0002000-0002999","0003000-0003999", "0004000-0004999", "0005000-0005999"],
    "flavor" : "NuMu",
    "reco_base_out_path" : "/data/sim/IceCube/2020/filtered/level3/cascade/neutrino-generator",
    "hdf_file_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/spice_l3casc/NuMu_22080.h5",
    "hdf_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/spice_l3casc",
    "nfiles" : 5245,
}

spice_l3casc_qtot = {}

spice_l3casc_qtot["NuTau_midE1"] = {
    "dataset" : "22049",
    "subfolders" : 
    ["0000000-0000999"],
    "flavor" : "NuTau",
    "reco_base_out_path" : "/data/sim/IceCube/2020/filtered/level3/cascade/neutrino-generator",
    "hdf_file_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/spice_l3casc_nehaqtot/NuTau_22049.h5",
    "hdf_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/spice_l3casc_nehaqtot",
    "nfiles" : 495,
}

spice_l3casc_qtot["NuTau_highE1"] = {
    "dataset" : "22050",
    "subfolders" : 
    ["0000000-0000999", "0001000-0001999", "0002000-0002999"],
    "flavor" : "NuTau",
    "reco_base_out_path" : "/data/sim/IceCube/2020/filtered/level3/cascade/neutrino-generator",
    "hdf_file_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/spice_l3casc_nehaqtot/NuTau_22050.h5",
    "hdf_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/spice_l3casc_nehaqtot",
    "nfiles" : 2773,
}

spice_l3casc_qtot["NuTau_midE2"] = {
    "dataset" : "22085",
    "subfolders" : 
    ["0000000-0000999", "0001000-0001999"],
    "flavor" : "NuTau",
    "reco_base_out_path" : "/data/sim/IceCube/2020/filtered/level3/cascade/neutrino-generator",
    "hdf_file_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/spice_l3casc_nehaqtot/NuTau_22085.h5",
    "hdf_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/spice_l3casc_nehaqtot",
    "nfiles" : 1155,
}

spice_l3casc_qtot["NuTau_highE2"] = {
    "dataset" : "22086",
    "subfolders" : 
    ["0000000-0000999", "0001000-0001999", "0002000-0002999","0003000-0003999", "0004000-0004999", "0005000-0005999", "0006000-0006999"],
    "flavor" : "NuTau",
    "reco_base_out_path" : "/data/sim/IceCube/2020/filtered/level3/cascade/neutrino-generator",
    "hdf_file_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/spice_l3casc_nehaqtot/NuTau_22086.h5",
    "hdf_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/spice_l3casc_nehaqtot",
    "nfiles" : 6465,
}

spice_l3casc_qtot["NuE_midE1"] = {
    "dataset" : "22046",
    "subfolders" : 
    ["0000000-0000999"],
    "flavor" : "NuE",
    "reco_base_out_path" : "/data/sim/IceCube/2020/filtered/level3/cascade/neutrino-generator",
    "hdf_file_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/spice_l3casc_nehaqtot/NuE_22046.h5",
    "hdf_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/spice_l3casc_nehaqtot",
    "nfiles" : 525,
}

spice_l3casc_qtot["NuE_highE1"] = {
    "dataset" : "22047",
    "subfolders" : 
    ["0000000-0000999", "0001000-0001999", "0002000-0002999"],
    "flavor" : "NuE",
    "reco_base_out_path" : "/data/sim/IceCube/2020/filtered/level3/cascade/neutrino-generator",
    "hdf_file_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/spice_l3casc_nehaqtot/NuE_22047.h5",
    "hdf_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/spice_l3casc_nehaqtot",
    "nfiles" : 2998,
}

spice_l3casc_qtot["NuE_midE2"] = {
    "dataset" : "22082",
    "subfolders" : 
    ["0000000-0000999", "0001000-0001999"],
    "flavor" : "NuE",
    "reco_base_out_path" : "/data/sim/IceCube/2020/filtered/level3/cascade/neutrino-generator",
    "hdf_file_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/spice_l3casc_nehaqtot/NuE_22082.h5",
    "hdf_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/spice_l3casc_nehaqtot",
    "nfiles" : 1225,
}

spice_l3casc_qtot["NuE_highE2"] = {
    "dataset" : "22083",
    "subfolders" : 
    ["0000000-0000999", "0001000-0001999", "0002000-0002999","0003000-0003999", "0004000-0004999", "0005000-0005999", "0006000-0006999"],
    "flavor" : "NuE",
    "reco_base_out_path" : "/data/sim/IceCube/2020/filtered/level3/cascade/neutrino-generator",
    "hdf_file_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/spice_l3casc_nehaqtot/NuE_22083.h5",
    "hdf_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/spice_l3casc_nehaqtot",
    "nfiles" : 6987,
}

spice_l3casc_qtot["NuMu_midE1"] = {
    "dataset" : "22043",
    "subfolders" : 
    ["0000000-0000999"], # 675 files min 1 corrupt: run 196
    "flavor" : "NuMu",
    "reco_base_out_path" : "/data/sim/IceCube/2020/filtered/level3/cascade/neutrino-generator",
    "hdf_file_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/spice_l3casc_nehaqtot/NuMu_22043.h5",
    "hdf_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/spice_l3casc_nehaqtot",
    "nfiles" : 674,
}

spice_l3casc_qtot["NuMu_highE1"] = {
    "dataset" : "22044",
    "subfolders" : 
    ["0000000-0000999", "0001000-0001999", "0002000-0002999"],
    "flavor" : "NuMu",
    "reco_base_out_path" : "/data/sim/IceCube/2020/filtered/level3/cascade/neutrino-generator",
    "hdf_file_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/spice_l3casc_nehaqtot/NuMu_22044.h5",
    "hdf_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/spice_l3casc_nehaqtot",
    "nfiles" : 2250,
}

spice_l3casc_qtot["NuMu_midE2"] = {
    "dataset" : "22079",
    "subfolders" : 
    ["0000000-0000999", "0001000-0001999"],
    "flavor" : "NuMu",
    "reco_base_out_path" : "/data/sim/IceCube/2020/filtered/level3/cascade/neutrino-generator",
    "hdf_file_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/spice_l3casc_nehaqtot/NuMu_22079.h5",
    "hdf_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/spice_l3casc_nehaqtot",
    "nfiles" : 1579,
}

spice_l3casc_qtot["NuMu_highE2"] = {
    "dataset" : "22080",
    "subfolders" : 
    ["0000000-0000999", "0001000-0001999", "0002000-0002999","0003000-0003999", "0004000-0004999", "0005000-0005999"],
    "flavor" : "NuMu",
    "reco_base_out_path" : "/data/sim/IceCube/2020/filtered/level3/cascade/neutrino-generator",
    "hdf_file_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/spice_l3casc_nehaqtot/NuMu_22080.h5",
    "hdf_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/spice_l3casc_nehaqtot",
    "nfiles" : 5245,
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
    "reco_base_out_path" : "/data/ana/Diffuse/GlobalFit_Flavor/taupede/SnowStorm/RecowithBfr/Baseline",
    "hdf_file_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/spice_tau_reco/NuTau_22049.h5",
    "hdf_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/spice_tau_reco",
    "nfiles" : 495,
}

spice_tau_reco["NuTau_highE1"] = {
    "dataset" : "22050",
    "subfolders" : 
    ["0000000-0000999", "0001000-0001999", "0002000-0002999"],
    "flavor" : "NuTau",
    "reco_base_out_path" : "/data/ana/Diffuse/GlobalFit_Flavor/taupede/SnowStorm/RecowithBfr/Baseline",
    "hdf_file_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/spice_tau_reco/NuTau_22050.h5",
    "hdf_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/spice_tau_reco",
    "nfiles" : 2773,
}

spice_tau_reco["NuTau_midE2"] = {
    "dataset" : "22085",
    "subfolders" : 
    ["0000000-0000999", "0001000-0001999"],
    "flavor" : "NuTau",
    "reco_base_out_path" : "/data/ana/Diffuse/GlobalFit_Flavor/taupede/SnowStorm/RecowithBfr/Baseline",
    "hdf_file_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/spice_tau_reco/NuTau_22085.h5",
    "hdf_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/spice_tau_reco",
    "nfiles" : 1155,
}

spice_tau_reco["NuTau_highE2"] = {
    "dataset" : "22086",
    "subfolders" : 
    ["0000000-0000999", "0001000-0001999", "0002000-0002999","0003000-0003999", "0004000-0004999", "0005000-0005999", "0006000-0006999"],
    "flavor" : "NuTau",
    "reco_base_out_path" : "/data/ana/Diffuse/GlobalFit_Flavor/taupede/SnowStorm/RecowithBfr/Baseline",
    "hdf_file_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/spice_tau_reco/NuTau_22086.h5",
    "hdf_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/spice_tau_reco",
    "nfiles" : 6465, # 6466 to match neha
}

spice_tau_reco["NuE_midE1"] = {
    "dataset" : "22046",
    "subfolders" : 
    ["0000000-0000999"],
    "flavor" : "NuE",
    "reco_base_out_path" : "/data/ana/Diffuse/GlobalFit_Flavor/taupede/SnowStorm/RecowithBfr/Baseline",
    "hdf_file_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/spice_tau_reco/NuE_22046.h5",
    "hdf_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/spice_tau_reco",
    "nfiles" : 525,
}

spice_tau_reco["NuE_highE1"] = {
    "dataset" : "22047",
    "subfolders" : 
    ["0000000-0000999", "0001000-0001999", "0002000-0002999"],
    "flavor" : "NuE",
    "reco_base_out_path" : "/data/ana/Diffuse/GlobalFit_Flavor/taupede/SnowStorm/RecowithBfr/Baseline",
    "hdf_file_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/spice_tau_reco/NuE_22047.h5",
    "hdf_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/spice_tau_reco",
    "nfiles" : 2998,
}

spice_tau_reco["NuE_midE2"] = {
    "dataset" : "22082",
    "subfolders" : 
    ["0000000-0000999", "0001000-0001999"],
    "flavor" : "NuE",
    "reco_base_out_path" : "/data/ana/Diffuse/GlobalFit_Flavor/taupede/SnowStorm/RecowithBfr/Baseline",
    "hdf_file_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/spice_tau_reco/NuE_22082.h5",
    "hdf_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/spice_tau_reco",
    "nfiles" : 1225,
}

spice_tau_reco["NuE_highE2"] = {
    "dataset" : "22083",
    "subfolders" : 
    ["0000000-0000999", "0001000-0001999", "0002000-0002999","0003000-0003999", "0004000-0004999", "0005000-0005999", "0006000-0006999"],
    "flavor" : "NuE",
    "reco_base_out_path" : "/data/ana/Diffuse/GlobalFit_Flavor/taupede/SnowStorm/RecowithBfr/Baseline",
    "hdf_file_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/spice_tau_reco/NuE_22083.h5",
    "hdf_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/spice_tau_reco",
    "nfiles" : 6987,
}

spice_tau_reco["NuMu_midE1"] = {
    "dataset" : "22043",
    "subfolders" : 
    ["0000000-0000999"],
    "flavor" : "NuMu",
    "reco_base_out_path" : "/data/ana/Diffuse/GlobalFit_Flavor/taupede/SnowStorm/RecowithBfr/Baseline",
    "hdf_file_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/spice_tau_reco/NuMu_22043.h5",
    "hdf_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/spice_tau_reco",
    "nfiles" : 675,
}

spice_tau_reco["NuMu_highE1"] = {
    "dataset" : "22044",
    "subfolders" : 
    ["0000000-0000999", "0001000-0001999", "0002000-0002999"],
    "flavor" : "NuMu",
    "reco_base_out_path" : "/data/ana/Diffuse/GlobalFit_Flavor/taupede/SnowStorm/RecowithBfr/Baseline",
    "hdf_file_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/spice_tau_reco/NuMu_22044.h5",
    "hdf_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/spice_tau_reco",
    "nfiles" : 2250,
}

spice_tau_reco["NuMu_midE2"] = {
    "dataset" : "22079",
    "subfolders" : 
    ["0000000-0000999", "0001000-0001999"],
    "flavor" : "NuMu",
    "reco_base_out_path" : "/data/ana/Diffuse/GlobalFit_Flavor/taupede/SnowStorm/RecowithBfr/Baseline",
    "hdf_file_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/spice_tau_reco/NuMu_22079.h5",
    "hdf_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/spice_tau_reco",
    "nfiles" : 1579,
}

spice_tau_reco["NuMu_highE2"] = {
    "dataset" : "22080",
    "subfolders" : 
    ["0000000-0000999", "0001000-0001999", "0002000-0002999","0003000-0003999", "0004000-0004999", "0005000-0005999"],
    "flavor" : "NuMu",
    "reco_base_out_path" : "/data/ana/Diffuse/GlobalFit_Flavor/taupede/SnowStorm/RecowithBfr/Baseline",
    "hdf_file_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/spice_tau_reco/NuMu_22080.h5",
    "hdf_path" : "/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/spice_tau_reco",
    "nfiles" : 5245,
}

# spice_tau_reco["MuonGun_lowE"] = {
#     "dataset" : "21317",
#     "subfolders" : 
#     ["0000000-0000999", "0001000-0001999", "0002000-0002999","0003000-0003999", "0004000-0004999", "0005000-0005999",
#      "0006000-0006999", "0007000-0007999", "0008000-0008999","0009000-0009999", "0010000-0010999", "0011000-0011999",
#      "0012000-0012999", "0013000-0013999", "0014000-0014999","0015000-0015999", "0016000-0016999", "0017000-0017999",
#      "0018000-0018999", "0019000-0019999"],
#     "flavor" : "MuonGun",
#     "reco_base_out_path" : "/data/ana/Diffuse/GlobalFit_Flavor/taupede/MuonGun/RecowithBfr",
#     'hdf_path' : '/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/spice_tau_reco',
# }

# spice_tau_reco["MuonGun_midE"] = {
#     "dataset" : "21316",
#     "subfolders" : 
#     ["0000000-0000999", "0001000-0001999", "0002000-0002999", "0003000-0003999", "0004000-0004999", "0005000-0005999",
#      "0006000-0006999", "0007000-0007999", "0008000-0008999", "0009000-0009999", "0010000-0010999", "0011000-0011999",
#      "0012000-0012999", "0013000-0013999", "0014000-0014999", "0015000-0015999", "0016000-0016999", "0017000-0017999",
#      "0018000-0018999", "0019000-0019999", "0020000-0020999", "0021000-0021999", "0022000-0022999", "0023000-0023999",
#      "0024000-0024999", "0025000-0025999", "0026000-0026999", "0027000-0027999", "0028000-0028999", "0029000-0029999",
#      "0030000-0030999", "0031000-0031999", "0032000-0032999", "0033000-0033999", "0034000-0034999", "0035000-0035999",
#      "0036000-0036999", "0037000-0037999", "0038000-0038999", "0039000-0039999"],
#     "flavor" : "MuonGun",
#     "reco_base_out_path" : "/data/ana/Diffuse/GlobalFit_Flavor/taupede/MuonGun/RecowithBfr",
#     'hdf_path' : '/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/spice_tau_reco',
# }

# spice_tau_reco["MuonGun_highE"] = {
#     "dataset" : "21315",
#     "subfolders" : 
#     ["0000000-0000999", "0001000-0001999", "0002000-0002999","0003000-0003999", "0004000-0004999", "0005000-0005999",
#      "0006000-0006999", "0007000-0007999", "0008000-0008999","0009000-0009999", "0010000-0010999", "0011000-0011999",
#      "0012000-0012999", "0013000-0013999", "0014000-0014999"],
#     "flavor" : "MuonGun",
#     "reco_base_out_path" : "/data/ana/Diffuse/GlobalFit_Flavor/taupede/MuonGun/RecowithBfr",
#     'hdf_path' : '/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/spice_tau_reco',
# }

###
### Reconstructed files by Neha
### Selection: VHESelfVeto == false, CausalQTot > 6000, no energy cut!!
### Name: spice_tau_reco, before: neha_spice
###

spice_tau_reco_ensemble = {}

spice_tau_reco_ensemble["NuTau_midE"] = {
    "dataset" : "22017",
    "subfolders" : 
    ["0000000-0000999", "0001000-0001999", "0002000-0002999", "0003000-0003999"],
    "flavor" : "NuTau",
    "reco_base_out_path" : "/data/ana/Diffuse/GlobalFit_Flavor/taupede/SnowStorm/RecowithBfr/Perturbed",
    'hdf_path' : '/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/spice_tau_reco_ensemble',
}

spice_tau_reco_ensemble["NuTau_highE"] = {
    "dataset" : "22018",
    "subfolders" : 
    ["0000000-0000999", "0001000-0001999", "0002000-0002999","0003000-0003999", "0004000-0004999", "0005000-0005999",
     "0006000-0006999", "0007000-0007999", "0008000-0008999","0009000-0009999", "0010000-0010999", "0011000-0011999",
     "0012000-0012999", "0013000-0013999", "0014000-0014999","0015000-0015999", "0016000-0016999", "0017000-0017999",
     "0018000-0018999"],
    "flavor" : "NuTau",
    "reco_base_out_path" : "/data/ana/Diffuse/GlobalFit_Flavor/taupede/SnowStorm/RecowithBfr/Perturbed",
    'hdf_path' : '/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/spice_tau_reco_ensemble',
}

spice_tau_reco_ensemble["NuE_midE"] = {
    "dataset" : "22014",
    "subfolders" : 
    ["0000000-0000999", "0001000-0001999", "0002000-0002999", "0003000-0003999"],
    "flavor" : "NuE",
    "reco_base_out_path" : "/data/ana/Diffuse/GlobalFit_Flavor/taupede/SnowStorm/RecowithBfr/Perturbed",
    'hdf_path' : '/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/spice_tau_reco_ensemble',
}

spice_tau_reco_ensemble["NuE_highE"] = {
    "dataset" : "22015",
    "subfolders" : 
    ["0000000-0000999", "0001000-0001999", "0002000-0002999","0003000-0003999", "0004000-0004999", "0005000-0005999",
     "0006000-0006999", "0007000-0007999", "0008000-0008999","0009000-0009999", "0010000-0010999", "0011000-0011999",
     "0012000-0012999", "0013000-0013999", "0014000-0014999","0015000-0015999", "0016000-0016999", "0017000-0017999",
     "0018000-0018999", "0019000-0019999"],
    "flavor" : "NuE",
    "reco_base_out_path" : "/data/ana/Diffuse/GlobalFit_Flavor/taupede/SnowStorm/RecowithBfr/Perturbed",
    'hdf_path' : '/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/spice_tau_reco_ensemble',
}

spice_tau_reco_ensemble["NuMu_midE"] = {
    "dataset" : "22011",
    "subfolders" : 
    ["0000000-0000999", "0001000-0001999", "0002000-0002999", "0003000-0003999", "0004000-0004999"],
    "flavor" : "NuMu",
    "reco_base_out_path" : "/data/ana/Diffuse/GlobalFit_Flavor/taupede/SnowStorm/RecowithBfr/Perturbed",
    'hdf_path' : '/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/spice_tau_reco_ensemble',
}

spice_tau_reco_ensemble["NuMu_highE"] = {
    "dataset" : "22012",
    "subfolders" : 
    ["0000000-0000999", "0001000-0001999", "0002000-0002999","0003000-0003999", "0004000-0004999", "0005000-0005999",
     "0006000-0006999", "0007000-0007999", "0008000-0008999","0009000-0009999", "0010000-0010999", "0011000-0011999",
     "0012000-0012999", "0013000-0013999", "0014000-0014999"],
    "flavor" : "NuMu",
    "reco_base_out_path" : "/data/ana/Diffuse/GlobalFit_Flavor/taupede/SnowStorm/RecowithBfr/Perturbed",
    'hdf_path' : '/data/user/tvaneede/GlobalFit/reco_processing/hdf/output/spice_tau_reco_ensemble',
}



