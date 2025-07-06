import os
import shutil
import hashlib
from datetime import datetime
import argparse

from google.cloud import vision

# Optional: For AI photo classification using Google Cloud Vision
def ai_classify_image(file_path):
    """Return the first label from Google Cloud Vision label detection."""
    print("Calling Vision API on:", file_path)
    response = None
    try:
        client = vision.ImageAnnotatorClient()
        with open(file_path, "rb") as image_file:
            content = image_file.read()
        image = vision.Image(content=content)
        response = client.label_detection(image=image)
        labels = response.label_annotations
        if labels:
            return labels[0].description
    except Exception as e:
        print("Vision API classification error:", e)
        if response and getattr(response, "error", None) and getattr(response.error, "message", None):
            print("Vision API error message:", response.error.message)
    return "Uncategorized"

def get_file_hash(file_path, chunk_size=8192):
    sha256 = hashlib.sha256()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(chunk_size), b''):
            sha256.update(chunk)
    return sha256.hexdigest()

def infer_year(file_path):
    try:
        mtime = os.path.getmtime(file_path)
        return datetime.fromtimestamp(mtime).strftime('%Y')
    except Exception:
        return "UnknownYear"

def infer_type(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    if ext in ['.mp3', '.wav', '.flac', '.aac']:
        return "Music"
    elif ext in ['.jpg', '.jpeg', '.png', '.gif', '.bmp']:
        return "Photos"
    elif ext in ['.mp4', '.mov', '.avi', '.mkv']:
        return "Videos"
    elif ext in ['.psd', '.ai', '.svg']:
        return "Art"
    elif ext in ['.py', '.js', '.ts', '.rb']:
        return "Code"
    elif ext in ['.html', '.css', '.json', '.xml']:
        return "Web"
    else:
        return "Other"

def infer_project_or_genre(file_path, file_type):
    """Infer the project or genre for the given file."""
    parent = os.path.basename(os.path.dirname(file_path))

    result = ""
    if file_type in ("Photos", "Videos"):
        # Run classifier and store result
        result = ai_classify_image(file_path)
        print("Vision API result:", result)

    if not result or result == "Uncategorized":
        # Fallback to the parent folder name when classification fails
        result = parent if parent else "Uncategorized"

    return result

def generate_media_filename(file_path, file_type, project_or_genre):
    ts = datetime.fromtimestamp(os.path.getmtime(file_path)).strftime("%Y%m%d_%H%M%S")
    name, ext = os.path.splitext(os.path.basename(file_path))
    if file_type in ("Photos", "Videos"):
        clean_proj = project_or_genre.replace(" ", "_")
        return f"{clean_proj}_{ts}{ext}"
    return name + ext

def move_unique_files(source_folder, dest_folder, move_files=False, dry_run=False):
    hash_dict = {}
    for root, dirs, files in os.walk(source_folder):
        for filename in files:
            if filename.startswith('.') or filename.lower().startswith('._'):
                continue  # skip dotfiles
            full_path = os.path.join(root, filename)
            file_hash = get_file_hash(full_path)

            # Detect duplicate by content
            if file_hash in hash_dict:
                continue  # skip exact duplicate

            hash_dict[file_hash] = full_path

            year = infer_year(full_path)
            file_type = infer_type(full_path)
            project_or_genre = infer_project_or_genre(full_path, file_type)

            # Build target path: /YEAR/TYPE/PROJECT_OR_GENRE/filename
            target_dir = os.path.join(dest_folder, year, file_type, project_or_genre)
            os.makedirs(target_dir, exist_ok=True)

            # Handle versioning if a file with same name but different content exists
            if file_type in ("Photos", "Videos"):
                base_filename = generate_media_filename(full_path, file_type, project_or_genre)
            else:
                base_filename = filename
            final_path = os.path.join(target_dir, base_filename)
            version = 1
            while os.path.exists(final_path):
                # If the content is the same, it's already copied, so skip
                if get_file_hash(final_path) == file_hash:
                    break
                # Otherwise, rename to add version
                name, ext = os.path.splitext(base_filename)
                final_path = os.path.join(target_dir, f"{name}_v{version}{ext}")
                version += 1
            else:
                action = "Moved" if move_files else "Copied"
                if dry_run:
                    print(f"[DRY RUN] {action}: {full_path} -> {final_path}")
                else:
                    if move_files:
                        shutil.move(full_path, final_path)
                    else:
                        shutil.copy2(full_path, final_path)
                    print(f"{action}: {full_path} -> {final_path}")

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Organize files by Year/Type/Project with optional deduplication "
            "and versioning"
        )
    )
    parser.add_argument("source_folder", help="Path of the source folder")
    parser.add_argument("dest_folder", help="Path for the organized output")
    parser.add_argument(
        "--move",
        action="store_true",
        help="Move files instead of copying them",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show actions without writing any files",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    if not os.path.isdir(args.source_folder):
        print("Error: Source folder does not exist or is not accessible.")
        return

    os.makedirs(args.dest_folder, exist_ok=True)
    move_unique_files(
        args.source_folder,
        args.dest_folder,
        move_files=args.move,
        dry_run=args.dry_run,
    )
    print("Done! Check your new folder structure.")

if __name__ == "__main__":
    main()
