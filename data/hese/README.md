# Data hese

I am starting from the HESE events, already selected with proper GCD from Tianlu and Neha:
- /data/ana/Diffuse/GlobalFit_Flavor/taupede/data/Pass2/HESE

## versions

- v0: first test, one year, all reco with ibr and idc, and event generator. Not sure if I keep the right GCDs in the file for the ibr, idc, and eventgen reco. Not finished, cancelled by me.
- v1: stopping with ibr and idc, making it easy for myself

## 2022

Data taken from Emre's files, GCDs from:
- /data/exp/IceCube/2022/filtered/level2/IC86_2022_GoodRunInfo.txt

Stored in 
- GCD_2022.txt

## Livetime

With sum_livetimes.py. 368813893.34 exactly matches Neha, differs 1% with total from GRL. I add the 41473194.61 from Emre's processing.

```
        Runs              HESE (s)               GRL (s)    HESE versioned (s)     GRL versioned (s)
--------------------------------------------------------------------------------------------------------------
IC79_2010         1081           27110660.03           27131341.07                   N/A                   N/A
IC86_2011         1119           28803021.48           29520897.05                   N/A                   N/A
IC86_2012         1117           28067224.88           28317311.34                   N/A                   N/A
IC86_2013         1307           29927475.23           30819513.04                   N/A                   N/A
IC86_2014         1285           31370056.55           31526407.07                   N/A                   N/A
IC86_2015         1258           31349455.79           31557031.88                   N/A                   N/A
IC86_2016         1182           30661940.65           30827655.64                   N/A                   N/A
IC86_2017         1360           35161819.85           35504074.30           35161819.85           35504074.30
IC86_2018         1233           31621149.74           31865991.56           31621149.74           31865991.56
IC86_2019         1057           26598126.98           27068243.49           26598126.98           27068243.49
IC86_2020         1137           31158177.38           31212250.70           31158177.38           31212250.70
IC86_2021         1378           36984784.78           37209241.88           36984784.78           37209241.88
IC86_2022          N/A                   N/A           41473194.61                   N/A           41473194.61
--------------------------------------------------------------------------------------------------------------
TOTAL                           368813893.34          414033153.63          161524058.73          204332996.54
```

## Extra information

Official data IceCube:
- /data/exp/IceCube/{year}/filtered/{level}/ where level is level2, or level2pass2a before/during 2017

Neha’s Tau events
- /data/ana/Diffuse/GlobalFit_Flavor/taupede/data/Pass2/i3files/NoDeepCore/HESE12/Bfr/

All HESE events
- /data/ana/Diffuse/GlobalFit_Flavor/taupede/data/Pass2/HESE

Hese Events Emre 2022:
- /data/user/eyildizci/hese_tracks_processing/L5/IC86_2022
The files have couple additional keys like dnn classifier output, reco etc. but no cuts beyond hese cuts

