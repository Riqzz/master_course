import re

def match(ip):
    
    s1 = '(25[0-5]|(1\d|2[0-4]|[1-9]{1})\d|[1-9])' 
    s2_tuple = '((\.(25[0-5]|(1\d|2[0-4]|[1-9]{0,1})\d)){3})'

    ip_str = "^{}{}$".format(s1,s2_tuple)
    ip_pattern = re.compile(ip_str)
    result = re.search(ip_pattern, ip)

    if result is not None:
        print("successful: ", result.group())
    else:
        print("faild")

ip = '127.0.0.1'
match(ip)