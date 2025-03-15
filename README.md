# fastapi-todo project 

uv sync


uv run uvicorn main:app --reload 

or

uv run fastapi run

# auth check
curl -X POST "http://172.21.65.97:30101/realms/master/protocol/openid-connect/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "client_id=fastapi-todo" \
  -d "client_secret=gek0FJj8FCdu2cMGVGPFhWc5dAnbtR9B" \
  -d "username=krishna.km" \
  -d "password=Password1" \
  -d "grant_type=password"

# use the token got from above command

curl -X 'GET' \
  'http://localhost:8000/status/health' \
  -H 'accept: application/json' \
  -H "Authorization: Bearer <token>"


# load test 
install locust

uv add locust

create locustfile.py file 

run command:  locust

or

locust -f locustfile.py

or

locust -f locustfile.py --headless --users 10 --spawn-rate 10 --run-time 5m --html=locust_report.html

access locut ui at : http://localhost:8089/


## common load issues
too many file descriptors

fix:

wmic process where name="python.exe" CALL setpriority "above normal"

or

ulimit -n 100000

or

uvicorn app:app --host 0.0.0.0 --port 8000 --loop uvloop

or increase gunicorn worker

gunicorn -k uvicorn.workers.UvicornWorker -w 4 app:app


