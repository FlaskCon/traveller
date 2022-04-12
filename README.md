
![](icon.png)

# Traveller


## Setup

Create venv named venv inside root folder

Activate it


Install requirements.txt


```bash
$ python -m pip install -r requirements/dev.txt
```

We are using MySQL but you can have a stab at a different db.

Create a db named traveller or whatever you want in your MySQL db.

<details>
  <summary>Setting up MySQL Database on Linux(if this is your first time with using MySQL database )</summary>

  - Start MySQL database
  ```bash
  $ systemctl start mysql
  ```

  (or)

  ```bash
  $ service mysql start
  ```
  - After starting MySQL database, login into the shell 

  ```bash
  $ mysql
  ```
  - Create a database  
  ```mysql
  mysql >  CREATE DATABASE traveller;
  ```
  - This will create the database in your local MySQL server, you can exit the Mysql shell and complete the remaining steps
</details>

Change directory to the traveller folder

```bash
$ cd traveller
```

Create folder called instance and a file called config.py in it

```bash
$ mkdir instance #auto ignored by git
$ touch instance/config.py
```

In instance/config.py set the __SQLALCHEMY_URI__. For MySQL it will be like this (the file should contain only that):

```
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@localhost/traveller'
```
'mysql+pymysql://username:password@localhost/dbname'.

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

Then, to get development example data (make sure requirements in requirements/dev.txt are installed)

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
