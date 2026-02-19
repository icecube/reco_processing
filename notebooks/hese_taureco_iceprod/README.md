# hese taureco iceprod

## compare_local_iceprod
In taureco_iceprod_v2 I think I have been missing files in my hdf: it tells me I combined x files, but I actually got less because I had my print statement after removing corrupted files. Use:
```
runs = simulation_datasets["taureco_iceprod_v2"]["NuMu_midE"]["hdf_file"]["I3EventHeader"]["Run"]
num_unique_runs = len(set(runs))
print(num_unique_runs)
```
Then the number of events match perfectly with my local processing.

Everythings matches quite nicely!

Even in taureco_iceprod v3 we have the same problem. Studying this further in a separate notebook. 

## compare statistics

already with v2, so not everything yet, we have about a factor 2 more events than the spice analysis

              astro_NuE astro_NuMu astro_NuTau
spice-v3.2.1   65680.00   46848.00    58597.00
ftp-v3        101152.00   83000.00   104742.00

## study_muons

Without 60 TeV cut:
total events thijs 1180
total events neha: 46.0
With 60 TeV cut:
total events neha: 20.0

what was wrong? probably many things. running hese filter with 500 frames, merging and duplicating the same hdf file multiple times
Now fixed in taureco_iceprod_v3.