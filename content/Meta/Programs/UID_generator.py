import hashlib
import base64

def short_uid(authority_string, length=6):
    digest = hashlib.sha1(authority_string.encode("utf-8")).digest()
    slug = base64.b32encode(digest).decode("utf-8").rstrip("=")
    return slug[:length]

authority_string = "a"
print(short_uid(authority_string))
