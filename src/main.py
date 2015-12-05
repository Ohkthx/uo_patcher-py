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
        
        for le_file in file_list:
            installed_md5 = file_check.grab_hash(uo_path + le_file)
            if installed_md5 == True:
                # Doesn't exist. Download it.
                proc_file = file_process.grab_file(file_dict[le_file]['URL'])
                file_to_mv = file_process.pull_file(proc_file)
            elif installed_md5:
                # Compare file's hash to dictionary.
                if file_check.check_hash(installed_md5, file_dict[le_file]['Hash']):
                    print("They match!")
                else:
                    # Hashes do not match...
                    proc_file = file_process.grab_file(file_dict[le_file]['URL'])
                    file_to_mv = file_process.pull_file(proc_file)
            else:
                print("Bad file.")


