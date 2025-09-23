import mysql.connector

class DBConnection:
    dbcon = None

    def connect(self):
        self.dbcon = mysql.connector.connect(host="localhost",
                                            user="weather_usr",
                                            password="190602RmSl&",
                                            database="weather_db")

    def select(self, query):
        cursor = self.dbcon.cursor()
        cursor.execute(query)
        return cursor.fetchall()

    def insert(self, query, val):
        cursor = self.dbcon.cursor()
        cursor.execute(query, val)
        self.dbcon.commit()
        return cursor.lastrowid

    def update(self, query):
        cursor = self.dbcon.cursor()
        cursor.execute(query)
        self.dbcon.commit()

    def delete(self, query):
        cursor = self.dbcon.cursor()
        cursor.execute(query)
        self.dbcon.commit()

    def close(self):
        self.dbcon.close()