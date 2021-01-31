import hashlib
class Password:

    def __init__(self,id, newPassword, oldPassword):
        self.id = id
        self.newPassword = newPassword
        self.oldPassword = oldPassword
    
    def hashig(self):
        oldPsw = hashlib.md5(self.oldPassword.encode()).hexdigest()
        newPsw = hashlib.md5(self.newPassword.encode()).hexdigest()

        dic = {
            "ID": self.id,
            "oldPassword": oldPsw,
            "newPassword": newPsw
        }

        return dic