import shutil

import click
import os
import pandas as pd
import subprocess
from account import Account, get_all_accounts, create_account, \
    get_account, delete_account, reset_and_import, create_account_csv, get_all_accounts_to_export
from tabulate import tabulate

# sqlite-utils db.db "select * from accounts"
# pyinstaller --onefile --windowed main.py --name pwd-buddy
# sudo mkdir /usr/local/bin/pwd-buddy && sudo cp ./dist/pwd-buddy /usr/local/bin/pwd-buddy
# sqlite-utils db.db "select * from accounts" --csv > accounts.csv


@click.group()
def account():
    """Aplicação de linha de comando para gerenciar contas e senhas"""


@account.command()
def getall():
    columns = [column.key for column in Account.__table__.columns]
    results = get_all_accounts()
    if results:
        click.echo(tabulate(results, headers=columns, tablefmt='fancy_grid'))
    else:
        click.echo("Ocorreu um erro")
    return


@account.command()
@click.option('-n', '--name', help='Nome do site ao qual se refere a conta',
              required=True, type=str)
def getone(name: str):
    columns = [column.key for column in Account.__table__.columns]
    results = get_account(name)
    if results:
        click.echo(tabulate(results, headers=columns, tablefmt='fancy_grid'))
    else:
        click.echo("Ocorreu um erro")
    return


@account.command()
@click.option('-n', '--name', help='Nome do site ao qual se refere a conta', required=True, type=str)
@click.option('-e', '--email', help='Email da conta cadastrada', required=True, type=str)
def create(name: str, email: str):
    columns = [column.key for column in Account.__table__.columns]
    result = create_account(name=name, email=email)
    if result:
        click.echo('Conta cadastrada')
        click.echo(tabulate(result, headers=columns, tablefmt='fancy_grid'))
    else:
        click.echo('Ocorreu um erro')


@account.command()
@click.option('-n', '--name', help='Nome do site ao qual se refere a conta', required=True, type=str)
@click.option('-e', '--email', help='Email da conta cadastrada', required=True, type=str)
def delete(name: str, email: str):
    columns = [column.key for column in Account.__table__.columns]
    result = delete_account(name=name, email=email)
    if result:
        click.echo('Conta deletada com sucesso')
        click.echo(tabulate(result, headers=columns, tablefmt='fancy_grid'))
    else:
        click.echo('Ocorreu um erro')


@account.command()
@click.option('-p', '--path', help='Diretório para onde o .csv será exportado',
              required=True, type=str)
def export(path: str):
    app_path = os.path.dirname(__file__)
    path = os.path.join('/home/arthurfernandes', path)

    if os.path.isdir(path):
        columns = [column.key for column in Account.__table__.columns]
        accounts = get_all_accounts_to_export()
        shutil.copy(os.path.join(app_path, 'secret.key'), os.path.join(path, 'secret.key'))
        with open(os.path.join(path, 'accounts.csv'), 'w') as file:
            file.write(','.join(columns))
            for acc in accounts:
                file.write('\n{}'.format(','.join(
                    str(field) for field in acc))
                )
            file.close()
        return

    click.echo("O caminho é inválido")


@account.command()
@click.option('-p', '--path', help='Diretório de onde o .csv será importado',
              required=True, type=str)
def importcsv(path: str):
    app_path = os.path.dirname(__file__)
    shutil.copy(os.path.join('/home/arthurfernandes/', path, 'secret.key'), os.path.join(app_path, 'secret.key'))
    path = os.path.join('/home/arthurfernandes/', path, 'accounts.csv')

    if os.path.isfile(path):
        reset_and_import()
        data = pd.read_csv(path)
        for d in data.values:
            create_account_csv(name=d[1], email=d[2], password=d[3])
        return

    click.echo("O caminho é inválido")


if __name__ == "__main__":
    account(prog_name="main")
