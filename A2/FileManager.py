import os, logging, sys, json, re

class FileManager():

    def __init__(self, verbose, dir_path, accept_type):

        self.dir_path = os.path.dirname(os.path.realpath(__file__)) + "/" + dir_path
        self.code = ""
        self.content = ""
        self.accept_type = accept_type
        self.status = { "200":"OK", "400":"Bad Request", "401":"Unauthorized", "404":"Not Found"}
        self.disposition = ""
        # Set Logging info
        if(verbose):
            logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y/%m/%d %H:%M:%S', stream=sys.stdout, level=logging.DEBUG)
        else:
            logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y/%m/%d %H:%M:%S', stream=sys.stdout, level=logging.INFO)

    def get_files_list(self):
        # Support HTML/XML/TXT/JSON
        if (self.accept_type == "NONE"):
            self.code = "400"
            return self.html_exception_handler(self.code, self.status.get("400"), "Accept file type not supported.")

        files_list = []
        self.code = "200"

        for (self.dir_path, dir_names, file_names) in os.walk(self.dir_path):
            files_list.extend(file_names)

        content = " ".join(files_list)
    
        self.generate_file_by_type(self.accept_type, content)

    
    def generate_file_by_type(self, accept_type, content):

        if(accept_type == "json"):
            self.content = json.dumps({"data":content}, indent=2, sort_keys=True) 
        elif(accept_type == "txt"):
            self.content = content
        elif(accept_type == "xml"):
            self.generate_xml_file(content)
        else:
            self.generate_html_file(content)


    def get_file_content(self, path):

        # Handle Content-Disposition 
        if("/download" in path):
            file_name = re.findall(r'/(.+?)/', path)[0]
            logging.debug(f"File Name => {file_name}")
            path = "/" + file_name
            self.disposition = f"Content-Disposition: attachment; filename=\"{file_name}.{self.accept_type}\"\r\n"

        dir_path = self.dir_path + path
        
        if("../" in dir_path):
            self.code = "401"
            logging.info(f"Attempt get content from path: {dir_path}, cause 401 - \"Unauthorized\"")
            self.html_exception_handler(self.code, self.status.get("401"), "Attempt access unauthorized file.")

        elif(not os.path.exists(dir_path)):
            self.code = "404"
            logging.info(f"Attempt get content from path: {dir_path}, cause 404 - \"Not Found\"")
            self.html_exception_handler(self.code, self.status.get("404"), "Access file not exist.")

        else:
            self.code = "200"
            logging.info(f"Attempt get content from path: {dir_path}, cause 200 - \"OK\"")
            with open(dir_path) as file:
                content = file.read()
                logging.debug(f"POST Body Value from file -> {content}") 
            self.generate_file_by_type(self.accept_type, content)


    def post_file_handler(self, path, content):

        dir_path = self.dir_path + path

        if("../" in dir_path):
            self.code = "401"
            logging.info(f"Attempt post content to path: {dir_path}, cause 401 - \"Unauthorized\"")
            self.html_exception_handler(self.code, self.status.get("401"), "Attempt access unauthorized file.")

        elif(not os.path.exists(dir_path)):
            self.code = "404"
            logging.info(f"Attempt post content to path: {dir_path}, cause 404 - \"Not Found\"")
            self.html_exception_handler(self.code, self.status.get("404"), "Access file not exist.")

        else:
            self.code = "200"
            logging.info(f"Attempt post content to path: {dir_path}, cause 200 - \"OK\"")
            with open(dir_path, "w") as file:
                file.write(content)
            file.close()
            logging.debug(f"POST Body Value into {path} -> {content}") 


    def html_exception_handler(self, code, status, msg):
        self.content =  (
                        "<html>\n"+
                        f"  <head><title>{code} {status}</title></head>\n"+
                        "  <body>\n"
                        f"    <center><h1>{code} -- {status}</h1></center>\n"
                        f"    <center><h1>{msg}</h1></center>\n"
                        "  </body>\n"
                        "</html>\n")


    def generate_xml_file(self, content):
        self.content = (
                "<note>\n"+
                "  <heading> XML File </heading>\n"+
                f"  <body>{content}</body>\n"+
                "</note>\n")


    def generate_html_file(self, content):
        self.content =  (
                "<html>\n"+
                "  <head><title>HTML File</title></head>\n"+
                "  <body>\n"
                f"    <center><h1>{content}</h1></center>\n"
                "  </body>\n"
                "</html>\n")