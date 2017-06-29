# pupil_labs_screen_calib
A proof of concept HMD calibration app for a pupil-labs eye tracker, based on hmd_eyes/hmd_calibration_client. Designed to calibrate a fixed-head eyetracker against a screen. 

## Requirements
- python3
- pip install zmq PyQt5 msgpack-python

## Usage
First run the pupil labs pupil_capture GUI separately, and make sure the two eye sources are connected to the right inputs. Then launch the app:
```
python main.py
```
 
