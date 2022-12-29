import os
from shutil import copyfile

import tomlkit as toml
from natsort import natsorted, ns

from Models.Patch import Patch

def get_toml_files(path: str) -> tuple:
  results = []
  files_in_directory = natsorted(
    os.listdir(path),
    # Using name w/o code as key
    key=lambda name: name.lower()[name.find('-') + 1:].strip()
  )

  for file in files_in_directory:
      if file.endswith('.patch.toml'):
          results.append(file)
  return tuple(results)

def parse_toml(path: str) -> dict:
  file_data = None
  with open(path, "rb") as file:
    file_data = toml.load(file)
  return file_data

def get_toml_patches(toml: dict) -> dict:
  toml_data = {}
  for patch_data in toml["patch"]:
    patch = Patch(patch_data["name"], patch_data)
    toml_data[patch_data["name"]] = patch
  return toml_data

def save_toml(path: str, data: dict) -> bool:
  print('Data to write:', str(data)[:50])
  print('Saving', toml.dumps(data))
  try:
    with open(path, "w") as file:
      file.write(toml.dumps(data))
    print('saved')
    return True
  except Exception as e:
    print(f'IO error:', e)
  return False

def backup_file(filepath: str) -> str | None:
  if not (os.path.exists(filepath)):
    return None
  
  filepath = os.path.realpath(filepath).replace('\\','/')
  path = os.path.dirname(filepath)
  name = os.path.splitext(os.path.basename(filepath))[0]
  backup_dest = f'{path}/{name}.bak'

  copyfile(
    src= filepath,
    dst= backup_dest
  )

  return backup_dest
