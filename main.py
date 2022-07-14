import tkinter as tk
from tkinter import filedialog
import os
from os import listdir
from os.path import isfile, join, isdir
import shutil

root = tk.Tk()
root.withdraw()

dir_path = filedialog.askdirectory()
currentProject_name = dir_path.rsplit('/', 1)[1]
newProject_name = input("Enter new project name : ")

filesToRemove = [
    ".vs", ".slo", ".lo", ".o", ".obj", ".gch", ".pch", ".so", ".dylib", ".dll", ".mod", ".lai", ".la", ".a", ".lib",
    ".exe", ".out", ".app", ".ipa", ".suo", ".opensdf", ".sdf", ".VC.dv", ".VC.opensd", ".png", "_BuildData.uassset"]
foldersToRemove = ["Build", "Binaries", "Saved", "Intermediate", "DerivedDataCache", ".vs"]
folderToIgnore = [".git", "Content", ".idea","Config","Platforms","Plugins","Script"]


def removeFile(path, file):
    if(file in filesToRemove):
        os.remove(path+"/"+file)
        return True
    return False


def removeDir(path, dir_name):
    if(dir_name in foldersToRemove):
        shutil.rmtree(path+"/"+dir_name)
        return True
    return False


def checkIfDirContainsUProject():
    items = [f for f in listdir(dir_path)]
    for item in items:
        if "uproject" in item:
            return True
    print("You did not select a Unreal Project path!")
    return False


def changeDirName(path, dir_name):
    if(dir_name in folderToIgnore):
        return ""
    if(removeDir(path, dir_name)):
        return ""
    cur_dir_path = path + "/"+dir_name
    if currentProject_name in dir_name:
        new_dir_name = dir_name.replace(currentProject_name, newProject_name)
        new_dir_path = path+"/"+new_dir_name
        os.rename(cur_dir_path, path+"/"+new_dir_name)
        cur_dir_path = new_dir_path
    elif currentProject_name.lower() in dir_name:
        new_dir_name = dir_name.replace(currentProject_name.lower(), newProject_name.lower())
        new_dir_path = path+"/"+new_dir_name
        os.rename(cur_dir_path, path+"/"+new_dir_name)
        cur_dir_path = new_dir_path
    elif currentProject_name.upper() in dir_name:
        new_dir_name = dir_name.replace(currentProject_name.upper(), newProject_name.upper())
        new_dir_path = path+"/"+new_dir_name
        os.rename(cur_dir_path, path+"/"+new_dir_name)
        cur_dir_path = new_dir_path
    return cur_dir_path


def changeFileName(path, file):
    if(removeFile(path, file)):
        return ""
    if "." in file:
        file_split = file.rsplit('.', 1)
        file = file_split[0]
        file_type = "."+file_split[1]
    cur_file_path = path + "/"+file+file_type
    if currentProject_name in file:
        new_file = file.replace(currentProject_name, newProject_name)
        new_file_path = path+"/"+new_file+file_type
        os.rename(cur_file_path, new_file_path)
        cur_file_path = new_file_path
    elif currentProject_name.lower() in file:
        new_file = file.replace(currentProject_name.lower(), newProject_name.lower())
        new_file_path = path+"/"+new_file+file_type
        os.rename(cur_file_path, new_file_path)
        cur_file_path = new_file_path
    elif currentProject_name.upper() in file:
        new_file = file.replace(currentProject_name.upper(), newProject_name.upper())
        new_file_path = path+"/"+new_file+file_type
        os.rename(cur_file_path, new_file_path)
        cur_file_path = new_file_path
    return cur_file_path


def inplace_change(file_path, old_string, new_string):
    # Safely read the input filename using 'with'
    with open(file_path, encoding="cp437") as f:
        s = f.read()
        if old_string not in s:
            return
    # Safely write the changed content, if found in the file
    with open(file_path, 'w', encoding="cp437") as f:
        s = s.replace(old_string, new_string)
        f.write(s)


def searchThrough(path):

    items = [f for f in listdir(path)]
    for item in items:
        if isfile(path+"/"+item):
            file_path = changeFileName(path, item)
            if not file_path == "":
                print(file_path)
                inplace_change(file_path, currentProject_name, newProject_name)
                inplace_change(file_path, currentProject_name.lower(), newProject_name.lower())
                inplace_change(file_path, currentProject_name.upper(), newProject_name.upper())
        else:
            dir_path = changeDirName(path, item)
            if not dir_path == "":
                print(dir_path)
                searchThrough(dir_path)


bSearch = checkIfDirContainsUProject()
if bSearch:
    searchThrough(dir_path)
    new_dir_path = dir_path.replace(currentProject_name, newProject_name)
    os.rename(dir_path, new_dir_path)
