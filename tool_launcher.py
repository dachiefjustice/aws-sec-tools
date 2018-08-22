#!/usr/bin/python3
import sys
import os.path
import os

# Define variables used throughout script
aws_credfile_path = "/home/awssec/.aws/credentials"
container_aws_dir = "/home/awssec/.aws"

# Messages for the user
tool_selection_message = """
========================================
This convenience script changes to tool installation directories, activates the tool's virtualenv (if needed), and either prints the tool's help message or launches the tool (depending how the tool is written). See README.md or https://github.com/dachiefjustice/aws-sec-tools for more info.

Tools available:
1. Scout2 (print help, enter virtualenv)
2. Prowler (print help, enter virtualenv)
3. CloudSploit Scan (prompt for creds, launch scan immediately after)
4. S3-Inspector (launch immediately with credentials from ~/.aws)
5. AWS Bucket Dump (print help, enter virtualenv)
6. AWS CLI (enter virtualenv)
7. AWS Shell (enter virtualenv, launch shell)
8. Pacu (enter virtualenv, launch shell)
========================================

Which tool would you like (1-8)? """

credfile_found_message = """========================================
Found probable AWS credentials at " + aws_credfile_path + ",  most bundled tools will use this."
========================================
"""
credfile_notfound_message = """========================================
Couldn't find AWS credentials file in ~/.aws, most bundled tools need this to work. Try re-running the container and mapping your ~/.aws dir to "+ container_aws_dir + " using the -v flag.
========================================
"""

# Check for existence of AWS credential file
def do_awscreds_exist():
  return os.path.exists(aws_credfile_path)

# Return True if input is 1-7, False otherwise
def validate_tool_selection(user_input):
  valid_input = False
  selected_tool_num = 0
  
  try:
    selected_tool_num = int(user_input)
  except ValueError:
    valid_input = False
  
  if selected_tool_num in range(1,9):
    valid_input = True
  
  return valid_input

# Check for ~/.aws/credentials, notify if not found
if do_awscreds_exist():
  print(credfile_found_message)
else:
  print(credfile_notfound_message)

# Print tool list, prompt for selection
user_tool_selection = input(tool_selection_message)
user_tool_num = 0

# Validate user's tool choice
if validate_tool_selection(user_tool_selection):
  user_tool_num = int(user_tool_selection)
else:
  print("Invalid tool selection, re-run script and try again.") 
  sys.exit(1)

# User selection is valid, launch the selected tool with the right environment settings
if user_tool_num == 1: # Scout2
  os.system("cd scout2; source bin/activate; Scout2 --help; /bin/bash")
  sys.exit(0)
elif user_tool_num == 2: # Prowler
  os.system("source awscli/bin/activate; cd prowler; ./prowler -h; /bin/bash")
  sys.exit(0)
elif user_tool_num == 3: # CloudSploit Scan
  print("CloudSploit Scan runs immediately after providing credentials, ctrl + C now if you want to exit")
  aws_access_key_input = input("Enter your AWS access key: ")
  aws_secret_key_input = input("Enter your AWS secret key: ")
  os.environ['AWS_ACCESS_KEY_ID'] = aws_access_key_input
  os.environ['AWS_SECRET_ACCESS_KEY'] = aws_secret_key_input
  os.system("cd cloudsploitscan; node index.js")
  sys.exit(0)
elif user_tool_num == 4: # s3-inspector
  os.system("cd s3inspector; source bin/activate; python2 s3inspector.py; /bin/bash")
  sys.exit(0)
elif user_tool_num == 5: # AWS Bucket Dump
  os.system("cd awsbucketdump; source bin/activate; python3 AWSBucketDump.py -h; /bin/bash")
  sys.exit(0)
elif user_tool_num == 6: # AWS CLI
  os.system("cd awscli; source bin/activate; echo 'AWS CLI now available'; /bin/bash")
  sys.exit(0)
elif user_tool_num == 7: # AWS Shell
  os.system("cd awsshell; source bin/activate; aws-shell")
  sys.exit(0)
elif user_tool_num == 8: # Pacu
  os.system("cd pacu; source bin/activate; python3 pacu.py")
  sys.exit(0)
else:
  print("Invalid tool selection, re-run script and try again.")
  sys.exit(1)

sys.exit(0)
