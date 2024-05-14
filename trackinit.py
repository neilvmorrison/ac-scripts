import os
import json
import bpy
import configparser

config = configparser.ConfigParser()

def create_blender_file(filename):
  bpy.ops.wm.new_mainfile()
  bpy.ops.mesh.primitive_cube_add(size=2)
  bpy.context.object.location = (0, 0, 0)
  bpy.ops.wm.save_as_mainfile(filepath=filename)

def create_ui_json_file(file_details):
  return

def create_file(directory, filename, content = "Initialize your configs here!"):
  filepath = os.path.join(directory, filename)
  with open(filepath, 'w', ) as newfile:
    newfile.write(content)

def create_dir(root, dirname):
  new_dir = os.path.join(root, dirname)
  try:
    os.makedirs(new_dir)
    return new_dir
  except FileExistsError:
    print(f"You already have a project at {dirname}")
    return new_dir
  except Exception as e:
    print(f"An error occurred: {e}")
    return None
  
def create_structure(root_dir, structure, trackname):
  for item in structure:
    if isinstance(item, str):
      filename = f"{trackname}.kn5" if item == "trackname.kn5" else item
      create_file(root_dir, filename)
    elif isinstance(item, dict):
      for dirname, content in item.items():
        dir = trackname if dirname == "trackname" else dirname
        new_dir = create_dir(root_dir, dir)
        if new_dir:
          create_structure(new_dir, content, trackname)

def main():
  dir_path = os.getcwd()
  conf_file_path = os.path.join(dir_path, 'config.ini')
  config.read(conf_file_path)
  mod_root = config.get('directories', 'track_mods_root')
  struct_file_path = os.path.join(dir_path, 'project_structure.json')

  structure = {}
  with open(struct_file_path, 'r') as structfile:
    structure = json.load(structfile)


  track_name = input("Enter the name of your track: ").strip()
  formatted_track_name = track_name.replace(' ', '_').lower()
  project_root_dir = os.path.join(mod_root, formatted_track_name + "_project")
  create_structure(project_root_dir, structure, formatted_track_name)
  print(f"Project initialized at {project_root_dir}")

main()