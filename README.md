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
