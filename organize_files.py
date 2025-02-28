import os
import shutil
from datetime import datetime

# Get the user's home directory dynamically
user_home = os.path.expanduser("~")

# Define folders to scan
folders_to_scan = [
    os.path.join(user_home, "Desktop"),
    os.path.join(user_home, "Documents"),
    os.path.join(user_home, "Downloads"),
    os.path.join(user_home, "Pictures"),
    os.path.join(user_home, "Videos"),
    os.path.join(user_home, "Music"),
]

# Define subject-based categories
subject_categories = {
    "resume": ["resume", "cv", "curriculum vitae"],
    "taxes": ["tax", "irs", "w2", "1099"],
    "school": {
        "math": ["math", "algebra", "calculus"],
        "science": ["science", "biology", "chemistry", "physics"],
        "history": ["history", "world war", "civil war"],
        "english": ["essay", "literature", "writing"]
    },
    "lab work": {
        "matlab": [".m", "matlab"],
        "simulink": [".slx", "simulink"],
        "stateflow": [".sfx", "stateflow"]
    },
    "protocols": ["protocol", "experiment", "procedure"],
    "timecards": ["timecard", "timesheet", "work hours"]
}

# Define file type categories
extension_categories = {
    ".jpg": "Images",
    ".jpeg": "Images",
    ".png": "Images",
    ".gif": "Images",
    ".bmp": "Images",
    ".svg": "Images",
    ".tiff": "Images",

    ".mp4": "Videos",
    ".mkv": "Videos",
    ".mov": "Videos",
    ".avi": "Videos",
    ".flv": "Videos",

    ".mp3": "Music",
    ".wav": "Music",
    ".aac": "Music",
    ".flac": "Music",

    ".pdf": "Documents",
    ".docx": "Documents",
    ".doc": "Documents",
    ".xlsx": "Documents",
    ".xls": "Documents",
    ".pptx": "Documents",
    ".ppt": "Documents",
    ".txt": "Documents",

    ".zip": "Compressed",
    ".rar": "Compressed",
    ".tar": "Compressed",
    ".gz": "Compressed",

    ".exe": "Applications",
    ".msi": "Applications",

    ".m": "Lab Work/Matlab",
    ".slx": "Lab Work/Simulink",
    ".sfx": "Lab Work/Stateflow",
    ".py": "Programming/Python Scripts",
    ".ipynb": "Programming/Jupyter Notebooks",
}

def create_folder(path):
    """Create a folder if it doesn't exist."""
    os.makedirs(path, exist_ok=True)

def categorize_file(filename):
    """Categorize a file based on its extension."""
    _, extension = os.path.splitext(filename)
    return extension_categories.get(extension.lower(), "Other")

def find_subject_category(filename):
    """Find the subject category of a file."""
    file_lower = filename.lower()
    for subject, subcategories in subject_categories.items():
        if isinstance(subcategories, dict):  # Nested subcategories
            for subtopic, keywords in subcategories.items():
                if any(keyword in file_lower for keyword in keywords):
                    return os.path.join(subject, subtopic)
        else:
            if any(keyword in file_lower for keyword in subcategories):
                return subject
    return None  # No matching subject category

def move_file(file_path, destination_folder):
    """Move and rename files to avoid conflicts."""
    try:
        create_folder(destination_folder)

        # Add timestamp to filename to avoid overwriting files
        file_date = datetime.fromtimestamp(os.path.getmtime(file_path))
        new_filename = f"{file_date.strftime('%Y-%m-%d_%H-%M-%S')}-{os.path.basename(file_path)}"
        new_path = os.path.join(destination_folder, new_filename)

        shutil.move(file_path, new_path)
        print(f"Moved: {file_path} → {new_path}")
    except Exception as e:
        print(f"Error moving '{file_path}': {e}")

def organize_files():
    """Organize files across multiple folders."""
    for folder in folders_to_scan:
        if os.path.exists(folder):
            print(f"\n📂 Organizing files in: {folder}")

            files = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]

            for file in files:
                file_path = os.path.join(folder, file)

                # Check if the file belongs to a subject category
                subject_folder = find_subject_category(file)
                if subject_folder:
                    subject_path = os.path.join(folder, "Subjects", subject_folder)
                    move_file(file_path, subject_path)
                    continue  # Skip further classification

                # Otherwise, categorize by file type
                file_category = categorize_file(file)
                category_path = os.path.join(folder, "File Types", file_category)
                move_file(file_path, category_path)

    print("\n✅ All files have been organized successfully!")

if __name__ == "__main__":
    organize_files()
