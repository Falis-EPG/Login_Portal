from flask import Flask, request, jsonify
import mysql.connector
from flask_cors import CORS
import re



app = Flask(__name__)
CORS(app)


app = Flask(__name__)
CORS(app)

print('Server Login - Started ######...######...######...')
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

        query = ('SELECT token FROM user_table WHERE username=%s AND password=%s')
        cursor.execute(query, (username, password))
        token = cursor.fetchone()

        print(username, password, token)

        print("Data Consulted SUCCESSFULY: 200")

        cursor.close()
        connection.close()

        print("Connection Closed: 200")


        if token:
            return jsonify({'success': True, 'token': token})
        else:
            return jsonify({'success': False, 'message': 'Invalid Username or password'})

 
 
@app.route('/verify_token', methods=['POST', 'OPTIONS'])
def verify_token():
    print('Connect Success: 200')

    if request.method =='OPTIONS':
        return jsonify({'success': True})

    if request.method == 'POST':
        data = request.json
        token = data.get('token')

        print('Token Colected...!...')

        db_config = {
            'user': 'user',
            'password': 'password',
            'host': 'host',
            'database': '__db__'
            }

        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)

        query = 'SELECT * FROM user_table WHERE token=%s'
        cursor.execute(query, (token,))
        result = cursor.fetchone()
        print(result)

        cursor.close()
        connection.close()

        print("Verification Success: 200, Connection with database closed...!...")

        if result:
            print('success')
            return jsonify({'success': True})
        else:
            return jsonify({'success': False})

##########################################################################################################################


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
