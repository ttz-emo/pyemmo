from configparser import ConfigParser
import os
import glob
from collections import defaultdict
from datetime import datetime

import re



def updateConfig(test_type: str, test_id: int, test_case: str):
    
    '''
    Function to update config file to generate proper test file name
    '''

    curr_datetime = datetime.now().strftime("%Y%m%d_%H%M%S")
    parser = ConfigParser()
    config_path = os.path.join(os.path.abspath('.'), "pytest.ini")
    parser.read(config_path)
    dest_name = f"logs/{test_type}/test_{test_id}_{test_case}/{curr_datetime}.log"
    parser.set('pytest', 'log_file', dest_name)

    with open(config_path, 'w+') as config_file:
        parser.write(config_file)
    return curr_datetime, dest_name

import os


def count_files(folder_path: str) -> dict:
    '''
    Function to count files of each type in a path.
    Args: folder_path: path to count in. Needs to be abs path to the dest folder
    Output: n-items Dict 
        - 1st entry being folder_path, 
        - 2nd till n-th entries: key = file type, value = count  
    '''
    file_type_list_raw = glob.glob(os.path.join(folder_path, "*.*"))
    file_type_list = [x.split(".")[1] for x in [x.split("\\")[-1] for x in file_type_list_raw]]
    file_type_counter = defaultdict(list)
    file_type_counter["dir"] = folder_path
    for file_type in file_type_list:
        if file_type_counter[file_type] == []:
            file_type_counter[file_type] = 1
        else:
            file_type_counter[file_type] += 1
    return file_type_counter


def geoFileParser(raw_path: str):
    exclude_indicators = ["//"]
    with open(raw_path, "r") as file:
        content = file.read()
        content_lines = content.split(";")
        temp = []
        result = {}
        for i, line in enumerate(content_lines[:20]):
            delete_target = []
            for ind in exclude_indicators:
                delete_target += re.findall(f"{ind}.*\n*", line)
            for targ in delete_target:
                line = line.replace(targ, "")
            
            temp.append(line)
    return temp


        # TODO: parse result into things
        # for line in temp:
        #     cleaned = line.replace("\n","").replace(" ","").replace("\t","")
        #     if (cleaned.find("[")!=-1):
        #         # print(cleaned.find("["))
        #         # print(cleaned)
        #         split_index = cleaned.find("[")
        #         a = [cleaned[:split_index], cleaned[split_index+1 : -2]]
        #     else:
        #         a = cleaned.split("=")
            
        #     result[a[0]] = a[1]