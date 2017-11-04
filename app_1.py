class User:
    def __init__(self, user_name, auth_playerids):
        self.user_name = user_name
        self.auth_playerids = auth_playerids
        self.oppo_playerids = list(set(range(6)) - set(self.auth_playerids))
class App:

    def table_login(self, user_name):
        if len(self.current_users) == 0: 
            self.current_users.append(User(user_name, [0,2,4]))
        elif len(self.current_users) == 1: 
            self.current_users.append(User(user_name, [1,3,5]))
        else:
            self.current_users.append(User(user_name, []))

        

