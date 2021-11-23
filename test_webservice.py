import json
import mysql.connector
from flask import Flask, render_template, jsonify, request


app = Flask(__name__)
app.debug = True

def getData():
    conn = mysql.connector.Connect(host="127.0.0.1", user="root", password="password", database="finalprojectiot")
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


@app.route("/", methods=['GET'])
def reports():
    result_data = getData()
    r = json.loads(result_data)
    if result_data != None:
        return render_template('reports.html', result_data=r)
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
