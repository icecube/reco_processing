import os, sys


datasets_tau_reco = {
  23436: {"flavor": "NuMu", "energy": "low", "true_dataset": 22646},
  23435: {"flavor": "NuMu", "energy": "mid", "true_dataset": 22645},
  23434: {"flavor": "NuMu", "energy": "high", "true_dataset": 22644},
  23433: {"flavor": "NuTau", "energy": "high", "true_dataset": 22635},
  23432: {"flavor": "NuTau", "energy": "mid", "true_dataset": 22634},
  23431: {"flavor": "NuTau", "energy": "low", "true_dataset": 22633},
  23430: {"flavor": "NuE", "energy": "low", "true_dataset": 22614},
  23429: {"flavor": "NuE", "energy": "mid", "true_dataset": 22613},
  23428: {"flavor": "NuE", "energy": "high", "true_dataset": 22612}
}

datasets_level4_6 = {
  23155: {"flavor": "NuMu", "energy": "low", "true_dataset": 22646},
  23154: {"flavor": "NuMu", "energy": "mid", "true_dataset": 22645},
  23153: {"flavor": "NuMu", "energy": "high", "true_dataset": 22644},
  23152: {"flavor": "NuTau", "energy": "high", "true_dataset": 22635},
  23151: {"flavor": "NuTau", "energy": "mid", "true_dataset": 22634},
  23150: {"flavor": "NuTau", "energy": "low", "true_dataset": 22633},
  23149: {"flavor": "NuE", "energy": "low", "true_dataset": 22614},
  23148: {"flavor": "NuE", "energy": "mid", "true_dataset": 22613},
  23147: {"flavor": "NuE", "energy": "high", "true_dataset": 22612}
}

for dataset in datasets_tau_reco:
  cmd = f"python /data/user/tvaneede/GlobalFit/SnowStorm_systematics/iceprod_req_harvest/iceprod-requirements-harvesting/fetch_iceprod_stats.py logs data/{dataset}.hdf5 -d {dataset} -p 1"
  os.system(cmd)
