from configparser import ConfigParser
import os

from datetime import datetime



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