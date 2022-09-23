import re
import socket
from tabnanny import verbose
from urllib import response
from urllib.parse import urlparse

BUFF_SIZE = 1024
# 300 Multiple Choices 301 Moved Permanently 302 Found 303 See Other
REDIRECT_CODE = ["300", "301", "303"]
class Httpc():

    def __init__(self):
        self.is_verbose = False
        self.is_headers = ""
        #self.get_header = "User-Agent: Concordia-HTTP/1.0\r\n"
        pass

    def get_help_info(self, arg):
        if(arg == "normal"):
            print('\nhttpc is a curl-like application but supports HTTP protocol only.\n' +
            'Usage: \n' + 
            '  httpc command [arguments]\n' + 
            'The commands are: \n' + 
            '  get executes a HTTP GET request and prints the response.\n' +
            '  post executes a HTTP POST request and prints the resonse.\n' +
            '  help prints this screen.\n')
        elif(arg == "get"):
            print('\nusage: httpc get [-v] [-h key:value] URL\n' +
            'Get executes a HTTP GET request for a given URL.\n' +
            '  -v Prints the detail of the response such as protocol, status, and headers.\n' +
            '  -h key:value Associates headers to HTTP Request with the format \'key:value\'.\n')
        else:
            print('\nusage: httpc post [-v] [-h key:value] [-d inline-data] [-f file] URL\n' +
            'Post executes a HTTP POST request for a given URL with inline data or from file.\n' +
            '  -v Prints the detail of the response such as protocol, status, and headers.\n' +
            '  -h key:value Associates headers to HTTP Request with the format \'key:value\'.\n' +
            '  -d string Associates an inline data to the body HTTP POST request.\n' +
            '  -f file Associates the content of a file to the body HTTP POST request\n' +
            'Either [-d] or [-f] can be used but not both.\n')

    def execute(self, cmd):
        if("help" in cmd and "get" in cmd):
            self.get_help_info("get")
        elif("help" in cmd and "post" in cmd):
                self.get_help_info("post")
        elif("help" in cmd):
            self.get_help_info("normal")
        elif(cmd.startswith("get") or cmd.startswith("post")):
            self.http_request(cmd)
        else:
            print("[ERROR]: Invalid Command. Type help to list commands. Press 'Ctrl+C' or Type 'quit' to terminate.")
    
    def http_request(self, cmd):

        self.is_verbose = True if ("-v" in cmd) else False
        self.is_headers = "User-Agent: Concordia-HTTP/1.0\r\n" + self.get_headers_value(cmd) if ("-h" in cmd) else "User-Agent: Concordia-HTTP/1.0\r\n"

        url = (re.findall(r'(https?://\S+)', cmd))[0]
        if("'" in url): url = url[:-1]
        print("[DEBUG]: url ->", type(url), url)
        url = urlparse(url)
        print("[DEBUG]: url parse ->", url)
        if(cmd.startswith("get")): self.get_request(url)

        pass

    def get_request(self, url):
        path_with_param = url.path
        if(url.query): path_with_param += '?' + url.query
        get_header = ( 
            "GET "+ path_with_param + " HTTP/1.0\r\n" +
            self.is_headers + "\r\n" +
            "Host:" + url.hostname + "\r\n\r\n")
        self.socket_server(url, get_header)

    # def get_redirect_request(self, location):
    #     path_with_param = url.path
    #     if(url.query): path_with_param += '?' + url.query
    #     get_header = ( 
    #         "GET "+ path_with_param + " HTTP/1.0\r\n" +
    #         self.is_headers + "\r\n" +
    #         "Host:" + url.hostname + "\r\n\r\n")
    #     self.socket_server(url, get_header)

    def socket_server(self, url_parsed, request):
 
        client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        try:
            print("[DEBUG]:", url_parsed)
            client_socket.connect((url_parsed.hostname, 80))
            print('[DEBUG]: Socket Connect Success')

            client_socket.sendall(request.encode("utf-8"))

            response = client_socket.recv(BUFF_SIZE)

            response_parsed = HttpResponse(response.decode("utf-8"))

            self.print_content(response_parsed)

            if(response_parsed.code in REDIRECT_CODE):

                print("[DEBUG]: GET Redirect To", response_parsed.location)
                
                url = "http://httpbin.org" + response_parsed.location[0]
                self.get_request(urlparse(url))

        finally:  
            client_socket.close()

    def get_headers_value(self, cmd):
        values = re.findall(r'(\S+:\S+)', cmd)
        for value in values:
            if("https://" in value or "http://" in value): values.remove(value)
        print("[DEBUG]: Get Headers Value =>", "\r\n".join(values))
        return "\r\n".join(values)

    def print_content(self, response):
        # lines = content.split("\r\n")
        print("[DEBUG]: Received Response. \n")
        #response = HttpResponse(content)
        if(self.is_verbose):
            for line in response.header: print(line)
        for line in response.body: print(line)

    def parse_content(self, content):
        pass
class HttpResponse():

  def __init__(self, response):
    self.text = response
    self.parseText()

  def parseText(self):
    texts = self.text.split("\r\n\r\n")
    self.header = texts[0].split("\r\n")
    self.body = texts[1].split("\r\n")

    #infos = lines[0].split(" ")

    self.code = self.header[0].split(" ")[1]
    self.status = self.header[0].split(" ")[2]
    print("[DEBUG]: Code ->", self.code, "Statue ->", self.status)
    self.location = " "
    if(self.code in REDIRECT_CODE):
    #   self.location = lines[1].split(" ")[1].split("//")[1][:-1]
        for header in self.header:
            if("location" in header): self.location = re.findall(r'(\S+/\S+)', header)
    print("[DEBUG]: Redirect to ", self.location)


httpc = Httpc()

print("==== Welcome to HTTPC Service ==== \n  Type help to list commands.\n  Press 'Ctrl+C' or Type 'quit' to terminate.")
# Program Start
while True:
    cmd = input("\n")
    if("quit" in cmd):
         break
    print("[DEBUG]:",cmd)
    httpc.execute(cmd)
