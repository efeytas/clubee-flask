'''pip3 install flask'''
from flask import Flask,render_template,request,jsonify
import mysql.connector

app = Flask('__name__')


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/api/register' , methods=['POST'])
def register():
    connection = mysql.connector.connect(
        host = "clubeedatabase.cucgzk7st4ht.eu-central-1.rds.amazonaws.com",
        user = "admin",
        password  = "admin123",
        database = "clubeedb"
    )
    content = request.json
    query = f"INSERT INTO users (full_name,email,amazon_id,studentnumber) VALUES ('{content['full_name']}', '{content['email']}','{content['amazon_id']}',{content['studentnumber']} );"
    cursor = connection.cursor()
    cursor.execute(query)
    connection.commit()
    return jsonify("Registered")


@app.route('/api/event/join', methods=['POST'])
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

@app.route('/api/profile/<int:Number>', methods=['GET'])
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

@app.route('/api/chapter/<int:Number>', methods=['GET'])
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

@app.route('/api/events/all', methods=['GET'])
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

@app.route('/api/events/highlighted'  , methods=['GET'])
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

@app.route('/api/event/participated/<int:Number>', methods=['GET'])
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




@app.route('/chapteradmin', methods=['GET'])
def chapteradmin():
    return render_template('chapteradmin.html')

@app.route('/api/createevent', methods=['POST'])
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
    



if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000)
    #app.run(debug=True) #can alter host and port number here. Right now the default host is localhost and port is 5000