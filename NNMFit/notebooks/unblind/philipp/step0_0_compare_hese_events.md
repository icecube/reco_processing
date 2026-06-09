

# Summary

Only event I am missing in v2 compared to v1:
```
	dataset	run	event	reco_energy
0	IC86_2014	125914	75630389	72763.011514
```
where v1 is based on `/data/ana/Diffuse/GlobalFit_Flavor/taupede/data/Pass2/HESE`, which contains all HESE runs, empty for when no event was found. In v1:
```
dataio-shovel /data/ana/Diffuse/GlobalFit_Flavor/taupede/data/Pass2/HESE/IC86_2014/Run00125914.i3.zst
CausalQTot = 6000.12
```
In my v2 processing, it is just below threshold:
```
HESE_CausalQTot [I3PODHolder<double>]:
5994.3
```

The other way around, there is quite a bit missing in v1:

Neha folder all: `/data/ana/Diffuse/GlobalFit_Flavor/taupede/data/Pass2/HESE`
Neha folder event: `/data/ana/Diffuse/GlobalFit_Flavor/taupede/data/Pass2/i3files/NoDeepCore/HESE12/Bfr`

```
dataset	run	event	reco_energy	hese_causal_qtot	in_neha_all	in_neha_event comment
0	IC86_2011	119311	430943	3.269002e+05	14156.095864	False	False 
1	IC86_2011	119583	141609	5.709847e+04	6875.744233	False	False
2	IC86_2012	121947	7181486	7.449678e+04	9355.539456	True	False empty file, only GCD
3	IC86_2013	122752	41309299	1.482176e+05	19691.222671	False	True
4	IC86_2013	123770	442256	4.169044e+06	6157.379055	False	False
5	IC86_2013	122604	17469985	2.250298e+05	18581.193399	False	True
6	IC86_2014	126359	9400616	2.526825e+04	6008.448549	True	False, empty file, only GCD
7	IC86_2015	127751	927145	2.326454e+05	8745.913758	False	False
8	IC86_2020	134994	1103075	3.565653e+05	10871.700004	False	False
```

This is all quite messy, I don't even know which folder Neha used for her analysis. I will only compare my v2 processing with Neha's 60 TeV h5 file and see what's up. 

# Compare with Emre

Event 470241 of run 125826 in IC86_2014	seems to be missing from your processing. Both in:
```
/data/user/eyildizci/hese_tracks_processing/L5/IC86_2014/
```
and in 
```
/data/user/eyildizci/hese_tracks_processing/L5/new_IC86_2014/
```
This should be a good run, it is listed in: `/data/exp/IceCube/2014/filtered/level2pass2a/IC86_2014_GoodRunInfo.txt`

According to my processing, it has:
```
HESE_VHESelfVeto false
CausalQTot 37147
```

# Missing in my v2 processing

Two events from 2014 missing in my analysis compared to Emre. In run 125627 and 125914.

Both logs in `/scratch/tvaneede/reco/hese_data_filter/filter_dag_hese_data_v2` tell me:
```
less logs/IC86_2014_Run00125627.out
less logs/IC86_2014_Run00125914.out 
No HESE events found, skipping output
```

Only 125627 is missing in my v1 processing, which was based on the files in `/data/ana/Diffuse/GlobalFit_Flavor/taupede/data/Pass2/i3files/NoDeepCore/HESE12/Bfr`.

For 125627, I see in the good run list `/data/exp/IceCube/2014/filtered/level2pass2a/IC86_2014_GoodRunInfo.txt`: validated manually. Has lost files. It is also a short run of 4465.19 s. I am rechecking if I should have this event. I check Emre's file, and it's actually empty: `/data/user/eyildizci/hese_tracks_processing/L5/new_IC86_2014/Run00125627_MJD56987.i3.bz2`

Now for 125914. Emre's file has 1 event:
```
I3EventHeader [I3EventHeader]:
[ I3EventHeader:
        StartTime: 2015-01-14 17:51:02.181,645,208,4 UTC
         EndTime : 2015-01-14 17:51:02.181,664,546,4 UTC
           RunID : 125914
        SubrunID : 0
         EventID : 75630389
      SubEventID : 0
  SubEventStream : InIceSplit
]
```
but it has
```
HESE_CausalQTot [I3PODHolder<double>]:
5994.3
```
So I am not sure why he has it in the first place. But in Neha's file, it is:
```
dataio-shovel /data/ana/Diffuse/GlobalFit_Flavor/taupede/data/Pass2/i3files/NoDeepCore/HESE12/Bfr/IC86_2014/Run00125914_MJD57036_Taupede_out.i3.bz2 
CausalQTot 6000.12
```

So far no events missing in my processing!!
