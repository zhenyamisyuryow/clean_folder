import sys
import shutil
import zipfile
import re
from pathlib import Path
import os

base_folders = ['images', 'videos', 'documents', 'music', 'archives']
EXTENSIONS = {
    'images': ['.jpg', '.jpeg', '.png', '.svg'],
    'videos': ['.mp4', '.avi', '.mov', '.mkv'],
    'documents': ['.txt', '.docx','.doc', '.pdf', '.xlsx', '.pptx'],
    'music': ['.mp3', '.ogg', '.wav', '.amr'],
    'archives': ['.zip', '.gz', '.tar']
}
CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
            "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")
TRANS = {}
for c, t in zip(CYRILLIC_SYMBOLS, TRANSLATION):
    TRANS[ord(c)] = t
    TRANS[ord(c.upper())] = t.upper()


summary = {"images": [],
           "videos":[],
           "documents": [],
           "music": [],
           "archives": [],
           "known_extensions": [],
           "unknown_extensions": []}


def create_folders(path):
    for folder in base_folders:
        f_path = path / folder
        f_path.mkdir(exist_ok=True)

def normalize(item):
    new_name = re.sub(r'\W','_', item.stem.translate(TRANS))
    if item.is_file():
        new_name = new_name + item.suffix
    return item.with_name(new_name)

def process_archives(archives_path):
    arch_path = Path(archives_path)
    for i in arch_path.iterdir():
        try:
            shutil.unpack_archive(i, arch_path/i.stem)
        except:
            print("Archive is broken or format is invalid.")
            continue


def parse_folder(path):
    main_path = Path(sys.argv[1])
    for item in path.iterdir():
        normalize(item)
        if item.is_file():
            extension = item.suffix.lower()
            for category, extensions in EXTENSIONS.items():
                if extension in extensions:
                    summary[category].append(item.name)
                    summary["known_extensions"].append(item.suffix)
                    target_path = main_path / category
                    shutil.move(item, target_path)
                    break
            else:
                if not extension in extensions:
                    summary["unknown_extensions"].append(item.suffix)
                if path != main_path:
                    shutil.move(item, main_path)
        elif item.is_dir() and item.name not in base_folders:
            parse_folder(item)
            try:
                item.rmdir()
            except OSError:
                pass
    return summary


def main():
    if len(sys.argv) < 2:
        print("Path hasn't been provided. Please provide path parameter.")
        return
    folder_path = Path(sys.argv[1])

    create_folders(folder_path)
    parse_folder(folder_path)
    process_archives(folder_path/'archives')

if __name__ == '__main__':
    main()