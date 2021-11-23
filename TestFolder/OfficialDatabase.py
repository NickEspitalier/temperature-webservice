from datetime import datetime
from TestFolder.DBReports import DBReports

reports = DBReports()

reportsCollection = reports.select_all_reports()
my_reports = reports.select_reports(2)

# creating a datetime value

time = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
print(time)
add_report = reports.insert_reports(time, 34.5, 70.0)

print(reportsCollection)
print(my_reports)
print(add_report)
