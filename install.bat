echo "Downloading python 3.10 installer"
curl -o python-installer.exe https://www.python.org/ftp/python/3.10.4/python-3.10.4-amd64.exe

echo "Installing python 3.10"
python-installer.exe

del python-installer.exe

echo "Installing libraries"
py -3.10 -m pip install -r requirements.txt