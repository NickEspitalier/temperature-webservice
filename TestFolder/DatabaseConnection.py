import mysql.connector
from datetime import datetime


class DatabaseConnection(object):

    def __init__(self):
        try:
            self.config_file = "my.config"
            self.connex = mysql.connector.connect(option_files=self.config_file)
        except mysql.connector.Error as e:
            print(e)
            self.close()

    def execute_select_query(self, table_name, params=None):
        return_set = []
        cursor = self.connex.cursor(dictionary=True)
        if params is None:
            cursor.execute("SELECT * FROM {} ORDER BY date_time DESC".format(table_name))
        else:
            where_clause = "WHERE " + " AND ".join(['`' + k + '` = %s' for k in params.keys()])
            print(where_clause)

            values = list(params.values())
            print(values)

            sql = "SELECT * FROM {} ".format(table_name) + where_clause
            print(sql)
            cursor.execute(sql, values)

        for x in cursor:
            return_set.append(x)

        cursor.close()
        return return_set

    def execute_insert_query(self, table_name, date, temperature, humidity):

        cursor = self.connex.cursor(dictionary=True)

        beginning_sql_statement = "INSERT INTO finalprojectiot.{}".format(table_name)
        column_title = "(date_time, temp_result, hum_result)"
        data_added = "VALUES('{}', {}, {})".format(date, temperature, humidity)

        sql_command = beginning_sql_statement + column_title + data_added
        print(sql_command)
        cursor.execute(sql_command)
        self.connex.commit()

