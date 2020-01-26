import csv
from pathlib import Path
from zipfile import ZipFile
import os
import shutil

PACKAGE_PATH = "P:/PATH/TO/PROJECT/SRC/"
GRADEBOOK_CSV_PATH = "P:/PATH/TO/CSV.csv"
LAB_SECTIONS = ["L2M", "L2N"]

# Add/replace package name in java file


def correct_package(filepath, package_name):
    try:
        lines = open(filepath).read().splitlines()
        no_package_name = True
        # Search first 5 lines for a package statement
        if len(lines) > 5:
            for i in range(5):
                if "package " in lines[i]:
                    # Replace package import line
                    print(f"Package Name changed to {package_name}")
                    lines[i] = "package " + package_name + ";\n"
                    no_package_name = False
            if no_package_name:
                # Add package import line
                print(f"Added Package Name {package_name}")
                lines = ["package " + package_name + ";\n"] + lines
            # Re-write file with new package name
            open(filepath, "w").write('\n'.join(lines))
    except:
        print(f"Error reading file: {filepath}")

# Returns list of Java files in the folder


def search_java(zip):
    files = []
    for filename in zip.namelist():
        if ".java" in filename:
            files.append(filename)
    return files

# Extract and move to eclipse


def extract_move(ID, assign_name, section, zip):
    print(
        f"\n\nFile: {ID}\nAssignment: {assign_name}\nSection: {section}\n_________________\n")
    # Create project folder
    project_path = PACKAGE_PATH+assign_name+"/"+section+"/"+ID
    if not os.path.exists(PACKAGE_PATH+assign_name):
        os.mkdir(PACKAGE_PATH+assign_name)
    if not os.path.exists(PACKAGE_PATH+assign_name+"/"+section):
        os.mkdir(PACKAGE_PATH+assign_name+"/"+section)
    if not os.path.exists(PACKAGE_PATH+assign_name+"/"+section+"/"+ID):
        os.mkdir(PACKAGE_PATH+assign_name+"/"+section+"/"+ID)
    # Extract Java files and move to project folder
    for javafile in search_java(zip):
        try:
            zip.extract(javafile, project_path)
            try:
                # Move to project folder
                os.rename(project_path+"/"+javafile, project_path +
                          "/"+os.path.basename(javafile))
            except:
                print(f"File {javafile} already processed.")
        except:
            print(f"Skipping BAD ZIP")
    # Delete non-Java files
    for path in os.listdir(project_path):
        if os.path.isdir(project_path+'/'+path):
            shutil.rmtree(project_path+"/"+path)
        else:
            correct_package(project_path+"/"+path,
                            f"{assign_name}.{section}.{ID}")


# Extract download from canvas
with ZipFile("Submissions.zip", 'r') as zip:
    zip.extractall()


for lab_section in LAB_SECTIONS:

    # Read IDs from csv
    id_list = []

    with open(GRADEBOOK_CSV_PATH, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        count = 0
        for row in csv_reader:
            if count == 0:
                count += 1
            elif row["Lab"] == lab_section:
                id_list.append(row["Student Number"])
            count += 1

    for filename in os.listdir("./"):
        for ID in id_list:
            if ID in filename:
                try:
                    extract_move("ID_" + ID, os.path.basename(
                        os.path.abspath("")), lab_section, ZipFile(filename))
                except:
                    print(f"Error unzipping bad zip: {filename}")
