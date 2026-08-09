# Coincident Events

Two HESE events were flagged as coincident and stored separately from the main event selection:

```
/data/ana/Diffuse/GlobalFit_Flavor/taupede/data/Pass2/i3files/NoDeepCore/HESE12/Bfr/coinc/
├── Run00131680_MJD58422_0_Taupede_out.i3.bz2   →  Run 131680, Event 66412090
└── Run00132143_MJD58519_0_Taupede_out.i3.bz2   →  Run 132143, Event 36142391
```

## Notebook

[`coincident_events.ipynb`](coincident_events.ipynb) checks whether both events appear in:

- `HESE12.hdf5` — the reference HESE12 event selection
- `EvtGen_merged.h5` — our v3 processing output

and prints a table of Run, Event, RecoETot, and HESE_CausalQTot for each.

Both events are present in both files. Summary:

| Source | Run | Event | RecoETot (GeV) | HESE_CausalQTot |
|---|---|---|---|---|
| HESE12.hdf5 | 131680 | 66412090 | 201,392 | 17,246 |
| EvtGen_merged.h5 | 131680 | 66412090 | 225,256 | 15,959 |
| HESE12.hdf5 | 132143 | 36142391 | 190,087 | 9,295 |
| EvtGen_merged.h5 | 132143 | 36142391 | 199,361 | 6,855 |

Note: HESE12.hdf5 does not store `HESE_CausalQTot` directly — the notebook uses `Homogenized_QTot` as a proxy for that file.
