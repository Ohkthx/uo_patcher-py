import xml.etree.ElementTree as ET
import os.path
import urllib.request as urlrequest
from os import name as osname
from json import loads
from configparser import ConfigParser

# # # # # # # # # # # # # # # # # # # # # # # # 
# Responsible for parsing the Updates.xml file
#   ( SUPER ) important.
# # # # # # # # # # # # # # # # # # # # # # # #
patcher_update_url = "https://raw.githubusercontent.com/0x1p2/uo_patcher-py/master/README.md"
# # # # # # # # # # # # # # # # # # # # # # # # 


def xmlparse(xml_data):
    ''' Parses the XML file passed to it. This XML should be obtained
    from a remote host/server and should include the file names, hashes,
    locations(URL), and description of all files that are to be updated. '''
    root = ET.fromstring(xml_data)   # Assign the tree/root of the XML string
    file_dict = {}              # Blank dictionary to hold the informaton of the file.
    file_list = []              # This will append to a list in the dictionary a list of the filenames.

    for UpdateObject in root[0].findall('UpdateObject'):    
        DisplayName = UpdateObject.find('DisplayName').text     # Value of DisplayName
        FileName = UpdateObject.find('FileName').text           # Value of FileName
        URL = UpdateObject.find('URL').text                     # Value of URL
        Description = UpdateObject.find('Description').text     # Value of Description
        Hash = UpdateObject.find('Hash').text.lower()           # Value of Hash (to lowercase to match)

        file_dict[DisplayName] = { "DisplayName": DisplayName,"FileName": FileName, "URL": URL, "Description": Description, "Hash": Hash }
        file_list.append(DisplayName)       # Here's that appen we talked about earlier in the file.

    file_dict['files'] = file_list          # Lastly assign the list to "Files" in the dictionary.

    return file_dict                        # Return the dictionary to be used.


def conf_write(config):
    ''' Creates and writes changes to configuration files.
    If "None" is passed to the function it creates, otherwise it
    writes new changes. '''
    if not os.path.exists('config.ini') and config == None:                              # First time write/create.
        config = ConfigParser()    
        config['Files'] = {
                'XML_URL': 'http://www.uoforever.com/patches/UOP/Updates.xml',
                'UO_Directory': '' }
        config['Files']['config'] = os.getcwd() + "/config.ini"
        config['Hashes'] = {}
    with open(config['Files']['config'], 'w') as configfile:
        config.write(configfile)

    return config


def conf_read():
    ''' Loads the configuration file. If it doesn't exist it will then call
    the write function to create a new configuration file. Then it will load it. '''
    if not os.path.exists('config.ini'):
        print("\nCreating configuration file...")
        config = conf_write(None)
    else:
        print("\nLoading configuration file...")
        config = ConfigParser()

    config.read('config.ini')

    return config

def check_forupdates(app_version):
    with urlrequest.urlopen(patcher_update_url) as update_check:
        foreign_request = loads(update_check.readline().decode())

    if app_version < float(foreign_request['Current-Version']):
        if osname == 'nt':
            # Get the new executable
            print("Windows host.")
        else:
            # Get individual scripts
            print("Linux Host.")
        return True
    else:
        return False


