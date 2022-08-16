import json
from jsonpath_ng import parse
import Automatic_Mapping as AM
#JSON paths generated are stored in json_path_list
json_path_val_pair = []
def json_path_gen(filename):
    json_list = []
    json_path_list = []
    def disp_paths(data, p='obj'):
        for key,val in (data.items() if type(data) is dict else enumerate(data)):
            if type(val) is dict:
                disp_paths(val, '{}/{}'.format(p, key))
            elif type(val) is list:
                for key_one, val_one in enumerate(val):
                    if type(val_one) is dict or type(val_one) is list:
                        disp_paths(val_one, '{}/{}[{}]'.format(p, key, key_one))
                    else:
                        json_list.append('{}/{}[{}] = {}'.format(p, key, key_one, val_one))
            else:
                f = '{}/{}={}' if type(data) is dict else '{}[{}]={}'
                json_list.append(f.format(p, key, val))
        return json_list

    with open(str(filename), "r") as f:
        data = json.load(f)
        final_json_list = disp_paths(data)
    path_val_pair = [0]*len(final_json_list)  #Creating a list  with all elements initialised to 0 with given size
    arr = []
    for i in range(len(final_json_list)):
        arr = final_json_list[i].split('=')
        path_val_pair[i] = ((arr[0],arr[1]))
        json_path_val_pair.append(path_val_pair[i])#To store the path, val as a pair 
        json_path_list.append(path_val_pair[i][0])
    
    return json_path_list 
   

def format_json_path(json_path):
    return json_path
#Returns parsable JSON path after giving generated JSON path
def parse_path(path):
    path = path.replace('/','.')
    path = path
    path = path.replace('obj.','')
    arr = path.split('.')
    for a in range(len(arr)):
        if ' ' in arr[a]:
            arr[a] = '"'+arr[a]+'"'

    path = ('.'.join(arr))
    return path
# Return json value stored at the end of the path as dictionary
def json_value_up(filename,path):
    with open(filename, 'r') as json_file:
        json_data = json.load(json_file)
    path = parse_path(path)
    jsonpath_expression = parse(path)
    for match in jsonpath_expression.find(json_data):
        return match.value
# Return json value stored at the end of path as a string
def json_value(path) :
    for i in range(len(json_path_val_pair)):
        if(str(path) == str(json_path_val_pair[i][0])):
            return json_path_val_pair[i][1]
# Return json value stored at the end of the path as dictionary
def json_value_dict(filename,path) :
    with open(filename,'r') as json_file:
        data = json.load(json_file)
    path = path.replace('/','"."')
    path = path + '"'
    path = path.replace('obj".','')
    jsonpath_expression = parse(path)
    for match in jsonpath_expression.find(data):
        return (match.value)

def update_value_json(val,path,filename):
    with open(filename, 'r') as json_file:
        json_data = json.load(json_file)
    path = parse_path(path)
    jsonpath_expression = parse(path)
    jsonpath_expression.find(json_data)
    jsonpath_expression.update(json_data,val)
    with open(filename,'w') as file:
        json.dump(json_data,file,indent = 2)

def key_val_pair_json(filename,json_list):
    key_val_pair_json = []
    depth = 1
    for i in range(len(json_list)):
        AM.getXml_Json_Match(filename,json_list[i],depth,key_val_pair_json,False)
    return key_val_pair_json


