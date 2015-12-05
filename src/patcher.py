import os

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
            local_md5 = file_check.grab_hash(uo_path + le_file)             # MD5 of the local file.
            if local_md5 == True:                                           # Really means the file doesn't exist locally.
                proc_file = file_process.grab_file(file_dict[le_file]['URL'])   # Downloads the file.
                mv_me = file_process.pull_file(proc_file)                       # Extracts the file.
                os.rename(mv_me, uo_path + mv_me)                               # Moves the file to the uo_path
            elif local_md5:                                                     # Means it isn't blank/
                if file_check.check_hash(local_md5, file_dict[le_file]['Hash']):    # Check against the XML Hash
                    print("Matching hashes, %s already installed." % le_file)       #  Matches: Do nothing.
                else:
                    proc_file = file_process.grab_file(file_dict[le_file]['URL'])   #  Not matching:
                    mv_me = file_process.pull_file(proc_file)                       # Download, extract
                    os.rename(mv_me, uo_path + mv_me)                               # And move to the uo_path
            else:
                print("Bad file.")      # Something is wrong with the file and is unknown. Just a catch.
    

