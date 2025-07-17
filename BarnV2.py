import subprocess
import cv2
import numpy as np
import time
import uiautomator2 as u2
import os
import shutil
from datetime import datetime

device_id = "emulator-5556"  # Replace with your actual device ID
d = u2.connect(device_id)

PROFILES_DIR = "/data/data/android/KRL/PROFILES"
SHARED_PREFS_DIR = "/data/data/com.supercell.hayday/shared_prefs"
COMPLETED_DIR = "/data/data/android/KRL/COMPLETED"
hayday_package_name = "com.supercell.hayday"
hayday_activity_name = "com.supercell.hayday.GameApp"

profile_folders = [f"jacky{i if i > 1 else ''}" for i in range(1, 11)]

def tap(x, y):
    d.click(x, y)
    print(f"Tapped at ({x}, {y})")

def swipe(start_x, start_y, end_x, end_y, duration=0.13):
    d.swipe(start_x, start_y, end_x, end_y, duration)
    print(f"Swiped from ({start_x}, {start_y}) to ({end_x}, {end_y}) with duration {duration}")

def open_app(package_name, activity_name):
    cmd = f"adb -s {device_id} shell am start -n {package_name}/{activity_name}"
    subprocess.run(cmd, shell=True)
    print(f"Opened app {package_name}/{activity_name}")
    time.sleep(1)

def kill_app(package_name):
    cmd = f"adb -s {device_id} shell am force-stop {package_name}"
    subprocess.run(cmd, shell=True)
    print(f"Killed app {package_name}")

def capture_screenshot(filename):
    cmd = f"adb -s {device_id} shell screencap -p /sdcard/{filename}.png"
    subprocess.run(cmd, shell=True)
    cmd = f"adb -s {device_id} pull /sdcard/{filename}.png"
    subprocess.run(cmd, shell=True)
    print(f"Captured screenshot {filename}.png")
    time.sleep(0.5)

def get_pixel_color(image_path, x, y):
    image = cv2.imread(image_path)
    if image is None:
        print(f"Could not read the image: {image_path}")
        return None
    return image[y, x]

def color_similarity_percentage(color1, color2):
    max_distance = np.sqrt(3 * (255 ** 2))
    distance = np.linalg.norm(np.array(color1) - np.array(color2))
    return (1 - distance / max_distance) * 100

def clear_shared_prefs():
    # Remove everything in shared_prefs using root
    subprocess.run(f"adb -s {device_id} shell su -c 'rm -rf {SHARED_PREFS_DIR}/*'", shell=True)
    print("Cleared shared_prefs on device.")
    time.sleep(2)

def copy_profile_to_shared_prefs(profile_folder):
    src = f"{PROFILES_DIR}/{profile_folder}"  # <-- Add slash here
    dst = SHARED_PREFS_DIR
    # Remove everything in shared_prefs
    subprocess.run(f"adb -s {device_id} shell su -c 'rm -rf {dst}/*'", shell=True)
    # Copy profile files to shared_prefs
    subprocess.run(f"adb -s {device_id} shell su -c 'cp -r {src}/* {dst}/'", shell=True)
    time.sleep(2)

def move_profile_to_completed(profile_folder):
    src = f"{PROFILES_DIR}/{profile_folder}"  # <-- Add slash here
    dst = f"{COMPLETED_DIR}/{profile_folder}"
    # Move the profile folder to COMPLETED using root
    subprocess.run(f"adb -s {device_id} shell su -c 'mv {src} {dst}'", shell=True)
    print(f"Moved {profile_folder} to COMPLETED on device.")
    time.sleep(2)

def crop_screenshot(input_path, output_path, crop_x, crop_y, width, height):
    img = cv2.imread(input_path)
    if img is None:
        print(f"Could not open {input_path}")
        return
    cropped = img[crop_y:crop_y+height, crop_x:crop_x+width]
    cv2.imwrite(output_path, cropped)
    print(f"Cropped image saved to {output_path}")

target_color = [165, 74, 0]  # Target color in BGR format
pixel_x, pixel_y = 630, 454  # Coordinates of the pixel to check

cycle_round = 1

start_time = time.time()

for idx, profile_folder in enumerate(profile_folders):
    print(f"Processing farm: {profile_folder}")

    # 1. Clear shared_prefs
    clear_shared_prefs()

    # 2. Copy profile to shared_prefs
    copy_profile_to_shared_prefs(profile_folder)
    print(f"Copied {profile_folder} to shared_prefs.")
    time.sleep(1.5)

    # 3. Open Hay Day 
    open_app(hayday_package_name, hayday_activity_name)
    time.sleep(1.5)

    # 5. Wait for color match or timeout
    color_matched = False
    color_start_time = time.time()
    while True:
        time.sleep(1)
        capture_screenshot("screen")
        offsets = [(-1, -1), (0, 0), (1, 1), (1, 0), (0, 1), (-1, 0), (0, -1), (-1, 1), (1, -1)]
        detected_colors = {}
        for dx, dy in offsets:
            x, y = pixel_x + dx, pixel_y + dy
            color = get_pixel_color("screen.png", x, y)
            if color is not None:
                detected_colors[(x, y)] = color[::-1]  # Convert BGR to RGB
        for pos, color in detected_colors.items():
            print(f"Detected color at {pos}: RGB {color}")
        current_color = detected_colors.get((pixel_x, pixel_y), None)
        if current_color is not None:
            similarity = color_similarity_percentage(current_color, target_color)
            print(f"Color similarity: {similarity:.2f}%")
            if similarity > 80:
                print(f"Color matched {similarity:.2f}% with {target_color}")
                time.sleep(3)
                color_matched = True
                break
        if time.time() - color_start_time > 30:
            kill_app(hayday_package_name)
            time.sleep(1)
            open_app(hayday_package_name, hayday_activity_name)
            time.sleep(1)
            color_start_time = time.time()
            continue

    time.sleep(0.5)
    time.sleep(1)
    tap(440, 90)
    time.sleep(1)

    # 6. Take screenshot with unique name (profile folder name)
    current_date = datetime.now().strftime("%d.%m.%Y")
    screenshot_name = f"{profile_folder}_{current_date}"
    capture_screenshot(screenshot_name)
    time.sleep(1)
    print("BARN LOADED/SCREENSHOTED")
    time.sleep(1.5)

    # Crop the screenshot and save as farm name
    crop_screenshot(
        f"{screenshot_name}.png",
        f"{profile_folder}_cropped.png",
        crop_x=129,
        crop_y=72,
        width=359-129,
        height=373-72
    )

    # 7. Move profile to COMPLETED
    move_profile_to_completed(profile_folder)
    print(f"Moved {profile_folder} to COMPLETED.")

    # 8. Kill Hay Day app after finishing a farm
    kill_app(hayday_package_name)
    print(f"Finished processing {profile_folder}.\n")
    time.sleep(1)

elapsed_time = time.time() - start_time
minutes = int(elapsed_time // 60)
seconds = int(elapsed_time % 60)
print(f"All farms have been processed. Total time: {minutes} minutes and {seconds} seconds.")