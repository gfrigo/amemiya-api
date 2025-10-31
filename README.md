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

# Referência da API

Os endpoints funcionam com quatro métodos HTTP:

- **GET** para métodos de Busca / Consulta, como *query* de dados de um usuário;
- **POST** para métodos de Inserção / Criação, como criação de veículos ou *upload* de uma nota;
- **PUT** para métodos de Atualização / Alteração, como troca de foto de perfil ou alteração de dados de um usuário;
- **DELETE** para métodos de Remoção de um registro, como deleção de um anexo.

## Descrição de *endpoints*



### /user

**A ser retrabalhado**  
*Endpoints* de usuário

#### /fetch (POST json)  
Consulta de dados de um usuário

**Parâmetros**:  
`user_id`: integer

**Chamada exemplo**:  

HTTP Client:
>     POST http://localhost:8000/user/fetch
>     Content-Type: application/json
> 
>     {
>       "user_id": 30
>     }

CMD:
>     curl -X POST "http://localhost:8000/user/fetch" -H "Content-Type: application/json" -d "{\"user_id\": 30}"
  
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

#### /add (POST json)  
Adiciona registro de um usuário

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

#### /edit (POST json)  
Modifica o registro de um usuário

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

#### /profile_picture/{user_id} (PUT form-data)  
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
 
#### /remove (POST json)  
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
