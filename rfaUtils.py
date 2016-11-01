'''
Created on Oct 19, 2016

@author: Siarhei Shpak
'''
from datetime import datetime
import os , sys

test_case_keys_list = ['tcid', 'rest_URL', 'HTTP_method', 'HTTP_RC_desired', 'param_list']

def getLog(log_dir_name):
    """
    Creates 'logs' directory, if it doesn't exist,
    creates or opens a log file in 'logs' directory.
    """
    # assign a current working directory + log_dir_name to log_dir variable (platform independent)
    log_dir = os.path.join(os.getcwd(), log_dir_name)
    # or --> script directory: log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), log_dir_name)
    # or --> user directory: log_dir = os.path.join(os.path.expanduser("~"), log_dir_name)
    
    # get program name 
    program_name = str(sys.argv[0]).split('/')[len(str(sys.argv[0]).split('/')) - 1]
    
    try:
        # if logs directory(!) doesn't exist, create it
        if not os.path.isdir(log_dir):
            os.makedirs(log_dir)
        # open log file with prefix and timestamp (platform independent) in Append mode
        log = open(os.path.join(log_dir, program_name + "_" + getCurTime("%Y%m%d_%H-%M") + ".log"), "a")
        return log
    except (OSError, IOError):
        # return -1 in case of exception
        return -1


def qaPrint(log, message):
    """
    Prints 'timestamp + message' to console and writes it to the log file
    """
    # current date and time as string + message. example: [Oct 25 01:52:33.000001] TC1 - Passed
    log_message = getCurTime("[%b %d %H:%M:%S.%f]") + " " + message
    # prints log_message
    print (log_message)
    # writes message to a log file
    log.write(log_message + "\n")


def getCurTime(date_time_format):
    """
    Returns current date_time as a string formatted according to date_time_format
    """
    date_time = datetime.now().strftime(date_time_format)
    return date_time


def getLocalEnv(env_file_path):
    '''
    Returns dictionary of environment settings
    '''
    # creates empty dictionary of environment settings
    env_dict = {}
    # open environment file for reading
    try:
        env_file = open(env_file_path, "r")
        for line in env_file:
            # save left part of the string divided by '=' as dictionary key
            key = line.split('=')[0].rstrip() # rstrip() removes '\n'
            # save left right of the string divided by '=' as dictionary value
            value = line.split('=')[1].rstrip() # rstrip() removes '\n'
            # add key-value pair to the dictionary
            if key not in env_dict:
                env_dict[key] = value
            else:
                return -1
        env_file.close()
        return env_dict
    except (IOError, OSError):
        # return -1 in case of error
        return -1 
    
def getTestCases(test_run_id):
    '''
    Returns dictionary of test case settings
    '''
    # create empty dictionary of testcase settings
    test_case_dict = {}
    # open test case file for reading
    try:
        test_case_file = open(str(test_run_id) + '.txt', 'r')
    except:
        return -1
    # saving content of the test case file into test_case_dict dictionary
    for line in test_case_file:
        # create empty inserted dictionary
        test_case_insert_dict = {}
        # saving content of the test case file into test_case_insert_dict dictionary
        for i in range (0, len(test_case_keys_list)):
            # use elements of 'test_case_keys_list' list as keys
            key = test_case_keys_list[i]
            # use content of test case file as dictionary values
            value = line.split('|')[i].rstrip() # rstrip() removes '\n'
            # insert key-value pair into 'test_case_insert_dict'
            if key not in test_case_insert_dict:
                test_case_insert_dict[key] = value
            else:
                return -1
        # use number of test case as key for 'test_case_dict' dictionary
        key = line.split('|')[0].rstrip() # rstrip() removes '\n'
        # use 'test_case_insert_dict' as value for 'test_case_dict' dictionary
        value = test_case_insert_dict
        # insert key-value pair into 'test_case_dict'
        if key not in test_case_dict:
            test_case_dict[key] = value
        else:
            return -1
    # close test case file
    test_case_file.close()
    return test_case_dict
