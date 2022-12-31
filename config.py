import os
import platform

if platform.system() == "Windows":
    SECRETS_FOLDER = os.path.join(os.path.expanduser('~'), 'OneDrive', 'Documentos', 'pwd-buddy-secrets')
else:
    SECRETS_FOLDER = os.path.join(os.path.expanduser('~'), 'Documentos', 'pwd-buddy-secrets')

if not os.path.isdir(SECRETS_FOLDER):
    os.mkdir(SECRETS_FOLDER)

APP_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)))
SECRET = os.path.join(SECRETS_FOLDER, 'secret.key')
SECRET_FILE = os.path.join(SECRETS_FOLDER, 'secret_file.key')
ACCOUNTS_TXT = os.path.join(APP_PATH, 'accounts.txt')
ACCOUNTS_CSV = os.path.join(APP_PATH, 'accounts.csv')