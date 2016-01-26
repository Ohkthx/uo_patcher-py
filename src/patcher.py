import os
from threading import Thread
import urllib.request
import errno
from shutil import rmtree

import file_hash
import file_process
import file_parser

# # # # # # # # # # # # # # # # # # #
# Created by: Ryan Ball (0x1p2/Schism)
# Date created: December 4th, 2016
# # # # # # # # # # # # # # # # # # # # # # # # #
# This is the core of the script.
#  Calls all of the other functions that were
#  were created.
# # # # # # # # # # # # # # # # # # # # # # # # #
version = 1.11                                      # Current Version number for the application.
tag = "v1.11-beta"
print("Created by: 0x1p2 (Ryan Ball), Version: %s" % tag)
if file_parser.check_forupdates(version):           #  Compares and checks for updates to the patcher.
    print("  Updated patching client.")

# # # # # # # # # # # # # # # # # # # # # # # # # 

config = file_parser.conf_read()                    # Read configuration file, if non-existent it creates.

if 'xml_url' in config['Files']:                    # If xml is defined in configuration file..
    update_xml = config['Files']['xml_url']         #   use that one.
else:
    update_xml = "http://www.ultima-shards.com/patches/UOP/Updates.xml" # Else, use a pre-defined.

if not config['Files']['uo_directory']:
    dir_list = file_process.getUOPath()             # Just ya. Full path.
    uo_path = ""                                    # Null out uo_path

    for directory in dir_list:
        if not os.path.exists(directory): # Verify that the UO path does indeed exist.. otherwise exit.
            pass
        else:
            print("Updating \"config.ini\" with discovered Ultima directory:")
            config['Files']['uo_directory'] = directory             # Use the uo_directory in configuration
            file_parser.conf_write(config)                          # Write changes to config file.
            print(" Ultima Directory:\n    %s\n" % directory)       # Pretty, pretty display of directory.
            uo_path = directory                                     # Set the path
else:
    uo_path = config['Files']['uo_directory']                       # Use the path in configuration file.
    print(" Ultima Directory:\n    %s\n" % uo_path)

if not uo_path:
    print("Directory not found for Ultima Online.")
    print("You need to add your path to the configuration file called: \"config.ini\"")
    if os.name == "nt":
        input("   Press any key to exit...")        # A pause for windows users.
    exit()


#   Pull the Update(s).xml   #
THREADS = []                    # Empty list for thread names. This is to combine at end.
file_process.cwdPatchDir("forward")      # Changes the directory to the patching directory

try:
    with urllib.request.urlopen(update_xml) as url:             # Opens the URL.
        le_xml_data = url.read()                                # Places all data from the URL into le_xml_data variable.
except IOError as conn_err:
    print("  [ ERROR ]  IO Error: [Code: %s, %s]" % (conn_err.errno, conn_err.strerror))
    print("Unable to access remote repository for updating Ultima Online.")
    print("Check network connection and/or config.ini for correct repository.")
    print("Exiting...")
    exit()

if not le_xml_data:                                         # If it doesn't download, it will simply be skipped.
    print("An error occured with: %s" % update_xml)
else:
    print(" Parsing XML file for new content...\n")
    file_dict = file_parser.xmlparse(le_xml_data)        # Parse the XML file. 
    file_list = file_dict['files']              # Assign the list of files from file_dict (see file_parser.py)
    for le_file in file_list:
        #print("  Checking: %s " % le_file)
        T = Thread(target=file_process.taskFile, args=(config, file_dict[le_file], uo_path, ) ) # Create a thread per update file to leverage bandwidth
        THREADS.append(T)       # Add the thread to the list for joining...


# # # # # # # # # # # # # # # # # # # # #
# #   CLEAN UP  THREADS and DIRECTORIES 

for x in THREADS:
    x.start()       # Start all of the threads.

for x in THREADS:
    x.join()        # Wait for thread to finish before exiting.
    
if file_process.cwdPatchDir("back"):                    # Function returns TRUE if uo_patch is a subdirectory
    rmtree("uo_patch/", ignore_errors=True)      #  Removes the patch directory since it isn't needed anymore.

print("\n Update check complete.")

if os.name == 'nt':
    input("\nPress any key to continue...")
