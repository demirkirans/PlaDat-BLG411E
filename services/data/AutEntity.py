import hashlib
class AutEntity(object):

    def __init__(self, email, psw, userName=""):

        self.email = email
        self.password = psw
        self.userName = userName

    def hashing(self):
        self.password = hashlib.md5(self.password.encode()).hexdigest()