# Learning Media Search API Demo #

This is a demonstration of how the PBS Learning Media API might be used to
display search results on a third party website.


## Installation ##

Use the following Bash commands to set the project up.

```bash
# Set up Python3 Virtual Environment
export ve=path/to/virtual/environment
virtualenv --python=python3 ${ve}
. ${ve}/bin/activate

# Install the requirements.
pip install -r requirements.txt

# Initialize an SQLite database.
./manage.py syncdb

# Add a file to keep your private keys in.
# You should add your secrets to the file, too!
touch ./lmdemo/secrets.py

# Run the demo server.
./manage.py runserver
```


## lmdemo/secrets.py ##

Your secret information needs to be kept secret.  This project uses a
`secrets.py` file that is imported into the Django settings file.  The file
will need the following settings for the project to work:

```python    
# Place all private settings into a secrets module.  Don't check it in.
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = ''

# Production Login Bypass Credentials
LOGIN_BYPASS_KEY = ''

# PBS LM API security credentials.
LMAPI_URI = ''
LMAPI_USERNAME = ''
LMAPI_APIKEY = ''
```

You can generate a new Django style secret key with the following Python:

```python
import random
sysrnd = random.SystemRandom()
chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
''.join([sysrnd.choice(chars) for i in range(50)])
```

You can obtain LearningMedia credentials from your contact at PBS.

