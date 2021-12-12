import json
import mysql.connector
import datetime
from flask import Flask
from flask import render_template, jsonify, request


app = Flask(__name__)


@app.route("/", methods=['GET'])
def get_all_reports():
    result_data = getData()
    r = json.loads(result_data)
    if result_data != None:
        return render_template('reports.html', result_data=r)
    else:
        message = "An error in retrieving the data has occurred"
        return render_template('error.html', error_message=message)


@app.route('/get', methods=['GET'])
def get_last():
    return jsonify(getLatestData())


@app.route('/post/report', methods=['POST'])
def insert_report():
    temp = request.json["temp_result"]
    hum = request.json["hum_result"]
    date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    insertData(date, temp, hum)
    #changed to 200 to match rasp-pi code
    return app.response_class(response="Success", status=200)


@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'not found'}), 404


def getData():
    conn = mysql.connector.Connect(host="NickEspitalier.mysql.pythonanywhere-services.com", user="NickEspitalier", password="CloudyJJ12", database="NickEspitalier$finalprojectiot")
    mycurs = conn.cursor()
    data = []
    mycurs.execute("SELECT * FROM reports ORDER BY date_time DESC")
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


def getLatestData():
    conn = mysql.connector.Connect(host="NickEspitalier.mysql.pythonanywhere-services.com", user="NickEspitalier",
                                   password="CloudyJJ12", database="NickEspitalier$finalprojectiot")
    mycurs = conn.cursor()
    mycurs.execute("SELECT * FROM reports ORDER BY report_id DESC LIMIT 1;")
    data = mycurs.fetchall()
    conn.close()
    return data;


def insertData(date, temperature, humidity):
    conn = mysql.connector.Connect(host="NickEspitalier.mysql.pythonanywhere-services.com", user="NickEspitalier",
                                   password="CloudyJJ12", database="NickEspitalier$finalprojectiot")
    mycurs = conn.cursor()
    mycurs.execute("INSERT INTO reports (date_time, temp_result, hum_result) VALUES (%s, %s, %s);",[date, temperature, humidity])
    conn.commit()
    conn.close()