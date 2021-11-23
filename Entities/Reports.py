class Reports:
    report_id = 0
    date_time = ""
    temp_result = 0.0
    hum_result = 0.0

    def __init__(self, date_time, temp_result, hum_result):
        self.date_time = date_time
        self.temp_result = temp_result
        self.hum_result = hum_result
