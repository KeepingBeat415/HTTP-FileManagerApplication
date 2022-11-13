## Run Router for simulate UDP protocol packet delayed and drop

- Default router address: localhost:8080
- Max delay: 3000ms (limit by UDP waiting timeout)

### Router Setting

- ./router -port=3000 --drop-rate=0.5 --max-delay=0ms --seed=8080 (drop rate only)
- ./router -port=3000 --drop-rate=0 --max-delay=1000ms --seed=8080 (delayed only)
- ./router -port=3000 --drop-rate=0.3 --max-delay=1000ms --seed=8080 (both drop and delay)

## The cURL-like command line

### HTTP GET

- httpc get -v -h Accept:application/xml 'http://localhost:8080/' (GET file list)
- httpc get -v -h Accept:application/json 'http://localhost:8080/foo' (GET 'foo' file content)

### HTTP POST

- httpc post -v -h Content-Type:application/json -d '{"File Path": "data/foo","Course": "COMP445","Assignment": 3}' http://localhost:8080/foo (Good Case, inline parameter post)
