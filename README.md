# amemiya-api

# Rodando a API

Instale as dependências:
>     pip install -r requirements.txt

Preencha o arquivo `.env` com os dados de conexão do Banco de Dados:
>     DB_HOST
>     DB_USER
>     DB_PASSWORD
>     DB_SCHEMA

Inicie o servidor:
>     uvicorn main:app --reload

Ou use `docker compose` para levantar ambiente de teste (MySQL + Mosquitto + API + worker):

```
docker compose up --build
```

Observações importantes:
- O endpoint de login agora retorna um token JWT no campo `token` quando autenticado com sucesso. Use esse token para autenticação nas chamadas que venham a exigir um Bearer token.
- Senhas são armazenadas (ou serão migradas) como hash bcrypt quando possível. Caso a tabela contenha senhas em texto, no primeiro login a senha será re-hashada automaticamente.
- Para testes MQTT local: há um endpoint de publicação `POST /mqtt/publish?company_id=<id>&device_id=<id>` que publica no tópico `amemiya/{company_id}/device/{device_id}/telemetry`.

Aviso de segurança: o `docker/mosquitto/mosquitto.conf` atual permite conexões anônimas e serve apenas para testes locais. Para produção use o arquivo de template `docker/mosquitto/secure_mosquitto.conf` e siga as instruções para habilitar TLS e autenticação.

Simulador Node.js (dispositivo)
--------------------------------

Um simulador simples em Node.js foi adicionado em `tools/device_simulator`. O simulador faz o seguinte fluxo:

- Faz `POST /login/` na API com `email` e `password` para obter um JWT.
- Conecta ao broker MQTT (EMQX) em `mqtt://localhost:1883` usando o JWT como `password` (o plugin `emqx_auth_http` vai validar o token contra `/mqtt/auth`).
- Publica N mensagens no tópico `amemiya/{company_id}/device/{device_id}/telemetry`.

Como usar o simulador (exemplo):

1. Instalar dependências do simulador (dentro da pasta `amemiya-api`):

```powershell
cd amemiya-api\tools\device_simulator
npm install
```

2. Executar simulador (exemplo):

```powershell
node index.js --company 1 --device device01 --email teste@example.com --password teste123 --count 10 --interval 500
```

Parâmetros úteis:
- `--api`: base URL da API (default `http://localhost:8000`)
- `--broker`: URL do broker MQTT (default `mqtt://localhost:1883`)
- `--company`, `--device`, `--email`, `--password` são obrigatórios
- `--count`: quantas mensagens publicar (default 5)
- `--interval`: intervalo em ms entre mensagens (default 1000)

Observações de segurança e execução:
- O EMQX no `docker-compose` está configurado para usar o plugin `emqx_auth_http` e chama `POST http://api:8000/mqtt/auth` para validar tokens. O simulador passa o token obtido como `password` na conexão MQTT.
- Em ambiente local, as portas expostas no `docker-compose` são: `1883` (MQTT), `8083` (WebSocket) e `18083` (dashboard EMQX). Devem estar livres para serem usadas.

Criação automática da tabela `Telemetry`:
---------------------------------------

Ao iniciar a API (via `uvicorn` ou via `docker compose up`), o serviço executa uma verificação e cria a tabela `Telemetry` caso ela não exista. A tabela usa tipo `JSON` para o campo `payload` (MySQL 5.7+/8.0+).

DDL usado (apenas para referência):

```sql
CREATE TABLE IF NOT EXISTS Telemetry (
	id BIGINT AUTO_INCREMENT PRIMARY KEY,
	company_id INT NULL,
	device_id VARCHAR(128) NULL,
	payload JSON,
	created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

Se preferir criar a tabela manualmente, use o DDL acima no seu banco.

Testes automatizados
---------------------

Para executar os testes unitários criados (autenticação e worker mockado):

1. Instale dependências de teste (dentro de `amemiya-api`):

```powershell
pip install -r requirements.txt
```

2. Execute o pytest na pasta `amemiya-api`:

```powershell
cd amemiya-api
pytest -q
```

Os testes usam mocks e não precisam de broker/DB reais para executar.

Script SQL
----------

Um script SQL para criar a tabela `Telemetry` manualmente foi adicionado em `amemiya-api/sql/create_telemetry_table.sql`.


---

# Referência da API

Os endpoints funcionam com quatro métodos HTTP:

- **GET** para métodos de Busca / Consulta, como *query* de dados de um usuário;
- **POST** para métodos de Inserção / Criação, como criação de veículos ou *upload* de uma nota;
- **PUT** para métodos de Atualização / Alteração, como troca de foto de perfil ou alteração de dados de um usuário;
- **DELETE** para métodos de Remoção de um registro, como deleção de um anexo.

---

## *Endpoints* de usuário

**A ser retrabalhado**  

| Endpoint                                                                 | Tipo | Formato             | Formato da Resposta | Descrição                                    |
|--------------------------------------------------------------------------|------|---------------------|---------------------|----------------------------------------------|
| [/user/fetch](#fetch-post-json)                                          | POST | application/json    |                     | Consulta de dados de um ou múltiplos usuário |
| [/user/add](#add-post-json)                                              | POST | application/json    |                     | Adiciona o registro de um usuário            | 
| [/user/edit](#edit-post-json)                                            | POST | application/json    |                     | Modifica o registro de um usuário            | 
| [/user/profile_picture/{user_id}](#profile_pictureuser_id-put-form-data) | PUT  | multipart/form-data |                     | Modifica a foto de perfil de um usuário      |
| [/user/remove](#edit-post-json)                                          | POST | application/json    |                     | Remove o registro de um usuário              |

---

[<-](#endpoints-de-usuário)

### /fetch (POST json)  
Consulta de dados de um ou múltiplos usuário

**Parâmetros**:  
`company_id`: *integer*    
`user_id`: *integer* (opcional)

**Chamada exemplo**:  

HTTP Client:
>     POST http://localhost:8000/user/fetch
>     Content-Type: application/json
> 
>     {
>       "company_id": 1,
>       "user_id": 30
>     }

CMD:
>     curl -X POST "http://localhost:8000/user/fetch" -H "Content-Type: application/json" -d "{\"company_id\": 1, \"user_id\": 30}"
  
**Resposta**:  
>     200 OK
> 
>     {
>       "detail": {
>         "user_id":30,
>         "user_name":"teste123",
>         "inner_register":"1",
>         "password":"teste123",
>         "email":"teste2@example.com",
>         "telephone":"2345678901",
>         "role_id":1,
>         "admin":0,
>         "company_id":1,
>         "profile_picture_id":1,
>         "active_user":1
>       }
>     }

---

[<-](#endpoints-de-usuário)

### /add (POST json)  
Adiciona o registro de um usuário

**Parâmetros**:  
`user_name`: *string*  
`inner_register`: *string* (opcional)  
`password`: *string*  
`email`: *string*  
`telephone`: *string*  
`role_id`: *integer*  
`admin`: *boolean* (opcional, *default* False)  
`company_id`: *integer*  
`active_user`: *boolean* (opcional, *default* True)

**Chamada exemplo**:  

HTTP Client:
>     POST http://localhost:8000/user/add
>     Content-Type: application/json
> 
>     {
>       "user_name": "teste_add",
>       "inner_register": "12a3bc",
>       "password": "senhaTeste",
>       "email": "teste_add@example.com",
>       "telephone": "1234567890",
>       "role_id": "1",
>       "admin": "True",
>       "company_id": "1"
>     }

CMD:
>     curl -X POST "http://localhost:8000/user/add" -H "Content-Type: application/json" -d "{\"user_name\":\"teste_add\",\"inner_register\":\"12a3bc\",\"password\":\"senhaTeste\",\"email\":\"teste_add@example.com\",\"telephone\":\"1234567890\",\"role_id\":\"1\",\"admin\":\"True\",\"company_id\":\"1\"}"

**Resposta**:  
>     {
>       "detail":"User added successfully"
>     }

---

[<-](#endpoints-de-usuário)

### /edit (POST json)  
Modifica o registro de um usuário dados os campos a serem modificados

**Parâmetros**:  
`user_id`: *integer*  
`user_name`: *string* (opcional)  
`inner_register`: *string* (opcional)  
`password`: *string* (opcional)  
`email`: *string* (opcional)  
`telephone`: *string* (opcional)  
`role_id`: *integer* (opcional)  
`admin`: *boolean* (opcional)  
`company_id`: *integer* (opcional)  
`active_user`: *boolean* (opcional)

**Chamada exemplo**:  

HTTP Client:
>     POST http://localhost:8000/user/edit
>     Content-Type: application/json
> 
>     {
>       "user_id": "30",
>       "user_name": "teste_edit",
>       "telephone": "234567890",
>       "admin": "False"
>     }

CMD:
>     curl -X POST "http://localhost:8000/user/edit" -H "Content-Type: application/json" -d "{\"user_id\":\"30\",\"user_name\":\"teste_edit\",\"telephone\":\"234567890\",\"admin\":\"False\"}"

**Resposta**:  
>     {
>       "detail":"User edited successfully"
>     }

---

[<-](#endpoints-de-usuário)

### /profile_picture/{user_id} (PUT form-data)  
Adiciona a foto de perfil de um usuário

**Parâmetros**:  
`company_id`: *integer*  
`user_id`: *integer*  
`file_type`: *string*
`file`: *file/binary* (arquivo como multipart/form-data)

**Chamada exemplo**:  

HTTP Client:
>     PUT http://localhost:8000/user/profile_picture/30
>     Content-Type: multipart/form-data
> 
>     {
>       "company_id": "1",
>       "file_type": "png",
>       "file": "@teste_profile_picture.png"
>     }

CMD:
>     curl -X PUT "http://localhost:8000/user/profile_picture/30" -F "company_id=1" -F "file_type=png" -F "file=@teste_profile_picture.png"

**Resposta**:  
>     {
>       "detail":"User edited successfully"
>     }

---

[<-](#endpoints-de-usuário)

### /remove (POST json)  
Remove o registro de um usuário
**ATENÇÃO: Remover um registro remove as entries dependentes deste usuário em cascata, como todos os anexos adicionados.**

**Parâmetros**:  
`user_id`: *integer*

**Chamada exemplo**:  

HTTP Client:
>     POST http://localhost:8000/user/remove
>     Content-Type: application/json
> 
>     {
>       "user_id": "30"
>     }

CMD:
>     curl -X POST "http://localhost:8000/user/remove" -H "Content-Type: application/json" -d "{\"user_id\":\"30\"}"

**Resposta**:  
>     {
>       "detail":"User removed successfully"
>     }

---

## *Endpoints* de anexo

| Endpoint                                                | Tipo   | Formato             | Descrição                                |
|---------------------------------------------------------|--------|---------------------|------------------------------------------|
| [/attachment/{company_id}](#company_id-get)             | GET    |                     | Consulta de dados um ou múltiplos anexos |
| [/attachment/](#-post-multipartform-data)               | POST   | multipart/form-data | Adiciona registro de um anexo            | 
| [/attachment/{attachment_id} ](#attachment_id-put-json) | PUT    | application/json    | Modifica o registro de um usuário        | 
| [/attachment/{attachment_id}](#attachment_id-delete)    | DELETE |                     | Remove o registro de um anexo            |

---

[<-](#endpoints-de-anexo)

### /{company_id} (GET)  
Consulta de dados um ou múltiplos anexos

**Parâmetros**:  
`company_id`: *int*  
`user_id`: *int* (opcional)  
`attachment_type`: *str* (opcional)  
`date_range_start`: *str* (opcional)  
`date_range_end`: *str* (opcional)

**Chamada exemplo**:  

HTTP Client:
>     GET http://localhost:8000/attachment/123?user_id=45&attachment_type=image&date_range_start=2025-01-01&date_range_end=2025-12-31


CMD:
>     curl -X GET "http://localhost:8000/attachment/1?user_id=1&date_range_start=2025-09-01&date_range_end=2025-12-31"
  
**Resposta**:  
>     {  
>       "detail":{   
>         "1":{  
>           "company_name":"root",  
>             "user_name":"Felipe Almeida de Carvalho",  
>             "file_data":"...",  
>             "file_type":"png",  
>             "attachment_type":"profile_picture",  
>             "upload_date":"2025-10-30T18:39:49"  
>         }, "1":{  
>             "company_name":"root",  
>             "user_name":"Felipe Almeida de Carvalho",  
>             "file_data":"...",  
>             "file_type":"png",  
>             "attachment_type":"profile_picture",  
>             "upload_date":"2025-10-30T18:41:21"  
>         }, "3":{  
>             "company_name":"root",  
>             "user_name":"Felipe Almeida de Carvalho",  
>             "file_data":"...",  
>             "file_type":"png",  
>             "attachment_type":"profile_picture",  
>             "upload_date":"2025-10-30T18:42:58"   
>         }  
>       }  
>     }

---

[<-](#endpoints-de-anexo)

### / (POST multipart/form-data)  
Adiciona registro de um anexo

**Parâmetros**:  
`company_id`: *int* (form field)  
`user_id`: *int* (form field)  
`file`: *file* (binary, UploadFile)  
`file_type`: *str* (form field)  
`attachment_type`: *str* (form field)

**Chamada exemplo**:  

HTTP Client:
>     POST http://localhost:8000/attachment/
>     Content-Type: multipart/form-data
>     
>     company_id=1
>     user_id=1
>     file=@teste.png
>     file_type=png
>     attachment_type=nota_fiscal

CMD:
>     curl -X POST "http://localhost:8000/attachment/" -F "company_id=1" -F "user_id=1" -F "file=@teste.png" -F "file_type=png" -F "attachment_type=nota_fiscal"

**Resposta**:  
>     {
>       "detail":"Attachment added successfully"
>     }

---

---

[<-](#endpoints-de-anexo)

### /{attachment_id} (PUT json)  
Modifica o registro de um anexo dados os campos a serem modificados

**Parâmetros**:  
`attachment_id`: *integer*  
`uploaded_by_company_id`: *integer* (opcional)  
`uploaded_by_user_id`: *integer* (opcional)  
`file_data`: *string* (opcional)  
`file_type`: *string* (opcional)  
`attachment_type`: *string* (opcional)  

**Chamada exemplo**:  

HTTP Client:
>     PUT http://localhost:8000/attachment/7
>     Content-Type: application/json
> 
>     {
>       "uploaded_by_company_id": "1",
>       "uploaded_by_user_id": "32",
>       "attachment_type": "teste"
>     }

CMD:
>     curl -X PUT "http://localhost:8000/attachment/7" -H "Content-Type: application/json" -d "{\"uploaded_by_company_id\":\"1\",\"uploaded_by_user_id\":\"32\",\"attachment_type\":\"teste\"}"

**Resposta**:  
>     204 No Content

---

[<-](#endpoints-de-anexo)

### /{attachment_id} (DELETE)  
Remove o registro de um anexo

**Parâmetros**:  
`attachment_id`: *integer*

**Chamada exemplo**:  

HTTP Client:
>     DELETE http://localhost:8000/attachment/7

CMD:
>     curl -X DELETE "http://localhost:8000/attachment/7"

**Resposta**:  
>     204 No Content

---

## *Endpoints* de login

**A ser retrabalhado**  

| Endpoint                    | Tipo | Formato             | Descrição                                 |
|-----------------------------|------|---------------------|-------------------------------------------|
| [/login/](#fetch-post-json) | POST | application/json    | Recebe dados de login e verifica o acesso |

---

[<-](#endpoints-de-login)

### / (POST json)  
Verifica o acesso das credenciais de login

**Parâmetros**:  
`email`: *string*    
`password`: *string*

**Chamada exemplo**:  

HTTP Client:
>     POST http://localhost:8000/login/
>     Content-Type: application/json
> 
>     {
>       "email": "teste@example.com",
>       "password": "teste123"
>     }

CMD:
>     curl -X POST "http://localhost:8000/login/" -H "Content-Type: application/json" -d "{\"email\": \"teste@example.com\", \"password\": \"teste123\"}"
  
**Resposta**:  
>     {
>       "detail": {
>         "access": true,
>         "data": {
>           "user_id": 1,
>           "user_name": "Felipe Almeida de Carvalho",
>           "inner_register": "1",
>           "email": "flpalmeidac@gmail.com",
>           "telephone": "5511981272374",
>           "role_name": "Função Teste",
>           "admin": true,
>           "company_name": "root",
>           "profile_picture": "..."
>         }
>       }
>     }

---

## *Endpoints* de servidor

| Endpoint                           | Tipo | Formato | Formato da Resposta | Descrição                     |
|------------------------------------|------|---------|---------------------|-------------------------------|
| [/server/status](#fetch-post-json) | GET  |         | json                | Verifica o status do servidor |

---

[<-](#endpoints-de-servidor)

### / (GET)  
Verifica o status do servidor e retorna a data e hora do servidor

**Chamada exemplo**:  

HTTP Client:
>     GET http://localhost:8000/server/status

CMD:
>     curl -X GET "http://localhost:8000/server/status"
  
**Resposta**:  
>     200 OK
>     
>     {
>       "server_status":"OK",
>       "server_time":"2025-11-02 20:45:57"
>     }

---

## *Endpoints* de veículo

**A ser retrabalhado**  

| Endpoint                                  | Tipo | Formato da Requisição | Formato da Resposta | Descrição                                     |
|-------------------------------------------|------|-----------------------|---------------------|-----------------------------------------------|
| [/vehicle/fetch](#vehiclefetch-post-json) | POST | application/json      | json                | Consulta de dados de um ou múltiplos veículos |
| [/vehicle/add](#add-post-json)            | POST | application/json      | json                | Adiciona o registro de um veículo             | 
| [/vehicle/edit](#edit-post-json)          | POST | application/json      | json                | Modifica o registro de um veículo             | 
| [/vehicle/remove](#edit-post-json)        | POST | application/json      | json                | Remove o registro de um veículo               |

---

[<-](#endpoints-de-veículo)

### /vehicle/fetch (POST json)  
Consulta de dados de um ou múltiplos veículos

**Parâmetros**:  
`company_id`: *integer*    
`vehicle_id`: *integer* (opcional)

**Chamada exemplo**:  

HTTP Client:
>     POST http://localhost:8000/vehicle/fetch
>     Content-Type: application/json
> 
>     {
>       "company_id": 1,
>       "user_id": 2
>     }

CMD:
>     curl -X POST "http://localhost:8000/vehicle/fetch" -H "Content-Type: application/json" -d "{\"company_id\": 1, \"vehicle_id\":\"2\"}"
  
**Resposta**:  
>     200 OK
> 
>     {
>       "detail":{
>         "3":{
>           "company_id":1,
>           "name":"Veículo Teste 2",
>           "license_plate":"23b456d",
>           "brand":"Teste2",
>           "model":"Modelo Teste 2",
>           "year":2026,
>           "notes":null,
>           "last_used":null,
>           "last_user_id":null,
>           "active_vehicle":true
>         }
>       }
>     }

---

[<-](#endpoints-de-veículo)

### /add (POST json)  
Adiciona o registro de um veículo

**Parâmetros**:  
`company_id`: *string*  
`name`: *string*  
`license_plate`: *string*  
`brand`: *string*  
`model`: *string*  
`year`: *integer*  

**Chamada exemplo**:  

HTTP Client:
>     POST http://localhost:8000/vehicle/add
>     Content-Type: application/json
> 
>     {
>       "company_id": "1",
>       "name": "Veículo Teste",
>       "license_plate": "test123",
>       "brand": "Marca Teste",
>       "model": "Modelo Teste",
>       "year": "2025"
>     }

CMD:
>     curl -X POST "http://localhost:8000/vehicle/add" -H "Content-Type: application/json" -d "{\"company_id\":\"1\",\"name\":\"Veículo Teste\",\"license_plate\":\"test123\",\"brand\":\"Marca Teste\",\"model\":\"Modelo Teste\",\"year\":\"2025\"}"

**Resposta**:  
>     {
>       "detail":"Vehicle added successfully"
>     }

---

[<-](#endpoints-de-veículo)

### /edit (POST json)  
Modifica o registro de um veículo dados os campos a serem modificados

**Parâmetros**:  
`vehicle_id`: *integer*  
`company_id`: *integer* (opcional)  
`name`: *string* (opcional)  
`license_plate`: *string* (opcional)  
`brand`: *string* (opcional)  
`model`: *string* (opcional)  
`year`: *integer* (opcional)  
`notes`: *boolean* (opcional)  
`last_used`: *string* (opcional)  
`last_user_id`: *integer* (opcional)
`last_user_id`: *integer* (opcional)
`active_vehicle`: *boolean* (opcional)

**Chamada exemplo**:  

HTTP Client:
>     POST http://localhost:8000/user/edit
>     Content-Type: application/json
> 
>     {
>       "vehicle_id": "4",
>       "name": "teste_edit",
>       "acive_vehicle": false
>     }

CMD:
>     curl -X POST "http://localhost:8000/vehicle/edit" -H "Content-Type: application/json" -d "{\"vehicle_id\":\"4\",\"name\":\"teste_edit\",\"active_vehicle\":false}"

**Resposta**:  
>     {
>       "detail":"Vehicle edited successfully"
>     }

---

[<-](#endpoints-de-veículo)

### /remove (POST json)  
Remove o registro de um veículo
**ATENÇÃO: Remover um registro remove as entries dependentes deste veículo em cascata, como todas as rotas adicionados.**

**Parâmetros**:  
`vehicle_id`: *integer*

**Chamada exemplo**:  

HTTP Client:
>     POST http://localhost:8000/vehicle/remove
>     Content-Type: application/json
> 
>     {
>       "vehicle_id": "4"
>     }

CMD:
>     curl -X POST "http://localhost:8000/vehicle/remove" -H "Content-Type: application/json" -d "{\"vehicle_id\":\"4\"}"

**Resposta**:  
>     {
>       "detail":"Vehicle removed successfully"
>     }
