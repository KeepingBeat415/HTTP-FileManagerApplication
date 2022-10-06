## HTTPC HELP

- httpc help
- httpc help get
- httpc help post

## HTTP GET

- httpc get 'http://httpbin.org/get?course=networking&assignment=1'
- httpc get -v 'http://httpbin.org/get?course=networking&assignment=1'
- httpc get -h key:value 'http://httpbin.org/get?course=networking&assignment=1'
- httpc get -h key1:value1 -h key2:value2 'http://httpbin.org/get?course=networking&assignment=1'
- httpc get -v 'http://httpbin.org/status/301'
- httpc get 'http://httpbin.org/status/418' -o teapot_GET.txt
- httpc get 'http://httpbin.org/get?course=networking&assignment=1' -o hello_GET.txt

## HTTP POST

- httpc post -v -h Content-Type:application/json -h Accept:application/json http://httpbin.org/post
- httpc post -v -h Content-Type:application/json -d '{"Course": "COMP445","Assignment": 1}' http://httpbin.org/post
- httpc post -h Content-Type:application/json -f POST.json http://httpbin.org/post
- httpc post -v -h Content-Type:application/json -d '{"Course": "COMP445","Assignment": 1}' -f hello_POST.json http://httpbin.org/post
- httpc post -v http://httpbin.org/status/301
- httpc post -v -h Content-Type:application/json -d '{"Course": "COMP445","Assignment": 1}' http://httpbin.org/post -o hello_POST.txt
