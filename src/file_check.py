import hashlib
import os.path

# # # # # # # # # # # # # # # # # # #
# le_file is the dl'd file.
# i_file is the installed file.
# # # # # # # # # # # # # # # # # # # 

def grab_hash(le_file_name):
    if os.path.isfile(le_file_name):
        le_file = open(le_file_name, 'rb')
    else:
        return False

    buff = le_file.read()
    le_md5 = hashlib.md5(buff).hexdigest()
    return le_md5

def check_hash(i_file, n_file):
    if not i_file == n_file:
        # If they do not match, it will return false and prompt download.
        return False
    else:
        # If the do match. Download will not happen and not be pushed in a list.
        return True




