'''pip3 install flask'''
from flask import Flask,render_template,request,jsonify, redirect, url_for,session
import mysql.connector
import json
import functools
with open('config.json') as config_file:
    data = json.load(config_file)
    api_key = data['api_key']

is_logged = False
"""from flask_cognito_auth import CognitoAuthManager
from flask_cognito_auth import login_handler
from flask_cognito_auth import logout_handler
from flask_cognito_auth import callback_handler



application.config['AWS_DEFAULT_REGION'] = 'eu-central-1'
application.config['AWS_COGNITO_DOMAIN'] = 'https://clubbee.auth.eu-central-1.amazoncognito.com'
application.config['AWS_COGNITO_USER_POOL_ID'] = 'eu-central-1_SJQdxqfBU'
application.config['AWS_COGNITO_USER_POOL_CLIENT_ID'] = '5764t5luntj97cns1pl0qj445l'
application.config['AWS_COGNITO_USER_POOL_CLIENT_SECRET'] = 'ue1dun0v1bdohvuhr22i4foqsit2j0hl0sooilolennlldeh4h5'

cognito = CognitoAuthManager(application)
"""



application = Flask('__name__')

def api_auth(func):
    def decorator(func):   
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if request.headers.get('auth-key') == api_key:
                return func(*args, **kwargs)
            else:
                return jsonify("Unauthorized")
        return wrapper
    return decorator(func)

@application.route('/', methods=['POST','GET'])
def home():  
    global is_logged
    if request.method == 'POST': 
    
        connection = mysql.connector.connect(
                host = "clubeedatabase.cucgzk7st4ht.eu-central-1.rds.amazonaws.com",
                user = "admin",
                password  = "admin123",
                database = "clubeedb"
            )
        content = request.json
        query = f"SELECT * FROM users WHERE email ='{content['email']}' AND admin_password={content['admin_password']};"
        cursor = connection.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        print(result)
        if len(result) > 0:
            is_logged = True
            return jsonify({"email" : result[0][2]},
                           {"studentnumber" : result[0][4]},
                           {"full_name" : result[0][1]},
                           {"id" : result[0][0]})
        else:
            return jsonify("Wrong email or password")
    elif request.method=="GET":
        if is_logged:
            return render_template("home.html")  
        else:
            return render_template("login.html")
    

    
#registration
@application.route('/api/register' , methods=['POST']) # full-name, email, amazon-id(NULL), studentnumber vermen gerekiyor üye oluyor
@api_auth
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
    query = f"INSERT INTO users (full_name,email,admin_password,studentnumber) VALUES ('{content['full_name']}', '{content['email']}','{content['admin_password']}',{content['studentnumber']} );"
    cursor = connection.cursor()
    cursor.execute(query)
    connection.commit()
    return jsonify("Registered")

#join to event
@application.route('/api/event/join', methods=['POST']) # eventid, studentnumber vermen gerekiyor join
@api_auth
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
    resultid = cursor.fetchone()

    query = f"SELECT * FROM attendance WHERE user_id = {resultid[0]} AND event_id = {content['eventid']};"
    cursor = connection.cursor()
    cursor.execute(query)
    result = cursor.fetchall()

    if len(result) > 0:
        return "Already joined"
    else:
        query = f"INSERT INTO attendance (status,user_id, event_id) VALUES (0,{resultid[0]}, {content['eventid']});"
        cursor.execute(query)
        connection.commit()
        return "Joined"
    
#view profile of student
@application.route('/api/profile/<int:Number>', methods=['GET']) # /api/profile/150180086 GET attığın zaman sana userın bilgilerini döndürür [[6,"Efe Yigit Tas","tase18@itu.edu.tr",null,"150180086"]]
@api_auth
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

#view profile of chapter
@application.route('/api/chapter/<int:Number>', methods=['GET']) # /api/chapter/1 GET attığın zaman sana chapterın bilgilerini döndürür [[2,"DSC ITU is a non-profit developer group to learn, share, connect and delevop tech skills. Join us!","ITU DSC ",1,7]]
@api_auth
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

#view all events (?)
@application.route('/api/events/all', methods=['GET'])
@api_auth
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

#view events of specific club
@application.route('/api/events/<int:Number>', methods=['GET']) # /api/events/1 GET attığın zaman sana eventın bilgilerini döndürür [[1,"DSC ITU is a non-profit developer group to learn, share, connect and delevop tech skills. Join us!","ITU DSC ",1,7]]
@api_auth
def event(Number):
    connection = mysql.connector.connect(
        host = "clubeedatabase.cucgzk7st4ht.eu-central-1.rds.amazonaws.com",
        user = "admin",
        password = "admin123",
        database = "clubeedb"
    )
    query = f"SELECT * FROM event WHERE id = {Number};"
    cursor = connection.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    return result

#view events highlighted
@application.route('/api/events/highlighted'  , methods=['GET'])
@api_auth
def highlighted():
    connection = mysql.connector.connect(
        host = "clubeedatabase.cucgzk7st4ht.eu-central-1.rds.amazonaws.com",
        user = "admin",
        password = "admin123",
        database = "clubeedb"
    )
    query = f"SELECT * FROM event WHERE highlighted = 1 AND eventstatus = 1;"
    cursor = connection.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    return result

#view active members of specific chapter
@application.route('/api/activechapters/<int:Number>', methods=['GET'])  # number = studentnumber
@api_auth
def activemembers(Number):
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
    query = f"SELECT * FROM active WHERE user_id = {result[0]} and status = 1;"
    cursor.execute(query)
    result = cursor.fetchall()
    for i in range(len(result)):
        query = f"SELECT name FROM chapter WHERE id = {result[i][1]};"
        cursor.execute(query)
        result[i] = cursor.fetchone()
    return result

#view events partcicipated of specific user
@application.route('/api/event/participated/<int:Number>', methods=['GET']) # number = studentnumber
@api_auth
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
    query = f"SELECT * FROM event WHERE id IN (SELECT event_id FROM attendance WHERE user_id = {result[0]} AND status = 1);"
    cursor.execute(query)
    result = cursor.fetchall()
    return result

#view events applied of specific user
@application.route('/api/event/applied/<int:Number>', methods=['GET']) # number = studentnumber
@api_auth
def applied(Number):
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


#HTML render for chapter admin 
@application.route('/chapteradmin', methods=['GET'])
@api_auth
def chapteradmin():
    return render_template('chapteradmin.html')

#create event
@application.route('/api/createevent', methods=['POST']) 
@api_auth
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

#edit event description
@application.route('/api/edit-event-description', methods=['POST'])
@api_auth
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


#edit highlight event
@application.route('/api/highlight-event', methods=['POST'])
@api_auth
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
    print("Sucessfully highlighted")
    return jsonify("Event Highlighted")

#edit status of event
@application.route('/api/edit-event-status', methods=['POST'])
@api_auth
def editeventstatus():
    connection = mysql.connector.connect(
        host = "clubeedatabase.cucgzk7st4ht.eu-central-1.rds.amazonaws.com",
        user = "admin",
        password = "admin123",
        database = "clubeedb"
    )
    content = request.json
    query = f"UPDATE event SET eventstatus = {content['eventstatus']} WHERE id = {content['event_id']};"
    cursor = connection.cursor()
    cursor.execute(query)
    connection.commit()
    return jsonify("Event Status Updated")

#update attendance of user in chapter
@application.route('/api/update-attendance/<int:Number>', methods=['POST'])
@api_auth
def updateattendancestatus(Number):
    connection = mysql.connector.connect(
        host = "clubeedatabase.cucgzk7st4ht.eu-central-1.rds.amazonaws.com",
        user = "admin",
        password = "admin123",
        database = "clubeedb"
    )
    content = request.json
    query = f"SELECT id FROM users WHERE studentnumber = {Number};"
    cursor = connection.cursor()
    cursor.execute(query)
    result = cursor.fetchone()
    query = f"UPDATE attendance SET status = {content['status']} WHERE event_id = {content['event_id']} AND user_id = {result[0]};"
    cursor.execute(query)
    connection.commit()
    return jsonify("Attendance Status Updated")

#edit chapter description
#editted
@application.route('/api/update-chapter-description', methods=['POST'])
@api_auth
def updatechapterdescription():
    connection = mysql.connector.connect(
        host = "clubeedatabase.cucgzk7st4ht.eu-central-1.rds.amazonaws.com",
        user = "admin",
        password = "admin123",
        database = "clubeedb"
    )
    content = request.json
    print(content)
    query = f"UPDATE chapter SET description = '{content['description']}' WHERE id = {content['chapter_id']};"
    cursor = connection.cursor()
    cursor.execute(query)
    connection.commit()
    return jsonify("Chapter Description Updated")

#admin page icin sayfa 

@application.route('/admin/events' , methods=['GET','POST'])
def admin_events():
    if is_logged == False:
        return redirect('/')
    return render_template('events.html')

@application.route('/admin/chapterprofile',methods=['POST', 'GET'])
def admin_chapter_profile():
    if is_logged == False:
        return redirect('/')
    return render_template('chapterprofile.html')

@application.route('/admin/activemembers')
def admin_active_members():
    if is_logged == False:
        return redirect('/')
    return render_template('active_members.html')

@application.route('/admin/adminprofile')
def admin_admin_profile():
    if is_logged == False:
        return redirect('/')
    return render_template('chapteradmin.html')

@application.route('/admin/events/addevents',methods=['POST', 'GET'])
def admin_add_events():
    if is_logged == False:
        return redirect('/')
    return render_template('add_event.html')

#new

@application.route('/admin/chapter/addactivemember',methods=['POST', 'GET'])
def admin_add_active_member():
    if is_logged == False:
        return redirect('/')
    return render_template('add_activemember.html')

@application.route('/admin/chapter/editevent/',methods=['POST', 'GET'])
def admin_edit_event():
    if is_logged == False:
        return redirect('/')
    return render_template('edit_event.html')

#yeni fonksiyonlar

@application.route('/admin/activemembersinchapter/<int:Number>', methods=['GET'])  # number = studentnumber
@api_auth
def activemembersinchapter(Number):
    connection = mysql.connector.connect(
        host = "clubeedatabase.cucgzk7st4ht.eu-central-1.rds.amazonaws.com",
        user = "admin",
        password = "admin123",
        database = "clubeedb"
    )

    cursor = connection.cursor()
    query = f"SELECT * FROM active WHERE chapter_id = {Number} and status = 1;"
    cursor.execute(query)
    result = cursor.fetchall()
    for i in range(len(result)):
        query = f"SELECT * FROM users WHERE id = {result[i][2]};"
        cursor.execute(query)
        result[i] = cursor.fetchone()
    return result


@application.route('/admin/adminofchapter/<int:Number>', methods=['GET'])  # number = studentnumber
@api_auth
def adminofchapter(Number):
    connection = mysql.connector.connect(
        host = "clubeedatabase.cucgzk7st4ht.eu-central-1.rds.amazonaws.com",
        user = "admin",
        password = "admin123",
        database = "clubeedb"
    )
    cursor = connection.cursor()
    query = f"SELECT * FROM chapter WHERE id = {Number};"
    cursor.execute(query)
    result = cursor.fetchall()
    query = f"SELECT * FROM users WHERE id = {result[0][4]};"
    cursor.execute(query)
    result = cursor.fetchall()
    return result


@application.route('/admin/addactivemember/<int:Number>', methods=['POST']) 
@api_auth
def addactivemember(Number):
    connection = mysql.connector.connect(
        host = "clubeedatabase.cucgzk7st4ht.eu-central-1.rds.amazonaws.com",
        user = "admin",
        password = "admin123",
        database = "clubeedb"
    )
    content = request.json
    query=f"SELECT id FROM users WHERE studentnumber = {content['studentnumber']};"
    cursor = connection.cursor()
    cursor.execute(query)
    result = cursor.fetchone()
    if len(result)==0:
        return jsonify("Such student doesn't exist")
    else:
        query=f"SELECT chapter_id FROM active WHERE user_id = {result[0]};"
        cursor.execute(query)
        result1 = cursor.fetchone()
        print("The result")
        print(result1[0])
        print(" ")
        print(Number)
        if result1[0]==Number:
            return jsonify("Student already active member")
        else:
            query = f"INSERT INTO active (status,chapter_id ,user_id) VALUES (1,{Number}, {result[0]});"
            cursor.execute(query)
            connection.commit()
            return jsonify("Student added")


@application.route('/admin/events/<int:Number>', methods=['GET']) # /api/events/1 GET attığın zaman sana eventın bilgilerini döndürür [[1,"DSC ITU is a non-profit developer group to learn, share, connect and delevop tech skills. Join us!","ITU DSC ",1,7]]
@api_auth
def view_events_chapter(Number):
    connection = mysql.connector.connect(
        host = "clubeedatabase.cucgzk7st4ht.eu-central-1.rds.amazonaws.com",
        user = "admin",
        password = "admin123",
        database = "clubeedb"
    )
    query = f"SELECT * FROM event WHERE chapter_id = {Number};"
    cursor = connection.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    return result

#edit unhighlight event
@application.route('/api/unhighlight-event', methods=['POST'])
def unhighlightevent():
    connection = mysql.connector.connect(
        host = "clubeedatabase.cucgzk7st4ht.eu-central-1.rds.amazonaws.com",
        user = "admin",
        password = "admin123",
        database = "clubeedb"
    )
    content = request.json
    query = f"UPDATE event SET highlighted = 0 WHERE id = {content['event_id']};"
    cursor = connection.cursor()
    cursor.execute(query)
    connection.commit()
    return jsonify("Event Unhighlighted")

@application.route('/getstudent/<int:Number>', methods=['GET']) 
@api_auth
def getstudent(Number):
    connection = mysql.connector.connect(
        host = "clubeedatabase.cucgzk7st4ht.eu-central-1.rds.amazonaws.com",
        user = "admin",
        password = "admin123",
        database = "clubeedb"
    )
    query = f"SELECT * FROM users WHERE email = {Number};"
    cursor = connection.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    print(result+"Here is result amk")
    return result

@application.route('/getchapterid/<int:Number>', methods=['GET']) 
@api_auth
def getchapterid(Number):
    connection = mysql.connector.connect(
        host = "clubeedatabase.cucgzk7st4ht.eu-central-1.rds.amazonaws.com",
        user = "admin",
        password = "admin123",
        database = "clubeedb"
    )
    query = f"SELECT id FROM chapter WHERE admin_id = {Number};"
    cursor = connection.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    return result

@application.route('/logout')
def logout():
    global is_logged
    is_logged = False
    return redirect('/')

if __name__ == "__main__":
    application.run()
    #application.run(debug=True) #can alter host and port number here. Right now the default host is localhost and port is 5000