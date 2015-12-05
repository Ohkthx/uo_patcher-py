import zipfile
import urllib.request
import os.path

# # # # # # # # # # # # # # # # # # # # # # #
# host = "http://www.uoforever.com/"
# path = "patches/MUL/"
# filename = "Updates.xml"
#
# file_list is a list containing all ultima files.
# # # # # # # # # # # # # # # # # # # # # # # 

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


def pull_file(zipdfile, file_list):
    if not os.path.isfile(zipdfile):
        return False
    raw_name = os.path.splitext(zipdfile)[0]
    ext = ".mul"
    if not zipfile.is_zipfile(zipdfile):
        return False
    le_zip = zipfile.ZipFile(zipdfile)
    zip_file = le_zip.extract(raw_name + ext)
    if os.path.isfile(raw_name + ext):
        return raw_name + ext
    else:
        return False

