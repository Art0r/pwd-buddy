#!/usr/bin/zsh

APP_PATH="$HOME/.local/share/pwd-buddy"

if [[ -d $APP_PATH ]]
then
    rm -rf "$APP_PATH"
fi

mkdir "$APP_PATH"
chmod u+x account.py
#python - << EOF
#from account import reset_and_import
#reset_and_import()
#EOF
pyinstaller --windowed --add-data "client_secret.json:." \
 --add-data "settings.yaml:." main.py --name pwd-buddy
#cp ./client_secret.json "$APP_PATH"
#cp ./settings.yaml "$APP_PATH"
cp -r ./dist/pwd-buddy/* "$APP_PATH"
