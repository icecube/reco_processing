Scripts taken from 
- Globalfit cascades: /home/pfuerst/software/analysis/GP_globalfit/muon_KDEs/produce_Muongun_kde.ipynb
- HESE copy from neha: /data/user/nlad/NNMFitStuff/KDE_pfuerst.ipynb
- HESE my own iteration: hese_muons_kde.ipynb. Turns out I miss one event that Neha had:
36	21316	2914	0	21574.159645	1.354741	1.713973e-09	3.599342e-09
For me reconstructed below 60 TeV, for Neha at 138 TeV. Giving a factor 4.5/5 increase in the total rate. So my muon template is a factor 4.5/5 too small. I make another iteration, scaling the weights up by 4.5

- Turns out Neha made a mistake. You don't scale the Muonweights up with 2.1, you compare the muon weights with the number of tagged muons in https://journals.aps.org/prd/pdf/10.1103/PhysRevD.104.022002?casa_token=58sqMWLHsc0AAAAA%3ArZ02R5g8rVUUV-AJW5qPgqWepJhiGpKa90hdWQ7dDFuExNzBDdHOmaKyATm-YBFGjU-MQG3onXcRg-sR, and then you have an additional factor 2.1 scaling. That is now implemented in hese_muons_paper.ipynb. It was actually quite close to my scaled muon template.