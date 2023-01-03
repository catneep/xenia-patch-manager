import os
from shutil import copyfile

import tomlkit as toml
from natsort import natsorted

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

def parse_toml(path: str) -> dict | None:
  file_data = None
  try:
    with open(path, "rb") as file:
      file_data = toml.load(file)
  except PermissionError as e:
    print(
      "## Permission Error (Most likely file doesn't exist)",
      e,
      "Returning file_data=:",
      file_data, sep= '\n\t')
  return file_data

def get_toml_patches(toml: dict | None) -> dict:
  if not toml:
    return {}
  toml_data = {}
  for patch_data in toml["patch"]:
    patch = Patch(patch_data["name"], patch_data)
    toml_data[patch_data["name"]] = patch
  return toml_data

def save_toml(path: str, data: dict) -> bool:
  print('Parsed data:', str(data)[:50])
  print('Data written:', toml.dumps(data), sep= '\n')
  try:
    with open(path, "w") as file:
      file.write(toml.dumps(data))
    print('Data saved!')
    return True
  except Exception as e:
    print(f'IO error:', e)
  return False

def backup_file(filepath: str) -> str | None:
  if not (os.path.exists(filepath)):
    print('Source file does not exist')
    return None
  
  filepath = os.path.realpath(filepath).replace('\\','/')
  path = os.path.dirname(filepath)
  name = os.path.splitext(os.path.basename(filepath))[0]
  backup_dest = f'{path}/{name}.bak'

  try:
    copyfile(
      src= filepath,
      dst= backup_dest
    )

    return backup_dest
  except:
    print('IO Error')
    return None
