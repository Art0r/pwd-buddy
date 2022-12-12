#!/usr/bin/zsh

APP_PATH="/usr/local/bin/pwd-buddy"

if [[ -d $APP_PATH ]]
then
    sudo -u root rm -rf $APP_PATH
fi

sudo -u root mkdir $APP_PATH
pyinstaller --onefile --windowed main.py --name pwd-buddy
sudo -u root cp ./dist/pwd-buddy /usr/local/bin/pwd-buddy