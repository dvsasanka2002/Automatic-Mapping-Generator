import json
import JSON_Functions as Jf
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

# src_file = "Broker_Application_XML_Output.json"
# trg_file = "Non-ACORD_XML_For_SubmittionToCarrier.json"
def function_json(src_file,trg_file,json_src_path,json_trg_path):
    arr = json_trg_path.split('/')
    li = []
    json_nodes = []
    value_one = Jf.json_value_dict(src_file,json_src_path)
    value_two = Jf.json_value_dict(trg_file,json_trg_path)
    if(value_one or value_two == None):
        value_one = Jf.json_value_up(src_file,json_src_path)
        value_two = Jf.json_value_up(trg_file,json_trg_path)

    list1 = [0]*len(value_one)
    for i in range(len(value_one)):
        dict_one = value_one[i]
        dict_two = value_two[i]
        if(arr[-1] == "risks"):
            node = []
            p = []
            for val in dict_one.keys():
                node.append(val)
                if(type(dict_one[val]) != dict):
                    p.append((val,dict_one[val]))
                elif(type(dict_one[val]) == dict):
                    for w in dict_one[val].keys():
                        p.append((w,dict_one[val][w]))
                    
            k = []
            for v in dict_two.keys():
                for j in range(len(lines)):
                    if v in pair[j][1]:
                        k.append((v,pair[j][0]))
            m = []
            for a,b in k:
                for c,d in p:
                    if b == c:
                        m.append((a,b,d))
                        dict_two[a] = d
            li.append(dict_two) 
        elif(arr[-1] == "locations"):
            node = []
            p = []
            for val in dict_one.keys():
                node.append(val)
                if(type(dict_one[val]) != dict):
                    p.append((val,dict_one[val]))
                elif(type(dict_one[val]) == dict):
                    for w in dict_one[val].keys():
                        p.append((w,dict_one[val][w]))
            k = []
            for v in dict_two.keys():
                for j in range(len(lines)):
                    if v in pair[j][1]:
                        k.append((v,pair[j][0]))
            m = []
            for a,b in k:
                for c,d in p:
                    if b == c:
                        m.append((a,b,d))
                        dict_two[a] = d
            li.append(dict_two)            
    return li

def JSON_JSON_Mapping(src_file,trg_file):
    json_src_path = "obj/carrier submission/CommercialGeneralLiability/Classifications"
    json_src_path_one = "obj/carrier submission/Locations"
    json_trg_path = "obj/quoteRequest/lines[0]/risks"
    json_trg_path_one = "obj/quoteRequest/locations"
    l = function_json(src_file,trg_file,json_src_path,json_trg_path)
    l1 = function_json(src_file,trg_file,json_src_path_one,json_trg_path_one)
    with open("risks.json","w") as f:
        f.write('[')
        for i in range(len(l)):
            json.dump(dict(l[i]),f,indent= 2)
            if i < len(l) - 1:
                f.write(',')
        f.write(']')
    with open("risks.json","r") as f:
        risk_data = f.read()
    with open("locations.json","w") as f:
        f.write('[')
        for i in range(len(l1)):
            json.dump(dict(l1[i]),f,indent= 2)
            if i < len(l1) - 1:
                f.write(',')
        f.write(']')
    with open("locations.json","r") as f:
        location_data = f.read()
    Jf.update_value_json(json.loads(risk_data),json_trg_path,"output.json")
    Jf.update_value_json(json.loads(location_data),json_trg_path_one,"output.json")