Scripts taken from 
- Globalfit cascades: /home/pfuerst/software/analysis/GP_globalfit/muon_KDEs/produce_Muongun_kde.ipynb
- HESE copy from neha: /data/user/nlad/NNMFitStuff/KDE_pfuerst.ipynb
- HESE my own iteration: hese_muons_kde.ipynb. Turns out I miss one event that Neha had:
36	21316	2914	0	21574.159645	1.354741	1.713973e-09	3.599342e-09
For me reconstructed below 60 TeV, for Neha at 138 TeV. Giving a factor 4.5/5 increase in the total rate. So my muon template is a factor 4.5/5 too small. I make another iteration, scaling the weights up by 4.5