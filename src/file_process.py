import zipfile
import urllib.request
import os
import shutil

import file_hash
import file_parser

# # # # # # # # # # # # # # # # # # # #
# Responsible for processing the files
#  Downloads files
#  Extracts files from ZIP Archive
# # # # # # # # # # # # # # # # # # # # 

# Create directory where all ZIP and .XML files will be stored
def cwdPatchDir():
    ''' Creates and/or changes to the patching directory. '''
    if not os.path.exists("uo_patch/"):
        os.makedirs("uo_patch/")
        os.chdir("uo_patch/")   # Changes to the directory.
    else:
        os.chdir("uo_patch/")   # Changes to the directory.


def taskFile(config, file_info, uo_path):
    ''' This is the function that is called on thread creation. 
    It is responsible for executing the downloading. verifying,
    and installation of files. Also it writes the updated hashes
    to the configuration file. '''
    if file_info['DisplayName'] in config['Hashes']:
        local_f_md5 = config['Hashes'][file_info['DisplayName']]            # Get key from dictionary instead of computing.
    else:
        local_f_md5 = file_hash.grab_hash(uo_path + file_info['DisplayName'])  # Compute the hash of the local file

    if local_f_md5 == True:                                                 # If the file doesn't exist..
        dl_file = grab_file(file_info['URL'])                               # Download it,
        le_file = pull_file(dl_file)                                        # Extract it.
        config['Hashes'][file_info['DisplayName']] = file_info['Hash']
        file_parser.conf_write(config)

        for files in le_file:
            shutil.copy(files, uo_path + files)                             # Move it to the uo_directory.
            print(" [%s]  Moved to the Ultima Directory." % files)

    elif local_f_md5:                                                       # If hash is computed.
        if file_hash.check_hash(local_f_md5, file_info['Hash']):            # Check against the XML Hash
            config['Hashes'][file_info['DisplayName']] = file_info['Hash']
            file_parser.conf_write(config)
            print(" [%s]  Matching Hashes. Not installing." % file_info['DisplayName'])

        else:
            dl_file = grab_file(file_info['URL'])                           # Else, download the file
            le_file = pull_file(dl_file)                                    #  Extract the file.
            config['Hashes'][file_info['DisplayName']] = file_info['Hash']
            file_parser.conf_write(config)

            for files in le_file:
                shutil.copy(files, uo_path + files)                        #  Move the file to the new location.
                print(" [%s]  Moved to the Ultima Directory." % files)      

    else:
        print(" [%s]  Bad file." % file_info['DisplayName'])


def grab_file(le_url):
    ''' Downloads the fules and saves them. '''
    le_file = le_url.split('/')[-1:][0]     # Get the file name from the URL.
    print(" [%s]  Downloading file." % le_file)
    pull = urllib.request.urlopen(le_url)   # Pull the file from the the URL.
    with open(le_file, 'wb') as f:          # Write to the file the contents.
        f.write(pull.read())

    if os.path.isfile(le_file):                 # Verify the file exists in uo_patch/
        print(" [%s]  File download complete." % le_file)  # Announce it succeeded.
        return le_file                          #  Return the name of the file.
    else:
        print(" [%s]  Download failed." % le_file)               # Something happened? I've didn't witness it...
        return False                            #  Return failure. :[


def pull_file(zipdfile):
    ''' Extracts files from a ZIP Archive. It returns a list of all files
    that are part of the Archive. '''
    if not os.path.isfile(zipdfile):            # Double check the file passed is indeed a file.
        return False                            #   Return failure if not.
    elif not zipfile.is_zipfile(zipdfile):      # Double check the file is a ZIP archive
        return False                            #  Return failure if it is not.

    le_zip = zipfile.ZipFile(zipdfile)          # Set the zip file to the class.
    raw_name = le_zip.namelist()                # Extract the name of the contents.
    for files in raw_name:
        zip_file = le_zip.extract(files)        # PRESS THE RED BUTTON DEEDEE! (extract)
        print(" [%s]  Extracted from archive." % files) # Extract files
    
    for files in raw_name:
        if not os.path.isfile(files):               # If files do not exists....
            return False                            # Some serious shit must've happened. idk

    return raw_name        


def getUOPath():
    ''' Gets the predefined and "common" installation directories of Ultima Online.
    These will be ignored if a file is outlined in the configuration file. '''
    if os.name == "nt":
        base_dir = os.environ['SystemDrive'] + "/"                 # Base directory for windows.
        uo_dirs = [
                base_dir + "Program Files (x86)/Electronic Arts/Ultima Online Classic/",    # 64-bit Post-XP
                base_dir + "Program Files/Electronic Arts/Ultima Online Classic/",          # 32-bit System
                base_dir + "Games/Electronic Arts/Ultima Online Classic/",                  # Windows 10?
                ]
    else:
        base_dir = os.environ['HOME'] + "/"                         # Home directory + wineprefix
        uo_dirs = [
                base_dir + ".wine32/drive_c/Program Files/Electronic Arts/Ultima Online Classic/",  # Common extension
                base_dir + ".wine/drive_c/Program Files/Electronic Arts/Ultima Online Classic/",    # Default wine32
                base_dir + ".wine/drive_c/Program Files {x86)/Electronic Arts/Ultima Online Classic/",  # Default wine6
                ]

    return uo_dirs                                        # WONDER TWIN POWERS ACTIVATE


def client_update(url):
    file_name = url.split('/')[-1]          # Grab the file name.
    try:
        remote_file = urllib.request.urlopen(url)   # Open the remote end.
        local_file = open(file_name, 'wb')      # Set object for local file
    
        file_size = float(remote_file.headers['Content-Length'])    
        print("  Downloading: %s\n Size: %.2fMB" % (file_name, file_size/(1024.0 * 1024.0)))

        block_size = 8192
        file_size_dl = 0

        while True:
            buffer = remote_file.read(block_size)
            if not buffer:
                break

            file_size_dl += len(buffer)
            local_file.write(buffer)

            status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
            status = status + chr(8)*(len(status)+1)
            print(status)

        local_file.close()

    except IOError:
        print("Having issues with remote pulling: %s" % file_name)



