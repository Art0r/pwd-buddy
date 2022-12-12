from cryptography.fernet import Fernet
import os


class Crypt:
    KEY_PATH: str
    key: bytes

    def __init__(self, app_path: str):
        self.KEY_PATH = os.path.join(app_path, 'secret.key')
        if not os.path.isfile(self.KEY_PATH):
            with open(self.KEY_PATH, 'wb') as file:
                key = Fernet.generate_key()
                file.write(key)
                file.close()
                self.__load_key()
        else:
            self.__load_key()

    def __load_key(self) -> None:
        self.key = open(self.KEY_PATH, 'rb').read()

    def encrypt_text(self, text: str) -> str:
        f = Fernet(self.key)
        token = f.encrypt(text.encode('latin1'))
        return token.decode('latin1')

    def decrypt_text(self, text: str) -> str:
        f = Fernet(self.key)
        token = f.decrypt(text)
        return token.decode('latin1')