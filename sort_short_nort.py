import os
import shutil
import hashlib
from datetime import datetime

# Optional: For AI photo classification (stub function for now)
def ai_classify_image(file_path):
    # TODO: Plug in AI model or API
    # Return something like "Family", "Travel", "Music", etc.
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
    # Add your custom rules for genre/project here
    # For photos, you could run AI classifier
    if file_type == "Photos" or file_type == "Videos":
        return ai_classify_image(file_path)
    # For code/art, maybe use parent folder as project
    parent = os.path.basename(os.path.dirname(file_path))
    return parent if parent else "Uncategorized"

def move_unique_files(source_folder, dest_folder):
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
                shutil.copy2(full_path, final_path)
                print(f"Copied: {full_path} -> {final_path}")

def main():
    print("Organize ALL your files by Year / Type / Project_or_Genre with deduplication and versioning.\n")
    source_folder = input("Enter the FULL path of your source folder: ").strip()
    dest_folder = input("Enter the FULL path for your new organized folder: ").strip()

    if not os.path.isdir(source_folder):
        print("Error: Source folder does not exist or is not accessible.")
        return

    os.makedirs(dest_folder, exist_ok=True)
    move_unique_files(source_folder, dest_folder)
    print("Done! Check your new folder structure.")

if __name__ == "__main__":
    main()
