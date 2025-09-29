import os, sys


datasets_snowstorm = {
  23460: {"flavor": "NuTau", "energy": "high"},
  23459: {"flavor": "NuTau", "energy": "mid"},
  23458: {"flavor": "NuTau", "energy": "low"},

  23457: {"flavor": "NuE", "energy": "high"},
  23456: {"flavor": "NuE", "energy": "mid"},
  23455: {"flavor": "NuE", "energy": "low"},

  23454: {"flavor": "NuMu", "energy": "high"},
  23453: {"flavor": "NuMu", "energy": "mid"},
  23452: {"flavor": "NuMu", "energy": "low"},
  23451: {"flavor": "NuMu", "energy": "lowlow"},

}

for dataset in datasets_snowstorm:
  cmd = f"python /data/user/tvaneede/GlobalFit/SnowStorm_systematics/iceprod_req_harvest/iceprod-requirements-harvesting/fetch_iceprod_stats.py logs data/{dataset}.hdf5 -d {dataset} -p 1"
  os.system(cmd)
