# Data hese

I am starting from the HESE events, already selected with proper GCD from Tianlu and Neha:
- /data/ana/Diffuse/GlobalFit_Flavor/taupede/data/Pass2/HESE
This didn't work, so I did my own filtering in the `filter/` folder

## versions

- v0: first test, one year, all reco with ibr and idc, and event generator. Not sure if I keep the right GCDs in the file for the ibr, idc, and eventgen reco. Not finished, cancelled by me.
- v1: stopping with ibr and idc, making it easy for myself
- v2: I ran the reconstruction on my own processing of filtering, which was v2 filter
- v3: I copied v2 files, but removed runs where we had inactive strings, see active_string_requirement

## 2022

Data taken from Emre's files, GCDs from:
- /data/exp/IceCube/2022/filtered/level2/IC86_2022_GoodRunInfo.txt

Stored in 
- GCD_2022.txt

## Livetime

Calculated using active_string_requirement/sum_livetimes.py

Dataset              GRL   Bad_i3   Bad_it  ASR_fail     Pass         Total (s)        Bad_i3 (s)        Bad_it (s)      ASR_fail (s)          Pass (s)  Kept (%)
-----------------------------------------------------------------------------------------------------------------------------------------------------------------
Processing IC79_2010 (1084 runs) ...
IC79_2010           1084        0        0        3     1081       27131341.07              0.00              0.00          20681.04       27110660.03    99.92%
Processing IC86_2011 (1207 runs) ...
IC86_2011           1207        6        0       42     1159       29520897.05          89183.61              0.00         245390.43       29186323.01    98.87%
Processing IC86_2012 (1188 runs) ...
IC86_2012           1188        2        0       53     1133       28317311.34          29529.51              0.00         157336.90       28130444.93    99.34%
Processing IC86_2013 (1524 runs) ...
IC86_2013           1524        0        3      151     1370       30819513.04              0.00          86409.00         523580.96       30209523.08    98.02%
Processing IC86_2014 (1338 runs) ...
IC86_2014           1338        0        1       31     1306       31526407.07              0.00           1589.32          68426.93       31456390.82    99.78%
Processing IC86_2015 (1343 runs) ...
IC86_2015           1343        0        0       49     1294       31557031.88              0.00              0.00          79838.19       31477193.69    99.75%
Processing IC86_2016 (1247 runs) ...
IC86_2016           1247        0        0       46     1201       30827655.64              0.00              0.00         124069.78       30703585.86    99.60%
Processing IC86_2017 (1446 runs) ...
IC86_2017           1446        0        0       53     1393       35504074.30              0.00              0.00         146899.70       35357174.60    99.59%
Processing IC86_2018 (1304 runs) ...
IC86_2018           1304        0        0       41     1263       31865991.56              0.00              0.00         123830.47       31742161.09    99.61%
Processing IC86_2019 (1116 runs) ...
IC86_2019           1116        0        0       29     1087       27068243.49              0.00              0.00         289981.80       26778261.69    98.93%
Processing IC86_2020 (1152 runs) ...
IC86_2020           1152        0        0       11     1141       31212250.70              0.00              0.00          33122.11       31179128.59    99.89%
Processing IC86_2021 (1436 runs) ...
IC86_2021           1436        0        0       48     1388       37209241.88              0.00              0.00         182465.75       37026776.13    99.51%
Processing IC86_2022 (1597 runs) ...
IC86_2022           1597        0        0       29     1568       41473194.61              0.00              0.00          45516.53       41427678.08    99.89%
-----------------------------------------------------------------------------------------------------------------------------------------------------------------
TOTAL              16982        8        4      586    16384      414033153.63         118713.12          87998.32        2041140.59      411785301.60    99.46%

(GCD files read for borderline runs: 572)

### Attic, this is outdated, for v2, did not include active string requirement

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

