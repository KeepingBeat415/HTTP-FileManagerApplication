import re
import sys
import socket
from urllib.parse import urlparse
import os.path

PORT = 80
BUFF_SIZE = 1024
REDIRECT_CODE = ["301", "303"] # 300 Multiple Choices 301 Moved Permanently 302 Found 303 See Other

class Httpc():

    def __init__(self):
        self.is_verbose = False
        self.is_download = False
        self.passed_headers = ""
        self.file_name = ""
        self.body = ""
        pass


    def execute_curl(self, cmd):
        if("help" in cmd and "get" in cmd):
            self.get_help_info("get")
        elif("help" in cmd and "post" in cmd):
            self.get_help_info("post")
        elif("help" in cmd):
            self.get_help_info("none")
        # elif("https://" not in cmd or "http://" not in cmd):
        #     print("[ERROR]: Invalid URL Path. Type help to list commands. Press 'Ctrl+C' or Type 'quit' to terminate.")
        elif("-d" in cmd and "-f" in cmd):
            print("[ERROR]: Invalid Command. POST should have either -d or -f but not both.")
        elif(cmd.startswith("get") or cmd.startswith("post")):
            self.http_request(cmd)
        else:
            print("[ERROR]: Invalid Command. Type help to list commands. Press 'Ctrl+C' or Type 'quit' to terminate.")
    

    def http_request(self, cmd):

        if ("-v" in cmd): self.is_verbose = True

        if ("-o" in cmd): 
            self.file_name = (re.findall(r'-o (\S.+?\S+)', cmd))[0]
            self.is_download = True
        if ("-f" in cmd): self.file_name = (re.findall(r'-f (\S.+?\S+)', cmd))[0]

        if ("-h" in cmd): self.passed_headers =  self.get_passed_headers_value(cmd)
        if ("-d" in cmd or "-f" in cmd): self.body = self.get_passed_body_value(cmd)

        url = (re.findall(r'(https?://\S+)', cmd))[0]
        if("'" in url): url = url[:-1]

        if(cmd.startswith("get")): self.get_request(urlparse(url))
        if(cmd.startswith("post")): self.post_request(urlparse(url))


    def get_request(self, url):

        path_with_query = url.path
        if(url.query): path_with_query += '?' + url.query

        header = ( 
            "GET " + path_with_query + " HTTP/1.0\r\n" +
            "Host:" + url.hostname + "\r\n" +
            "User-Agent: Concordia-HTTP/1.0\r\n" +
            self.passed_headers + "\r\n" +
            "\r\n")
        self.server_socket(url, header)


    def post_request(self, url):
        header = (
            "POST " + url.path + " HTTP/1.0\r\n" +
            "Host: " + url.hostname + "\r\n" +
            "User-Agent: Concordia-HTTP/1.0\r\n" +
            self.passed_headers + "\r\n" +
            "Content-Length: " + str(len(self.body)) + "\r\n" +
            "\r\n"
        )
        self.server_socket(url, header + self.body)


    def server_socket(self, url_parsed, request):
 
        client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

        try:
            print("[DEBUG]:", url_parsed)

            client_socket.connect((url_parsed.hostname, PORT))
            print('[DEBUG]: Socket Connect Success')

            client_socket.sendall(request.encode("utf-8"))

            response = client_socket.recv(BUFF_SIZE)

            response_parsed = HttpResponseParsed(response.decode("utf-8"))

            if(self.is_download): self.download_response(response_parsed)

            self.print_response(response_parsed)

            if(response_parsed.code in REDIRECT_CODE):

                print("[DEBUG]: GET Redirect To", response_parsed.location)
                
                url = url_parsed.scheme + "://" + url_parsed.hostname + response_parsed.location[0]
                self.get_request(urlparse(url))

        finally:  
            client_socket.close()


    def get_passed_headers_value(self, cmd):

        headers = re.findall(r'-h (\S+:\S+)', cmd)
        print("[DEBUG]: Get Headers Value =>", "\r\n".join(headers))
        return "\r\n".join(headers)


    def get_passed_body_value(self, cmd):
        bodies = ""
        if ("-d" in cmd):
            bodies = re.findall(r'\'(.+?)\'', cmd)[0]
            print("[DEBUG]: POST Body Value from inline =>", bodies)
        if ("-f" in cmd):
            if (os.path.exists(self.file_name)):
                with open(self.file_name) as file:
                    bodies = file.read().replace('\n', '')
                    print("[DEBUG]: POST Body Value from file =>", bodies)
            else:
                print("[DEBUG]: The File NOT Exited.")
                sys.exit()
        return bodies


    def download_response(self, response):

        print("[DEBUG]: Download Response Body into", self.file_name)

        for line in response.body: print(line)

        file = open(self.file_name, "w") if (os.path.exists(self.file_name)) else open(self.file_name, "a")
  
        for line in response.body: file.write(line)

        file.close()


    def print_response(self, response):

        print("[DEBUG]: Received Response. \n")

        if(self.is_verbose):
            for line in response.headers: print(line)

        for line in response.body: print(line)


    def get_help_info(self, arg):
        if(arg == "post"):
            print('\nusage: httpc post [-v] [-h key:value] [-d inline-data] [-f file] URL\n' +
            'Post executes a HTTP POST request for a given URL with inline data or from file.\n' +
            '  -v Prints the detail of the response such as protocol, status, and headers.\n' +
            '  -h key:value Associates headers to HTTP Request with the format \'key:value\'.\n' +
            '  -d string Associates an inline data to the body HTTP POST request.\n' +
            '  -f file Associates the content of a file to the body HTTP POST request\n' +
            'Either [-d] or [-f] can be used but not both.\n')
        elif(arg == "get"):
            print('\nusage: httpc get [-v] [-h key:value] URL\n' +
            'Get executes a HTTP GET request for a given URL.\n' +
            '  -v Prints the detail of the response such as protocol, status, and headers.\n' +
            '  -h key:value Associates headers to HTTP Request with the format \'key:value\'.\n')
        else:
            print('\nhttpc is a curl-like application but supports HTTP protocol only.\n' +
            'Usage: \n' + 
            '  httpc command [arguments]\n' + 
            'The commands are: \n' + 
            '  get executes a HTTP GET request and prints the response.\n' +
            '  post executes a HTTP POST request and prints the resonse.\n' +
            '  help prints this screen.\n')

class HttpResponseParsed():

  def __init__(self, response):
    self.parseText(response)

  def parseText(self, response):

    contents = response.split("\r\n\r\n")

    self.headers = contents[0].split("\r\n")
    self.body = contents[1].split("\r\n")
    self.code = self.headers[0].split(" ")[1]
    self.status = " ".join(self.headers[0].split(" ")[2:])
    self.location = " "
    
    print("[DEBUG]: Response Code ->", self.code, " Response Statue ->", self.status)

    if(self.code in REDIRECT_CODE):
        for header in self.headers:
            if("location" in header): self.location = re.findall(r'(\S+/\S+)', header)
        #print("[DEBUG]: Redirect to ", self.location)


print("==== Welcome to HTTPC Service ==== \n  Type help to list commands.\n  Press 'Ctrl+C' or Type 'quit' to terminate.")
# Program Start
while True:
    cmd = input("\n")
    if("quit" in cmd): break
    httpc = Httpc()
    httpc.execute_curl(cmd)
