def table_login(user):
    if len(app.current_users) == 0: 
        user.auth_playerids = [0,2,4]
        user.oppo_playerids = list(set(range(6)) - set(self.auth_playerids))
    elif len(app.current_users) == 1: 
        user.auth_playerids = [1,3,5]
        user.oppo_playerids = list(set(range(6)) - set(self.auth_playerids))
    app.current_users.append(user)

        
