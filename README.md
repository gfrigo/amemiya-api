# amemiya-api

Para Iniciar o servidor da Api:

"uvicorn main:app --reload"

Envio de dados de login:

bash: "curl -i -X POST "http://127.0.0.1:8000/login"   -H "Content-Type: application/json"   -d '{"user":"userTeste","password":"senhaCerta"}'"

cmd: curl -i -X POST "http://127.0.0.1:8000/login" -H "Content-Type: application/json" -d {\\"user\\":\\"userTeste\\",\\"password\\":\\"senhaCerta\\"}"

exemplo de resposta:

HTTP/1.1 200 OK
date: Wed, 15 Oct 2025 20:02:25 GMT
server: uvicorn
content-length: 222
content-type: application/json

{
    "detail": {
        "name": "userTeste",
        "inner_register": null,
        "email": "teste@example.com",
        "telephone": "0123456789", 
        "role": "Função Teste",
        "admin": 1,
        "company": "root",
        "image_path": "assets/profiles/default.png"
    }
}

Envio de dados de edição de usuário:

cmd:

curl -i -X POST "http://127.0.0.1:8000/user/edit" -H "Content-Type: application/json" -d "{\\"user_id\\":1, \\"user_name\\":\\"Felipe Almeida\\",\\"inner_register\\":\\"1\\",\\"email\\":\\"flpalmeidac@gmail.com\\",\\"telephone\\":\\"11981272374\\",\\"role_id\\":1,\\"admin\\":false,\\"company_id\\":1,\\"image_path\\":\\"assets/felipe.png\\",\\"active_user\\":true}"

exemplo de resposta:

HTTP/1.1 201 Created
date: Fri, 17 Oct 2025 17:06:41 GMT
server: uvicorn
content-length: 46
content-type: application/json

{
    "detail": "User register edited successfully"
}

## Running the API

- Install dependencies: pip install -r requirements.txt
- Create a .env file with:
  - DB_HOST=
  - DB_USER=
  - DB_PASSWORD=
  - DB_SCHEMA=
  - (optional) APP_NAME, APP_VERSION
- Start server: uvicorn main:app --reload

## Health Check

- GET http://127.0.0.1:8000/health → {"status": "ok"}

## Notes

- Configuration is centralized in app/settings.py (loaded from .env).
- Validation for required fields now returns HTTP 400 automatically when missing.
- Class User_Endpoints was renamed to UserEndpoints for PEP8 compliance.
