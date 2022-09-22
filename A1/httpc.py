import re
import socket
from urllib.parse import urlparse

BUFF_SIZE = 1024
class Httpc():

    def __init__(self):
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
        url = (re.findall(r'(https?://\S+)', cmd))[0]
        if("'" in url): url = url[:-1]
        print("[DEBUG]: url ->", type(url), url)
        url = urlparse(url)
        print("[DEBUG]: url parse ->", url)
        if(cmd.startswith("get")): self.get_request(url)

        pass

    def get_request(self, url):
        headers = ( "GET "+ url.path + " HTTP/1.0\r\n"  
                "Host:" + url.hostname + "\r\n\r\n")
        self.socket_server(url, headers)
        pass

    def socket_server(self, url_parsed, request):
 
        client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        try:
            client_socket.connect((url_parsed.hostname, 80))
            print('[DEBUG]: Socket Connect Success')

            client_socket.sendall(request.encode("utf-8"))

            response = client_socket.recv(BUFF_SIZE)

            self.print_content(response.decode("utf-8"))

        finally:  
            client_socket.close()
    
    def print_content(self, content):
        lines = content.split("\r\n")
        print("[DEBUG]: Received Response. \n")
        for line in lines: print(line)

httpc = Httpc()

print("==== Welcome to HTTPC Service ==== \n  Type help to list commands.\n  Press 'Ctrl+C' or Type 'quit' to terminate.")
# Program Start
while True:
    cmd = input("\n")
    if("quit" in cmd):
         break
    print("[DEBUG]:",cmd)
    httpc.execute(cmd)
