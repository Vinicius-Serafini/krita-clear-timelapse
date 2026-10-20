import os
import argparse
import shutil
from datetime import datetime
from PIL import Image, ImageStat


def is_mostly_white(filepath, threshold=250):
    """Detects if an image is white using an average brightness threshold."""
    try:
        with Image.open(filepath) as img:
            # Convert to Greyscale (L mode) to get brightness easily
            stat = ImageStat.Stat(img.convert('L'))
            average_brightness = stat.mean[0]
            
            # If average is > threshold (e.g. 250/255), it's a white frame
            return average_brightness > threshold
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return False


def create_backup(target_folder, filenames):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_folder = os.path.join(target_folder, f"backup_{timestamp}")
    suffix = 1
    while os.path.exists(backup_folder):
        backup_folder = os.path.join(target_folder, f"backup_{timestamp}_{suffix}")
        suffix += 1

    try:
        os.makedirs(backup_folder)
        for filename in filenames:
            shutil.copy2(
                os.path.join(target_folder, filename),
                os.path.join(backup_folder, filename),
            )
    except OSError as e:
        print(f"Backup failed: {e}")
        print(f"No images were changed. Partial backup, if any, is at: {backup_folder}")
        return None

    print(f"Backup created: {backup_folder}")
    return backup_folder


def clean_timelapse(target_folder):
    # Support both PNG and JPG
    valid_extensions = ('.png', '.jpg', '.jpeg')

    if not os.path.isdir(target_folder):
        print(f"Folder not found: {target_folder}")
        return

    # 1. Gather all image files
    all_files = sorted([f for f in os.listdir(target_folder) 
                       if f.lower().endswith(valid_extensions)
                       and os.path.isfile(os.path.join(target_folder, f))])

    if all_files and create_backup(target_folder, all_files) is None:
        return
    
    remaining_files = []

    print("Step 1: Removing white/blank frames...")
    for filename in all_files:
        path = os.path.join(target_folder, filename)
        if is_mostly_white(path):
            print(f"Deleting: {filename} (White frame detected)")
            os.remove(path)
        else:
            remaining_files.append(filename)

    # 2. Re-index remaining files to 0000000.png/jpg
    print(f"\nStep 2: Re-indexing {len(remaining_files)} images...")
    for index, filename in enumerate(remaining_files):
        old_path = os.path.join(target_folder, filename)
        
        # Keep original extension
        ext = os.path.splitext(filename)[1].lower()
        new_filename = f"{index:07d}{ext}"
        new_path = os.path.join(target_folder, new_filename)

        if old_path != new_path:
            # Use a temporary name if the file already exists to avoid collisions
            if os.path.exists(new_path):
                temp_path = new_path + ".tmp"
                os.rename(old_path, temp_path)
                os.rename(temp_path, new_path)
            else:
                os.rename(old_path, new_path)

    print("Process complete!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("path", help="Path to the folder")
    args = parser.parse_args()
    clean_timelapse(args.path)