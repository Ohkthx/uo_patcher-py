import xml.etree.ElementTree as ET

# # # # # # # # # # # # # # # # # # # # # # # # 
# Responsible for parsing the Updates.xml file
#   ( SUPER ) important.
# # # # # # # # # # # # # # # # # # # # # # # #


def parse(xml_file):
    tree = ET.parse(xml_file)   # Assign the tree of the XML
    root = tree.getroot()       # Get that root (of the XML, (UpdateCollection))
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

