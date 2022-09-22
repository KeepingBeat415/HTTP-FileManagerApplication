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
        if(("help" in cmd and "get" in cmd) or "get" in cmd):
            self.get_help_info("get")
        elif(("help" in cmd and "post" in cmd) or "post" in cmd):
                self.get_help_info("post")
        elif("help" in cmd):
            self.get_help_info("normal")
        else:
            print("[ERROR]: Invalid Command. Type help to list commands. Press 'Ctrl+C' or Type 'quit' to terminate.")


httpc = Httpc()
print("==== Welcome to HTTPC Service ==== \n  Type help to list commands.\n  Press 'Ctrl+C' or Type 'quit' to terminate.")
# Program Start
while True:
    cmd = input("\n")
    if("quit" in cmd):
         break
    print("[DEBUG]:",cmd)
    httpc.execute(cmd)
