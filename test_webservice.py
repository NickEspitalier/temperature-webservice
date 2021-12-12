import json
from datetime import time

import mysql.connector
from flask import Flask, render_template, jsonify, request
import logging

app = Flask(__name__)
app.debug = True

def db_connect():
    try:
        db_connection = mysql.connector.connect(host="127.0.0.1", user="root", password="password", database="finalprojectiot")
        # If connection is not successful
    except logging.error as e:
        print("Can't connect to database")
        return 0
        # If Connection Is Successful
    print("Connected")
    # Making Cursor Object For Query Execution
    return db_connection

def getLatestsTemp():
    conn = db_connect()
    mycurs = conn.cursor()
    data = []
    mycurs.execute("SELECT * FROM temperature ORDER BY date DESC LIMIT 1")
    for row in mycurs:
        report_id = row[0]
        hum_result = row[1]
        date_time = str(row[2])
        data.append({'report_id': report_id, 'hum_result': hum_result, 'date_time': date_time})
        r = json.dumps(data)
    conn.close()
    return r

def getLatestsHum():
    conn = db_connect()
    mycurs = conn.cursor()
    data = []
    mycurs.execute("SELECT * FROM humidity ORDER BY date DESC LIMIT 1")
    for row in mycurs:
        report_id = row[0]
        temp_result = row[1]
        date_time = str(row[2])
        data.append({'report_id': report_id, 'hum_result': temp_result, 'date_time': date_time})
        r = json.dumps(data)
    conn.close()
    return r

def getDataRangeHum(start, finish):
    conn = db_connect()
    mycurs = conn.cursor()
    data = []
    query="SELECT * FROM temperature WHERE(date BETWEEN %s AND %s"
    mycurs.execute(query, (start,finish))
    for row in mycurs:
        report_id = row[0]
        hum_result = row[1]
        date_time = str(row[2])
        data.append({'report_id': report_id, 'hum_result': hum_result, 'date_time': date_time})
        r = json.dumps(data)
    conn.close()
    return r

def getDataRangeHum(start, finish):
    conn = db_connect()
    mycurs = conn.cursor()
    data = []
    query = "SELECT * FROM humidity WHERE(date BETWEEN %s AND %s"
    mycurs.execute(query, (start, finish))
    for row in mycurs:
        report_id = row[0]
        temp_result = row[1]
        date_time = str(row[2])
        data.append({'report_id': report_id, 'hum_result': temp_result, 'date_time': date_time})
        r = json.dumps(data)
    conn.close()
    return r

def getData():
    conn = db_connect()
    mycurs = conn.cursor()
    data = []
    mycurs.execute("SELECT * FROM temperature ORDER BY date_time DESC")
    for row in mycurs:
        report_id = row[0]
        date_time = str(row[1])
        temp_result = row[2]
        hum_result = row[3]
        data.append({'report_id': report_id, 'date_time': date_time,
                     'temp_result': temp_result, 'hum_result': hum_result})
        r = json.dumps(data)
    conn.close()
    return r


@app.route("/temperature", methods=['GET'])
def reports():
    temp_data = getLatestsTemp()
    r = json.loads(temp_data)
    if temp_data != None:
        return render_template('reports.html', temp_data=r)
    else:
        message = "An error in retrieving the data has occurred"
        return render_template('error.html', error_message=message)



@app.route("/humidity", methods=['GET'])
def reports():
    hum_data = getLatestsHum()
    r = json.loads(hum_data)
    if hum_data != None:
        return render_template('reports.html', hum_data=r)
    else:
        message = "An error in retrieving the data has occurred"
        return render_template('error.html', error_message=message)


@app.route("/", methods=['POST'])
def dateRangehumidity():
    start = request.form.get('from',time.strftime("%Y-%m-%d %H:%M:%S"))
    finish = request.form.get('to',time.strftime("%Y-%m-%d %H:%M:%S"))

    hum_data = getDataRangeHum(start, finish)
    r = json.loads(hum_data)
    if hum_data != None:
        return render_template('reports.html', hum_data=r)
    else:
        message = "An error in retrieving the data has occurred"
        return render_template('error.html', error_message=message)


@app.route("/", methods=['POST'])
def dateRangetemp():
    start = request.form.get('tempfrom',time.strftime("%Y-%m-%d %H:%M:%S"))
    finish = request.form.get('tempto',time.strftime("%Y-%m-%d %H:%M:%S"))

    temp_data = getDataRangeHum(start, finish)
    r = json.loads(temp_data)
    if temp_data != None:
        return render_template('reports.html', temp_data=r)
    else:
        message = "An error in retrieving the data has occurred"
        return render_template('error.html', error_message=message)


@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'not found'}), 404


@app.route('/postjson', methods=['POST'])
def postJsonHandler():
    content = request.get_json()
    print(content)
    return 'JSON posted'


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
