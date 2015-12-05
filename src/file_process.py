import zipfile
import urllib.request
import os

# # # # # # # # # # # # # # # # # # # #
# Responsible for processing the files
#  Downloads files
#  Extracts files from ZIP Archive
# # # # # # # # # # # # # # # # # # # # 

# Create directory where all ZIP and .XML files will be stored
if not os.path.exists("uo_patch/"):
    os.makedirs("uo_patch/")
    os.chdir("uo_patch/")   # Changes to the directory.
else:
    os.chdir("uo_patch/")   # Changes to the directory.

def grab_file(le_url):
    print("Pulling: %s" % le_url)
    le_file = le_url.split('/')[-1:][0]     # Get the file name from the URL.
    pull = urllib.request.urlopen(le_url)   # Pull the file from the the URL.
    with open(le_file, 'wb') as f:          # Write to the file the contents.
        f.write(pull.read())

    if os.path.isfile(le_file):                 # Verify the file exists in uo_patch/
        print("Downloaded file: %s" % le_file)  # Announce it succeeded.
        return le_file                          #  Return the name of the file.
    else:
        print("Download failed?")               # Something happened? I've didn't witness it...
        return False                            #  Return failure. :[


def pull_file(zipdfile):
    if not os.path.isfile(zipdfile):            # Double check the file passed is indeed a file.
        return False                            #   Return failure if not.
    elif not zipfile.is_zipfile(zipdfile):      # Double check the file is a ZIP archive
        return False                            #  Return failure if it is not.

    le_zip = zipfile.ZipFile(zipdfile)          # Set the zip file to the class.
    raw_name = le_zip.namelist()[0]             # Extract the name of the contents.
    zip_file = le_zip.extract(raw_name)              # PRESS THE RED BUTTON DEEDEE! (extract)

    if os.path.isfile(raw_name):                # Verify the raw, extracted, file exists.
        return raw_name                         #  Return the name of the file!
    else:
        return False                            # Some serious shit must've happened. idk

