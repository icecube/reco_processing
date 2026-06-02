from icecube import icetray, dataclasses, dataio
from icecube._frame_object_diff import (I3CalibrationDiff, I3DOMCalibrationDiff, I3DOMCalibrationMapDiff)

def get_dom_cal( gcd ):

    gcd_base = dataio.I3File(gcd)

    calib = None

    while gcd_base.more():
        frame = gcd_base.pop_frame()
        if frame.Has('I3Calibration'):
            calib = frame["I3Calibration"]

    dom_cal = calib.dom_cal

    return dom_cal

dom_cal_base = get_dom_cal( "/data/user/tvaneede/GlobalFit/reco_processing/GCD/GeoCalibDetectorStatus_2020.Run134142.Pass2_V0.i3.gz" )
dom_cal_chris = get_dom_cal( "/data/user/tvaneede/GlobalFit/reco_processing/GCD/gcd_pass2_rde.i3.gz" )

x = I3DOMCalibrationMapDiff( dom_cal_base, dom_cal_chris )