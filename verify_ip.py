# https://www.geeksforgeeks.org/python-program-to-validate-an-ip-address/

import re

# Make a regular expression
# for validating an Ip-address
regex = "^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])$"


# Define a function for
# validate an Ip addess
def verify_ip(ip_addr):

    # pass the regular expression
    # and the string in search() method
    if(re.search(regex, ip_addr)):
        return True
    else:
        return False
