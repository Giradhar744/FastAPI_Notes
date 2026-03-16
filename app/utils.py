from pwdlib import PasswordHash

# password Hashing
password_convertor = PasswordHash.recommended()


def hash(password: str):
    return password_convertor.hash(password)

def verify_user(plain_password, hashed_password):
    return password_convertor.verify(plain_password, hashed_password)