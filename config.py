import os

if not os.path.isdir(os.path.join(os.path.expanduser('~'), 'Documentos', 'pwd-buddy-secrets')):
    os.mkdir(os.path.join(os.path.expanduser('~'), 'Documentos', 'pwd-buddy-secrets'))

APP_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)))
APP_KEY = os.getenv('APP_KEY')
APP_SECRET = os.getenv('APP_SECRET')
SECRET = os.path.join(os.path.expanduser('~'), 'Documentos', 'pwd-buddy-secrets', 'secret.key')
SECRET_FILE = os.path.join(os.path.expanduser('~'), 'Documentos', 'pwd-buddy-secrets', 'secret_file.key')
ACCOUNTS_TXT = os.path.join(APP_PATH, 'accounts.txt')
ACCOUNTS_CSV = os.path.join(APP_PATH, 'accounts.csv')