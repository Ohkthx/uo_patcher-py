import zipfile
import urllib.request
import os.path
import os

# # # # # # # # # # # # # # # # # # # # # # #
# host = "http://www.uoforever.com/"
# path = "patches/MUL/"
# filename = "Updates.xml"
#
# file_list is a list containing all ultima files.
# # # # # # # # # # # # # # # # # # # # # # # 

if not os.path.exists("uo_patch/proc/"):
    os.makedirs("uo_patch/proc/")
    os.chdir("uo_patch/")
else:
    os.chdir("uo_patch/")

def grab_file(le_url):
    print("Pulling: %s" % le_url)
    le_file = le_url.split('/')[-1:][0]
    pull = urllib.request.urlopen(le_url)
    with open(le_file, 'wb') as f:
        f.write(pull.read())

    if os.path.isfile(le_file):
        print("Downloaded file: %s" % le_file)
        return le_file
    else:
        print("Download failed?")
        return False


def pull_file(zipdfile):
    if not os.path.isfile(zipdfile):
        return False
    elif not zipfile.is_zipfile(zipdfile):
        return False

    le_zip = zipfile.ZipFile(zipdfile)
    raw_name = le_zip.namelist()[0]
    zip_file = le_zip.extractall() #(raw_name + ext)

    if os.path.isfile(raw_name):
        return raw_name
    else:
        return False

