import hashlib


def generate_id(comment):
    md5_hash = hashlib.md5()
    md5_hash.update(comment.encode('utf-8'))
    return md5_hash.hexdigest()


def create(comment_id,
           comment_path,
           comment_description,
           comment_end_line=1,
           comment_start_line=1,
           comment_snipset=True,
           comment_language=None):
    return {
        "id": comment_id,
        "comment": comment_description,
        "position": {
            "language": comment_language,
            "path": comment_path,
            "startInLine": comment_start_line,
            "endInLine": comment_end_line,
            "snipset": comment_snipset
        }
    }
