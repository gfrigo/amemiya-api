# amemiya-api

Para Iniciar o servidor da Api:

"uvicorn main:app --reload"

Tente enviar credenciais de login:

bash: "curl -i -X POST "http://127.0.0.1:8000/login"   -H "Content-Type: application/json"   -d '{"user":"userTeste","password":"senhaCerta"}'"

cmd: curl -i -X POST "http://127.0.0.1:8000/login" -H "Content-Type: application/json" -d "{\"user\":\"userTeste\",\"password\":\"senhaCerta\"}"

exemplo de resposta:

HTTP/1.1 200 OK
\
date: Wed, 15 Oct 2025 20:02:25 GMT
\
server: uvicorn
\
content-length: 222
\
content-type: application/json

{
    "detail":{
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
