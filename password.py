import hashlib
import os.path

users: dict = {}
users_file = 'conf/users.txt'


class Password:
    def __init__(self):
        if os.path.isfile(users_file):
            password_file = open(users_file, 'r', encoding='utf-8')
            d = {}
            for line in password_file.readlines():
                entry = line.rstrip('\n').split(" ")
                d[entry[0]] = entry[1]
            self.users = d
            password_file.close()
        else:
            print(f"File '{users_file}' does not exist.")
        print(f"Password initialized with {self.users} users.")

    def verify_password(self, username: str, password: str) -> bool:
        """ Verifies the password of the user which is stored in 'users.txt' in sha1 form

        :param username name of the user
        :param password the password the user entered

        """
        if username in self.users:
            encrypted_password = hashlib.sha1(password.encode('utf-8')).hexdigest()
            match = encrypted_password == self.users.get(username)
            return match
        return False
