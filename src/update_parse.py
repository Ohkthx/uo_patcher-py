import xml.etree.ElementTree as ET

def parse(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    file_dict = {}
    file_list = []

    for UpdateObject in root[0].findall('UpdateObject'):
        DisplayName = UpdateObject.find('DisplayName').text
        FileName = UpdateObject.find('FileName').text
        URL = UpdateObject.find('URL').text
        Description = UpdateObject.find('Description').text
        Hash = UpdateObject.find('Hash').text.lower()

        file_dict[DisplayName] = { "DisplayName": DisplayName,"FileName": FileName, "URL": URL, "Description": Description, "Hash": Hash }
        file_list.append(DisplayName)

    file_dict['files'] = file_list
    return file_dict

