import re, sys, json, time, socket, logging
from urllib import response
from urllib.parse import urlparse
import os.path
import threading

from FileManager import FileManager


BUFF_SIZE = 1024

class Httpfs():

    def __init__(self):
        self.url = ""
        self.port = 8080
        # self.is_verbose = False
        self.dic_path = "data"
        self.process_get_file = False
        self.code = ""
        self.status = { "200":"OK", "400":"Bad Request", "401":"Unauthorized", "404":"Not Found", "505":"HTTP Version Not Supported"}

    def execute_cmd(self, cmd):
        if(cmd.startswith("httpfs")):
            if("-v" in cmd): 
                logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y/%m/%d %H:%M:%S', stream=sys.stdout, level=logging.DEBUG)
            else:
                logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y/%m/%d %H:%M:%S', stream=sys.stdout, level=logging.INFO)

            if("-p" in cmd and re.search(r'-p (\S.+?\S+)', cmd)): self.port = int(re.findall(r'-p (\S.+?\S+)', cmd)[0])
            if("-d" in cmd and re.search(r'-d (\S.+?\S+)', cmd)): self.dic_path = re.findall(r'-d (\S.+?\S+)', cmd)[0]
            
            self.run_server()
        else:
            print("\n[ERROR]: Invalid Command.")

    def run_server(self):
        logging.info('HTTP file server socket is running...')
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #try:
        listener.bind((self.url, self.port))
        listener.listen(5)
        logging.info(f'Socket is listening at {self.port}')
        while True:
            conn, addr = listener.accept()
            threading.Thread(target=self.http_handler, args=(conn, addr)).start()
        #finally:
        #listener.close()
        # 	while True:
        #     	conn, addr = listener.accept()
        #     	threading.Thread(target=handle_client, args=(conn, addr)).start()

    def http_handler(self, conn, addr):
        #print('[DEBUG]: HTTP Handler Called.')
        try:
            data = b''
            while True:
                temp = conn.recv(BUFF_SIZE)
                data += temp
                if(len(temp) < BUFF_SIZE): break;
                #conn.sendall(data)

            request_pared = HttpRequestParsed(data.decode('utf-8'))

            self.response_body = request_pared.response_body
            self.process_get_file = request_pared.process_get_file

            if(self.process_get_file):
                self.handle_files_request(request_pared.method, request_pared.path, request_pared.accept_type)

            response_content = self.generate_response_content(request_pared)

            logging.debug('[DEBUG]: Received HTTP Request ->', data)
            conn.send(response_content.encode('utf-8'))
        finally:
            conn.close()
    
    def handle_files_request(self, method, path, accept_type):

        file_manager = FileManager(self.dic_path, accept_type)

        if(method == "GET"):
            if(path == "/"):
                file_manager.get_files_list()
            else:
                file_manager.get_file_content(path)
                # if(file_manager.status == "200"):
                # #     self.response_body["data"] = file_manager.content
                # # else:
                #     self.response_body = file_manager.content
                #     self.code = file_manager.code
            self.response_body = file_manager.content
            self.code = file_manager.code

    def generate_response_content(self, request):
        header = (
            request.http_version + " " + self.code + " " + self.status.get(self.code) + "\r\n" +
            "Date: " + self.get_date() + "\r\n" +
            "Content-Type: " + request.accept_type + "\r\n" +
            "Content-Length: " + str(len(self.response_body)) + "\r\n" +
            "Connection: close \r\n" +
            "\r\n"
        )
        if (not self.process_get_file): self.response_body = json.dumps(self.response_body, indent=2, sort_keys=True) 

        return header + self.response_body
        pass

    def get_date(self):
        return time.strftime("%a, %d %b %y %H:%M:%S", time.localtime(time.time()))

class HttpRequestParsed():
    def __init__(self, request):
        self.response_body = {}
        self.process_get_file = False
        self.content_type = "json"
        self.accept_type = "json"
        self.path = ""
        self.parseText(request)
    
    def parseText(self, request):

        header, body = request.split("\r\n\r\n")
        headers = header.split("\r\n")
        print("\n[DEBUG]: Received headers ==>", headers[0])
        self.method, self.path, self.http_version = headers[0].split(" ")

        if(re.search(r'Accept:\s*(.+?\S+)', header)):
            accept_type = re.findall(r'Accept:\s*(.+?\S+)', header)[0]
            logging.debug(f"Processing request with accept type {accept_type}")
            self.accept_type = self.process_accept_type(accept_type)

        print("[DEBUG]: method -> ", self.method, " path -> ", self.path, " version -> ", self.http_version, " accept type ->", self.accept_type)

        if (re.search(r'/get\?(\S+)', self.path)):
            dic = {}
            params = re.findall(r'/get\?(\S+)', self.path)[0]
            for param in params.split("&"):
                key, value = param.split("=")
                dic[key] = value
            self.response_body["arg"] = dic
        else:
            self.process_get_file = True
        dic = {}
        for header in headers[1:]:
            key, value = header.split(":")
            dic[key] = value
        self.response_body["headers"] = dic

        if(len(body)>0): self.response_body["data"] = body

        #self.response_body = json.dumps(self.response_body, indent=2, sort_keys=True)

    def process_accept_type(self, accept_type):
        dic_type = {"application/json":"json", "application/xml":"xml", "text/html":"html", "text/plain":"txt"}
        return dic_type.get(accept_type, "NONE")


print("\n"+"="*10+"Welcome to Httpfs Server"+"="*10)
# Initial HTTP 
httpfs = Httpfs()
# Program Start
while True: 
    try:
        cmd = input("\nHttpfs is a simple file server." +
                    "\nusage: Httpfs [-v] [-p PORT] [-d PATH-TO-DIR]" +
                    "\n-v  Prints debugging messages." +
                    "\n-p  Specifies the port number that the server will listen and serve at. Default is 8080." +
                    "\n-d  Specifies the directory that the server will use to read/write requested files." +
                    "\nDefault is the current directory when launching the application." +
                    "\nPress 'Ctrl+C' or Type 'quit' to terminate.\n\n")
        if("quit" in cmd): break
        httpfs.execute_cmd(cmd)
    except KeyboardInterrupt:
        sys.exit()