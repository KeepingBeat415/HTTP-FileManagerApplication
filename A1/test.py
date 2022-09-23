import re

# str = "get -h key1:value1 key2:value2 'http://httpbin.org/get?course=networking&assignment=1'"

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

str = "httpc -v 'http://httpbin.org/get?course=networking&assignment=1' -o hello.txt"


print(file_name)