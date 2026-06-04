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

# Missing in Neha i3 files

Not even sure if it is Neha's i3 files, because they don't match her h5 files perfectly. 

The three missing events (compared to Emre) are
```
0	IC86_2013	122604
1	IC86_2013	122752
2	IC86_2014	125627
```
where the last one was not an actual event. Just an empty file in Emre's processing. The two events in 2013 actually have sizable energies and QTot
```
	dataset	run	event	reco_energy	qtot
37	IC86_2013	122752	41309299	1.482176e+05	19691.222671
37	IC86_2013	122752	41309299	1.482176e+05	19691.222671
```

When I look into her h5 files,

# Events missing/changing after energy cut

## IC86_2011

Run 11931, event 430943