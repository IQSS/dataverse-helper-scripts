from os.path import isdir, isfile, join, dirname, abspath
from os import makedirs
import json
import sys
import random

STRESS_TEST_DIR = dirname(abspath(__file__))

# ----------------------------
# Pull in util scripts
# ----------------------------
HELPER_SCRIPTS_DIR = join(dirname(STRESS_TEST_DIR))#, 'helper_utils')
sys.path.append(HELPER_SCRIPTS_DIR)
print (HELPER_SCRIPTS_DIR)
from helper_utils.msg_util import *




# ----------------------------
# Any needed credentials -
#  stored in a JSON file
# ----------------------------
KEY_PERSISTENT_IDS = 'PERSISTENT_IDS'

CREDS_FNAME = join(STRESS_TEST_DIR, 'creds.json')
CREDS_LOOKUP = {}
def get_creds_info(key_name):
    global CREDS_LOOKUP
    assert isfile(CREDS_FNAME), 'File not found: %s' % CREDS_FNAME

    if key_name in CREDS_LOOKUP:
        return CREDS_LOOKUP.get(key_name)

    json_creds = json.loads(open(CREDS_FNAME, 'r').read())

    assert key_name in json_creds, 'Key *%s* not found in creds file' % key_name

    cred_value = json_creds.get(key_name)

    CREDS_LOOKUP[key_name] = cred_value

    return cred_value
    
    
def get_user_creds(user_number=1):
    
    user_list = get_creds_info('USERS')
    assert user_list is not None,  'USERS list not found in creds file'
    assert len(user_list) > 0,  'USERS list in creds file is empty'
    assert user_number > 0,  'user_number must be greater than 0'
    assert len(user_list) >= user_number,\
      'USERS list only has %s users. You asked for creds user: %s' % (len(user_list), user_number)
    
    user_creds = user_list[user_number-1]
    return (user_creds['username'], user_creds['password'])

def get_num_user_creds():
    user_list = get_creds_info('USERS')
    assert user_list is not None,  'USERS list not found in creds file'
    assert len(user_list) > 0,  'USERS list in creds file is empty'

    return len(user_list)

def get_random_user_creds():

    user_num = random.randint(1, get_num_user_creds())

    return get_user_creds(user_num)