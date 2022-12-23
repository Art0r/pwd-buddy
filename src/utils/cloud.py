from dropbox import DropboxOAuth2FlowNoRedirect
from dropbox.exceptions import ApiError, AuthError
from prompt_toolkit.styles import Style
from prompt_toolkit import HTML, print_formatted_text
from config import APP_PATH
import dropbox
import os

from yaspin import yaspin

style_ok = Style.from_dict({
    'msg': '#50FC00 bold',
    'sub-msg': '#C3FFA7 italic'
})

style_fail = Style.from_dict({
    'msg': '#FF0000 bold',
    'sub-msg': '#FE8787 italic'
})


class AuthCloud:
    _APP_KEY: str
    _APP_SECRET: str
    _ACCESS_TOKEM: str

    def __init__(self, f):
        self._APP_KEY = "5zkrhpwo6bug4bl"
        self._APP_SECRET = "20uqxx3b9bv4ogv"
        self.f = f

    def __call__(self, *args, **kwargs):
        auth_flow = DropboxOAuth2FlowNoRedirect(self._APP_KEY, self._APP_SECRET)
        authorize_url = auth_flow.start()
        print("1. Go to: " + authorize_url)
        print("2. Click \"Allow\" (you might have to log in first).")
        print("3. Copy the authorization code.")
        auth_code = input("Enter the authorization code here: ").strip()
        try:
            oauth_result = auth_flow.finish(auth_code)
            self._ACCESS_TOKEN = oauth_result.access_token

        except AuthError as e:
            print('Error: %s' % (e,))
            exit(1)

        return self.f(self, access_token=self._ACCESS_TOKEN)


class ManageCloud:
    def __init__(self):
        pass

    @AuthCloud
    def delete_all_then_upload(self, access_token: str):
        dbx = dropbox.Dropbox(oauth2_access_token=access_token)
        try:
            files = dbx.files_list_folder('')
            for file in files.entries:
                if file.name == 'accounts.txt':
                    dbx.files_delete_v2('/accounts.txt')
            try:
                spinner = yaspin(text='Exportando...', color='cyan')
                spinner.start()
                txt = open(os.path.join(APP_PATH, 'accounts.txt'), 'rb').read()
                dbx.files_upload(txt, '/accounts.txt')
                spinner.stop()
                return True
            except ApiError as e:
                print(e.args[1])
                return False
        except ApiError as e:
            print(e.args[1])
            return False

    @AuthCloud
    def download_file(self, access_token: str):
        dbx = dropbox.Dropbox(oauth2_access_token=access_token)
        spinner = yaspin(text='Importando...', color='cyan')
        spinner.start()
        try:
            metadata, res = dbx.files_download('/accounts.txt')
            if not res.content:
                spinner.stop()
                print_formatted_text(HTML(
                    u"<b>></b> <msg>Erro</msg> <sub-msg>Erro fazer o download</sub-msg>"
                ), style=style_fail)
            else:
                file = open(os.path.join(APP_PATH, 'accounts.txt'), 'wb')
                file.write(res.content)
                spinner.stop()
        except ApiError as e:
            spinner.stop()
            print_formatted_text(HTML(
                u"<b>></b> <msg>Erro</msg> <sub-msg>Erro ao importar: {}</sub-msg>".format(e.args[1])
            ), style=style_fail)

