import json
import mysql.connector
from flask import Flask, request, jsonify, render_template
# import uuid
# import jwt
# from werkzeug.security import generate_password_hash, check_password_hash
# import datetime

app = Flask(__name__)

# this is the secret token
#app.config['SECRET_KEY'] = 'myS3cr3tK3y'


# this is to connect to the database on pythonanywhere
def db_connect():
    try:
        db_connection = mysql.connector.connect(host="NickEspitalier.mysql.pythonanywhere-services.com",
                                                user="NickEspitalier", password="CloudyJJ12",
                                                database="NickEspitalier$finalprojectiot")
        # If connection is not successful
    except:
        print("Can't connect to database")
        return 0
    # If Connection Is Successful
    print("Connected")

    # Making Cursor Object For Query Execution
    return db_connection


# this is where the data from the raspberry pi is posted in the service
@app.route('/post/report', methods=['POST'])
def insert_report():
    temp = request.json["temp_result"]
    hum = request.json["hum_result"]

    insertTemperatureAndHumidity(temp, hum)
    return app.response_class(response="Success", status=201)


# this is how the temperature is stored inside the temperature table in the database of the service
def insertTemperatureAndHumidity(temp, hum):
    conn = db_connect()

    mycurs = conn.cursor(dictionary=True)

    sql_statement = "INSERT INTO temperature(temp_result, date_time, posted) VALUES(%s, NOW()-INTERVAL 5 HOUR, %s);"
    sql_statement2 = "INSERT INTO humidity(hum_result, date_time, posted) VALUES(%s, NOW()-INTERVAL 5 HOUR, %s);"

    values = [temp, 1]
    values2 = [hum, 1]

    mycurs.execute(sql_statement, values)
    conn.commit()

    mycurs.execute(sql_statement2, values2)
    conn.commit()

    mycurs.close()
    conn.close()


# this is how the data is being displayed on the main menu when appearing on main menu
@app.route("/", methods=['GET'])
def get_all_data():
    temperature_data = getTemperature()
    humidity_data = getHumidity()

    t = json.loads(temperature_data)
    h = json.loads(humidity_data)

    if temperature_data != None:
        return render_template('reports.html', temperature=t, humidity=h)
    else:
        message = "An error in retrieving the data has occurred"
        return render_template('error.html', error_message=message)


# this is where you get all the temperatures sent to the database
def getTemperature():
    conn = db_connect()
    mycurs = conn.cursor()
    temperatures = []

    mycurs.execute("SELECT * FROM temperature ORDER BY date_time DESC")

    for row in mycurs:
        id = row[0]
        temp_result = str(row[1])
        date_time = row[2].strftime("%Y-%m-%d %H:%M:%S")
        posted = row[3]
        temperatures.append({'id': id, 'temp_result': temp_result,
                             'date_time': date_time, 'posted': posted})
        r = json.dumps(temperatures)

    mycurs.close()
    conn.close()
    return r


# this is where you get all the humidities sent to the database
def getHumidity():
    conn = db_connect()
    mycurs = conn.cursor()
    humidities = []

    mycurs.execute("SELECT * FROM humidity ORDER BY date_time DESC")

    for row in mycurs:
        id = row[0]
        hum_result = str(row[1])
        date_time = row[2].strftime("%Y-%m-%d %H:%M:%S")
        posted = row[3]
        humidities.append({'id': id, 'hum_result': hum_result,
                           'date_time': date_time, 'posted': posted})
        r = json.dumps(humidities)

    mycurs.close()
    conn.close()
    return r


# display the latest temperature and humidity on the website
@app.route("/getlatest", methods=['GET'])
def return_temperature_in_table():
    temperature = getLatestTemp()
    humidity = getLatestHum()

    t = json.loads(temperature)
    h = json.loads(humidity)

    if temperature != None:
        return render_template('reports.html', temperature=t, humidity=h)
    else:
        message = "An error in retrieving the data has occurred"
        return render_template('error.html', error_message=message)


# get latest temperature
def getLatestTemp():
    conn = db_connect()
    mycurs = conn.cursor()
    data = []

    mycurs.execute("SELECT * FROM temperature ORDER BY date_time DESC LIMIT 1")

    for row in mycurs:
        id = row[0]
        temp_result = row[1]
        date_time = str(row[2])
        data.append({'id': id, 'temp_result': temp_result, 'date_time': date_time})
        r = json.dumps(data)

    mycurs.close()
    conn.close()
    return r


# get latest humidity
def getLatestHum():
    conn = db_connect()
    mycurs = conn.cursor()
    data = []
    mycurs.execute("SELECT * FROM humidity ORDER BY date_time DESC LIMIT 1")

    for row in mycurs:
        id = row[0]
        hum_result = row[1]
        date_time = str(row[2])
        data.append({'id': id, 'hum_result': hum_result, 'date_time': date_time})
        r = json.dumps(data)

    mycurs.close()
    conn.close()
    return r


# @app.route('/get', methods=['GET'])
# def get_last():
#    return jsonify(getLatestData())


# def getLatestData():
#    conn = mysql.connector.Connect(host="NickEspitalier.mysql.pythonanywhere-services.com", user="NickEspitalier",
#                                   password="CloudyJJ12", database="NickEspitalier$finalprojectiot")
#    mycurs = conn.cursor()
#    mycurs.execute("SELECT * FROM reports ORDER BY report_id DESC LIMIT 1;")
#    data = mycurs.fetchall()
#    conn.close()
#    return data;


# this is the request to create a new user
# @app.route('/register', methods=['POST'])
# def signup_user():

#    user_name = request.json["user_name"]
#    password = request.json["password"]

#    insert_user(user_name, password)
#    return app.response_class(response="Success", status=201)


# this is the method where the user information is formatted and sent to the database
# def insert_user(user_name, password):

#    conn = db_connect()
#    mycurs = conn.cursor(dictionary=True)

#    user_id=str(uuid.uuid4())
#    name = user_name
#    hashed_pw = generate_password_hash(password, method="sha256")

#    sql_statement = "INSERT INTO user(user_id, user_name, password) VALUES(%s, %s, %s);"

#    value = [user_id, name, hashed_pw]

#    mycurs.execute(sql_statement, value)
#    conn.commit()

#    mycurs.close()
#    conn.close()


# this is the request to login to the main page
# @app.route('/login', methods=['GET'])
# def login_user():

#    conn = db_connect()
#    mycurs = conn.cursor(dictionary=True)


#   auth = request.authorization

#    if not auth or not auth.username or not auth.password:
#        return make_response('Could not verify', 401, {'WWW.Authentication': 'Basic Realm: "login required"'})

#    sql_statement = "SELECT user_name, password from user where user_name = %s"

#    value = [auth.username]

#    user = mycurs.execute(sql_statement, value)


#    if check_password_hash(user.password, auth.password):
#        token = jwt.encode(
#            {'user_id': user.user_id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
#            app.config['SECRET_KEY'], algorithm="HS256")

#        return jsonify({"token": token})

#    return make_response('Could not verify', 401, {'WWW.Authentication': 'Basic Realm: "login incorrect"'})


# this is the request to get temperature between two date range
# @app.route("/temperature", methods=['POST', 'GET'])
# def dateRangeTempAndHum():

# if request.method == 'POST':
#    start = request.args.get('start')
#    finish = request.args.get('finish')

#    temperature = getDataRangeTemp(start, finish)
#    humidity = getDataRangeHum(start, finish)


#    t = json.loads(temperature)
#    h = json.loads(humidity)

# else:
#    if temperature != None:
#        return render_template('reports.html', temperature=t, humidity=h)
#    else:
#        message = "An error in retrieving the data has occurred"
#        return render_template('error.html', error_message=message)


# this is the select statement to get temperatures between two datetimes
# def getDataRangeTemp(start, finish):

#    conn = db_connect()
#    mycurs = conn.cursor()
#    data = []

#    query = "SELECT * FROM temperature WHERE(date_time BETWEEN %s AND %s)"
#    values = [start, finish]

#    print(values)

#    mycurs.execute(query, values)

#    for row in mycurs:
#        id = row[0]
#        temp_result = row[1]
#        date_time = str(row[2])
#        data.append({'id': id, 'temp_result': temp_result, 'date_time': date_time})
#        r = json.dumps(data)
#    conn.close()
#    return r


# this is the select statement to get humidities between two datetimes
# def getDataRangeHum(start, finish):
#    conn = db_connect()
#    mycurs = conn.cursor()
#    data = []
#    query= "SELECT * FROM humidity WHERE(date_time BETWEEN %s AND %s)"
#    values = [start, finish]

#    mycurs.execute(query, values)
#    for row in mycurs:
#        id = row[0]
#        hum_result = row[1]
#        date_time = str(row[2])
#        data.append({'id': id, 'hum_result': hum_result, 'date_time': date_time})
#        r = json.dumps(data)
#    conn.close()
#    return r


@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'not found'}), 404
