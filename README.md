# HARPIA Dual Detection package
Performs simultaneous, not referenced, detection for HARPIA spectrometer, equipped with two linear array sensors.

## Requirements
 - Installed Light Conversion Launcher application. It is used to run this 
   script.
 - Installed and running HARPIA Service App, version 1.11 or greater. Connection 
   with the spectrograph must be successful.
 
## Configuration
 - Start the Launcher application
 - In 'Packages' tab, choose 'Add New Package' and select 'main.py' file 
   of this package
 - The 'HARPIA REST' should be indicated as connected at '127.0.0.1' under the
   'Required connections'. If not, check HARPIA Service App and choose 'Refresh'
   in 'Connections' tab
 - Run the HARPIA Dual Detection script using the Launcher application
   by clicking 'Start'

## Operation
### Continuous acquisition
Click 'START/STOP CONTINUOUS ACQUISITION' to start/stop preview of the WLSc and 
transient absorption signals.

### Preset measurement
Configure and select a corresponding Transient Absorption measurement
preset in HARPIA Service App. In script, click 'START/STOP PRESET MEASUREMENT'
to start the measurement. Two files (`YYYYYMMDD_HHmm_detV.dat` and `YYYYYMMDD_HHmm_detH.dat`)
will be created in the folder, indacatd in 'Working directory` field.

### Calibration
- Without any sample (for measurement or calibration) inserted, click 'Measure WLSc without ref'
- Add the calibration sample and click `Measure WLSc with ref'
- Click 'CALIBRATE' to finish the calibration. The calibration report will be produced in 
  a seperate window.