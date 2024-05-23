import hashlib

def md5(file_path, blocksize=65536):
    m = hashlib.md5()
    with open(file_path , "rb" ) as f:
        chunk = f.read(blocksize)
        while chunk:
            m.update(chunk)
            chunk = f.read(blocksize)
    return m.hexdigest()