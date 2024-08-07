# Backups
Automatically backs up the contents of a directory

# Setup



## Environment

https://stackoverflow.com/questions/65722324/clone-a-python-virtualenv-to-an-offline-server

After cloning the repo, you can set up your environment by running `pip install -r requirements.txt`. If you will be running the scripts on an offline computer, you will have to download the wheelfiles before transferring to the offline computer by running the following commands.

Install wheelfiles before sending to offline computer

    pip freeze > requirements.txt
    pip download -r requirements.txt -d env

Add wheelfiles to offline python environment

    pip install -r requirements.txt --no-index --find-links env

