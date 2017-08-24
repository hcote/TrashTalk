class HtmlConstants:
    def __init__(self):
        self.password_pattern = "(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{6,}"
        self.password_title = "Must contain at least one number and one uppercase and lowercase letter, and at least 6 or more characters"

        self.username_pattern = "[a-zA-Z0-9]{2,}"
        self.username_title = "2-20 alpha-numeric characters"

        self.date_pattern = "(?:19|20)[0-9]{2}-(?:(?:0[1-9]|1[0-2])-(?:0[1-9]|1[0-9]|2[0-9])|(?:(?!02)(?:0[1-9]|1[0-2])-(?:30))|(?:(?:0[13578]|1[02])-31))"
        self.date_placeholder = "yyyy-mm-dd"

        self.time_pattern = "([0-9]|0[0-9]|1[0-2])(:[0-5][0-9])"
        self.time_placeholder = "hh:mm"
    # def get_password_pattern(self):
    #     return self.password_pattern
