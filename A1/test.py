import re
import sys
import os.path
str = "get -h key1:value1 -h key2:value2 'http://httpbin.org/get?course=networking&assignment=1'"

# str = "location: /redirect/1"

# values = re.findall(r'(\S+/\S+)', str)

# print(values)

# print('''
# httpc is a curl-like application but supports HTTP protocol only.
# Usage:
#   httpc command [arguments]
# The commands are:
#   get executes a HTTP GET request and prints the response.
#   post executes a HTTP POST request and prints the resonse.
#   help prints this screen.''')

# str = "httpc -v 'http://httpbin.org/get?course=networking&assignment=1' -o hello.txt"

# str = "HTTP/1.1 418 I'M A TEAPOT"

# status = " ".join(str.split(" ")[2:])
# print(status)
#print(file_name)

# str = "post -h Content-Type:application/json -d '{\"Course\":\"COMP445\",\"Assignment\": 1}' http://httpbin.org/post"
# # data = re.findall(r'\'(.+?)\'', str)[0]
# str = "post -v -h Content-Type:application/json -f POST.json http://httpbin.org/post"

# data = headers = re.findall(r'-f (\S.+?\S+)', str)
# data_list = data.split(",")
# for item in data_list: print(item, "\n")
# for value in values:
#     if("https://" in value or "http://" in value or ""): values.remove(value)
# print("[DEBUG]: Get Headers Value =>", "\r\n".join(values))

with open(os.path.join(sys.path[0], "POST.json"), 'r') as file:
    bodies = file.read().replace('\n', '')
    print("[DEBUG]: POST Body Value from file =>", bodies)
    file.close()
