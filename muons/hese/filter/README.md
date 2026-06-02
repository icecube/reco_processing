# filtering of muons hese

## versions

-v0
-v1
-v2: I removed the s frame of empty files, thus removing the muongun StaticSurfaceInjector. I added that now again. I think it is important for weighting. Something is wrong. In v1, I had many events double. In v2 I don't seem to have any events. My file is empty:
output/v2/21315/HESE_21315_0000000-0000999.i3.zst. Neha has /data/ana/Diffuse/GlobalFit_Flavor/taupede/MuonGun/RecowithBfr/hdf_files/NoDeepCore/AllHESE/21315_Tracks_0000000-0000999.hdf5.
-v3: In v2 I accidentally only processed 500 frames. I removed that number.
-v4: I am not sure what is going on, but I am missing events. Let's try again, not saving the s frames, and printing which events I am taking.