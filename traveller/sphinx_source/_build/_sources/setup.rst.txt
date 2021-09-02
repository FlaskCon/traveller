.. :tocdepth:: 5

Setup Mail Dev Environment
--------------------------

-   If you have Node.js, use the `maildev <https://github.com/maildev/maildev>`_ package. Install it using

.. code-block:: bash

    $ npm install -g maildev

-   Then serve it using

.. code-block:: bash

    $ maildev

-   Dev configs for this setup are:

.. code-block:: python

    # traveller/traveller/config.py
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

-   Go to http://127.0.0.1:1080 where it serves it's web interface by default. See mails arrive in your inbox!



Setup 
-----

Create venv named venv inside root folder

Activate it

Install requirements.txt

.. code-block:: bash

    python -m pip install -r requirements.txt

Create a db named traveller or whatever you want in your mysql db

.. code-block:: bash

    cd traveller

We are using MySQL but you can have a stab at a different db, just in instance/config.py set the SQLALCHEMY_URI. For mysql it will be like that:

.. code-block:: bash

    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@localhost/traveller'
    'mysql+pymysql://username:password@localhost/dbname'

Now run in traveller/traveller

.. code-block:: bash

    python manage.py initialise

Then

.. code-block:: bash

    python manage.py rundebug

Migrations:

.. code-block:: bash

    python manage.py db migrate
    python manage.py db upgrade


More info can be found in the shopyo docs: shopyo.readthedocs.io

Functionalities
Go to /dashboard

login with admin@domain.com / pass

click on admin and create a new role called reviewer

add new people and assign them the roles

go to conf on dashboard

create a new conf

add reviewers to conf

we'll db seed some folks soon