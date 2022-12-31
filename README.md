
# Pwd-buddy :lock: :key:

CLI wrote in python with click.py that uses cryptography.py to save passwords. Uploads to dropbox.

## Installation

Installing project with python.

### Linux
```bash
  git clone https://github.com/Art0r/pwd-buddy.git ~/pwd-buddy
  cd ~/pwd-buddy
  chmod +x ./setup.sh
  ./setup.sh
  # wait for setup to finish
  cd ~ && rm -rf ~/pwd-buddy/
  # if you use bash instead of zsh, change ~/.zshrc to ~/.bashrc
  echo export PATH='$HOME/.local/share/pwd-buddy:$PATH' >> ~/.zshrc
```

### Windows 11
```bash
$USER = [System.Environment]::UserName
$USER_PATH = "C:\Users\" + $USER
$APP_PATH= $USER_PATH + "\pwd-buddy"
$DOWNLOAD_PATH= $USER_PATH + "\Downloads\pwd-buddy"
rmdir -r $DOWNLOAD_PATH
git clone https://github.com/Art0r/pwd-buddy.git $DOWNLOAD_PATH
cd $DOWNLOAD_PATH
rmdir -r $APP_PATH
mkdir $APP_PATH
python -m venv venv
. venv\Scripts\activate
pip install -r requirements.txt
pyinstaller -c main.py --name pwd-buddy
cp -r .\dist\pwd-buddy\* $APP_PATH
deactivate
echo Instalação finalizada com sucesso
```
    
