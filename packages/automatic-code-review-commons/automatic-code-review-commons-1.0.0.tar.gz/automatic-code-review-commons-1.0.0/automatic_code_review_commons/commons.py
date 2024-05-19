import hashlib


def generate_id(comment):
    md5_hash = hashlib.md5()
    md5_hash.update(comment.encode('utf-8'))
    return md5_hash.hexdigest()
