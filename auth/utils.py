import hashlib 


def hash_password(val):
    sha = hashlib.sha1()
    sha.update(val)
    return sha.hexdigest()

