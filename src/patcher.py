import os
import threading

import file_check
import file_process
import xmlParser

# # # # # # # # # # # # # # # # # # # # # # # # #
# This is the core of the script.
#  Calls all of the other functions that were
#  were created.
# # # # # # # # # # # # # # # # # # # # # # # # #

def getUOPath():
    if os.name == "nt":
        base_dir = os.environ['SystemDrive'] + "\\"                 # Base directory for windows.
    else:
        base_dir = os.environ['HOME'] + "/.wine32/drive_c/"         # Home directory + wineprefix
    uo_dir = "Program Files/Electronic Arts/Ultima Online Classic/" # Common extension for all OSs.
    return base_dir + uo_dir                                        # WONDER TWIN POWERS ACTIVATE

uo_path = getUOPath()           # Just ya. Full path.

if not os.path.exists(uo_path): # Verify that the UO path does indeed exist.. otherwise exit.
    print("You need to edit the updater.py with the proper install location of UO.")
    exit()
else:
    print("\nUltima Directory: %s" % uo_path)   # Pretty, pretty display of directory.

## A list to contain all of the locations for Updates.xml ##
update_xml = [
        "http://www.uoforever.com/patches/UOP/Updates.xml",
        ]

#   Pull the Update(s).xml   #
for url in update_xml:                              # Process 1 URL at a time from update_xml
    le_file = file_process.grab_file(url)           # Downloads the Updater.xml file.
    if not le_file:                                 # If it doesn't download, it will simply be skipped.
        print("An error occured with: %s" % url)
    else:
        file_dict = xmlParser.parse(le_file)        # Parse the XML file.
        file_list = file_dict['files']              # Assign the list of files from file_dict (see xmlParser.py)
        
        for le_file in file_list:
            threading.Thread(target=file_process.taskFile, args=(file_dict[le_file], uo_path, ) ).start() # Create a thread per update file to leverage bandwidth

