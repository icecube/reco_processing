# Active String Requirement Check

Checks the active string requirement for HESE reco runs, inspired by `checkRuns()` in `makedag.py` (tyuan).

## What it checks

For each reco run file in `output/<version>/<dataset>/Taupede/`:

1. Extracts the run number from the filename.
2. Looks up the run in the GoodRunInfo file to get the GCD path.
3. Reads `BadDomsList` from the GCD file and checks:
   - **≥ 83 active strings** — strings with at least one working in-ice DOM (OMs 1–60, excluding IceTop OMs 61–66).
   - **No inactive outer-layer strings** — the 28 outer-layer strings must all be active.

GoodRunInfo paths:
- `>= 2017`: `/data/exp/IceCube/{year}/filtered/level2/{config}_{year}_GoodRunInfo.txt`
- `< 2017`: `/data/exp/IceCube/{year}/filtered/level2pass2a/{config}_{year}_GoodRunInfo.txt`

## Usage

```bash
./run.sh                                        # all datasets, version v2, Taupede
./run.sh --version v1
./run.sh --datasets IC86_2016 IC86_2017         # specific datasets
./run.sh --reco-type EvtGen
```

Output is printed to stdout and also saved to `check_active_strings.log`.

## Output

A per-dataset table listing each run with columns:

| Column | Description |
|---|---|
| `GRL_Active` | Active string count from the GoodRunInfo file |
| `GCD_Active` | Active string count computed from the GCD `BadDomsList` |
| `Inactive_OL` | Number of inactive outer-layer strings |
| `Pass` | `PASS` / `FAIL` / `N/A` (if GCD could not be read) |
| `Error` | Error message if the check failed |

Followed by a summary table over all datasets.

## Notes

- Requires icetray (`run.sh` sets up the environment via `icetray-shell`).
- Some GCD files contain `BadDomsList` entries with `string == 0` (null/sentinel OMKeys); these are silently skipped.
- The outer-layer string set matches the definition in `makedag.py`: `{1–7, 13, 14, 21, 22, 30, 31, 40, 41, 50, 51, 59, 60, 67, 68, 72–78}`.

## Output

./run.sh 
Processing IC79_2010 ...

--- IC79_2010 (6 runs) ---
         Run  GRL_Active  GCD_Active   Inactive_OL    Pass  Error
  ---------------------------------------------------------------
      115994          79          86             0    PASS  
      116528          79          86             0    PASS  
      116698          79          86             0    PASS  
      117371          79          86             0    PASS  
      117782          79          86             0    PASS  
      118145          79          86             0    PASS  
Processing IC86_2011 ...

--- IC86_2011 (21 runs) ---
         Run  GRL_Active  GCD_Active   Inactive_OL    Pass  Error
  ---------------------------------------------------------------
      118178          86          86             0    PASS  
      118283          86          86             0    PASS  
      118381          86          86             0    PASS  
      118435          86          86             0    PASS  
      118545          86          86             0    PASS  
      118549          86          86             0    PASS  
      118602          86          86             0    PASS  
      118607          86          86             0    PASS  
      119196          86          86             0    PASS  
      119214          86          86             0    PASS  
      119311          64          64            10    FAIL  
      119316          86          86             0    PASS  
      119352          86          86             0    PASS  
      119404          86          86             0    PASS  
      119470          86          86             0    PASS  
      119474          86          86             0    PASS  
      119583          85          85             0    PASS  
      119595          86          86             0    PASS  
      119674          86          86             0    PASS  
      119842          86          86             0    PASS  
      120045          86          86             0    PASS  
Processing IC86_2012 ...

--- IC86_2012 (9 runs) ---
         Run  GRL_Active  GCD_Active   Inactive_OL    Pass  Error
  ---------------------------------------------------------------
      120398          86          86             0    PASS  
      120421          86          86             0    PASS  
      120638          86          86             0    PASS  
      120844          86          86             0    PASS  
      120867          86          86             0    PASS  
      121240          86          86             0    PASS  
      121679          86          86             0    PASS  
      121947          86          86             0    PASS  
      122152          86          86             0    PASS  
Processing IC86_2013 ...

--- IC86_2013 (16 runs) ---
         Run  GRL_Active  GCD_Active   Inactive_OL    Pass  Error
  ---------------------------------------------------------------
      122604          85          85             1    FAIL  
      122649          86          86             0    PASS  
      122752          85          85             0    PASS  
      123217          86          86             0    PASS  
      123326          86          86             0    PASS  
      123770          47          47            15    FAIL  
      123867          86          86             0    PASS  
      123986          86          86             0    PASS  
      124098          86          86             0    PASS  
      124244          86          86             0    PASS  
      124256          86          86             0    PASS  
      124333          86          86             0    PASS  
      124455          86          86             0    PASS  
      124571          86          86             0    PASS  
      124625          86          86             0    PASS  
      124648          86          86             0    PASS  
Processing IC86_2014 ...

--- IC86_2014 (15 runs) ---
         Run  GRL_Active  GCD_Active   Inactive_OL    Pass  Error
  ---------------------------------------------------------------
      124852          86          86             0    PASS  
      124927          86          86             0    PASS  
      125071          86          86             0    PASS  
      125335          86          86             0    PASS  
      125365          86          86             0    PASS  
      125826          86          86             0    PASS  
      125975          86          86             0    PASS  
      125979          86          86             0    PASS  
      126090          86          86             0    PASS  
      126099          86          86             0    PASS  
      126283          86          86             0    PASS  
      126307          86          86             0    PASS  
      126320          86          86             0    PASS  
      126359          86          86             0    PASS  
      126367          86          86             0    PASS  
Processing IC86_2015 ...

--- IC86_2015 (9 runs) ---
         Run  GRL_Active  GCD_Active   Inactive_OL    Pass  Error
  ---------------------------------------------------------------
      126406          86          86             0    PASS  
      126838          86          86             0    PASS  
      126865          86          86             0    PASS  
      127210          86          86             0    PASS  
      127225          86          86             0    PASS  
      127339          86          86             0    PASS  
      127751          47          47            15    FAIL  
      127762          86          86             0    PASS  
      127853          86          86             0    PASS  
Processing IC86_2016 ...

--- IC86_2016 (43 runs) ---
         Run  GRL_Active  GCD_Active   Inactive_OL    Pass  Error
  ---------------------------------------------------------------
      128027          86          86             0    PASS  
      128224          86          86             0    PASS  
      128239          86          86             0    PASS  
      128290          86          86             0    PASS  
      128340          86          86             0    PASS  
      128557          86          86             0    PASS  
      128582          86          86             0    PASS  
      128619          86          86             0    PASS  
      128672          86          86             0    PASS  
      128695          86          86             0    PASS  
      128747          86          86             0    PASS  
      128766          86          86             0    PASS  
      128767          86          86             0    PASS  
      128773          86          86             0    PASS  
      128782          86          86             0    PASS  
      128809          86          86             0    PASS  
      128814          86          86             0    PASS  
      128903          86          86             0    PASS  
      128952          86          86             0    PASS  
      128973          86          86             0    PASS  
      129004          86          86             0    PASS  
      129019          86          86             0    PASS  
      129031          86          86             0    PASS  
      129047          86          86             0    PASS  
      129112          86          86             0    PASS  
      129135          86          86             0    PASS  
      129155          86          86             0    PASS  
      129157          86          86             0    PASS  
      129165          86          86             0    PASS  
      129170          86          86             0    PASS  
      129174          86          86             0    PASS  
      129253          86          86             0    PASS  
      129281          86          86             0    PASS  
      129313          86          86             0    PASS  
      129316          86          86             0    PASS  
      129317          86          86             0    PASS  
      129374          86          86             0    PASS  
      129402          86          86             0    PASS  
      129456          86          86             0    PASS  
      129474          86          86             0    PASS  
      129497          86          86             0    PASS  
      129504          86          86             0    PASS  
      129510          86          86             0    PASS  
Processing IC86_2017 ...

--- IC86_2017 (18 runs) ---
         Run  GRL_Active  GCD_Active   Inactive_OL    Pass  Error
  ---------------------------------------------------------------
      129541          86          86             0    PASS  
      129678          86          86             0    PASS  
      129866          86          86             0    PASS  
      129997          86          86             0    PASS  
      130111          86          86             0    PASS  
      130126          86          86             0    PASS  
      130171          86          86             0    PASS  
      130219          86          86             0    PASS  
      130241          86          86             0    PASS  
      130275          86          86             0    PASS  
      130322          86          86             0    PASS  
      130492          86          86             0    PASS  
      130561          86          86             0    PASS  
      130590          86          86             0    PASS  
      130730          86          86             0    PASS  
      130932          86          86             0    PASS  
      130937          86          86             0    PASS  
      130949          86          86             0    PASS  
Processing IC86_2018 ...

--- IC86_2018 (16 runs) ---
         Run  GRL_Active  GCD_Active   Inactive_OL    Pass  Error
  ---------------------------------------------------------------
      131404          86          86             0    PASS  
      131408          86          86             0    PASS  
      131502          86          86             0    PASS  
      131505          86          86             0    PASS  
      131624          86          86             0    PASS  
      131680          86          86             0    PASS  
      131913          86          86             0    PASS  
      131999          86          86             0    PASS  
      132077          86          86             0    PASS  
      132143          86          86             0    PASS  
      132216          86          86             0    PASS  
      132229          86          86             0    PASS  
      132379          86          86             0    PASS  
      132518          86          86             0    PASS  
      132587          86          86             0    PASS  
      132628          86          86             0    PASS  
Processing IC86_2019 ...

--- IC86_2019 (18 runs) ---
         Run  GRL_Active  GCD_Active   Inactive_OL    Pass  Error
  ---------------------------------------------------------------
      132765          86          86             0    PASS  
      132886          86          86             0    PASS  
      132992          86          86             0    PASS  
      133002          86          86             0    PASS  
      133062          86          86             0    PASS  
      133089          86          86             0    PASS  
      133132          86          86             0    PASS  
      133340          86          86             0    PASS  
      133428          86          86             0    PASS  
      133436          86          86             0    PASS  
      133601          86          86             0    PASS  
      133611          86          86             0    PASS  
      133685          86          86             0    PASS  
      133715          86          86             0    PASS  
      133974          86          86             0    PASS  
      133997          86          86             0    PASS  
      134004          86          86             0    PASS  
      134086          86          86             0    PASS  
Processing IC86_2020 ...

--- IC86_2020 (10 runs) ---
         Run  GRL_Active  GCD_Active   Inactive_OL    Pass  Error
  ---------------------------------------------------------------
      134533          86          86             0    PASS  
      134599          86          86             0    PASS  
      134758          86          86             0    PASS  
      134866          86          86             0    PASS  
      134912          86          86             0    PASS  
      134994          47          47            15    FAIL  
      135113          86          86             0    PASS  
      135136          86          86             0    PASS  
      135196          86          86             0    PASS  
      135302          86          86             0    PASS  
Processing IC86_2021 ...

--- IC86_2021 (12 runs) ---
         Run  GRL_Active  GCD_Active   Inactive_OL    Pass  Error
  ---------------------------------------------------------------
      135504          86          86             0    PASS  
      135747          86          86             0    PASS  
      135946          86          86             0    PASS  
      136027          86          86             0    PASS  
      136160          86          86             0    PASS  
      136348          86          86             0    PASS  
      136368          86          86             0    PASS  
      136673          86          86             0    PASS  
      136692          86          86             0    PASS  
      136768          86          86             0    PASS  
      136876          86          86             0    PASS  
      136889          86          86             0    PASS  
Processing IC86_2022 ...

--- IC86_2022 (19 runs) ---
         Run  GRL_Active  GCD_Active   Inactive_OL    Pass  Error
  ---------------------------------------------------------------
      136918          86          86             0    PASS  
      136985          86          86             0    PASS  
      137007          86          86             0    PASS  
      137160          86          86             0    PASS  
      137167          86          86             0    PASS  
      137489          86          86             0    PASS  
      137512          86          86             0    PASS  
      137527          86          86             0    PASS  
      137661          86          86             0    PASS  
      137786          86          86             0    PASS  
      137845          86          86             0    PASS  
      137891          86          86             0    PASS  
      137930          86          86             0    PASS  
      138035          86          86             0    PASS  
      138065          86          86             0    PASS  
      138069          86          86             0    PASS  
      138125          86          86             0    PASS  
      138134          86          86             0    PASS  
      138611          86          86             0    PASS  

======================================================================
SUMMARY
======================================================================
  Dataset           Total    Pass    Fail  Missing  Errors
  --------------------------------------------------------
  IC79_2010             6       6       0        0  
  IC86_2011            21      20       1        0  
  IC86_2012             9       9       0        0  
  IC86_2013            16      14       2        0  
  IC86_2014            15      15       0        0  
  IC86_2015             9       8       1        0  
  IC86_2016            43      43       0        0  
  IC86_2017            18      18       0        0  
  IC86_2018            16      16       0        0  
  IC86_2019            18      18       0        0  
  IC86_2020            10       9       1        0  
  IC86_2021            12      12       0        0  
  IC86_2022            19      19       0        0  
  --------------------------------------------------------
  TOTAL               212     207       5        0
======================================================================