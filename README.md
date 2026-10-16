# TDS FastAPI Stats API

## Local run
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

Test: `curl -i 'http://127.0.0.1:8000/stats?values=1,2,3'`

Allowed preflight:
```bash
curl -i -X OPTIONS 'http://127.0.0.1:8000/stats' -H 'Origin: https://dash-e51i9s.example.com' -H 'Access-Control-Request-Method: GET'
```

Rejected-origin preflight (must have no Access-Control-Allow-Origin):
```bash
curl -i -X OPTIONS 'http://127.0.0.1:8000/stats' -H 'Origin: https://evil.example' -H 'Access-Control-Request-Method: GET'
```

## Deploy on Render
1. Push these files to a GitHub repository.
2. In Render, choose New + -> Web Service and connect the repository.
3. Use build command `pip install -r requirements.txt`.
4. Use start command `uvicorn main:app --host 0.0.0.0 --port $PORT`.
5. Deploy and test `/stats?values=1,2,3`.
6. Submit the actual public base URL Render gives you.
