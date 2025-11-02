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

| Endpoint                                                                 | Tipo | Formato             | Descrição                                    |
|--------------------------------------------------------------------------|------|---------------------|----------------------------------------------|
| [/user/fetch](#fetch-post-json)                                          | POST | application/json    | Consulta de dados de um ou múltiplos usuário |
| [/user/add](#add-post-json)                                              | POST | application/json    | Adiciona o registro de um usuário            | 
| [/user/edit](#edit-post-json)                                            | POST | application/json    | Modifica o registro de um usuário            | 
| [/user/profile_picture/{user_id}](#profile_pictureuser_id-put-form-data) | PUT  | multipart/form-data | Modifica a foto de perfil de um usuário      |
| [/user/remove](#edit-post-json)                                          | POST | application/json    | Remove o registro de um usuário              |

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
>       "company_id": 1
>       "user_id": 30
>     }

CMD:
>     curl -X POST "http://localhost:8000/user/fetch" -H "Content-Type: application/json" -d "{\"company_id\": 1, \"user_id\": 30}"
  
**Resposta**:  
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

[<-](#user)

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

***

---

## *Endpoints* de anexo

| Endpoint                                                | Tipo   | Formato             | Descrição                                |
|---------------------------------------------------------|--------|---------------------|------------------------------------------|
| [/attachment/{company_id}](#company_id-get)             | GET    |                     | Consulta de dados um ou múltiplos anexos |
| [/attachment/](#-post-multipartform-data)               | POST   | multipart/form-data | Adiciona registro de um anexo            | 
| [/attachment/{attachment_id} ](#attachment_id-put-json) | POST   | application/json    | Modifica o registro de um usuário        | 
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