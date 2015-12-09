### Ultima Online Patcher.
This is a patcher for Ultima Online that works on GNU/Linux and Windows. It can potentially also work on OSX (Not tested.)

### Installation:
```bash
# Git way of installation:
git clone https://github.com/0x1p2/uo_patcher-py
cd uo_patcher-py/src
python patcher.py
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
+ Uses threads to leverage the bandwidth throttle of the remote repository.
+ *NEW*: Creates configuration file on first launch.
+ *NEW*: Uses Ultima Online directory in configuration file for updating. Otherwise attempts to use from pre-defined list.
+ *NEW*: Stores location of configuraton file (config.ini) <-- Do no modify please.
+ *NEW*: After and update: Stores precomputed hashes of downloaded (now local) files so it cuts down on future downloading time. 
+ *NEW*: Uses XML in configuration file for downloads. If it is not present, it uses a predefined in the script.


##### Versions:
+ v1.0-alpha (Dec 9th, 2015) - Although it's been usable for a few days now, version 1 is identified as v1 due to being the first single-packaged executable usabled by Microsoft Windows users.

##### Dev notes:
+ [ X ] URL parsing. *URL library
+ [ X ] Process new updates (as in check what is new- possibly from a config file on remote)
+ [ X ] Configuration file storing current version to compare if update is needed? (Checks against local hashes)
+ [ X ] Configuration file storing Ultima Online directory location (wineprefix)
+ [ X ] Parse XML files. 
+ [ X ] md5sum hashes: Store in configuration file. JSON or XML?
+ [ X ] Store the filename:hash into a dictionary.
+ [ X ] Download zip archive
+ [ X ] Extract zip archive
+ [ -- ] Read XML and parsing XML without downloading.
+ [ -- ] Check for application updates **nix & windows.
+ [ -- ] Prompt for setting first repository (generate a config file)
