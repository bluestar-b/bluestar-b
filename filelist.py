import os
import json
import stat
import time

def get_file_metadata(file_path):
    try:
        file_stats = os.stat(file_path)
        file_metadata = {
            'file': file_path.lstrip('./'),
            'size': file_stats.st_size,
            'permissions': oct(file_stats.st_mode & 0o777),
            'last_modified': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(file_stats.st_mtime)),
            'type': 'directory' if os.path.isdir(file_path) else 'regular file'
        }
        return file_metadata
    except Exception as e:
        return None

def gather_file_metadata(root_dir):
    file_metadata_list = []
    for root, dirs, files in os.walk(root_dir):
        if '.git' in root:
            continue
        for file_name in files:
            file_path = os.path.join(root, file_name)
            metadata = get_file_metadata(file_path)
            if metadata:
                file_metadata_list.append(metadata)
    return file_metadata_list

if __name__ == '__main__':
    root_directory = '.'
    file_metadata = gather_file_metadata(root_directory)
    with open('file_list.json', 'w') as json_file:
        json.dump(file_metadata, json_file, indent=4)
