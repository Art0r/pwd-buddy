import shutil
import click
import os
import pandas as pd
from src.utils.cloud import ManageCloud
from src.account import Account, get_all_accounts, create_account, \
    get_account, delete_account, reset_all, create_account_csv, get_all_accounts_to_export
from tabulate import tabulate
from prompt_toolkit.styles import Style
from prompt_toolkit import HTML, print_formatted_text
from yaspin import yaspin
from cryptography.fernet import Fernet
from config import APP_PATH, ACCOUNTS_TXT, ACCOUNTS_CSV, SECRET_FILE, SECRET

style_ok = Style.from_dict({
    'msg': '#50FC00 bold',
    'sub-msg': '#C3FFA7 italic'
})

style_fail = Style.from_dict({
    'msg': '#FF0000 bold',
    'sub-msg': '#FE8787 italic'
})


@click.group()
def account():
    """Aplicação de linha de comando para gerenciar contas e senhas"""


@account.command()
def getall():
    spinner = yaspin(text='Carregando...', color='cyan')
    spinner.start()
    columns = [column.key for column in Account.__table__.columns]
    results = get_all_accounts()
    if results:
        spinner.stop()
        click.echo(tabulate(results, headers=columns, tablefmt='grid'))
    else:
        spinner.stop()
        print_formatted_text(HTML(
            u"<b>></b> <msg>Erro</msg> <sub-msg>Não há nenhuma conta para ser retornada</sub-msg>"
        ), style=style_fail)
    return


@account.command()
@click.option('-n', '--name', help='Nome do site ao qual se refere a conta',
              required=True, type=str)
def getone(name: str):
    spinner = yaspin(text='Carregando...', color='cyan')
    spinner.start()
    columns = [column.key for column in Account.__table__.columns]
    results = get_account(name)
    if results:
        spinner.stop()
        click.echo(tabulate(results, headers=columns, tablefmt='grid'))
    else:
        spinner.stop()
        print_formatted_text(HTML(
            u"<b>></b> <msg>Erro</msg> <sub-msg>Não há nenhuma conta com esse nome</sub-msg>"
        ), style=style_fail)
    return


@account.command()
@click.option('-n', '--name', help='Nome do site ao qual se refere a conta', required=True, type=str)
@click.option('-e', '--email', help='Email da conta cadastrada', required=True, type=str)
def create(name: str, email: str):
    spinner = yaspin(text='Criando...', color='cyan')
    spinner.start()
    result = create_account(name=name, email=email)
    columns = [column.key for column in Account.__table__.columns]
    if result:
        spinner.stop()
        print_formatted_text(HTML(
            u"<b>></b> <msg>OK</msg> <sub-msg>A conta foi cadastrada com sucesso</sub-msg>"
        ), style=style_ok)
        click.echo(tabulate(result, headers=columns, tablefmt='grid'))
    else:
        spinner.stop()
        print_formatted_text(HTML(
            u"<b>></b> <msg>Erro</msg> <sub-msg>Ocorreu um erro ao criar uma conta</sub-msg>"
        ), style=style_fail)


@account.command()
@click.option('-n', '--name', help='Nome do site ao qual se refere a conta', required=True, type=str)
@click.option('-e', '--email', help='Email da conta cadastrada', required=True, type=str)
def delete(name: str, email: str):
    spinner = yaspin(text='Deletando...', color='cyan')
    spinner.start()
    result = delete_account(name=name, email=email)
    if result:
        spinner.stop()
        print_formatted_text(HTML(
            u"<b>></b> <msg>OK</msg> <sub-msg>A conta foi deletada com sucesso</sub-msg>"
        ), style=style_ok)
    else:
        spinner.stop()
        print_formatted_text(HTML(
            u"<b>></b> <msg>Erro</msg> <sub-msg>Não há nenhuma conta com esse nome e email</sub-msg>"
        ), style=style_fail)


@account.command()
@click.option('-p', '--path', help='Pasta para onde os segredos serão movidos',
              required=True, type=str, default="Documentos")
def export(path: str):
    columns = [column.key for column in Account.__table__.columns]
    accounts = get_all_accounts_to_export()
    if not accounts:
        print_formatted_text(HTML(
            u"<b>></b> <msg>Erro</msg> <sub-msg>Erro ao buscar contas</sub-msg>"
        ), style=style_fail)
        return
    output = ""
    key = Fernet.generate_key()
    f = Fernet(key)

    if os.path.isfile(ACCOUNTS_TXT):
        os.remove(ACCOUNTS_TXT)

    with open(ACCOUNTS_TXT, 'wb') as file:
        output += ','.join(columns)
        for acc in accounts:
            output += '\n{}'.format(','.join(str(field) for field in acc))
        enc = f.encrypt(output.encode('latin1'))
        file.write(enc)
        file.close()
    manage = ManageCloud()
    result = manage.delete_all_then_upload()
    os.remove(ACCOUNTS_TXT)
    if result:
        print_formatted_text(HTML(
            u"<b>></b> <msg>OK</msg> <sub-msg>O upload foi realizado com sucesso</sub-msg>"
        ), style=style_ok)
    else:
        print_formatted_text(HTML(
            u"<b>></b> <msg>Erro</msg> <sub-msg>Erro ao fazer o upload para a pasta</sub-msg>"
        ), style=style_fail)
    with open(os.path.join(APP_PATH, 'secret_file.key'), 'wb') as file:
        file.write(key)
        file.close()
    try:
        shutil.move(
            os.path.join(APP_PATH, 'secret.key'),
            os.path.join(SECRET)
        )
        shutil.move(
            os.path.join(APP_PATH, 'secret_file.key'),
            os.path.join(SECRET_FILE)
        )
    except Exception as e:
        print_formatted_text(HTML(
            u"<b>></b> <msg>Erro</msg> <sub-msg>Caminho inválido: {}</sub-msg>".format(e.args[1])
        ), style=style_fail)


@account.command()
@click.option('-p', '--path', help='Pasta para onde os segredos serão movidos',
              required=True, type=str, default="Documentos")
def importcsv(path: str):
    reset_all()
    manage = ManageCloud()
    manage.download_file()
    try:
        shutil.move(
            os.path.join(SECRET),
            os.path.join(APP_PATH, 'secret.key')
        )
        shutil.move(
            os.path.join(SECRET_FILE),
            os.path.join(APP_PATH, 'secret_file.key')
        )

        txt = open(ACCOUNTS_TXT, 'rb').read()
        secret_file = open(os.path.join(APP_PATH, 'secret_file.key'), 'rb').read()
        f = Fernet(secret_file)
        dec = f.decrypt(txt)
        with open(ACCOUNTS_CSV, 'w') as file:
            file.write(dec.decode('latin1'))
            file.close()
        data = pd.read_csv(ACCOUNTS_CSV)
        for d in data.values:
            create_account_csv(name=d[1], email=d[2], password=d[3])

    except Exception as e:
        print_formatted_text(HTML(
            u"<b>></b> <msg>Erro</msg> <sub-msg>Erro ao importar: {}</sub-msg>".format(e.args[1])
        ), style=style_fail)
    finally:
        os.remove(ACCOUNTS_TXT)
        os.remove(ACCOUNTS_CSV)


@account.command()
def reset():
    reset_all()
