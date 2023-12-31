# Aston Attention Lapse Research Project

## Description

Our project aims to noninvasively track an operator's attention during assembly tasks using a multimodal dataset that includes gaze, head pose, sound detection, and visual recognition from various angles. Wearable eye-tracking glasses (Pupil Core) and multiple cameras with microphones (Azure Kinect DK) will capture the data.
These files were used to synchronize the two Azure Kinect Cameras as well as the Pupil Eye Core tracker, allowing for precise data recording.

## Getting Started

### Setup

* Ensure to follow https://github.com/pupil-labs/pupil guide on setup, it will provide all the necessary dependencies needed for this.

### Executing program

* Once the Pupil guide has been followed, you will then need to add these files into pupil/pupil_src
* Ensure the files have the correct paths;
   * recordGUI.py (script_path variable needs to be set to path/of/synchronization_script1.ps1)
   * record_capture.py (k4a_recorder_path variable needs to be set to path/of/k4arecorder.exe and python_command variable to PythonVersion/python.exe)
   * synchronization_script1.ps1 ($recordCommand and $stopCommand variable to PythonVersion/python.exe)
* Once all the relevant changes have been made, you will then need to ensure the Azure Kinect cameras are properly connected and synced up.
* Ensure Pupil Core Eye Tracker and Pupil Capture software is on.
* Once all setup, configured and ready, then open up RecordGUI and press Record to start recording both modalities simultaneously. 

## Help

If support is required, please raise an issue.

## Authors

Contributors names and contact info

Junaid Akhtar [LinkedIn](https://www.linkedin.com/in/junaid-akhtar-152baa1b7/)

Zhuangzhuang Dai [LinkedIn](https://www.linkedin.com/in/zhuangzhuang-dai-140566144/)

## Version History

* 0.1
    * Initial Release

## License

This project is licensed under the [MIT] License - see the LICENSE.md file for details
