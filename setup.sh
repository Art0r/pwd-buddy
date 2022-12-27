#!/usr/bin/zsh
APP_PATH="$HOME/.local/share/pwd-buddy"

if [[ -d "./venv" ]]
then
    rm -rf "./venv"
fi

python3 -m venv venv
. venv/bin/activate
pip install -r requirements.txt

if [[ -d $APP_PATH ]]
then
    rm -rf "$APP_PATH"
fi

mkdir "$APP_PATH"
pyinstaller -w main.py --name pwd-buddy --icon="./static/key.ico"
cp -r ./dist/pwd-buddy/* "$APP_PATH"
cp .env "$APP_PATH"
