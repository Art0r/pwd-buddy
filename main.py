import shutil
import click
import os
import pandas as pd
from drive import delete_all_then_upload, download
from account import Account, get_all_accounts, create_account, \
    get_account, delete_account, reset_all, create_account_csv, get_all_accounts_to_export
from tabulate import tabulate
from prompt_toolkit.styles import Style
from prompt_toolkit import HTML, print_formatted_text
from yaspin import yaspin


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
        click.echo(tabulate(results, headers=columns, tablefmt='fancy_grid'))
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
        click.echo(tabulate(results, headers=columns, tablefmt='fancy_grid'))
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
    if result:
        spinner.stop()
        print_formatted_text(HTML(
            u"<b>></b> <msg>OK</msg> <sub-msg>A conta foi cadastrada com sucesso</sub-msg>"
        ), style=style_ok)
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
            u"<b>></b> <msg>OK</msg> <sub-msg>A conta foi deletada com sucesso"
            u" para ser retornada</sub-msg>"
        ), style=style_ok)
    else:
        spinner.stop()
        print_formatted_text(HTML(
            u"<b>></b> <msg>Erro</msg> <sub-msg>Não há nenhuma conta com esse nome e email</sub-msg>"
        ), style=style_fail)


@account.command()
@click.option('-uf', '--upload_folder', help='Url da pasta no drive para onde será feito o upload',
              required=True, type=str)
def export(upload_folder: str):
    spinner = yaspin(text='Exportando...', color='cyan')
    spinner.start()

    columns = [column.key for column in Account.__table__.columns]
    accounts = get_all_accounts_to_export()
    if not accounts:
        spinner.stop()
        print_formatted_text(HTML(
            u"<b>></b> <msg>Erro</msg> <sub-msg>Erro ao buscar contas</sub-msg>"
        ), style=style_fail)
        return
    with open('accounts.csv', 'w') as file:
        file.write(','.join(columns))
        for acc in accounts:
            file.write('\n{}'.format(','.join(
                str(field) for field in acc))
            )
        file.close()
    result = delete_all_then_upload(upload_folder)
    if result:
        spinner.stop()
        print_formatted_text(HTML(
            u"<b>></b> <msg>OK</msg> <sub-msg>O upload foi realizado com sucesso</sub-msg>"
        ), style=style_ok)
    else:
        spinner.stop()
        print_formatted_text(HTML(
            u"<b>></b> <msg>Erro</msg> <sub-msg>Erro ao fazer o upload para a pasta</sub-msg>"
        ), style=style_fail)


@account.command()
@click.option('-df', '--download_folder', help='Url da pasta no drive da onde será feito o download',
              required=True, type=str)
def importcsv(download_folder: str):
    spinner = yaspin(text='Importando...', color='cyan')
    spinner.start()
    app_path = os.path.dirname(__file__)

    reset_all()
    download(download_folder)
    data = pd.read_csv(os.path.join(app_path, 'accounts.csv'))
    for d in data.values:
        create_account_csv(name=d[1], email=d[2], password=d[3])
    spinner.stop()
    return


if __name__ == "__main__":
    account(prog_name="main")
