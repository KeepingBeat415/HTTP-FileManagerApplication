import os, logging, sys, json
# application/json
# text/html
# text/plain



class FileManager():

    def __init__(self, dir_path, accept_type):
        # self.method = method
        self.dir_path = os.path.dirname(os.path.realpath(__file__)) + "/" + dir_path
        self.code = ""
        self.content = ""
        self.accept_type = accept_type
        self.status = { "200":"OK", "400":"Bad Request", "401":"Unauthorized", "404":"Not Found"}
        logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y/%m/%d %H:%M:%S', stream=sys.stdout, level=logging.INFO)


    def get_files_list(self):

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
                print(f"[DEBUG]: POST Body Value from file -> {content}") 
            self.generate_file_by_type(self.accept_type, content)

    
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