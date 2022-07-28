import xml.etree.ElementTree as ET

tree = ET.parse('useful_files/2.xml')
root = tree.getroot()

objs = root.findall('object')

for element in objs:
    print(element.tag)
    polygon = element.find('polygon')
    