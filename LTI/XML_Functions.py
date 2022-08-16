from lxml import etree
from xml.etree import ElementTree as et 
import Automatic_Mapping as AM
import JSON_Functions as Jf
#xml_list with all xml paths
def xml_path_gen(filename):
    xml_list = [] 
    with open(filename, 'r') as f:
        root = etree.parse(f)
        for e in root.iter():
            path = root.getelementpath(e)
            xml_list.append(path)
    del xml_list[0]
    return xml_list

#Format XML Path
def format_xml_path(xml_path):
    arr = str(xml_path).split('/')
    if(arr[-1] == 'CoverageCd'):
        xml_path = xml_path.replace('CoverageCd','Limit/FormatCurrencyAmt/Amt')
    elif(arr[-1] == 'DeductibleAppliesToCd'):
        xml_path = xml_path.replace('DeductibleAppliesToCd','FormatInteger')
    return xml_path

#Get the XML value stored
def xml_value(filename,path):
    tree = et.parse(filename)
    root = tree.getroot()
    val = root.find(path).text
    return val

def key_val_pair_xml(filename,xml_list):
    key_val_pair_xml = []
    depth = 1
    for i in range(len(xml_list)):
        AM.getXml_Json_Match(filename,xml_list[i],depth,key_val_pair_xml,True)
    return key_val_pair_xml
    

def get_matched_xml_path(path):
    for a,b in AM.final_res:
        if(path == a):
            return b

def modify_value(value,path,filename):
    value = str(value)
    tree = et.parse(filename)
    if tree.find(path) != None:
        tree.find(path).text = str(value)
    tree.write(filename)