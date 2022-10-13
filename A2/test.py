import re, json, time, os
# from os import walk

# str = "GET /get?course=networking&assignment=1 Content-Type:Hello-world HTTP/1.0 Host:localhost User-Agent: Concordia-HTTP/1.0 key1:value1 key2:value2"

# content_type = re.findall(r'Content-Type:(\S+)',str) if re.search(r'Content-Type:(\S+)',str) else "application/json"



# temp = re.findall(r'/get\?(\S+)', str)

# print(temp)

# headers = {"key1":"value1", "key2":"value2"}
# param = {"course":"network", "assignment":1}

# body = {"arg":headers, "headers":param}


# body = json.dumps(body)

# print(body)

# str = "GET /get?course=networking&assignment=1 HTTP/1.0"

# method, path, http_version = str.split(" ")

# print(method, " ", path, " ", http_version)


# time_obj = time.time()
# # getting local time from current time in seconds
# local_time = time.localtime(time_obj)

# print("The time tuple:", local_time)

# # Formatting the time to display in string format
# print('Formatted Time:', time.strftime("%a, %d %b %y %H:%M:%S", local_time))

# cmd = "httpfs -v -p PORT -d PATH-TO-DIR"

# temp = re.findall(r'-p (\S.+?\S+)', cmd)

# print(temp)

#list to store files name
# dir_path = os.path.dirname(os.path.realpath(__file__))
# dir_path += "/data/../data/../data/bar"
# res = []
# for (dir_path, dir_names, file_names) in os.walk(dir_path):
#     #print(dir_names)
#     res.extend(file_names)
# # res = os.listdir(dir_path)
# print(json.dumps(res))


# if(os.path.exists(dir_path)):
#     print("==>")

# def exception_handler(code, status):
#     return (
#     "<html>\n"+
#     f"<head><title>{code} {status}</title></head>\n"+
#     "<body>"
#     f"<center><h1>{code} {status}</h1></center>\n"
#     "</body>\n"
#     "</html>\n")

# print(exception_handler("404","NON FOUND"))

# path = os.path.dirname(os.path.realpath(__file__)) + "/" + "data" + "/bar"

# path = "/Users/_seven/Desktop/COMP 445/COMP-445/A2/data/foo"
# print(os.path.exists(path))

# with open(path) as file:
#         data = file.read().replace('\n', '')
#         print(f"[DEBUG]: POST Body Value from file -> {data}") 

# headers = "Accept: application/json afasdfga"

# print(re.findall(r'Accept:\s*(.+?\S+)', headers))

# dic_type = {"application/json":"json", "text/html":"html", "text/plain":"txt"}

# print(type(dic_type.get("hello", "NONE")))


# str = "/foo/download"

# file_name = re.findall(r'/(.+?)/', str)[0]


# print(file_name)

str = "www"

if(str): print("==<")

