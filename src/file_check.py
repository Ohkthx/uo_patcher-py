import hashlib
import os.path

# # # # # # # # # # # # # # # # # # #
# le_file is the dl'd file.
# file_installed is the installed file.
# # # # # # # # # # # # # # # # # # # 

def grab_hash(le_file_name):
    print("Checking: %s" % le_file_name)
    if os.path.isfile(le_file_name):
        le_file = open(le_file_name, 'rb')
    else:
        return True

    buff = le_file.read()
    le_md5 = hashlib.md5(buff).hexdigest()
    return le_md5

def check_hash(file_installed, file_dl):
    if not file_installed == file_dl:
        # If they do not match, it will return false and prompt download.
        return False
    else:
        # If the do match. Download will not happen and not be pushed in a list.
        return True




