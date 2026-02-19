from icecube import dataio, icetray
import sys
import glob

def main():
    if len(sys.argv) < 2:
        print("Usage: python count_pframes.py <input.i3[.zst|.gz]>")
        return

    fname = sys.argv[1]
    p_count = 0

    print("*" in fname)

    if "*" in fname:
        infiles = sorted(glob.glob(fname))
        for infile in infiles:
            p_count_file = 0
            evt_ids = []
            f = dataio.I3File(infile)
            while f.more():
                frame = f.pop_frame()
                if frame.Stop == icetray.I3Frame.Physics:
                    p_count_file += 1
                    evt_ids.append(frame["I3EventHeader"].event_id)
            p_count += p_count_file
            print(f"{p_count_file} Physics (P) frames in file {infile} {evt_ids}")
        print("total", p_count)
    else:
        f = dataio.I3File(fname)
        while f.more():
            frame = f.pop_frame()
            if frame.Stop == icetray.I3Frame.Physics:
                p_count += 1
        print(f"{p_count} Physics (P) frames in file {fname}")

if __name__ == "__main__":
    main()