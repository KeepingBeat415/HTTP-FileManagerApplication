import re, sys, json, time, socket, logging, os.path, threading, argparse
from FileManager import FileManager

BUFF_SIZE = 1024

class Httpfs():

    def __init__(self):
        self.url = ""
        self.port = 8080
        self.dir_path = "data"
        self.verbose = False
        self.access_file_manager = False
        self.disposition = ""
        self.code = ""
        self.status = { "200":"OK", "400":"Bad Request", "401":"Unauthorized", "404":"Not Found", "505":"HTTP Version Not Supported"}
        logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y/%m/%d %H:%M:%S', stream=sys.stdout, level=logging.DEBUG)

    # Parser input cmd setting
    def execute_cmd(self, cmd):

        if(cmd.startswith("httpfs")):
            
            try:
                # Using ArgumentParser Library
                cmd_parser = argparse.ArgumentParser(prog='httpfs', usage='%(prog)s [-v] [-p PORT] [-d PATH-TO-DIR]', description='Process some integers.')

                cmd_parser.add_argument('-v', dest='verbose', action=argparse.BooleanOptionalAction, help='verbose', default=False)
                cmd_parser.add_argument('-p', dest='port', help='server socket port', type=int, default=8080)
                cmd_parser.add_argument('-d', dest='dir_path', help='file manager directory', default='data')

                args = cmd_parser.parse_args(cmd[6:].split()) # remove httpfs
                logging.debug(f"Parser cmd As --> {args}")

                self.verbose, self.port, self.dir_path = args.verbose, args.port, args.dir_path
                # Display logging debug msg
                if(self.verbose):
                    logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y/%m/%d %H:%M:%S', stream=sys.stdout, level=logging.DEBUG)

                # Validated the file directory 
                is_exist_path = os.path.dirname(os.path.realpath(__file__)) + "/" + self.dir_path
                if(not os.path.exists(is_exist_path)): 
                    return logging.info("File Manger Server Directory is not exist.")

                logging.info(f"HTTP File Manager Server Setting: Port - {self.port}, Directory - {self.dir_path}, Verbose - {self.verbose}")

                self.run_server()
            except:
                logging.info("[ERROR]: Invalid Command, with UNKNOWN command.")
        else:
            logging.info("[ERROR]: Invalid Command, command should start with \"httpfs\"")

    # Run...
    def run_server(self):
        logging.info('HTTP File Manager Server Socket is running...')

        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listener.bind((self.url, self.port))
        listener.listen(5)

        try:
            while True:
                # Connecting with client socket
                conn, addr = listener.accept()
                threading.Thread(target=self.http_handler, args=(conn, addr)).start()
                logging.info(f'Socket is listening at {self.url}:{self.port}, with Thread Number: {threading.activeCount() - 1}')
        finally:
            logging.info(f'Socket is Disconnecting with {self.url}:{self.port}...')
            listener.close()

    # Handle receive HTTP msg
    def http_handler(self, conn, addr):

        try:
            data = b""
            while True:

                #temp = 
                data += conn.recv(BUFF_SIZE)
                if(len(conn.recv(BUFF_SIZE)) < BUFF_SIZE): 
                    #data += conn.recv(BUFF_SIZE)
                    break

                # temp = conn.recv(BUFF_SIZE)
                # data += temp
                # if(len(temp) < BUFF_SIZE): break;
            # Process HTTP request
            request_pared = HttpRequestParsed(data.decode('utf-8'))
            
            self.response_body = request_pared.response_body
            self.access_file_manager = request_pared.access_file_manager

            # Process Get/Post with File Manager
            if(self.access_file_manager):
                self.handle_files_request(request_pared.method, request_pared.path, request_pared.accept_type)

            response_content = self.generate_response_content(request_pared)

            logging.debug(f'Received HTTP Request -> {data}')
            conn.send(response_content.encode('utf-8'))
        finally:
            conn.close()
    
    # Call File Manager
    def handle_files_request(self, method, path, accept_type):

        file_manager = FileManager(self.verbose, self.dir_path, accept_type)

        if(method == "GET"):
            # General GET files list request as "/", and GET file content
            if(path == "/"):
                file_manager.get_files_list()
            else:
                file_manager.get_file_content(path)
            # Content-Disposition
            if(file_manager.disposition):
                self.disposition = file_manager.disposition

            self.response_body = file_manager.content
            self.code = file_manager.code
        
        if(method == "POST"):
            # General POST request as "/post"
            if(path == "/post"):
                self.code = "200"
                self.response_body = json.dumps(self.response_body, indent=2, sort_keys=True)
            else:
                file_manager.post_file_handler(path, self.response_body["data"])
                # With 200 code as successes, and ERROR with 401, 404
                if(file_manager.code == "200"):
                    self.response_body = json.dumps(self.response_body, indent=2, sort_keys=True)
                    self.code = file_manager.code
                else:
                    self.response_body = file_manager.content
                    self.code = file_manager.code


    def generate_response_content(self, request):

        header = (
            request.http_version + " " + self.code + " " + self.status.get(self.code) + "\r\n" +
            "Date: " + self.get_date() + "\r\n" +
            "Content-Type: " + self.process_content_type(request.accept_type) + "\r\n")
        
        if(self.disposition): header += self.disposition

        header += (
            "Content-Length: " + str(len(self.response_body)) + "\r\n" +
            "Connection: close \r\n" +
            "\r\n"
        )
        # Response with JSON Format with general GET or POST request
        if (not self.access_file_manager): self.response_body = json.dumps(self.response_body, indent=2, sort_keys=True)

        return header + self.response_body

    # Format time info for Logging
    def get_date(self):
        return time.strftime("%a, %d %b %y %H:%M:%S", time.localtime(time.time()))


    def process_content_type(self, accept_type):
        dic_type = {"json":"application/json;", "xml":"application/xml;", "html":"text/html;", "plain":"text/txt"}
        # if not exist, then set as NONE
        return dic_type.get(accept_type)

class HttpRequestParsed():
    def __init__(self, request):
        self.response_body = {}
        self.access_file_manager = False
        self.content_type = "json"
        self.accept_type = "json"
        self.path = ""
        self.parseText(request)
    
    def parseText(self, request):

        header, body = request.split("\r\n\r\n")
        headers = header.split("\r\n")

        logging.debug(f"Received Header -> {header}, Body -> {body}")

        self.method, self.path, self.http_version = headers[0].split(" ")
        # Request with Accept type
        if(re.search(r'Accept:(.+?\S+)', header)):
            accept_type = re.findall(r'Accept:\s*(.+?\S+)', header)[0]
            logging.debug(f"Processing request with accept type {accept_type}")
            self.accept_type = self.process_accept_type(accept_type)

        logging.debug(f"method -> {self.method}, path -> {self.path}, version -> {self.http_version}, accept type -> {self.accept_type}")

        # Process GET request with inline parameters, For example /get?course=networking&assignment=2
        if (re.search(r'/get\?(\S+)', self.path)):
            dic = {}
            params = re.findall(r'/get\?(\S+)', self.path)[0]
            for param in params.split("&"):
                key, value = param.split("=")
                dic[key] = value
            self.response_body["arg"] = dic
        else:
            self.access_file_manager = True

        # Process HTTP request with header
        dic = {}
        for header in headers[1:]:
            key, value = header.split(":")
            dic[key] = value
        self.response_body["headers"] = dic

        if(self.method == "POST"):
            self.access_file_manager = True
            self.response_body["data"] = body

    # Process only handle Four different type 
    def process_accept_type(self, accept_type):
        dic_type = {"application/json":"json", "application/xml":"xml", "text/html":"html", "text/plain":"txt"}
        # if not exist, then set as NONE
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