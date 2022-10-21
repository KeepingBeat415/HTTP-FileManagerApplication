import argparse
import logging





# str = "httpfs -v -p 8080 -d data"
cmd = "httpfs -v -p 9090 -d hete"

# if(cmd.startswith("httpfs")):

#     cmd = cmd[6:]
#             # Set Logging Debug or Info
#             if("-v" in cmd): 
#                 self.verbose = True
#                 logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y/%m/%d %H:%M:%S', stream=sys.stdout, level=logging.DEBUG)
#             else:
#                 self.verbose = False
#                 logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y/%m/%d %H:%M:%S', stream=sys.stdout, level=logging.INFO)
#             # Set Port
#             if("-p" in cmd and re.search(r'-p (\S.+?\S+)', cmd)): 
#                 self.port = int(re.findall(r'-p (\S.+?\S+)', cmd)[0])
#             # Set server directory
#             if("-d" in cmd and re.search(r'-d (\S.+?\S+)', cmd)):
#                 self.dir_path = re.findall(r'-d (\S.+?\S+)', cmd)[0]
#                 is_exist_path = os.path.dirname(os.path.realpath(__file__)) + "/" + self.dir_path
#                 if(not os.path.exists(is_exist_path)): 
#                     return logging.info("File Manger Server Directory is not exist.")
            
#             logging.info(f"HTTP File Manager Server Setting: Port - {self.port}, Directory - {self.dir_path}, Verbose - {self.verbose}")

#             self.run_server()
# else:
#     logging.info("\n[ERROR]: Invalid Command.")

try:
    cmd_parser = argparse.ArgumentParser(description='Process some integers.')

    cmd_parser.add_argument('-v', dest='verbose', action=argparse.BooleanOptionalAction, help='verbose', default=False)
    cmd_parser.add_argument('-p', dest='port', help='server socket port', type=int, default=8080)
    cmd_parser.add_argument('-d', dest='dir_path', help='file manager directory',default='data')
    args = cmd_parser.parse_args(cmd[6:0].split()) # remove httpfs

except:
    print("\n[ERROR]: Invalid Command.")
    #print(args)


            # # Set Logging Debug or Info
            # if("-v" in cmd): 
            #     self.verbose = True

            # else:
            #     self.verbose = False
                
            # # Set Port
            # if("-p" in cmd and re.search(r'-p (\S.+?\S+)', cmd)): 
            #     self.port = int(re.findall(r'-p (\S.+?\S+)', cmd)[0])
            # # Set server directory
            # if("-d" in cmd and re.search(r'-d (\S.+?\S+)', cmd)):
            #     self.dir_path = re.findall(r'-d (\S.+?\S+)', cmd)[0]

            

# class test1():

#     def __init__(self):
#         self.port = 0
#         pass

#     def run(self, cmd):
#         cmd_parser = argparse.ArgumentParser(description='Process some integers.')

#         # cmd_parser.add_argument('-v', dest='verbose', action=argparse.BooleanOptionalAction, help='verbose', default=False)
#         cmd_parser.add_argument('-p', dest=self.port, help='server socket port', type=int, default=8080)
#         #cmd_parser.add_argument('-d', dest='dir_path', help='file manager directory',default='data')
#         cmd_parser.parse_args(cmd.split())
#         print(f"==>{self.port}")

# test = test1()

# test.run("-p 2020")
# parser.add_argument('url', help='URL')
# parser.add_argument('-d', dest='data', help='POST data')
# parser.add_argument('-f', dest='infile', help='file containing POST data')
# parser.add_argument('-o', dest='outfile', help='file to store response')
# parser.add_argument('-H', dest='headers', action='append', help='HTTP Header to include')