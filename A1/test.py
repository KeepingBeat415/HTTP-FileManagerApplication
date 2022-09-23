import re

str = "get -h key1:value1 key2:value2 'http://httpbin.org/get?course=networking&assignment=1'"

str = "location: /redirect/1"

values = re.findall(r'(\S+/\S+)', str)

print(values)