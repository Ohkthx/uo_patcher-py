import hashlib
import os.path

# # # # # # # # # # # # # # # # # # #
# Reponsible for checking the files.
#  Gets the hashes of files
#  Checks hashes against each other.
# # # # # # # # # # # # # # # # # # # 


def grab_hash(le_file_path):
    ''' This will generate the hash of filename that is passed
    to this function. It will then return the value of the hash
    if the file is found. '''
    le_name = le_file_path.split('/')[-1:][0]   # Sets the name of the file to the final item
    print(" [%s]  Checking hash." % le_name)           #   in the path.
    if os.path.isfile(le_file_path):            # Check for the file existing...
        le_file = open(le_file_path, 'rb')      #  if so, Open the file.
    else:
        return True                             #  if not, flag "True" for downloading.

    buff = le_file.read()                       # Send the file into a buffer called "buff"
    le_md5 = hashlib.md5(buff).hexdigest()      # Get the hash!
    return le_md5                               # Return the computed md5hash of the file :D


def check_hash(file_installed, file_dl):        
    ''' Simple function for comparing. '''
    if not file_installed == file_dl:           # Checking the hashes bro, come at me...
        return False                            # If they do not match, flag for downloading new.
    else:
        return True                             # If they match, ignore this file. It exists... :[




