import os
import threading

import file_hash
import file_process
import file_parser

# # # # # # # # # # # # # # # # # # # # # # # # #
# This is the core of the script.
#  Calls all of the other functions that were
#  were created.
# # # # # # # # # # # # # # # # # # # # # # # # #

update_xml = [
        "http://www.uoforever.com/patches/UOP/Updates.xml",
        ]


# # # # # # END OF USER MODIFICATION # # # # # #

dir_list = file_process.getUOPath()           # Just ya. Full path.
uo_path = ""

for directory in dir_list:
    if not os.path.exists(directory): # Verify that the UO path does indeed exist.. otherwise exit.
        pass
    else:
        print("\nUltima Directory:\n    %s\n" % directory)   # Pretty, pretty display of directory.
        uo_path = directory

if not uo_path:
    print("Directory not found for Ultima Online.\n  You need to add your path to the configuration file.")
    if os.name == "nt":
        input("   Press any key to exit...")
    exit()

#   Pull the Update(s).xml   #
THREADS = []
for url in update_xml:                              # Process 1 URL at a time from update_xml
    le_file = file_process.grab_file(url)           # Downloads the Updater.xml file.
    if not le_file:                                 # If it doesn't download, it will simply be skipped.
        print("An error occured with: %s" % url)
    else:
        file_dict = file_parser.parse(le_file)        # Parse the XML file. 
        file_list = file_dict['files']              # Assign the list of files from file_dict (see file_parser.py)
        
        for le_file in file_list:
            T = threading.Thread(target=file_process.taskFile, args=(file_dict[le_file], uo_path, ) ) # Create a thread per update file to leverage bandwidth
            THREADS.append(T)

for x in THREADS:
    x.start()

for x in THREADS:
    x.join()

if os.name == 'nt':
    input("\nPress any key to continue...")
