import numpy as np
import JSON_Functions as Jf
import XML_Functions as Xf
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import xml.etree.ElementTree as etree
from xml.etree.ElementTree import Element,tostring
from lxml import etree
import xml.dom.minidom

model = SentenceTransformer('multi-qa-mpnet-base-cos-v1')

Logical_Key = []
#Custom Logic for the Logical Key
with open('synonyms.txt') as f:
    lines = f.readlines()
rows,cols = (len(lines),2)
val = [[0]*cols]*rows
arr = [[0]]*rows
pair = [[0]]*rows
for i in range(len(lines)):
    val[i] = lines[i].split('=')
    val[i][1] = val[i][1].replace('[',"")
    val[i][1] = val[i][1].replace(']\n',"")
    arr[i] = val[i][1].split(',')
    pair[i] = (val[i][0],arr[i])
    Logical_Key.append(val[i][0])
#Cosine Similarity
def find_similar(vector_representation,all_representations, k=1):
    similarity_matrix = cosine_similarity(vector_representation, all_representations)
    similarities = similarity_matrix[0]
    if k == 1:
        val = [np.argmax(similarities)]
        return [np.argmax(similarities)]
    elif k is not None:
        return np.flip(similarities.argsort()[-k:][::1])

embeddings_distilbert = model.encode(Logical_Key)

#Logical Key through Pre-Trained Model
def get_logical_key(physical_key) :
    search_string = physical_key
    search_vect = model.encode([search_string])
    k = 1
    distil_bert_similar_indexes = find_similar(search_vect,embeddings_distilbert,k) 
    output_data = []
    for index in distil_bert_similar_indexes :
        output_data.append(Logical_Key[index])
    return output_data

#Function to create Mapping
def getXML_Json_Matching(filename,path,depth,file_type):
    arr2 = str(path).split('/')
    if(depth <= len(arr2)):
        key = arr2[len(arr2) - depth]
        for j in range(len(lines)):
            for k in range(len(pair[j][1])):
                if(str(key) == str(pair[j][1][k])):
                    return pair[j][0]
                elif((file_type == True) and (Xf.xml_value(filename,path) != None) and (str(pair[j][1][k]) == str(Xf.xml_value(filename,path)))):
                    return pair[j][0]
                elif((file_type == False) and (Jf.json_value(path) != None) and (str(pair[j][1][k]) == str(Jf.json_value(path)))):
                    return pair[j][0]
        return "0"    
    else:
        val = str(get_logical_key(arr2[-1]))
        return val 

def getXml_Json_Match(filename,path,depth,key_val_pair,file_type):
    if(getXML_Json_Matching(filename,path,depth,file_type) != "0"):
        key_val_pair.append((path,getXML_Json_Matching(filename,path,depth,file_type)))
        return

    elif(getXML_Json_Matching(filename,path,depth,file_type) == "0"):
        getXml_Json_Match(filename,path,depth+1,key_val_pair,file_type)

def gen_XML_Nodes(json_path,xml_path):
    arr = xml_path.split('/')
    json_nodes = []
    value = Jf.json_value_dict("Broker_Application_XML_Output.json",json_path)
    list1 = [0]*len(value)
    for i in range(len(value)):
        dict = value[i]
        if(arr[-1] == "GeneralLiabilityClassification"):
            val1 = dict['LocationSequence']
            val1 = '"'+ str(val1)+'"'
            xmlstr = "<" + arr[-1] + " " + "LocationRef= " + val1 +  ">" + "</" + arr[-1] + ">"
            data = etree.XML(xmlstr)
        elif(arr[-1] == "Location"):
            val1 = dict['Sequence']
            val1 = '"'+ str(val1)+'"'
            xmlstr = "<" + arr[-1] + " " + "id= " + val1 +  ">" + "</" + arr[-1] + ">"
            data = etree.XML(xmlstr)
        else:
            return None
        for j in range(len(dict)):
            ele = dict.popitem()
            json_nodes.append(ele[0])                            
            sub_ele = etree.SubElement(data,str(ele[0]))
            sub_ele.text = str(ele[1]) 
        
        dom = xml.dom.minidom.parseString(etree.tostring(data))
        pretty_xml_as_string = dom.toprettyxml()
        pretty_xml_as_string = pretty_xml_as_string.replace('<?xml version="1.0" ?>',"")
        if(pretty_xml_as_string != None):
            list1[i] = (pretty_xml_as_string)
    return list1,json_nodes

def dict_to_xml(tag, d): 
    elem = Element(tag)
    for key, val in d.items():
        child = Element(key)
        child.text = str(val)
        elem.append(child)     
    return elem

def format_XML_File(json_path,xml_path,filename):
    list1,js = gen_XML_Nodes(json_path,xml_path)
    json_nodes = list(set(js))
    list2 = [0]*len(list1)
    root = etree.parse(filename).getroot().find(xml_path)
    xml_nodes = []
    for r in root.iter('*'):
        xml_nodes.append(r.tag)
    for i in range(len(list1)):
        while("{" in list1[i]):
            arr = list1[i].split('{')
            arr2 = arr[1].split('}')
            arr2 ='{'+arr2[0]+'}'
            s = eval(arr2)
            for a in range(len(s)):
                ele = s.popitem()
                json_nodes.append(ele[0])
            json_nodes = list(set(json_nodes))
            r = eval(arr2)
            e = dict_to_xml('h',r)
            string = str(tostring(e)).replace("b'","")
            string = string.replace("'"," ")
            data = etree.XML(string)
            dom = xml.dom.minidom.parseString(etree.tostring(data))
            pretty_xml_as_string = dom.toprettyxml()
            pretty_xml_as_string = pretty_xml_as_string.replace('<?xml version="1.0" ?>',"").replace('<h>', "").replace('</h>',"")
            list1[i] = list1[i].replace("{" + str(list1[i][list1[i].find(start:='{')+len(start):list1[i].find('}')]) + "}",pretty_xml_as_string)
        
        p = []
        for v in range(len(xml_nodes)):
            for j in range(len(lines)):
                for k in range(len(pair[j][1])):
                    if(str(xml_nodes[v]) == str(pair[j][1][k])):
                       list1[i] = list1[i].replace("<"+pair[j][0]+">","<"+xml_nodes[v]+">").replace("</"+pair[j][0]+">","</"+xml_nodes[v]+">")
                       list1[i] = list1[i].replace("<"+pair[j][0]+"/>","<"+xml_nodes[v]+"/>")
                       p.append((xml_nodes[v],pair[j][0]))
        
        lk = [] 
        for k,l in p:
            lk.append(str(k))
        with open("f.xml",'w') as f:
            f.write(list1[i])
        x_path = Xf.xml_path_gen("f.xml")
        tree = etree.parse("f.xml")
        root = tree.getroot()
        del_nodes = []
        for m in x_path:
            arr = m.split('/')
            if(len(arr) == 1):
                del_nodes.append(m)
            elif(len(arr) > 1):
                del_nodes.append(str(arr[-1]))       
        del_nodes_one = set(del_nodes)
        del_nodes_two = del_nodes_one - set(lk)
        for d in del_nodes_two:
            for node in tree.xpath(str(d)):
                if len(node.getchildren()) == 0:
                    node.getparent().remove(node)
                else:
                    for ch in node.getchildren():
                        if ch.tag in (del_nodes_two):
                            ch.getparent().remove(ch)
        arr = xml_path.split('/')
        if(arr[-1] == "GeneralLiabilityClassification"):
            for node in tree.xpath("OwnersBasis"):
                node.getparent().remove(node)
            pr_bas = tree.findall('PremiumBasis')
            for pb in pr_bas:
                exp = pb.findall('Exposure')
            for e in exp:
                sub_ele = etree.SubElement(root,e.tag)
                sub_ele.text = e.text
            for node in tree.xpath("PremiumBasis"):
                node.getparent().remove(node)
        elif(arr[-1] == "Location"):
            for node in tree.xpath("Addr"):
                for ex in node.getchildren():
                    if str(ex.tag) in del_nodes_two:
                        ex.getparent().remove(ex)                
          
        tree.write("newXML.xml")
        with open("newXML.xml","r") as f:
            list1[i] = f.read()    
        dom = xml.dom.minidom.parseString(etree.tostring(root))
        pretty_xml_as_string = dom.toprettyxml()
        pretty_xml_as_string = pretty_xml_as_string.replace('<?xml version="1.0" ?>',"")
        if(pretty_xml_as_string != None):
            list1[i] = (pretty_xml_as_string)
    return(list1)

