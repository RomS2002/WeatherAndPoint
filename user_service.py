from db_conn import DBConnection

class User:
    def __init__(self, usr_id = 0, username = None, password = None, weather = None):
        self.usr_id = usr_id
        self.username = username
        self.password = password
        self.weather = weather

class UserService:
    def __init__(self):
        self.con = DBConnection()
        self.con.connect()

    def find_user_by_username(self, username):
        res = self.con.select(f"SELECT * FROM users WHERE usr_username='{username}'")
        if len(res) == 0:
            return None
        return User(res[0][0], res[0][1], res[0][2], res[0][3])

    def close(self):
        self.con.close()