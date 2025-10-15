# amemiya-api

Para Iniciar o servidor da Api:

"uvicorn main:app --reload --host 0.0.0.0 --port 8000"

Tente enviar credenciais de login:

"curl -i -X POST "http://127.0.0.1:8000/login"   -H "Content-Type: application/json"   -d '{"user":"userTeste","password":"senhaCerta"}'"