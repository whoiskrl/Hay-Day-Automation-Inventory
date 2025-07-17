# HayDay-Farm-Automation

A Python script designed to automate certain tasks within the Hay Day Android game, specifically focused on managing farm profiles and taking screenshots of barn contents. This automation leverages `uiautomator2` for device interaction and `opencv` for image processing.

## Features ✨

* **Profile Management**: Automatically switches between Hay Day farm profiles by manipulating `shared_prefs` on the Android device.
* **App Control**: Opens and closes the Hay Day application as needed.
* **Color Detection**: Waits for a specific pixel color to appear on the screen, indicating a certain game state (e.g., barn loaded).
* **Automated Screenshots**: Captures full-screen and cropped screenshots of the farm/barn.
* **Profile Archiving**: Moves processed farm profiles to a "COMPLETED" directory.

## Requirements 🛠️

To run this script, you'll need:

* An **Android emulator** (e.g., NoxPlayer, BlueStacks, Android Studio Emulator) or a physical Android device.
* **ADB (Android Debug Bridge)** installed and configured on your system.
* **Root access** on your Android device/emulator is required for `shared_prefs` manipulation.
* **Python 3.x** installed.
* **`uiautomator2`** service installed on your Android device (the `u2.connect()` function usually handles this, but manual installation might be needed if issues arise).
* **Hay Day bot farm** barn must be in default place , where it was placed originally by game , if you don't know where it is located, check the example_farm.png in repository.
* ** Hay Day game_config.csv** [edit those if not yet - MaxZoom,150,, , DefaultZoom,25,, , MinZoom,25,, and extraMargin -600] , otherwise bot won't recognize the position of barn.

## Installation ⚙️

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/YourUsername/HayDay-Farm-Automation.git](https://github.com/YourUsername/HayDay-Farm-Automation.git)
    cd HayDay-Farm-Automation
    ```

2.  **Install Python dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Set up `uiautomator2` on your Android device/emulator:**
    Ensure your device is connected via ADB and `uiautomator2` is installed. You can typically do this by running `python -m uiautomator2 init` after connecting your device.

## Configuration 🔧

Before running the script, modify the following variables in `BarnV2.py` as per your setup:

* `device_id`: Replace `"emulator-5556"` with your Android device's ID (e.g., `adb devices` to find it).
* `PROFILES_DIR`: The directory on your Android device where your farm profiles are stored.
* `COMPLETED_DIR`: The directory on your Android device where processed profiles will be moved.
* `profile_folders`: Customize the list of your farm profile names.

   **Example for `PROFILES_DIR` and `COMPLETED_DIR` setup on Android:**
    You'll need to create these directories on your Android device's root or `/data/data` partition (which requires root access).
    For example, using `adb shell su -c 'mkdir -p /data/data/android/KRL/PROFILES'`

## Usage ▶️

1.  **Prepare your Android device/emulator**:
    * Ensure ADB debugging is enabled.
    * Grant root permissions to ADB if prompted, or ensure your emulator is rooted.
    * Place your Hay Day profiles in the `PROFILES_DIR` on your device. Each profile should be a folder containing the `shared_prefs` files for that farm.

2.  **Run the script:**
    ```bash
    python BarnV2.py
    ```

The script will automate the process of loading each farm, waiting for the barn to load (indicated by a specific pixel color), taking a screenshot, and moving the profile.

## Troubleshooting ⚠️

* **`Could not read the image`**: Ensure screenshots are being captured and pulled correctly. Check ADB connection and device permissions.
* **`Permission denied` for `rm` or `cp`**: This usually means you don't have proper root access or the `su` command isn't working as expected on your device.
* **Color detection issues**: The `target_color` and `pixel_x`, `pixel_y` coordinates might need adjustment based on your device's resolution or changes in the game's UI. You can use a tool to get the RGB values of pixels on your emulator screen.
* **App crashes/freezes**: Increase `time.sleep()` durations if the script is running too fast for your device to keep up.

## Contributing 🤝

Feel free to open issues or submit pull requests if you have suggestions for improvements or bug fixes.

## License 📄

This project is licensed under the [MIT License](LICENSE)
