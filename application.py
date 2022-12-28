'''pip3 install flask'''
from flask import Flask,render_template,request,jsonify, redirect, url_for
import mysql.connector
from flask_awscognito import AWSCognitoAuthentication
application = Flask('__name__')

application.config['AWS_DEFAULT_REGION'] = 'eu-central-1'
application.config['AWS_COGNITO_DOMAIN'] = 'https://clubbee.auth.eu-central-1.amazoncognito.com'
application.config['AWS_COGNITO_USER_POOL_ID'] = 'eu-central-1_SJQdxqfBU'
application.config['AWS_COGNITO_USER_POOL_CLIENT_ID'] = '20cc8at7flbjp8oe3hunkf810b'
application.config['AWS_COGNITO_USER_POOL_CLIENT_SECRET'] = ''
application.config['AWS_COGNITO_REDIRECT_URL'] = 'http://localhost:5000/aws_cognito_redirect'

aws_auth = AWSCognitoAuthentication(application)


@application.route('/')
@aws_auth.authentication_required
def home():
    claims = aws_auth.claims
    return render_template('home.html')

@application.route('/api/register' , methods=['POST'])
def register():
    connection = mysql.connector.connect(
        host = "clubeedatabase.cucgzk7st4ht.eu-central-1.rds.amazonaws.com",
        user = "admin",
        password  = "admin123",
        database = "clubeedb"
    )
    query = f"SELECT * FROM users WHERE studentnumber = {request.json['studentnumber']};"
    cursor = connection.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    if len(result) > 0:
        return jsonify("User already exists")
    content = request.json
    query = f"INSERT INTO users (full_name,email,amazon_id,studentnumber) VALUES ('{content['full_name']}', '{content['email']}','{content['amazon_id']}',{content['studentnumber']} );"
    cursor = connection.cursor()
    cursor.execute(query)
    connection.commit()
    return jsonify("Registered")


@application.route('/api/event/join', methods=['POST'])
def join():
    connection = mysql.connector.connect(
        host = "clubeedatabase.cucgzk7st4ht.eu-central-1.rds.amazonaws.com",
        user = "admin",
        password = "admin123",
        database = "clubeedb"
    )
    content = request.json
    query = f"SELECT id FROM users WHERE studentnumber = {content['studentnumber']};"
    cursor = connection.cursor()
    cursor.execute(query)
    result = cursor.fetchone()
    query = f"INSERT INTO attendance (status,user_id, event_id) VALUES (0,{result[0]}, {content['eventid']});"
    cursor.execute(query)
    connection.commit()
    return "Joined"

@application.route('/api/profile/<int:Number>', methods=['GET'])
def endpoint(Number):
    connection = mysql.connector.connect(
        host = "clubeedatabase.cucgzk7st4ht.eu-central-1.rds.amazonaws.com",
        user = "admin",
        password = "admin123",
        database = "clubeedb"
    )
    query = f"SELECT * FROM users WHERE studentnumber = {Number};"
    cursor = connection.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    return result

@application.route('/api/chapter/<int:Number>', methods=['GET'])
def chapter(Number):
    connection = mysql.connector.connect(
        host = "clubeedatabase.cucgzk7st4ht.eu-central-1.rds.amazonaws.com",
        user = "admin",
        password = "admin123",
        database = "clubeedb"
    )
    query = f"SELECT * FROM chapter WHERE id = {Number};"
    cursor = connection.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    return result

@application.route('/api/events/all', methods=['GET'])
@aws_auth.authentication_required
def events():
    connection = mysql.connector.connect(
        host = "clubeedatabase.cucgzk7st4ht.eu-central-1.rds.amazonaws.com",
        user = "admin",
        password = "admin123",
        database = "clubeedb"
    )
    query = f"SELECT * FROM event;"
    cursor = connection.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    return result

@application.route('/api/events/highlighted'  , methods=['GET'])
def highlighted():
    connection = mysql.connector.connect(
        host = "clubeedatabase.cucgzk7st4ht.eu-central-1.rds.amazonaws.com",
        user = "admin",
        password = "admin123",
        database = "clubeedb"
    )
    query = f"SELECT * FROM event WHERE highlighted = 1;"
    cursor = connection.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    return result

@application.route('/api/event/participated/<int:Number>', methods=['GET'])
def participated(Number):
    connection = mysql.connector.connect(
        host = "clubeedatabase.cucgzk7st4ht.eu-central-1.rds.amazonaws.com",
        user = "admin",
        password = "admin123",
        database = "clubeedb"
    )
    query = f"SELECT id FROM users WHERE studentnumber = {Number};"
    cursor = connection.cursor()
    cursor.execute(query)
    result = cursor.fetchone()
    query = f"SELECT * FROM event WHERE id IN (SELECT event_id FROM attendance WHERE user_id = {result[0]});"
    cursor.execute(query)
    result = cursor.fetchall()
    return result




@application.route('/chapteradmin', methods=['GET'])
def chapteradmin():
    return render_template('chapteradmin.html')

@application.route('/api/createevent', methods=['POST'])
def createevent():
    connection = mysql.connector.connect(
        host = "clubeedatabase.cucgzk7st4ht.eu-central-1.rds.amazonaws.com",
        user = "admin",
        password = "admin123",
        database = "clubeedb"
    )
    content = request.json
    query = f"INSERT INTO event (name,description,event_date,photolink,eventstatus,highlighted,chapter_id) VALUES ('{content['name']}', '{content['description']}','{content['event_date']}','{content['photolink']}',{content['eventstatus']}, {content['highlighted']},{content['chapter_id']});"
    cursor = connection.cursor()
    cursor.execute(query)
    connection.commit()
    return jsonify("Event Created")

@application.route('/api/edit-event-description', methods=['POST'])
def editchapterdescription():
    connection = mysql.connector.connect(
        host = "clubeedatabase.cucgzk7st4ht.eu-central-1.rds.amazonaws.com",
        user = "admin",
        password = "admin123",
        database = "clubeedb"
    )
    content = request.json
    query = f"UPDATE event SET description = '{content['description']}' WHERE id = {content['event_id']};"
    cursor = connection.cursor()
    cursor.execute(query)
    connection.commit()
    return jsonify("Event Description Updated")

@application.route('/api/highlight-event', methods=['POST'])
def highlightevent():
    connection = mysql.connector.connect(
        host = "clubeedatabase.cucgzk7st4ht.eu-central-1.rds.amazonaws.com",
        user = "admin",
        password = "admin123",
        database = "clubeedb"
    )
    content = request.json
    query = f"UPDATE event SET highlighted = 1 WHERE id = {content['event_id']};"
    cursor = connection.cursor()
    cursor.execute(query)
    connection.commit()
    return jsonify("Event Highlighted")


"""@application.route('/api/edit-chapter-description', methods=['POST'])
def editchapterdescription():
    connection = mysql.connector.connect(
        host = "clubeedatabase.cucgzk7st4ht.eu-central-1.rds.amazonaws.com",
        user = "admin",
        password = "admin123",
        database = "clubeedb"
    )
    content = request.json
    query = f"UPDATE chapter SET description = '{content['description']}' WHERE id = {content['chapter_id']};"
    cursor = connection.cursor()
    cursor.execute(query)
    connection.commit()
    return jsonify("Chapter Description Updated")
    #.
"""







if __name__ == "__main__":
    application.run()
    #application.run(debug=True) #can alter host and port number here. Right now the default host is localhost and port is 5000