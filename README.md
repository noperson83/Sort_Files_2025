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
