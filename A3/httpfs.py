import sys, time, socket, logging, os.path, threading, argparse
from FileManager import FileManager
from udpService import udpService
from const import *

class Httpfs():

    def __init__(self):
        self.url = SERVER_IP
        self.port = SERVER_PORT
        self.dir_path = "data"
        self.verbose = False
        self.status = { "200":"OK", "400":"Bad Request", "401":"Unauthorized", "404":"Not Found", "505":"HTTP Version Not Supported"}

    # Parser input cmd setting
    def execute_cmd(self, cmd):

        if(cmd.startswith("httpfs")):
            
            try:
                # Using ArgumentParser Library
                cmd_parser = argparse.ArgumentParser(prog='httpfs', usage='%(prog)s [-v] [-p PORT] [-d PATH-TO-DIR]', description='Process some integers.')

                cmd_parser.add_argument('-v', dest='verbose', action=argparse.BooleanOptionalAction, help='verbose', default=False)
                cmd_parser.add_argument('-p', dest='port', help='server socket port', type=int, default=8007)
                cmd_parser.add_argument('-d', dest='dir_path', help='file manager directory', default='data')

                args = cmd_parser.parse_args(cmd[6:].split()) # remove httpfs

                self.verbose, self.port, self.dir_path = args.verbose, args.port, args.dir_path
                # Display logging debug msg
                if(self.verbose):
                    logging.basicConfig(format='%(asctime)s [%(levelname)s]: %(message)s', datefmt='%Y/%m/%d %H:%M:%S', stream=sys.stdout, level=logging.DEBUG)
                else:
                    logging.basicConfig(format='%(asctime)s [%(levelname)s]: %(message)s', datefmt='%Y/%m/%d %H:%M:%S', stream=sys.stdout, level=logging.INFO)

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

        logging.info(f"HTTP File Manager Server is listening at {SERVER_IP}:{SERVER_PORT}.")

        # listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_udp_socket = udpService()
        server_udp_socket.conn.bind(('', SERVER_PORT))
        # listener.bind((self.url, self.port))

        try:

            while True:

                server_udp_socket.connect_client()

                #threading.Thread(target=self.http_handler, args=(server_udp_socket,)).start()
                self.http_handler(server_udp_socket)
                # data = server_udp_socket.received_data()

                # logging.debug(f'Received HTTP Request -> {data}')
                # logging.info(f'Socket is listening at {self.url}:{self.port}, Thread Number: {threading.activeCount() - 1}')
        finally:
            logging.info(f'Socket is Disconnecting with {self.url}:{self.port}...')
            server_udp_socket.close()

    # Handle receive HTTP msg
    def http_handler(self, server_udp_socket):

        try:

            data = server_udp_socket.received_data()

            # logging.debug(f'Received HTTP Request -> {data}')

            # Process HTTP request
            processed_response = FileManager(self.verbose, self.dir_path, data.decode("utf-8"))

            response_content = self.generate_response_content(processed_response)

            # logging.debug(f"response content: {response_content}")
            #conn.send(response_content.encode('utf-8'))
            server_udp_socket.send_data(response_content.encode("utf-8"))
        finally:
            logging.info("Client HTTP File Manager Server Request Processed.")


    def generate_response_content(self, response):

        header = (
            response.http_version + " " + response.code + " " + self.status.get(response.code) + "\r\n" +
            "Date: " + self.get_date() + "\r\n")
        # Response with Error Msg with HTML, if != "200"
        if(response.code != "200"):
            header += "Content-Type: text/html\r\n"
        else:
            header += "Content-Type: " + self.process_content_type(response.accept_type) + "\r\n"

        if(response.disposition): header += response.disposition

        header += (
            "Content-Length: " + str(len(response.response_content)) + "\r\n" +
            "Connection: close \r\n" +
            "\r\n"
        )

        return header + response.response_content

    # Format time info for Logging
    def get_date(self):
        return time.strftime("%a, %d %b %y %H:%M:%S", time.localtime(time.time()))


    def process_content_type(self, accept_type):
        dic_type = {"json":"application/json;", "xml":"application/xml;", "html":"text/html;", "txt":"text/txt"}
        # if not exist, then set as NONE
        return dic_type.get(accept_type)


print("\n"+"="*10+"Welcome to Httpfs Server"+"="*10)
# Initial HTTP 
httpfs = Httpfs()
# Program Start
# while True: 
#     try:
#         cmd = input("\nHttpfs is a simple file server." +
#                     "\nusage: Httpfs [-v] [-p PORT] [-d PATH-TO-DIR]" +
#                     "\n-v  Prints debugging messages." +
#                     "\n-p  Specifies the port number that the server will listen and serve at. Default is 8080." +
#                     "\n-d  Specifies the directory that the server will use to read/write requested files." +
#                     "\nDefault is the current directory when launching the application." +
#                     "\nPress 'Ctrl+C' or Type 'quit' to terminate.\n\n")
#         if("quit" in cmd): break
#         httpfs.execute_cmd(cmd)
#     except KeyboardInterrupt:
#         sys.exit()

# ============ AUTO DEBUG For A3 ============
input_cmd_A3 = [
"httpfs -v",
]


for cmd in input_cmd_A3:
    print("\ncmd -> "+cmd+"\n")
    httpfs.execute_cmd(cmd)





