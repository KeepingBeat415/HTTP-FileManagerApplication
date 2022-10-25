## Run Server with Commend Line: httpfs [-v] [-p PORT] [-d PATH-TO-DIR]

- Default Verbose: False, PORT: 8080, Directory: data
- Server handle response type with: application/json (default), text/plain, text/html, application/xml
- Content-Disposition: Get request with file name + "/download"

### Basic HTTP GET

- httpc get -v 'http://localhost:8080/get?course=networking&assignment=1'
- httpc get -v -h key1:value1 -h key2:value2 'http://localhost:8080/get?course=networking&assignment=1'

### GET File List

- httpc get -v -h Accept:application/xml 'http://localhost:8080/' (Good Case)
- httpc get -v -h Accept:application/pdf 'http://localhost:8080/' (Bad Case)

### GET File Content

- httpc get -v -h Accept:text/plain 'http://localhost:8080/teapot' (Good Case)
- httpc get -v -h Accept:text/html 'http://localhost:8080/sub/foo' (Good Case, access file in the sub-directory)

- httpc get -v -h Accept:text/html 'http://localhost:8080/foo.txt' (Bad Case, file not exist)
- httpc get -v -h Accept:text/html 'http://localhost:8080/sub/../../README.txt' (Bad Case, authority issue)

### Basic HTTP POST

- httpc post -v -h Content-Type:application/json -h Accept:application/json -d '{"Course": "COMP445","Assignment": 2}' http://localhost:8080/post

### POST File Content

- httpc post -v -h Content-Type:application/json -d '{"File Path": "data/foo","Course": "COMP445","Assignment": 2}' http://localhost:8080/foo (Good Case, inline parameter post)
- httpc post -v -h Content-Type:application/json -f bar http://localhost:8080/bar (Good Case, file content post)

- httpc post -v -h Content-Type:application/json -d '{"File Path": "fake/foo","Course": "COMP445","Assignment": 2}' http://localhost:8080/fake/foo (Bad Case, file not exist)
- httpc post -v -h Content-Type:application/json -f bar 'http://localhost:8080/sub/../../README.txt' (Bad Case, authority issue)

### Content-Disposition

- httpc get -v 'http://localhost:8080/foo/download' (Good Case)
- httpc get -v -h Accept:text/html 'http://localhost:8080/bar/download' (Good Case, with accept type)
