

![](icon.png)


# traveller

### Setup


Create venv named venv inside root folder

Activate it


Install requirements.txt

```bash
python -m pip install -r requirements.txt
```

Create a db named traveller or whatever you want in your mysql db

```bash
cd traveller
```
create folder called instance and a file called config.py in it

```bash
mkdir instance #auto ignored by git
touch instance/config.py
```

We are using MySQL but you can have a stab at a different db, 
just in instance/config.py set the SQLALCHEMY_URI. For mysql it
will be like that (the file should contain only that):


```bash
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@localhost/traveller'
```

'mysql+pymysql://username:password@localhost/dbname'


Now run in traveller/traveller

```bash
python manage.py initialise
```

Then

```bash
python manage.py rundebug
```

Migrations:

```bash
python manage.py db migrate
python manage.py db upgrade
```

More info can be found in the shopyo docs: [shopyo.readthedocs.io](https://shopyo.readthedocs.io/en/latest/)

### Setup Mail Dev Environment

We are using flask-mailman.

If you have Node.js, use the maildev package. Install it using

```python
$ npm install -g maildev
```

Then serve it using

```python
$ maildev
```

Dev configs for this setup are (already in config.py):

```python
# shopyo/shopyo/config.py
class DevelopmentConfig(Config):
    """Configurations for development"""

    ENV = "development"
    DEBUG = True
    LOGIN_DISABLED = False
    # control email confirmation for user registration
    EMAIL_CONFIRMATION_DISABLED = False
    # flask-mailman configs
    MAIL_SERVER = 'localhost'
    MAIL_PORT = 1025
    MAIL_USE_TLS = False
    MAIL_USE_SSL = False
    MAIL_USERNAME = '' # os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = '' # os.environ.get("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = 'ma@mail.com' # os.environ.get("MAIL_DEFAULT_SENDER")
```

Go to http://127.0.0.1:1080 where it serves it’s web interface by default. See mails arrive in your inbox!

Particularly useful when registering!

### Functionalities


Go to /dashboard

login with admin@domain.com / pass


click on admin and create a new role called reviewer

add new people and assign them the roles

go to conf on dashboard

create a new conf

add reviewers to conf

go to:

http://127.0.0.1:5000/y/2021/

we'll db seed some folks soon
