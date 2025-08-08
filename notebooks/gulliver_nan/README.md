I found a nan error in the gulliver minimizer: 

/scratch/tvaneede/reco/run_taupede_tianlu/v3/reco_dag_v3_22634_0000000-0000999/logs/NuGenCCNC.022634.000001.i3.zst.err 

WARN (I3Gulliver): (TaupedeFit_iMIGRAD_PPB0) minimizer attempts llh calculation with par[6]=nan after 154 proper calls and 0 NAN-ish calls (I3Gulliver.cxx:51 in void I3Gulliver::NANParError(const std::vector<double>&))
WARN (I3Gulliver): (TaupedeFit_iMIGRAD_PPB0) minimizer attempts llh calculation with par[6]=nan after 154 proper calls and 1 NAN-ish calls (I3Gulliver.cxx:51 in void I3Gulliver::NANParError(const std::vector<double>&))
WARN (I3Gulliver): (TaupedeFit_iMIGRAD_PPB0) minimizer attempts llh calculation with par[6]=nan after 154 proper calls and 2 NAN-ish calls (I3Gulliver.cxx:51 in void I3Gulliver::NANParError(const std::vector<double>&))
WARN (I3Gulliver): (TaupedeFit_iMIGRAD_PPB0) minimizer attempts llh calculation with par[6]=nan after 154 proper calls and 3 NAN-ish calls (I3Gulliver.cxx:51 in void I3Gulliver::NANParError(const std::vector<double>&))
WARN (I3Gulliver): (TaupedeFit_iMIGRAD_PPB0) minimizer attempts llh calculation with par[6]=nan after 154 proper calls and 4 NAN-ish calls (I3Gulliver.cxx:51 in void I3Gulliver::NANParError(const std::vector<double>&))
WARN (I3Gulliver): (TaupedeFit_iMIGRAD_PPB0) minimizer attempts llh calculation with par[6]=nan after 154 proper calls and 5 NAN-ish calls (I3Gulliver.cxx:51 in void I3Gulliver::NANParError(const std::vector<double>&))
WARN (I3Gulliver): (TaupedeFit_iMIGRAD_PPB0) minimizer attempts llh calculation with par[6]=nan after 154 proper calls and 6 NAN-ish calls (I3Gulliver.cxx:51 in void I3Gulliver::NANParError(const std::vector<double>&))
WARN (I3Gulliver): (TaupedeFit_iMIGRAD_PPB0) minimizer attempts llh calculation with par[6]=nan after 154 proper calls and 7 NAN-ish calls (I3Gulliver.cxx:51 in void I3Gulliver::NANParError(const std::vector<double>&))
WARN (I3Gulliver): (TaupedeFit_iMIGRAD_PPB0) minimizer attempts llh calculation with par[6]=nan after 154 proper calls and 8 NAN-ish calls (I3Gulliver.cxx:51 in void I3Gulliver::NANParError(const std::vector<double>&))
WARN (I3Gulliver): (TaupedeFit_iMIGRAD_PPB0) minimizer attempts llh calculation with par[6]=nan after 154 proper calls and 9 NAN-ish calls (I3Gulliver.cxx:51 in void I3Gulliver::NANParError(const std::vector<double>&))
WARN (I3Gulliver): (TaupedeFit_iMIGRAD_PPB0) (Further NAN attempts will not be reported individually) (I3Gulliver.cxx:58 in void I3Gulliver::NANParError(const std::vector<double>&))
NOTICE (I3Tray): I3Tray finishing... (I3Tray.cxx:525 in void I3Tray::Execute(bool, unsigned int))
WARN (I3SimpleFitter): (SPEFitSingle) Saw no events with at least one good fit. (I3SimpleFitter.cxx:527 in virtual void I3SimpleFitter::Finish())
WARN (I3IterativeFitter): (SPEFit2) Saw no events with at least one good fit. (I3IterativeFitter.cxx:591 in virtual void I3IterativeFitter::Finish())
ERROR (I3Gulliver): (TaupedeFit_iMIGRAD_PPB0) nr. of improper llh fcn calls (NAN parameters)by minimizer iminuit: 71. You should investigate this, it is very likely that something is screwed up. (I3Gulliver.cxx:36 in virtual I3Gulliver::~I3Gulliver())

here i am doing my due dillingence