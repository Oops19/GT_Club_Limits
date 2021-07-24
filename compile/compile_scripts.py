from Utilities.unpyc3_compiler import Unpyc3PythonCompiler

# This function invocation will compile the files found within Scripts/s4cl_sample_mod_scripts, put them inside of a file named s4cl_sample_mod.ts4script, and it will finally place that ts4script file within <Project>/Release/S4CLSampleMod.
import os
import shutil

author = 'o19'
mod_name = 'GT_Clubs_Limits'

release_directory = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(os.getcwd()))), 'Release')
mod_base_directory = os.path.join(release_directory, mod_name)
ts4_directory = os.path.join(mod_base_directory, 'Mods', f"_{author}_")

os.makedirs(ts4_directory, exist_ok=True)
print(f"{ts4_directory}")

Unpyc3PythonCompiler.compile_mod(
    names_of_modules_include=('gt_club_limits', 'libraries'),
    folder_path_to_output_ts4script_to=ts4_directory,
    output_ts4script_name='gt_club_limits'
)

src_folder = os.path.join(os.path.dirname(os.path.abspath(os.getcwd())), 'release_info')
for folder in ['mod_data', 'mod_documentation']:
    try:
        shutil.copytree(os.path.join(src_folder, folder), os.path.join(mod_base_directory, folder))
    except:
        print(f"WARNING: Remove the folder {os.path.join(mod_base_directory, folder)} to update the data.")

shutil.make_archive(os.path.join(release_directory, f"{mod_name}"), 'zip', mod_base_directory)
print(f'Created {os.path.join(release_directory, f"{mod_name}.zip")}')