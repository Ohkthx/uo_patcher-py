import os

import file_check
import file_process
import update_parse

def getUOPath():
    if os.name == "nt":
        base_dir = os.environ['SystemDrive'] + "\\"
    else:
        base_dir = os.environ['HOME'] + "/.wine32/drive_c/"
    uo_dir = "Program Files/Electronic Arts/Ultima Online Classic/"
    return base_dir + uo_dir

uo_path = getUOPath()

print("Ultima Install: %s" % uo_path)

update_xml = [
        "http://www.uoforever.com/patches/UOP/Updates.xml",
        "http://www.uoforever.com/patches/MUL/Updates.xml",
        ]

#   Pull the Update(s).xml   #
for url in update_xml:
    le_file = file_process.grab_file(url)
    if not le_file:
        print("An error occured with: %s" % url)
    else:
        file_dict = update_parse.parse(le_file)
        file_list = file_dict['files']

        installed_md5 = file_check.grab_hash(uo_path + file_list[0])
        if installed_md5 == True:
            # Doesn't exist. Download it.
            print("Downloading...")
        elif installed_md5:
            # Compare file's hash to dictionary.
            if file_check.check_hash(installed_md5, file_dict[file_list[0]]['Hash']):
                print("They match!")
            else:
                print("Filename: %s, Hash: %s" % (file_dict[file_list[0]]['DisplayName'], file_dict[file_list[0]]['Hash']))
                print("Filename: %s, Hash: %s" % (file_list[0], installed_md5))
        else:
            print("Bad file.")


