import CryptoUtils

PLAINTEXT_FILE = 'config.py.json'
KEY=""

def encrypt_file():

    with open(PLAINTEXT_FILE) as f:
        data_file = f.read()
    f.close()

    with open(PLAINTEXT_FILE + ".asc",'wb') as f:
        f.write(CryptoUtils.encrypt(data_file,KEY))
    f.close()

def decrypt_file():

    with open(PLAINTEXT_FILE + ".asc") as f:
        data_file = f.read()
    f.close()

    x = CryptoUtils.decrypt(data_file,KEY).decode("utf-8")

    with open(PLAINTEXT_FILE,'w') as f:
        f.write(x)
    f.close()

encrypt_file()
# decrypt_file()
