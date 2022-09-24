## HTTP GET

- get 'http://httpbin.org/get?course=networking&assignment=1'
- get -v 'http://httpbin.org/get?course=networking&assignment=1'
- get -h key:value 'http://httpbin.org/get?course=networking&assignment=1'
- get -h key1:value1 -h key2:value2 'http://httpbin.org/get?course=networking&assignment=1'
- get -v 'http://httpbin.org/status/301'
- get 'http://httpbin.org/status/418' -o hello_GET.txt
- get -v 'http://httpbin.org/get?course=networking&assignment=1' -o hello_GET.txt

## HTTP POST

- post -v -h Content-Type:application/json -h Accept:application/json http://httpbin.org/post
- post -v -h Content-Type:application/json -d '{"Course":"COMP445","Assignment": 1}' http://httpbin.org/post
- post -v -h Content-Type:application/json -f POST.json http://httpbin.org/post
- post -v -h Content-Type:application/json -d '{"Course":"COMP445","Assignment": 1}' -f POST.json http://httpbin.org/post
- post -v 'http://httpbin.org/status/301'
- post -v -h Content-Type:application/json -d '{"Course":"COMP445","Assignment": 1}' http://httpbin.org/post -o HELLO_POST.txt
