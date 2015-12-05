### Ultima Online Patcher.
This is a patcher for Ultima Online. It will check a remote host for updates
for a locally installed client. It will process the updates and replace the 
old files with the ones provided by the server. Written for python3.

### Installation:
```bash
# Git way of installation:
git clone https://github.com/0x1p2/uo_patcher-py
cd uo_updater-py/src
python updater.py
```

#### Features:
+ Connects to a designated server...
+ Downloads the Updates.xml and parses the XML for potentially new information.
+ Checks the data outlined in Updates.xml to local data and compares the hashes (Unique identity for the file)
+ If the files match, the file is ignored.
+ If the files do not exist locally, they are downloaded.
+ If the files exist but are outdated, the are redownloaded.
+ Extracts the updated files from their packaging (ZIP Archive)
+ Replaces old Ultima Files with the new patched files.



##### Dev notes:
+ [ X ] URL parsing. *URL library
+ [ - ] Process new updates (as in check what is new- possibly from a config file on remote)
+ [ - ] Configuration file storing current version to compare if update is needed?
+ [ - ] Configuration file storing Ultima Online directory location (wineprefix)
+ [ X ] Parse XML files. 
+ [ X ] md5sum hashes: Store in configuration file. JSON or XML?
+ [ X ] Store the filename:hash into a dictionary.
+ [ X ] Download zip archive
+ [ X ] Extract zip archive
