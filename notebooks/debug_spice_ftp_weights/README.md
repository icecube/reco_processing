I have tried to understand why I saw different event rates with my ftp processing, compared to Neha's spice files.

Turns out
- Simulations ftp-v3 / spice match very well
- QFilterMask HESEFilter_15 only checks for the HESE_VHESelfVeto == false, and selects HESE_CausalQTot > 1500
- The ftp-v3 l3 files also contain files without HESE_VHESelfVeto and HESE_CausalQTot, then HESEFilter_15 condition failed
- In order to get the right selection, I should check if HESE_VHESelfVeto, HESE_CausalQTot are present, and then HESE_CausalQTot > 6000
- Also fine: jsut check for HESE_CausalQTot in file, and HESE_CausalQTot > 6000

Problems:
- Still unclear why the HESEFilter_15 has fewer events over the full HESE_CausalQTot spectrum 

I got it!! Turns out, the pid_neha scripts had an error, and just stopped after certain events. Stay away from Veto_SRTOfflinePulses or Veto_SRTInIcePulses in bdt_var. These variables were anyway not used.