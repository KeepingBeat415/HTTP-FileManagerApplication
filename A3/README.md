./router --port=3000 --drop-rate=0.4 --max-delay=1000ms --seed=1

- httpc get -v 'http://localhost:8080/'
- httpc get -v 'http://localhost:8080/foo'

- httpc post -v -h Content-Type:application/json -d '{"File Path": "data/foo","Course": "COMP445","Assignment": 3}' http://localhost:8080/foo (Good Case, inline parameter post)
