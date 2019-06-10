import hashlib

users: dict = {}


class Password:
    def __init__(self):
        password_file = open('users.txt', 'r', encoding='utf-8')
        d = {}
        for line in password_file.readlines():
            entry = line.rstrip('\n').split(" ")
            d[entry[0]] = entry[1]
        self.users = d
        password_file.close()
        print(f"Password initialized with {self.users} {d} users.")

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
