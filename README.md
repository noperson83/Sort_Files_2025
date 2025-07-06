# Sort_Files_2025

This project organizes files into a structured folder hierarchy. Files are
sorted by the year they were last modified, their type (e.g. Music, Photos),
and an inferred project or genre.

## Setup

Install the required Python packages using `requirements.txt`:

```bash
pip install -r requirements.txt
```

This installs [Google Cloud Vision](https://cloud.google.com/vision) and
[`opencv-python-headless`](https://pypi.org/project/opencv-python-headless/)
for extracting video frames.

## Usage

The script is run from the command line and accepts a source folder and
destination folder:

```bash
python sort_short_nort.py <source_folder> <dest_folder>
```

Additional options:

- `--move` – move files instead of copying them.
- `--dry-run` – print actions without modifying any files.

For example:

```bash
python sort_short_nort.py ~/Downloads ~/Organized --move
```

### Media renaming

When processing Photos and Videos the tool renames files based on the detected
project or genre and the file's modification timestamp. For example an image in
the "Vacation" category is copied as `Vacation_20240101_101500.jpg`. Other file
types keep their original names.

### Google Cloud Vision integration

Photo categories are inferred using the Google Cloud Vision API. Videos are
classified by sampling a few frames with OpenCV and sending those images to the
Vision API. The most common label among the frames is used for the video's
category. If classification fails, the tool falls back to the video's parent
folder name.
To enable image classification, install the Vision dependency (via the
requirements file) and provide credentials:

```bash
pip install -r requirements.txt  # installs google-cloud-vision
export GOOGLE_APPLICATION_CREDENTIALS=/path/to/your/service-account.json
```

On Windows set the variable in PowerShell or Command Prompt:

```powershell
$env:GOOGLE_APPLICATION_CREDENTIALS = "C:\path\service-account.json"
```

```cmd
set GOOGLE_APPLICATION_CREDENTIALS="C:\path\service-account.json"
```

`GOOGLE_APPLICATION_CREDENTIALS` must point to a service account JSON file with
access to the Vision API.

If classification returns no label or `Uncategorized`, the tool falls back to
using the file's parent folder name to determine the project or genre.
