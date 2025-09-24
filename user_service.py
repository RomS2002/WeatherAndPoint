from db_conn import DBConnection

class User:
    def __init__(self, usr_id = 0, username = None, password = None, weather = None):
        self.usr_id = usr_id
        self.username = username
        self.password = password
        self.weather = weather

    def __str__(self):
        return f"User({self.usr_id}, {self.username}, {self.password}, {self.weather})"

class UserService:
    def __init__(self):
        self.con = DBConnection()
        self.con.connect()

    def find_user_by_username(self, username: str):
        res = self.con.select(f"SELECT * FROM users WHERE usr_username='{username}'")
        if len(res) == 0:
            return None
        print(f"Selected user: {res[0][1]}")
        return User(res[0][0], res[0][1], res[0][2], res[0][3])

    def add_new_user(self, user: User):
        return self.con.insert("INSERT INTO users (usr_username, usr_password, usr_weather) "
                              "VALUES(%s, %s, %s)", (user.username, user.password, user.weather))

    def update_user_weather(self, uid: int, weather: str):
        self.con.update(f"UPDATE users SET usr_weather = '{weather}' WHERE usr_id={uid}")

    def close(self):
        self.con.close()