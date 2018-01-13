import bcrypt


def hash_password(password):
    return bcrypt.hashpw(password, bcrypt.gensalt())


def check_password(password, salt, hashed):
    return bcrypt.hashpw(password, salt) == hashed
