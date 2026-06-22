

# Summary

My processings
- v1: reconstructed files in `/data/ana/Diffuse/GlobalFit_Flavor/taupede/data/Pass2/HESE/`
- v2: did my own filtering in filter/output/v2. Turns out I didn't know about the active string requirement
- v3: include the active string requirement. Based on v2 filtering, manually removed events

Highlights:
- 188 HESE events
- 110 after 60 TeV energy cut
- 19 extra HESE events in 2022, 12 after energy cut

## Compare v3 with v1

Only event I am missing in v3 compared to v1:
```
	dataset	run	event	reco_energy
0	IC86_2014	125914	75630389	72763.011514
```
In v1:
```
dataio-shovel /data/ana/Diffuse/GlobalFit_Flavor/taupede/data/Pass2/HESE/IC86_2014/Run00125914.i3.zst
CausalQTot = 6000.12
```
but in my processing 5994.3. One is calculated by the online filter, another by Neha's script. I use the online filter in data and simulations.

The other way around, there is quite a bit missing in v1:

```
dataset	run	event	reco_energy	hese_causal_qtot
0	IC86_2011	119583	141609	57098.471286	6875.744233
1	IC86_2012	121947	7181486	74496.777368	9355.539456
2	IC86_2013	122752	41309299	148217.639644	19691.222671
3	IC86_2014	126359	9400616	25268.249814	6008.448549
```

They were forgetting in the processing of `/data/ana/Diffuse/GlobalFit_Flavor/taupede/data/Pass2/HESE/`.

## Compare with Neha hd5 (HESE12) files

v3 events (after cut) not in HESE12: 15 (12 in 2022, 3 in overlapping dataset)
dataset	run	event	reco_energy	hese_causal_qtot
0	IC86_2012	121947	7181486	74496.777368	9355.539456
1	IC86_2014	125826	470241	416499.030804	38785.083770
2	IC86_2016	128672	38561326	83136.722946	7517.631427


HESE12 events not in v3 (after cut): 2
run	event	reco_energy
0	125914	75630389	70976.904502
1	127210	51027948	60806.979712
