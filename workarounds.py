from os import listdir, path
import platform

def list_dir(directory):
    directory_structure_raw = listdir(proccess_path(directory))
    directory_structure_new = {
        'folders': [],
        'files': [],
        'executables': []
    }
    for i in directory_structure_raw:
        full_path = f"{directory}{seperator()}{i}"
        print(full_path)
        if path.isdir(full_path):
            directory_structure_new['folders'].append(i)
        if i.split('.')[-1] in ['exe', 'msi']:
            directory_structure_new['executables'].append(i)
            continue

        if path.isfile(full_path):
            directory_structure_new['files'].append(i)

    return directory_structure_new


def proccess_path(path):
    system = platform.system()
    if system == "Windows":
        if path.endswith(':'):
            return path.replace(':', ':\\')
        else:
            return path
    else: return path

def seperator() -> str:
    system = platform.system()
    if system == "Windows":
        return "\\"
    else: return "/"

def get_drives():
    system = platform.system()
    if system == "Windows":
        drive_list = []
        for drive in range(ord('A'), ord('Z')):
            if path.exists(chr(drive) + ':'):
                drive_list.append(chr(drive))
        return drive_list
    else: return "/"