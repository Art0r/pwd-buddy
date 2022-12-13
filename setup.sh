#!/usr/bin/zsh

APP_PATH="/usr/local/bin/pwd-buddy"

if [[ -d $APP_PATH ]]
then
    sudo -u root rm -rf $APP_PATH
fi

sudo -u root mkdir $APP_PATH
chmod u+x account.py
python - << EOF
from account import reset_and_import
reset_and_import()
EOF
pyinstaller --windowed --add-data "pwd-buddy.db:." main.py --name pwd-buddy
sudo -u root cp -r ./dist/pwd-buddy /usr/local/bin
sudo -u root chmod -R 777 /usr/local/bin/pwd-buddy