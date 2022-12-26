#!/usr/bin/zsh
APP_PATH="$HOME/.local/share/pwd-buddy"

if [[ -d $APP_PATH ]]
then
    rm -rf "$APP_PATH"
fi

mkdir "$APP_PATH"
pyinstaller -w main.py --name pwd-buddy --icon="./static/key.ico"
cp -r ./dist/pwd-buddy/* "$APP_PATH"
cp .env "$APP_PATH"
