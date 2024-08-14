
#### 1. Introdução

Este documento detalha a implementação técnica da tela de login do Portal do Colaborador. A tela é responsável por gerenciar a autenticação dos usuários, armazenar tokens de sessão, e validar acessos subsequentes às diferentes páginas do portal. O código foi desenvolvido utilizando HTML, JavaScript, e Python, com integração ao banco de dados MySQL para verificação das credenciais.

#### 2. Estrutura da Tela de Login

A tela de login é composta por dois campos de entrada para o usuário: **Username** e **Password**, além de um botão de login. A estrutura em HTML é a seguinte:

```html
<input type="text" id="username" name="username" required>
<input type="password" id="password" name="password" required>
<button type="submit" class="button">Login</button>
```
![fdfddf](https://github.com/user-attachments/assets/0c04c8d5-90e0-4f29-ad0a-f52850f12966)


#### 3. Limpeza do Session Storage

Para garantir a segurança e evitar conflitos de autenticação entre diferentes sessões de usuários, o **Session Storage** é automaticamente limpo ao acessar a tela de login:

```javascript
<script>
    sessionStorage.removeItem('userToken');
</script>
```

#### 4. Interação com o Backend

Ao submeter o formulário de login, o evento é interceptado pelo JavaScript, que envia as credenciais do usuário para o servidor backend através de um `POST` na rota `/login_portal`.

##### 4.1 Código de Frontend (main.js)

```javascript
document.getElementById("loginForm").addEventListener("submit", function(event) {
    event.preventDefault();

    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    fetch('http://portal_ip/login_portal', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, password }),
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        if (data.success) {
            sessionStorage.setItem('userToken', data.token.token);
            window.location.href = '../pages/General/general.html'; // Redireciona para outra página
        } else {
            document.getElementById("responseMessage").textContent = data.message;
        }
    })
    .catch((error) => {
        console.error('Error:', error);
    });
});
```

##### 4.2 Código de Backend (Python - Flask)

O servidor Flask processa as credenciais e as valida contra o banco de dados MySQL. Se as credenciais estiverem corretas, um token de autenticação é retornado ao frontend.

```python
@app.route('/login_portal', methods=['POST', 'OPTIONS'])
def login():
    print('Connect Success: 200')

    if request.method =='OPTIONS':
        return jsonify({'success': True})

    if request.method == 'POST':

        data = request.json
        username = data.get('username')
        password = data.get('password')

        db_config = {
            'user': 'user',
            'password': 'password',
            'host': 'host',
            'database': '__db__'
        }

        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)

        query = ('SELECT token FROM login_users WHERE username=%s AND password=%s')
        cursor.execute(query, (username, password))
        token = cursor.fetchone()

        print(username, password, token)

        print("Data Consulted SUCCESSFULLY: 200")

        cursor.close()
        connection.close()

        print("Connection Closed: 200")

        if token:
            return jsonify({'success': True, 'token': token})
        else:
            return jsonify({'success': False, 'message': 'Invalid Username or Password'})
```

##### 4.3 Armazenamento do Token

Uma vez autenticado, o token retornado pelo backend é armazenado no **Session Storage** para validação em acessos futuros:

```javascript
sessionStorage.setItem('userToken', data.token.token);
```

#### 5. Validação de Sessão em Páginas Subsequentes

Toda vez que o usuário acessar uma página dentro do portal, o token armazenado no **Session Storage** é verificado para garantir que a sessão seja válida.

##### 5.1 Código de Validação de Sessão (JavaScript)

```javascript
document.addEventListener("DOMContentLoaded", function() {
    const token = sessionStorage.getItem('userToken');
    if (token) {
        fetch('http://portal_IP/verify_token', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ token }),
        })
        .then(response => response.json())
        .then(data => {
            if (!data.success) {
                window.location.href = '../../index.html'; // Redireciona para a tela de login se o token não for válido
                alert('Token de acesso inválido');
            }
        })
        .catch((error) => {
            console.error('Error:', error);
            alert(error);
            window.location.href = '../../index.html'; // Redireciona para a tela de login em caso de erro
        });
    } else {
        window.location.href = '../../index.html'; // Redireciona para a tela de login se não houver token
    }
});
```

##### 5.2 Verificação do Token no Backend (Python - Flask)

O backend verifica a validade do token ao recebê-lo na rota `/verify_token`. Se o token for válido, o usuário permanece na página, caso contrário, é redirecionado para a tela de login.

```python
@app.route('/verify_token', methods=['POST', 'OPTIONS'])
def verify_token():
    print('Connect Success: 200')

    if request.method =='OPTIONS':
        return jsonify({'success': True})

    if request.method == 'POST':
        data = request.json
        token = data.get('token')

        print('Token Collected...!...')

        db_config = {
            'user': 'user',
            'password': 'password',
            'host': 'host',
            'database': '__db__'
        }

        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)

        query = 'SELECT * FROM login_users WHERE token=%s'
        cursor.execute(query, (token,))
        result = cursor.fetchone()
        print(result)

        cursor.close()
        connection.close()

        print("Verification Success: 200, Connection with database closed...!...")

        if result:
            return jsonify({'success': True})
        else:
            return jsonify({'success': False})
```

#### 6. Considerações Finais

Este processo de autenticação e verificação de sessão garante a segurança e a integridade do acesso ao Portal do Colaborador, protegendo os dados do usuário e mantendo uma sessão segura e válida durante o uso do sistema.

Essa documentação visa proporcionar uma visão clara e detalhada do fluxo de autenticação, desde a coleta das credenciais do usuário até a verificação contínua de acesso, assegurando que as melhores práticas de segurança e desenvolvimento estejam sendo seguidas no projeto.
