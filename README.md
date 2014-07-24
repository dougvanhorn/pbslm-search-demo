# Learning Media Search API Demo #

This is a demonstration of how the PBS Learning Media API might be used to
display search results on a third party website.


## Installation ##

```bash
# Set up Python3 Virtual Environment
export ve=path/to/virtual/environment
virtualenv --python=python3 ${ve}
. ${ve}/bin/activate

# Install the requirements.
pip install -r requirements.txt

# Initialize an SQLite database.
./manage.py syncdb

./manage.py runserver
```

