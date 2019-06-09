import hashlib

user = "john"
pw = "supersecurepassword"

print("Add the following line to the users.txt\n")
print(f"{user} {hashlib.sha1(pw.encode('utf-8')).hexdigest()}")
