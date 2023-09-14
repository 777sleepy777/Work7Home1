from pathlib import Path
import re
from pathlib import Path
import shutil
import sys

image_files = list()
video_files = list()
doc_files = list()
music_files = list()
archive_files = list()
other_files = list()
extensions = set()
unknown_extensions = set()

registred_extension = {
    'images': ('.jpeg', '.png', '.jpg', '.svg'),
    'video': ('.avi', '.mp4', '.mov', '.mkv'),
    'documents': ('.doc', '.docx', '.txt', '.pdf', '.xls', '.xlsx', '.pptx'),
    'audio': ('.mp3', '.ogg', '.wav', '.amr'),
    'archives': ('.zip', '.gz', '.tar')
}

UKRAINIAN_SYMBOLS = "абвгґдеєжзиіїйклмнопрстуфхцчшщьюя"
TRANSLATION = ("a", "b", "v", "g", "g", "d", "e", "je", "j", "z", "i", "i", "ji", "j", "k", "l", "m", "n", "o", 
               "p", "r", "s", "t", "u", "f", "h", "ts", "ch", "sh", "sch", "", "yu", "ya")
TRANS = {}

for key, value in zip(UKRAINIAN_SYMBOLS, TRANSLATION):
    TRANS[ord(key)] = value
    TRANS[ord(key.upper())] = value.upper()

def main():
    path = sys.argv[1]
    root_folder = Path(path)
    global main_folder

    #if len(sys.argv) < 2:
    #    print('Enter path to folder which should be cleaned')
    #    exit()

   
    #root_folder = Path("D:\Projects\My_repo\Work7Home\clean_folder\clean_folder\ff")

    if (not root_folder.exists()) or (not root_folder.is_dir()):
        print('Path incorrect')
        exit()

    main_folder = root_folder
    
    cleaner(root_folder)


def cleaner(folder: Path):
   
    for file in folder.iterdir():

        if file.is_file():
            scan(file)

        if file.is_dir():
            cleaner(file)
            if not any(file.iterdir()):
                file.rmdir()
                
def scan(file: Path):
    extension = file.suffix.lower()
    file_name = file.stem
    
    known_extensions = False
    for key, values in registred_extension.items():
        if extension in values:
            known_extensions = True
            normalized_name = normalize(file_name)
            new_name = normalized_name + extension
            end_folder = main_folder.joinpath(key)
            end_folder.mkdir(exist_ok=True)
            new_file_path = end_folder.joinpath(new_name)
    
            if key == 'images':
                image_files.append(file)
            elif key == 'video':
                video_files.append(file)
            elif key == 'documents':
                doc_files.append(file)
            elif key == 'audio':
                music_files.append(file)
            elif key == 'archives':
                archive_files.append(file)
            extensions.add(extension)
        
            try:
                file.rename(new_file_path)
            except FileExistsError:
                new_file_path = end_folder.joinpath(normalized_name + '_' + extension)
                file.rename(new_file_path)

            if key == 'archives':
                archive_dir = end_folder.joinpath(normalized_name)  
                archive_dir.mkdir(exist_ok=True)  
                shutil.unpack_archive(new_file_path, archive_dir)

    if not known_extensions: 
        other_files.append(file)
        unknown_extensions.add(extension)

def normalize(name: str) -> str:
    new_name = name.translate(TRANS)
    new_name = re.sub(r'\W', "_", new_name)
    return new_name

if __name__ == '__main__':
    #path = sys.argv[1]
    #arg = Path(path)
    #main(arg.resolve())
    main()
    print(f"images: {image_files}\nvideo:{video_files}\ndocuments: {doc_files}\n \
          audio: {music_files}\narchives: {archive_files}\nother: {other_files}\n \
          processed extensions: {extensions}\nunknown extensions: {unknown_extensions}")
    exit()