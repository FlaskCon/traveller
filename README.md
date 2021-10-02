
![](icon.png)

# Traveller


## Quick Start with Docker Compose

Install Docker Compose and Docker on your machine if you haven't already:  [Install Docker Compose](https://docs.docker.com/compose/install/)

```bash
git clone https://github.com/FlaskCon/traveller

docker-compose up
```

## Manual Setup

Create venv named venv inside root folder

Activate it


Install requirements.txt

```bash
$ python -m pip install -r requirements.txt
```

You may also want to install dev_requirements.txt

```bash
$ python -m pip install -r dev_requirements.txt
```

### Create a database using PostgreSQL.

Here is an excellent guide on how to install and use PostgreSQL on Ubuntu 20.04:  [PostgreSQL Ubuntu 20.04 Guide](https://www.linode.com/docs/guides/how-to-install-use-postgresql-ubuntu-20-04/)

```bash
$ sudo -u postgres psql
postgres=# create database traveller;
postgres=# create user traveller with encrypted password 'traveller';
postgres=# grant all privileges on database traveller to traveller;
```

### Site Configuration

Change directory to the traveller folder

```bash
$ cd web/traveller
```

Create folder called instance and a file called config.py in it

```bash
$ mkdir instance #auto ignored by git
$ touch instance/config.py
```

In instance/config.py set the __SQLALCHEMY_URI__. For PostgreSQL it will be like this (the file should contain only that):

```
SQLALCHEMY_DATABASE_URI = 'postgresql://traveller:traveller@localhost:5432/traveller'
```

Create or edit traveller/config.json with the information needed for each environment.

for __development:__

```markdown
{
    "environment": "development",
    "admin_user": {
      "email": "admin@domain.com",
      "password": "pass"
    },
    "settings": {
      "APP_NAME": "Demo",
      "ACTIVE_FRONT_THEME": "blogus",
      "ACTIVE_BACK_THEME": "boogle",
      "CURRENCY": "MUR"
    }
}
```

and for __production:__

```markdown
{
    "environment": "production",
    "admin_user": {
      "email": "admin@domain.com",
      "password": "pass"
    },
    "settings": {
      "APP_NAME": "Demo",
      "ACTIVE_FRONT_THEME": "blogus",
      "ACTIVE_BACK_THEME": "boogle",
      "CURRENCY": "MUR"
    }
}
```

Now in traveller/traveller run:

```bash
$ python manage.py initialise
```

Then, to get development example data (make sure requirements in dev_requirements.txt are installed)

```bash
$ flask seed dev
```
Then

```bash
$ python manage.py rundebug
```

Migrations:

```bash
$ python manage.py db migrate
$ python manage.py db upgrade
```
More info can be found in the shopyo docs: [shopyo.readthedocs.io](https://shopyo.readthedocs.io/en/latest/)


## Setup Mail Dev Environment

We are using flask-mailman.

If you have Node.js, use the [maildev](https://github.com/maildev/maildev) package. Install it using

```bash
$ npm install -g maildev
```

Then serve it using

```bash
$ maildev
```

Dev configs for this setup are (already in config.py):

```python
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

Go to [http://127.0.0.1:1080](http://127.0.0.1:1080) where it serves it’s web interface by default. See mails arrive in your inbox!
Particularly useful when registering!

## Running tests

Go to traveller/traveller

```bash
$ python -m pytest .
```

## Some functionalities of app

Go to: [http://127.0.0.1:5000/dashboard](http://127.0.0.1:5000/dashboard)

Login with __username: admin@domain.com__ and __password: pass__

Click on admin and create a new role called reviewer

Add new people and assign them the roles

Go to dashboard and click on conf

Create a new conf

Add reviewers to conf

Go to: [http://127.0.0.1:5000/y/2021/](http://127.0.0.1:5000/y/2021/)

We'll db seed some folks soon
