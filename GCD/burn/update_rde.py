from icecube import icetray, dataclasses, dataio
import pandas as pd
import os

def update_gcd( infile, outfile ):

    gcdfile_in = dataio.I3File(infile, "r")
    gcdfile_out = dataio.I3File(outfile, "w")
    while gcdfile_in.more():
        frame = gcdfile_in.pop_frame()
        if frame.Stop == icetray.I3Frame.Calibration:
            calitem = frame["I3Calibration"]
            cal_o = calitem.dom_cal
            for key, item in cal_o.items():
                if (item.relative_dom_eff) == 1.35:
                    item.relative_dom_eff = 1.374
                cal_o[key] = item
            calitem.dom_cal = cal_o
            frame.Delete("I3Calibration")
            frame["I3Calibration"] = calitem

        gcdfile_out.push(frame)

gcds_in = pd.read_csv( "/data/user/tvaneede/GlobalFit/reco_processing/burn/run_gcd_list.csv" )
outpath = "/data/user/tvaneede/GlobalFit/reco_processing/GCD/burn/output/"

new_gcds = {}
livetimes = {}

for run in gcds_in["RunNum"]:
    infile = gcds_in[ gcds_in["RunNum"] == run ]["GCD"].iloc[0]
    filename = os.path.basename(infile).replace(".i3.zst", "")
    outfile = f"{outpath}/{filename}_update_rde.i3.zst" 

    if run < 129500: continue

    update_gcd(infile = infile, outfile=outfile)
    new_gcds[run] = outfile
    livetimes[run] = gcds_in[ gcds_in["RunNum"] == run ]["LiveTime"].iloc[0]

    print(run, livetimes[run])
    # break


rows = [
    (run, new_gcds[run], livetimes[run])
    for run in sorted(new_gcds.keys())
]

# Create DataFrame from dict
df = pd.DataFrame(rows, columns=["RunNum", "GCD", "LiveTime"])
df = df.sort_values("RunNum")
df.to_csv("run_gcd_list_update_rde.csv", index=False)
