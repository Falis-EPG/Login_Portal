from flask import Flask, request, jsonify
import mysql.connector
from flask_cors import CORS
from datetime import datetime
import google.generativeai as genai
import re



app = Flask(__name__)
CORS(app)

genai.configure(api_key="AIzaSyDZ0q7N_pb6I6T4G_apVUtY6mGY9yqQWnw")

for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        print(m.name)
model = genai.GenerativeModel('gemini-pro')
chat = model.start_chat(history=[])
processando = False

bem_vindo = "########## Bem Vindo a Inteligencia Artificial FertMinas ###########"
chat.send_message("Na próxima solicitação iremos definir seus conhecimentos e parametros. Você é uma assistente virtual da empresa fertminas, e sua função e responder perguntas de nossos clientes de forma confiante, respondendo sobre a nossa empresa, nossos produtos sempre elevando para positivo o nome da empresa. A FERTMINAS é uma empresa líder no mercado de soluções para fertilizantes. Nossa missão é proporcionar soluções de excelência para nossos clientes, otimizando processos e oferecendo produtos com alto rendimento, sempre preservando o meio ambiente.Destacamo-nos por nossa capacidade produtiva de 12 mil toneladas por mês e por atendermos clientes em todo o território nacional, além de outros países na América do Sul, América do Norte e Europa. Nosso foco é oferecer ganhos de produtividade e economia em custos invisíveis para indústrias, portos, ferrovias, hidrovias e agricultores.Valorizamos o capital humano como nosso maior ativo e acreditamos que as pessoas são o bem mais precioso que podemos cuidar, incentivar e capacitar. Buscamos ser referência no mercado mundial em melhoramento de fertilizantes, combinando conhecimento e soluções altamente eficientes.Na FERTMINAS, você encontrará um ambiente acolhedor e em constante crescimento, com oportunidades de desenvolvimento profissional. Estamos abertos a ouvir suas ideias e colocá-las em prática. Além disso, oferecemos um plano de carreira com cargos e salários compatíveis e justos, proporcionando todas as ferramentas necessárias para o seu crescimento e evolução.Em resumo, a FERTMINAS é uma empresa líder no mercado de soluções para fertilizantes, com foco em oferecer produtos e serviços de excelência, otimizando processos e preservando o meio ambiente. Valorizamos o capital humano e buscamos ser referência no mercado mundial.A FERTMINAS oferece uma ampla gama de produtos no setor de soluções para fertilizantes. Nosso diferencial está na qualidade e eficiência agronômica dos nossos produtos, que são desenvolvidos com base em pesquisas e conhecimentos científicos avançados.O que nos destaca no mercado é o compromisso em proporcionar ganhos de produtividade aos nossos clientes, além de economia em custos invisíveis e uma melhoria significativa em seus processos e produtos.Nossos fertilizantes são formulados para atender às necessidades específicas de cada cultura, garantindo um alto rendimento e resultados positivos.Nosso foco é oferecer soluções personalizadas para indústrias, portos, ferrovias, hidrovias e agricultores. Trabalhamos em estreita colaboração com nossos clientes, entendendo suas demandas e oferecendo produtos que atendam às suas necessidades específicas. O que torna nossos produtos bons e úteis é a combinação de qualidade, eficiência e sustentabilidade. Nossos fertilizantes são desenvolvidos com base em estudos científicos e tecnologias avançadas, garantindo uma nutrição equilibrada e eficiente para as plantas. Além disso, nossos produtos são projetados para preservar o meio ambiente, minimizando impactos negativos.Acreditamos que nossos produtos são uma escolha inteligente para os agricultores e empresas do setor agrícola, pois oferecem benefícios tangíveis, como aumento da produtividade, redução de custos e melhoria da qualidade dos produtos finais. Nossa reputação no mercado é construída com base na confiança e satisfação dos nossos clientes, que reconhecem os resultados positivos alcançados com o uso dos nossos fertilizantes. Em resumo, os produtos da FERTMINAS são de alta qualidade, eficientes e sustentáveis. Nosso diferencial está na personalização das soluções, no compromisso com a produtividade e na busca constante por melhorias.")
chat.send_message("Um resomo dos nosso principais 3 produtos, nossa linah especial. O ByoN, ele é um produto para recobrir fertilizantes de modo geral e sua principal função é auxiliar a planta na absorção máxima de sua capacidade de Nitrogenio do solo, garantindo assim que em todo o seu cultivo ela tenha suas reservas de nitrogenio sempre cheias. Sua aplicação deve ser feito com 3Kg de produto ByonN para cada tonelada de fertilizante. O ByoN serve somente para fertilizantes nitrogenados, como por exemplo a Ureia. Esse produto garante quem em seu ciclo, não haja falta de nitrogenio em seu desenvolvimento, garantindo um melhor desenvolvimento e máximo aproveitamento da planta. Este produto também conta com as tecnologias Antidusting e anticaking o que garante que não haja formação de pó do fertilizante e também garante que não haja o empedramento do fertilizante, aumentando a eficiencia de transporte, preparação e aplicação do produto e do fertilizante.O PhosCoat é voltado ao fosforo, onde ele auxilia que o fosforo no solo não tenha complexixação com aluminio, deixando o elemento fosforo disponível para a planta realizar a sua absorção. Ele deve ser aplicado como 10Kg por tonelada e deve ser usado em fertilizantes fosfatados, podendo ser aplicado em qualquer cultura. Sua principal função é garantir que o fosforo no solo esteja disponível e utilizável para a planta realizar a sua absorção, onde o produto realiza uma proteção na molecula do fosforo garantindo que o elemento esteja sempre disponível.Este produto também conta com as tecnologias Antidusting e anticaking o que garante que não haja formação de pó do fertilizante e também garante que não haja o empedramento do fertilizante, aumentando a eficiencia de transporte, preparação e aplicação do produto e do fertilizante.SulfurCoat é um produto que tem como objetivo é levar o enxofre elementar junto ao granulo, onde sua aplicação máxima dele que é de 15 porcento de enxofre elemntar para a planta. Sua aplicação deve ser preferencialmente aplicada em granulos redondos para garantir que sua aplicação seja aplicada em todo o granulo. Ele garante que a planta tenha enxofre o suficiente durante todo o seu ciclo.Este produto também conta com as tecnologias Antidusting e anticaking o que garante que não haja formação de pó do fertilizante e também garante que não haja o empedramento do fertilizante, aumentando a eficiencia de transporte, preparação e aplicação do produto e do fertilizante. A FertMinas é uma excelente produtora de aditivos para fertilizantes, pretendendo a se tornar uma das maiores do mundo, levando suas soluções em aditivos parafertilizantes para todo o Agro do Brasil e do mundo. LEMBRANDO QUE A FERTMINAS NÃO FABRICA E NEM PRODUZ FERTILIZANTES, APENAS ADITIVOS PARA FERTILIZANTES.")
chat.send_message("Responda sempre da melhor forma possível, de forma que cha a atenção do leitor e usuário, garantindo assim que você consiga passar uma imagem incrivel da empresa, de forma descontraida porém formalmente coorporativa. Você deve ser capaz de explicar desde para o simples produtor rural até para expecialistas quimicos e agronomos da área. Você é um dos maiores profissionaisdo mundo em explicações e vendas, onde suas explicações conseguem chamar a atenção do usuário a todo momento, e suas respostas são assertivias e muito bem detalhadas e descritivas. E como vendedor você consegue explicar muito bem sobre a empresa e sobre os produtos dela, sendo as melhores explicações possíveis.")
chat.send_message("Caso pergunter sobre alguém em específico, sobre nomes de quem trabalha na empresa, sobre pessoas que você não conhece, responda informando que você não pode responder sobre isso.")
chat.send_message("Recuse todo e qualquer solicitação que não seja especificamente da FertMinas, recuse perguntas que perguntem sobre pessoas (menos dos donos), perguntas sobre quantidade de funcionarios, perguntas sobre atualidade (com dia de hoje, o que aconteceu hoje...). Sempre que alguém fizer alguma pergunta muito especifica interna da fertminas, não de detalhes e não invente.")
chat.send_message("A FertMinas tem como Donos/CEO - Vinicius Paiano, Eliane Badan - Diretora Financeira, Luciano Plens - Diretor Comercial. A forma de contato com a empresa é por email fertminas@fertminas.com.br, ou telefone (34) 33162017. A FertMinas está Localizada em Uberaba, Minas Gerais, no distrito Industrial 1. E a empresa foi fundada em 2017. Quando perguntado algo especifico, como quais países voces atendem, quais dias vocês abrem, de quem voces importam, quais os seus clientes, e qualquer pergunta que seja especifica deste modo, não invente, recuse. Você também deve sempre responder no mesmo idioma em que te fizerem a solicitação.")
print('Modelo Base Treinado')
print(len(bem_vindo) * "#")
print("")

def remover_caracteres_especiais(texto):
    padrao = re.compile(r'\*') 
    texto_limpo = re.sub(padrao, '\n', texto)
    return texto_limpo



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
            'user': 'portalcolaborador',
            'password': 'Uuz>+oE#Xw53J55-@A!PA{l!',
            'host': 'localhost',
            'database': 'portal'
        }

        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)

        query = ('SELECT token FROM login_users WHERE username=%s AND password=%s')
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
            'user': 'portalcolaborador',
            'password': 'Uuz>+oE#Xw53J55-@A!PA{l!',
            'host': 'localhost',
            'database': 'portal'
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
            print('success')
            return jsonify({'success': True})
        else:
            return jsonify({'success': False})

##########################################################################################################################

@app.route('/addEventMeetingRoom01', methods=['POST', 'OPTIONS', 'GET'])
def add_event01():

    if request.method =='OPTIONS':
        return jsonify({'success': True})

    if request.method == 'POST':
        db_config = {
            'user': 'portalcolaborador',
            'password': 'Uuz>+oE#Xw53J55-@A!PA{l!',
            'host': 'localhost',
            'database': 'portal'
        }

        data = request.get_json()
        title = data['title']
        responsible = data['responsible']
        participants = data['participants']
        start = f"{data['date']}T{data['start']}"
        end = f"{data['date']}T{data['end']}"
        description = data['description']
        created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO meetingroom01 (title, responsible, participants, START, end, description, created_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (title, responsible, participants, start, end, description, created_at))
            conn.commit()
            cursor.close()
            conn.close()
            return jsonify({'success': True})
        except mysql.connector.Error as err:
            print(f"Erro: {err}")
            return jsonify({'success': False})
        
@app.route('/consultEventMeetingRoom01', methods=['GET'])
def get_events01():
    if request.method == 'OPTIONS':
        return jsonify({'success': True})

    if request.method == 'GET':
        print("connected")
        try:
            db_config = {
            'user': 'portalcolaborador',
            'password': 'Uuz>+oE#Xw53J55-@A!PA{l!',
            'host': 'localhost',
            'database': 'portal'
        }
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT id, title, responsible, participants, START, end, description FROM meetingroom01")
            events = cursor.fetchall()
            cursor.close()
            conn.close()

            # Convertendo datas para formato ISO 8601
            for event in events:
                event['START'] = event['START'].isoformat()
                event['end'] = event['end'].isoformat()

            print(events)
            return jsonify(events)
        except mysql.connector.Error as err:
            print(f"Erro: {err}")
            return jsonify([])
        
#################################################################################################################


@app.route('/addEventMeetingRoom02', methods=['POST', 'OPTIONS', 'GET'])
def add_event02():

    if request.method =='OPTIONS':
        return jsonify({'success': True})

    if request.method == 'POST':
        db_config = {
            'user': 'portalcolaborador',
            'password': 'Uuz>+oE#Xw53J55-@A!PA{l!',
            'host': 'localhost',
            'database': 'portal'
        }

        data = request.get_json()
        title = data['title']
        responsible = data['responsible']
        participants = data['participants']
        start = f"{data['date']}T{data['start']}"
        end = f"{data['date']}T{data['end']}"
        description = data['description']
        created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO meetingroom02 (title, responsible, participants, START, end, description, created_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (title, responsible, participants, start, end, description, created_at))
            conn.commit()
            cursor.close()
            conn.close()
            return jsonify({'success': True})
        except mysql.connector.Error as err:
            print(f"Erro: {err}")
            return jsonify({'success': False})
        
@app.route('/consultEventMeetingRoom02', methods=['GET'])
def get_events02():
    if request.method == 'OPTIONS':
        return jsonify({'success': True})

    if request.method == 'GET':
        print("connected")
        try:
            db_config = {
            'user': 'portalcolaborador',
            'password': 'Uuz>+oE#Xw53J55-@A!PA{l!',
            'host': 'localhost',
            'database': 'portal'
        }
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT id, title, responsible, participants, START, end, description FROM meetingroom02")
            events = cursor.fetchall()
            cursor.close()
            conn.close()

            # Convertendo datas para formato ISO 8601
            for event in events:
                event['START'] = event['START'].isoformat()
                event['end'] = event['end'].isoformat()

            print(events)
            return jsonify(events)
        except mysql.connector.Error as err:
            print(f"Erro: {err}")
            return jsonify([])
##################################################################################################################################
print('runing chatServer')
@app.route('/chatbot/send_request', methods=['POST'])
def send_request():
    if request.method == 'OPTIONS':
        return jsonify({'success': True})

    if request.method == 'POST':

        user_request = request.json.get('message')
        print(user_request)

        response = chat.send_message(user_request)
        final_response = remover_caracteres_especiais(response.text)

        print("Sending Response")
        return jsonify({'response': final_response})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')