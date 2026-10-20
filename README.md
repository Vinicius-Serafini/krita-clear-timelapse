# Clean Krita Timelapse Frames

`clean_timelapse.py` removes mostly white or blank frames from an image sequence and renumbers the remaining images. It is intended for a folder of frames exported from a Krita timelapse.

## Requirements

- Python 3
- Pillow

Install Pillow with:

```bash
python -m pip install Pillow
```

## Usage

Run the script with the path to the folder containing the frames:

```bash
python clean_timelapse.py "path/to/frames"
```

For example, on Windows:

```powershell
python .\clean_timelapse.py "C:\path\to\frames"
```

## What it does

1. Looks for `.png`, `.jpg`, and `.jpeg` files directly in the specified folder (it does not scan subfolders).
2. Creates a timestamped `backup_YYYYMMDD_HHMMSS` folder inside the target folder and copies all matching images into it, preserving file metadata. If that name already exists, a numeric suffix is added.
3. Sorts the filenames alphabetically and checks each image's average grayscale brightness.
4. Deletes images with an average brightness greater than `250` on a scale of `0` (black) to `255` (white).
5. Renames the remaining images sequentially, starting at `0000000` and preserving each file's extension (converted to lowercase).

Images that cannot be read are reported and left in place. If the folder does not exist, the script reports that and exits. If the backup cannot be completed, the script reports the error and does not delete or rename any images.

## Important

The script deletes frames it identifies as mostly white and renames the remaining files in place after backing up all matching images. The backup contains the images as they were before processing; it does not include other files in the target folder.
