import pathlib
import os
import shutil

def getListOfFilesMatchingVersion(file_paths, version):
    """
    Returns a list of files in the given path that contain the given version (or string).

    Parameters:
    file_paths (list of path): The paths to be checked.
    version (str): The version to search for (or string).

    Returns:
    dictionary of strings and path
    """
    results = {}

    #For each file in the file paths check for version string
    for path in file_paths:
        file_name = os.path.basename(path)
        print(path)
        if version in file_name:
            #If version is found then ew add it to the results dictionary key is without version and value is full path
            found_file_name = str(file_name).replace(version, "")
            results[found_file_name] = path
    return results

def getListOfFilesInDirectory(file_paths):
    """
    Returns a list of files in the given path.

    Parameters:
    file_paths (str): The directory to be checked.

    Returns:
    list of files in given path
    """
    
    return [file for file in file_paths.iterdir() if file.is_file()]

def compareTwoListsForNewVersion(old_files, old_version, new_files, new_version, replace_old_files):
    """
    Coppies files from the new files list as long as they are the same name as the ones in the old_filse list with only different versions

    Parameters:
    old_files (str): Files in the old directory to check for new versions of.

    old_version (str): Version of the files in the old directory.

    new_version (str): Version of the files in the new directory.

    replace_old_files (bool): Whether or not we delete the old version of the file in the folder if false the newer version is added to the directory and old version remains.

    Returns:
    none
    """
        
    #Check that old files is a dictionary
    if not isinstance(old_files, dict):
        raise ValueError("Old files must be a dictionary")
    
    #Check that new files is a dictionary
    if not isinstance(new_files, dict):
        raise ValueError("Old files must be a dictionary")

    for file in old_files:
        old_path = old_files[file]
        old_file_name = os.path.basename(old_path)
        old_directory = os.path.dirname(old_path)

        found_file_name = str(old_file_name).replace(old_version, "")

        if found_file_name in new_files.keys():
            new_path = new_files[found_file_name]
            new_file_name = os.path.basename(new_path)            

            replace = input(f"Replace {old_path} with {new_path}?\n")
            replace = replace.lower()

            if replace == "y" or replace == "yes" or replace == "true" or replace == "t":
                remove_old_file = False;

                # Ensure the file exists
                if not os.path.isfile(old_path):
                    print(f"The source file {old_path} does not exist.")
                    continue

                # Ensure the file exists
                if not os.path.isfile(new_path):
                    print(f"The source file {new_path} does not exist.")
                    continue

                #If the old file name and the new file name are somehow the same we need to make sure that the user knows that the file will be overwritten reguardless of replace_old_files
                if(old_file_name == new_file_name and not replace_old_files):
                    sureReplace = input("Old and new file names are the same would you like to replace the files?\n")
                    sureReplace = sureReplace.lower()

                    if sureReplace != "y" and sureReplace != "yes" and sureReplace != "true" and sureReplace != "t":
                        continue
                    else:
                        try:
                            print(f"renaming {old_path}")
                            os.rename(old_path, old_path + "_old")
                            remove_old_file = True
                        except Exception as e:
                            print(f"An exception occurred: {e}")
                            continue

                try:
                    shutil.copy(old_path, old_directory +  "\\" + new_file_name)

                    if replace_old_files:
                        os.remove(old_path)

                    #If we saved a backup copy of the original file lets remove that copy
                    if remove_old_file:
                        os.remove(old_path + "_old")

                except Exception as e:
                    print(f"An exception occurred: {e}")


if __name__ == "__main__":
    #Get location of files in the old path
    old_conforming_directory = pathlib.Path(input("What is the project directroy to update?\n"))
    #Get location of files in the new path
    new_conforming_directory = pathlib.Path(input("Where should we look for updated files?\n"))
    replace_old_files = input("Do you want to remove old files that are replaced?\n")
    old_version = input("What is the old version?\n")
    new_version = input("What is the new version?\n")

    replace_old_files = replace_old_files.lower()

    if replace_old_files == "y" or replace_old_files == "yes" or replace_old_files == "true" or replace_old_files == "t":
        replace_old_files = True
    else:
        replace_old_files = False

    #Get list of files in the old path
    old_files = getListOfFilesInDirectory(old_conforming_directory)
    #Get list of files in the new path
    new_files = getListOfFilesInDirectory(new_conforming_directory)

    #Cross reference list of files with the version number
    list_of_old_conforming_files = getListOfFilesMatchingVersion(old_files, old_version)
    list_of_new_conforming_files = getListOfFilesMatchingVersion(new_files, new_version)

    #Compare the new and old lists to move and/or replace the old versions with the files in the new folder
    compareTwoListsForNewVersion(list_of_old_conforming_files, old_version, list_of_new_conforming_files, new_version, replace_old_files)

