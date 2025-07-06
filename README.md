# Sort_Files_2025
This project organizes files into a structured folder hierarchy. Files are
sorted by the year they were last modified, their type (e.g. Music, Photos),
and an inferred project or genre.

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

Photo and video categories are inferred using the Google Cloud Vision API. To
enable this feature install the dependency and provide credentials:

```bash
pip install google-cloud-vision
export GOOGLE_APPLICATION_CREDENTIALS=/path/to/your/service-account.json
```

`GOOGLE_APPLICATION_CREDENTIALS` must point to a service account JSON file with
access to the Vision API.
