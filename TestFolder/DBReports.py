from TestFolder.DatabaseConnection import DatabaseConnection


class DBReports:
    dbConnection = DatabaseConnection()

    def select_all_reports(self):
        return self.dbConnection.execute_select_query("reports")

    def select_reports(self, reportID=int):
        return self.dbConnection.execute_select_query("reports", params={'report_id': reportID})

    # to do
    def insert_reports(self, date, temperature, humidity):
        return self.dbConnection.execute_insert_query("reports", date, temperature, humidity)
