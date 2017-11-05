class User:
    def __init__(self):
        self.id = id # int
        self.auth_playerids = []#auth_playerids
        self.oppo_playerids = []#list(set(range(6)) - set(self.auth_playerids))

user1 = User()
# global user list: app.current_users 


def table_login(user):
    if len(self.current_users) == 0: 
        app.current_users.append(User(user_name, [0,2,4]))
    elif len(self.current_users) == 1: 
        app.current_users.append(User(user_name, [1,3,5]))
    else:
        app.current_users.append(User(user_name, []))

        
table_login(user1)
   

