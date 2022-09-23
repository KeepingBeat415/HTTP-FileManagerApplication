## Heading

1. HTTP GET

- get 'http://httpbin.org/get?course=networking&assignment=1'
- get -v 'http://httpbin.org/get?course=networking&assignment=1'
- get -h key:value 'http://httpbin.org/get?course=networking&assignment=1'
- get -h key1:value1 key2:value2 'http://httpbin.org/get?course=networking&assignment=1'
- get -v 'http://httpbin.org/status/301'
- get 'http://httpbin.org/status/418' -o hello.txt
- get -v 'http://httpbin.org/get?course=networking&assignment=1' -o hello.txt
