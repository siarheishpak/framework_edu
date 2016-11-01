'''
Created on Oct 19, 2016

@author: Siarhei Shpak
'''
from rfaUtils import getLog, qaPrint, getLocalEnv, getTestCases

import sys, optparse

# path to the file with the description of environment variables
ENV_FILE = "local.properties"

# get the dictionary of the environment variables
env_dict = getLocalEnv(ENV_FILE)
# exit if file with environment variables wasn't found
if env_dict == -1:
    sys.exit("Failed to load environment variables")  

# get the log file handle
log = getLog(env_dict['log_dir'])
# exit if log creation failed
if log == -1:
    sys.exit("Failed to open or create log file")
    
qaPrint(log, 'Running %s script' % sys.argv[0])    


###################################
# Process command-line arguments
###################################

# Create array of case insensitive arguments on the base of sys.argv[1:]
case_insensitive_sys_args = []
for arguments in sys.argv[1:]:
    case_insensitive_sys_args.append(arguments.lower())

# Create OptionParser instance
parser = optparse.OptionParser(usage='Usage: %s [option]' % sys.argv[0])
# Specify possible options
parser.add_option('--testrun', action="store", dest="testrun", type="int",
                   help="id number of running test", metavar="Test_ID")

# Process command-line args
try:
    # Read command line args from case_insensitive_sys_args
    opts, args = parser.parse_args(case_insensitive_sys_args)
except (BaseException, Exception) as e:
    qaPrint(log, 'Wrong arguments. Use --help for details.')
    sys.exit()

# Save value of 'testrun' option as trid      
try:
    if opts.testrun >= 0 and opts.testrun <= 10000:
        trid = opts.testrun
    else:
        qaPrint(log, 'value of --testrun option should be in the range of [0;10000].')
        sys.exit()
except Exception as e:
    qaPrint(log, str(e))
    sys.exit()          


###################################
# Loading test cases
###################################

qaPrint(log, 'Loading test scenario_id=%s' % trid)
# get the dictionary of test cases from test scenario id = 'trid'
test_case = getTestCases(trid)
# exit if file with test cases wasn't found
if test_case == -1:
    qaPrint(log, 'Failed to open file with test cases')
    sys.exit()
else:
    qaPrint(log, 'Scenario_id=%s successfully loaded' % trid)    

qaPrint(log, str(test_case)) # STRING SHOULD BE REMOVED LATER


###################################
# Closing log file
###################################

if not log.closed:
    qaPrint(log, 'Closing log')
    log.close()
                