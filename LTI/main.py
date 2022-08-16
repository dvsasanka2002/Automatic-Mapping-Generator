# Step 1 : File generates a Logical Key and JSON Mapping
# Step 2 : File generates a Logical Key and XML Mapping
# Step 3 : File generates a XML and JSON Mapping
# Step 4: Creates an output.xml file after data transfer
import JSON_Functions as Jf
import XML_Functions as Xf
import Automatic_Mapping as AM
import JSON_JSON_Mapping as JJM
def parse_report_file(report_input_file):
    with open(report_input_file) as unknown_file:
        c = unknown_file.read(1)
        if c != '<':
            return True
        return False

Source_file = "Broker_Application_XML_Output.json"
Target_file = "ACORD_XML_For_SubmittionToCarrier.xml"
#Target_file = "Non-ACORD_XML_For_SubmittionToCarrier.json"
with open(Target_file,'r') as f:
    data = f.read()
if parse_report_file(Target_file):
    with open("output.json",'w') as f:
        f.write(data)
else:
    with open("file_copy.xml",'w') as f:
        f.write(data)

json_list_one = []
xml_list_one = []
json_list_two = []
xml_list_two= []
key_val_pair_json_one = []
key_val_pair_xml_one = []
key_val_pair_json_two = []
key_val_pair_xml_two = []
if(parse_report_file(Source_file)):
    JSON_FILE_ONE = Source_file
    json_list_one = Jf.json_path_gen(JSON_FILE_ONE)
    if(json_list_one != None):
        key_val_pair_json_one = Jf.key_val_pair_json(JSON_FILE_ONE,json_list_one)
else:
    XML_FILE_ONE = Source_file
    xml_list_one = Xf.xml_path_gen(XML_FILE_ONE)
    if(xml_list_one != None):
        key_val_pair_xml_one = Xf.key_val_pair_xml(XML_FILE_ONE,xml_list_one)
    

if(parse_report_file(Target_file)):
    JSON_FILE_TWO = Target_file
    json_list_two = Jf.json_path_gen(JSON_FILE_TWO)
    if(json_list_two != None):
        key_val_pair_json_two = Jf.key_val_pair_json(JSON_FILE_TWO,json_list_two)    
else:
    XML_FILE_TWO = Target_file
    xml_list_two = Xf.xml_path_gen(XML_FILE_TWO)
    if(xml_list_two != None):
        key_val_pair_xml_two = Xf.key_val_pair_xml(XML_FILE_TWO,xml_list_two)

def check_is_empty(list1,list2):
    if list1:
        return True
    else:
        return False

pair_one = key_val_pair_json_one if check_is_empty(json_list_one,xml_list_one) else key_val_pair_xml_one
bool_one = True if check_is_empty(json_list_one,xml_list_one) else False
pair_one_final = []
if(bool_one):
    for i,j in pair_one:
        pair_one_final.append((Jf.format_json_path(i),j))
else:
    for i,j in pair_one:
        pair_one_final.append((Xf.format_xml_path(i),j))

pair_two = key_val_pair_json_two if check_is_empty(json_list_two,xml_list_two) else key_val_pair_xml_two
bool_two = True if check_is_empty(json_list_two,xml_list_two) else False
pair_two_final = []
if(bool_two):
    for i,j in pair_two:
        pair_two_final.append((Jf.format_json_path(i),j))
else:
    for i,j in pair_two:
        pair_two_final.append((Xf.format_xml_path(i),j))


final_res = []
excel_res_store = []
json_matched_list = []
for a,b in pair_one_final:
    for c,d in pair_two_final:
        if(b == d):
            final_res.append((a,c))
            excel_res_store.append((a,b,c))
            json_matched_list.append(a)
if not(parse_report_file(Target_file)):
    grp_pair = []
    for i,j in final_res:
        arr = i.split('/')
        if "Insured" in arr and "Address" in arr:
            del((i,j))
        elif "BuildingID" in arr:
            del(i,j)
        elif(i[i.find(start:='Locations')+len(start)] == '['):
            if(j[j.find(start:='Location')+len(start)] == '/'):
                a = j.split('Location')
                arr = i.split('[')
                grp_pair.append((arr[0],a[0]+'Location'))
                del((i,j))
        elif(i[i.find(start:='Classifications')+len(start)] == '['):
            if(j[j.find(start:='GeneralLiabilityClassification')+len(start)] == '/'):
                a = j.split('GeneralLiabilityClassification')        
                arr = i.split('[')
                grp_pair.append((arr[0],a[0]+'GeneralLiabilityClassification'))
                del((i,j))
    file1 = "file_copy.xml"
    for i,j in (final_res):
        val = Jf.json_value(i)
        Xf.modify_value(val,Xf.format_xml_path(j),file1)

    grp_pair = list(set(grp_pair))
    for a,b in grp_pair:
        arr = b.split('/')
        if(arr[-1] == "Location" or arr[-1] == "GeneralLiabilityClassification"):
            tree = Xf.etree.parse('file_copy.xml')
            for node in tree.xpath(str(b)):
                node.getparent().remove(node)
        tree.write('file_copy.xml')
        list_k = AM.format_XML_File(str(a),str(b),Target_file)
        for i in range(len(list_k)):
            with open("f.xml",'w') as f:
                f.write(list_k[i])
                f.close()
            with open("file_copy.xml","r") as f:
                tree = Xf.etree.parse(f)
                root = tree.getroot()
                for e in root.iter():
                    if(e.tag == "GeneralLiabilityPolicyQuoteIngRq"):
                        v = e
                    elif(e.tag == "LiabilityInfo"):
                        v = e
                if(v == None):
                    break
            with open("f.xml","r") as f:
                data = f.read()
            with open('f.xml', 'w') as f:
                f.write("<x>\n" + data + "\n</x>")
                f.close()
            with open('f.xml','r') as a:
                r = Xf.etree.parse(a).getroot()
            v.extend(r)
            tree.write("file_copy.xml")
    import xml.dom.minidom

    dom = xml.dom.minidom.parse("file_copy.xml") 
    pretty_xml_as_string = dom.toprettyxml()
    with open("output.xml","w") as o:
        o.write(pretty_xml_as_string)
    import os
    if os.path.exists("f.xml"):
        os.remove("f.xml")
    if os.path.exists("newXML.xml"):
        os.remove("newXML.xml")
    if os.path.exists("file_copy.xml"):
        os.remove("file_copy.xml")
else:
    for i,j in (final_res):
        arr = i.split('/')
        if "Insured" in arr and "Address" in arr:
            del((i,j))
        elif "BuildingID" in arr:
            del(i,j)
        else:
            source_val = Jf.json_value(i)
            Jf.update_value_json(source_val,Xf.format_xml_path(j),'output.json')
    JJM.JSON_JSON_Mapping(Source_file,Target_file)
    import os
    if os.path.exists("risks.json"):
        os.remove("risks.json")
    if os.path.exists("locations.json"):
        os.remove("locations.json")



    
    

 





